#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import tempfile
import time

import json
import paramiko
from Crypto.PublicKey import RSA
import novaclient.exceptions as novaexception

from heat.common import exception
from heat.openstack.common import log as logging
from heat.engine import scheduler
from heat.engine.resources import instance
from heat.engine.resources.rackspace import rackspace_resource

logger = logging.getLogger(__name__)


class CloudServer(instance.Instance, rackspace_resource.RackspaceResource):
    """Resource for Rackspace Cloud Servers."""
    properties_schema = {
        'ServerName': {'Type': 'String', 'Required': True},
        'Flavor': {'Type': 'String', 'Required': True},
        'ImageName': {'Type': 'String', 'Required': True},
        'UserData': {'Type': 'String'},
        'PublicKey': {'Type': 'String'}
    }

    fedora_script = """#!/bin/bash

# Install cloud-init and heat-cfntools
yum install -y cloud-init python-boto python-pip
pip-python install heat-cfntools

# Create data source for cloud-init
mkdir -p /var/lib/cloud/seed/nocloud-net
mv /tmp/userdata /var/lib/cloud/seed/nocloud-net/user-data
touch /var/lib/cloud/seed/nocloud-net/meta-data
chmod 600 /var/lib/cloud/seed/nocloud-net/*

# Run cloud-init & cfn-init
cloud-init start
bash -x /var/lib/cloud/data/cfn-userdata > /root/cfn-userdata.log 2>&1
"""

    image_scripts = {
        "Fedora 17 (Beefy Miracle)": fedora_script,
        "Fedora 18 (Spherical Cow)": fedora_script
    }

    flavors = None

    # template keys supported for handle_update, note trailing comma
    # is required for a single item to get a tuple not a string
    update_allowed_keys = ('Metadata', 'Properties')
    update_allowed_properties = ('Flavor', 'ServerName')

    def validate(self):
        """Validate user parameters."""
        flavor = self.properties['Flavor']
        if flavor not in self._flavors()[0]:
            return {'Error': "Flavor not found."}

        image_name = self.properties['ImageName']
        if image_name not in self.image_scripts.keys():
            return {'Error': "Image %s not supported." % image_name}

    def _flavors(self):
        """Fetch flavors from the API or cache."""
        def get_flavors():
            return [flavor.id for flavor in self.nova().flavors.list()]
        time_now = time.time()
        if self.__class__.flavors:
            last_update = self.__class__.flavors[1]
            six_hours = 216000
            if (time_now - last_update) > six_hours:
                self.__class__.flavors = (get_flavors(), time_now)
        else:
            self.__class__.flavors = (get_flavors(), time_now)
        return self.__class__.flavors

    def _get_ip(self, ip_type):
        """Return the IP of the Cloud Server.

        :param ip_type: type of IP to retrieve, either "Public" or "Private"
        :returns: IP of Cloud Server
        :rtype: string
        """
        def ip_not_found():
            exc = exception.Error("Could not determine the %s IP of %s." %
                                  (ip_type, self.properties['ImageName']))
            raise exception.ResourceFailure(exc)

        server = self.nova().servers.get(self.resource_id)
        if ip_type not in server.addresses:
            ip_not_found()
        for ip in server.addresses[ip_type]:
            if ip['version'] == 4:
                return ip['addr']
        ip_not_found()

    def _public_ip(self):
        """Return the public IP of the Cloud Server."""
        return self._get_ip('public')

    def _private_ip(self):
        """Return the private IP of the Cloud Server."""
        try:
            return self._get_ip('private')
        except exception.ResourceFailure as ex:
            logger.info(ex.message)

    def _run_ssh_command(self, command):
        """Run a shell command on the Cloud Server via SSH.

        :param command: a string containing the command to run
        """
        with tempfile.NamedTemporaryFile() as private_key_file:
            private_key_file.write(self.private_key)
            private_key_file.seek(0)
            ssh = paramiko.SSHClient()
            public_ip = self._public_ip()
            ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
            ssh.connect(public_ip,
                        username="root",
                        key_filename=private_key_file.name)
            stdin, stdout, stderr = ssh.exec_command(command)
            logger.debug(stdout.read())
            logger.debug(stderr.read())

    def _sftp_files(self, files):
        """Transfer files to the Cloud Server via SFTP.

        :param files: a list containing one dictionary per file, each
                      containing a 'path' and 'data' value
        """
        with tempfile.NamedTemporaryFile() as private_key_file:
            private_key_file.write(self.private_key)
            private_key_file.seek(0)
            pkey = paramiko.RSAKey.from_private_key_file(private_key_file.name)
            public_ip = self._public_ip()
            transport = paramiko.Transport((public_ip, 22))
            transport.connect(hostkey=None, username="root", pkey=pkey)
            sftp = paramiko.SFTPClient.from_transport(transport)
            for remote_file in files:
                sftp_file = sftp.open(remote_file['path'], 'w')
                sftp_file.write(remote_file['data'])
                sftp_file.close()

    def handle_create(self):
        """Create a Rackspace Cloud Servers container.

        Rackspace Cloud Servers does not have the metadata service
        running, so we have to transfer the user-data file to the
        server and then trigger cloud-init.
        """
        # Retrieve server creation parameters from properties
        server_name = self.properties['ServerName']
        image_name = self.properties['ImageName']
        image_id = self._get_image_id(image_name)
        self.flavor = self.properties['Flavor']
        self.script = self.image_scripts[image_name]
        raw_userdata = self.properties['UserData'] or ''
        self.userdata = self._build_userdata(raw_userdata)
        user_public_key = self.properties['PublicKey'] or ''

        # Generate SSH public/private keypair
        rsa = RSA.generate(1024)
        self.private_key = rsa.exportKey()
        public_key = rsa.publickey().exportKey('OpenSSH')
        public_keys = public_key + "\n" + user_public_key
        personality_files = {"/root/.ssh/authorized_keys": public_keys}

        # Create server
        client = self.nova().servers
        server = client.create(server_name,
                               image_id,
                               self.flavor,
                               files=personality_files)

        # Save resource ID and private key to db
        self.resource_id_set(server.id)
        self.resource_private_key_set(self.private_key)

        return server

    def check_create_complete(self, server):
        """Check if server creation is complete and handle server configs."""
        server.get()  # Update server attributes
        if server.status in self._deferred_server_statuses:
            return False
        elif server.status == 'ERROR':
            exc = exception.Error("Build of server %s failed." % server.name)
            raise exception.ResourceFailure(exc)

        # Create heat-script and userdata files on server
        files = [
            {'path': "/tmp/userdata", 'data': self.userdata},
            {'path': "/root/heat-script.sh", 'data': self.script}
        ]
        self._sftp_files(files)

        # Connect via SSH and run script
        command = "bash -ex /root/heat-script.sh > /root/heat-script.log 2>&1"
        self._run_ssh_command(command)

        return True

    def handle_delete(self):
        """Delete the Cloud Server."""
        if self.resource_id is None:
            return

        try:
            server = self.nova().servers.get(self.resource_id)
        except novaexception.NotFound:
            pass
        else:
            delete = scheduler.TaskRunner(self._delete_server, server)
            delete(wait_time=0.2)

        self.resource_id = None

    def _delete_server(self, server):
        """Returns a coroutine that deletes the Cloud Server."""
        server.delete()
        while True:
            yield
            try:
                server.get()
            except novaexception.NotFound:
                break

    def _resize_server(self, server, flavor):
        """Returns a coroutine that resizes the Cloud Server."""
        server.resize(flavor)
        while True:
            yield
            server.get()
            logger.debug("resize server.status == %s" % server.status)
            # The server stays in "RESIZE" status while resizing
            if server.status == "RESIZE":
                continue
            elif server.status == "VERIFY_RESIZE":
                server.confirm_resize()
                logger.info("Successfully resized instance.")
                break
            else:  # Status will go back to "ACTIVE" upon error
                logger.info("Could not resize instance, reverting...")
                revert = scheduler.TaskRunner(self._revert_server, server)
                revert(wait_time=0.2)
                break

    def _revert_server(self, server):
        """Returns a coroutine that reverts a failed Cloud Server resize."""
        server.revert_resize()
        while True:
            yield
            server.get()
            logger.debug("revert server.status == %s" % server.status)
            # The server stays in "REVERT_RESIZE" status while reverting
            if server.status == "REVERT_RESIZE":
                continue
            elif server.status == "ACTIVE":  # Successful revert
                break
            else:  # "ERROR" or other status
                exc = exception.Error("Unable to revert resize of %s." %
                                      server.name)
                raise exception.ResourceFailure(exc)

    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        """Try to update a Cloud Server's parameters.

        If the Cloud Server's Metadata or Flavor changed, update the
        Cloud Server.  If any other parameters changed, re-create the
        Cloud Server with the new parameters.
        """
        server = self.nova().servers.get(self.resource_id)

        if 'Metadata' in tmpl_diff:
            self.private_key = self.resource_private_key_get()
            self.metadata = json_snippet['Metadata']
            metadata_string = json.dumps(self.metadata)

            files = [{'path': "/var/cache/heat-cfntools/last_metadata",
                      'data': metadata_string}]
            self._sftp_files(files)

            command = "bash -x /var/lib/cloud/data/cfn-userdata > " + \
                      "/root/cfn-userdata.log 2>&1"
            self._run_ssh_command(command)

        if 'Flavor' in prop_diff:
            self.flavor = json_snippet['Properties']['Flavor']
            resize = scheduler.TaskRunner(self._resize_server,
                                          server,
                                          self.flavor)
            resize(wait_time=1.0)

        # If ServerName is the only update, fail update
        if prop_diff.keys() == ['ServerName'] and \
           tmpl_diff.keys() == ['Properties']:
            raise exception.NotSupported(feature="Cloud Server rename")
        # Other updates were successful, so don't cause update to fail
        elif 'ServerName' in prop_diff:
            logger.info("Cloud Server rename not supported.")

        return True

    def _resolve_attribute(self, key):
        """Return the method that provides a given template attribute."""
        attribute_function = {
            'PublicIp': self._public_ip(),
            'PrivateIp': self._private_ip(),
            'PublicDnsName': self._public_ip(),
            'PrivateDnsName': self._public_ip()
        }
        if key not in attribute_function:
            raise exception.InvalidTemplateAttribute(resource=self.name,
                                                     key=key)
        function = attribute_function[key]
        logger.info('%s._resolve_attribute(%s) == %s'
                    % (self.name, key, function))
        return unicode(function)


# pyrax module is required to work with Rackspace cloud server provider.
# If it is not installed, don't register cloud server provider
def resource_mapping():
    if rackspace_resource.PYRAX_INSTALLED:
        return {
            'Rackspace::Cloud::Server': CloudServer
        }
    else:
        return {}
