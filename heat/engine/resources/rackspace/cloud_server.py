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

import json
import paramiko
from Crypto.PublicKey import RSA
import novaclient

from heat.common import exception
from heat.openstack.common import log as logging
from heat.engine import scheduler
from heat.engine.resources import instance
from heat.engine.resources.rackspace import rackspace_resource

logger = logging.getLogger(__name__)


class CloudServer(instance.Instance, rackspace_resource.RackspaceResource):
    """Resource for Rackspace Cloud Servers."""
    properties_schema = {
        'InstanceName': {'Type': 'String', 'Required': True},
        'Flavor': {'Type': 'String', 'Required': True},
        'ImageName': {'Type': 'String', 'Required': True},
        'UserData': {'Type': 'String'},
        'PublicKey': {'Type': 'String'}
    }

    rackspace_images = {
        "F17": "76856c8b-e56e-4301-b454-c8cd1be22cfb",
        "F18": "89e9ce4a-1261-49c3-8a35-17224411659d",
        "U12.04": "e4dbdba7-b2a4-4ee5-8e8f-4595b6d694ce"
    }

    rackspace_flavors = ["2", "3", "4", "5", "6", "7", "8"]

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
        "F17": fedora_script,
        "F18": fedora_script
    }

    # template keys supported for handle_update, note trailing comma
    # is required for a single item to get a tuple not a string
    update_allowed_keys = ('Metadata', 'Properties')
    update_allowed_properties = ('Flavor',)

    def _get_ip(self, ip_type):
        """Return the IP of the Cloud Server.

        :param ip_type: type of IP to retrieve, either "Public" or "Private"
        :returns: IP of Cloud Server
        :rtype: string
        """
        server = self.nova().servers.get(self.resource_id)
        if ip_type not in server.addresses:
            raise exception.IpNotFound
        for ip in server.addresses[ip_type]:
            if ip['version'] == 4:
                return ip['addr']
        raise exception.IpNotFound

    def _public_ip(self):
        """Return the public IP of the Cloud Server."""
        return self._get_ip('public')

    def _private_ip(self):
        """Return the private IP of the Cloud Server."""
        return self._get_ip('private')

    def _create_temp_file(self, data):
        """Return a temporary file containing the data passed in.

        :param data: a string containing data to be put in temporary file
        :returns: temporary file
        :rtype: NamedTemporaryFile
        """
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(data)
        temp_file.seek(0)
        return temp_file

    def _run_ssh_command(self, command):
        """Run a shell command on the Cloud Server via SSH.

        :param command: a string containing the command to run
        """
        private_key_file = self._create_temp_file(self.private_key)
        ssh = paramiko.SSHClient()
        public_ip = self._public_ip()
        ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        ssh.connect(public_ip,
                    username="root",
                    key_filename=private_key_file.name)
        private_key_file.close()  # Delete temp file
        stdin, stdout, stderr = ssh.exec_command(command)
        logger.debug(stdout.read())
        logger.debug(stderr.read())
        private_key_file.close()

    def _sftp_files(self, files):
        """Transfer files to the Cloud Server via SFTP.

        :param files: a list containing one dictionary per file, each
                      containing a 'path' and 'data' value
        """
        private_key_file = self._create_temp_file(self.private_key)
        pkey = paramiko.RSAKey.from_private_key_file(private_key_file.name)
        public_ip = self._public_ip()
        transport = paramiko.Transport((public_ip, 22))
        transport.connect(hostkey=None, username="root", pkey=pkey)
        sftp = paramiko.SFTPClient.from_transport(transport)
        for remote_file in files:
            sftp_file = sftp.open(remote_file['path'], 'w')
            sftp_file.write(remote_file['data'])
            sftp_file.close()
        private_key_file.close()

    def validate(self):
        """Validate the user-parameters."""
        image_name = self.properties['ImageName']
        if image_name not in self.rackspace_images:
            raise exception.ImageNotFound

        flavor = self.properties['Flavor']
        if flavor not in self.rackspace_flavors:
            raise exception.FlavorMissing

    def handle_create(self):
        """Create a Rackspace Cloud Servers container.

        Rackspace Cloud Servers does not have the metadata service
        running, so we have to transfer the user-data file to the
        server and then trigger cloud-init.
        """
        self.validate()

        # Retrieve server creation parameters from properties
        name = self.properties['InstanceName']
        image_name = self.properties['ImageName']
        image_id = self.rackspace_images[image_name]
        self.script = self.image_scripts[image_name]
        flavor = self.properties['Flavor']
        raw_userdata = self.properties['UserData'] or ''
        self.userdata = self._build_userdata(raw_userdata)
        user_public_key = self.properties['PublicKey'] or ''

        # Generate SSH public/private keypair
        rsa = RSA.generate(1024)
        private_key = rsa.exportKey()
        public_key = rsa.publickey().exportKey('OpenSSH')
        public_keys = public_key + "\n" + user_public_key
        personality_files = {"/root/.ssh/authorized_keys": public_keys}

        # Create server
        client = self.nova().servers
        server = client.create(name, image_id, flavor, files=personality_files)

        # Save resource ID and private key to db
        self.resource_id_set(server.id)
        self.resource_private_key_set(private_key)

        return server

    def check_create_complete(self, server):
        """Check if server creation is complete and handle server configs."""
        server.get()  # Update server attributes
        if server.status in self._deferred_server_statuses:
            return False
        elif server.status == 'ERROR':
            raise exception.ServerBuildFailed

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
        self.validate()

        if self.resource_id is None:
            return

        try:
            server = self.nova().servers.get(self.resource_id)
        except novaclient.exceptions.NotFound:
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
            except novaclient.exceptions.NotFound:
                break

    def _resize_server(self, server, flavor):
        """Returns a coroutine that resizes the Cloud Server"""
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
                raise exception.RevertFailed

    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        """Try to update a Cloud Server's parameters.

        If the Cloud Server's Metadata or Flavor changed, update the
        Cloud Server.  If any other parameters changed, re-create the
        Cloud Server with the new parameters.
        """
        self.validate()
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

        return True

    def FnGetAtt(self, key):
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
        logger.info('%s.GetAtt(%s) == %s' % (self.name, key, function))
        return unicode(function)


if rackspace_resource.PYRAX_INSTALLED:
    def resource_mapping():
        return {
            'Rackspace::Cloud::Server': CloudServer
        }
