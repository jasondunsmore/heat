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
import paramiko
import pyrax

from Crypto.PublicKey import RSA

from heat.engine.resources import instance
from heat.engine.resources.rackspace import rackspace_resource
from heat.openstack.common import log as logging
from heat.common import exception
from heat.db import api as db_api

logger = logging.getLogger(__name__)


class CloudServer(instance.Instance, rackspace_resource.RackspaceResource):
    """"""
    properties_schema = {
        'InstanceName': {'Type': 'String', 'Required': True},
        'Flavor': {'Type': 'String', 'Required': True},
        'ImageName': {'Type': 'String', 'Required': True},
        'UserData': {'Type': 'String'},
        'PublicKey': {'Type': 'String'}
    }

    rackspace_images = {
        "F17": "76856c8b-e56e-4301-b454-c8cd1be22cfb",
        "U12.04": "e4dbdba7-b2a4-4ee5-8e8f-4595b6d694ce"
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
        "F17": fedora_script,
        "F18": fedora_script
    }

    # template keys supported for handle_update, note trailing comma
    # is required for a single item to get a tuple not a string
    update_allowed_keys = ('Metadata', 'Properties')
    update_allowed_properties = ('Flavor',)

    def validate(self):
        return self.properties.validate()

    def _public_ip(self, addresses):
        error_message = 'Could not determine public IP of server'
        if 'public' not in addresses:
            raise exception.Error(error_message)
        for ip in addresses['public']:
            if ip['version'] == 4:
                return ip['addr']
        raise exception.Error(error_message)

    def _create_temp_file(self, data):
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(data)
        temp_file.seek(0)
        return temp_file

    def _run_ssh_command(self, server, command):
        private_key_file = self._create_temp_file(self.private_key)
        ssh = paramiko.SSHClient()
        public_ip = self._public_ip(server.addresses)
        ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        ssh.connect(public_ip,
                    username="root",
                    key_filename=private_key_file.name)
        private_key_file.close()  # Delete temp file
        stdin, stdout, stderr = ssh.exec_command(command)
        logger.debug(stdout.read())
        logger.debug(stderr.read())
        private_key_file.close()

    def _sftp_files(self, server, files):
        private_key_file = self._create_temp_file(self.private_key)
        pkey = paramiko.RSAKey.from_private_key_file(private_key_file.name)
        public_ip = self._public_ip(server.addresses)
        transport = paramiko.Transport((public_ip, 22))
        transport.connect(hostkey=None, username="root", pkey=pkey)
        sftp = paramiko.SFTPClient.from_transport(transport)
        for remote_file in files:
            sftp_file = sftp.open(remote_file['path'], 'w')
            sftp_file.write(remote_file['data'])
            sftp_file.close()
        private_key_file.close()

    def handle_create(self):
        """Create a Rackspace Cloud Servers container.

        Rackspace Cloud Servers does not have the metadata service
        running, so we have to transfer the user-data file to the
        server and then trigger cloud-init.

        """

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
        files = {"/root/.ssh/authorized_keys": public_keys}

        # Create server
        client = self.cloud_server().servers
        server = client.create(name, image_id, flavor, files=files)

        # Save resource ID and private key to db
        self.resource_id_set(server.id)
        self.resource_private_key_set(private_key)

        return server

    def check_create_complete(self, server):
        server.get()  # Update server attributes
        if server.status in self._deferred_server_statuses:
            return False
        elif server.status == 'ERROR':
            raise exception.Error('Server build failed.')

        # Create heat-script and userdata files on server
        files = [
            {'path': "/tmp/userdata", 'data': self.userdata},
            {'path': "/root/heat-script.sh", 'data': self.script}
        ]
        self._sftp_files(server, files)

        # Connect via SSH and run script
        command = "bash -ex /root/heat-script.sh > /root/heat-script.log 2>&1"
        self._run_ssh_command(server, command)

        return True

    def handle_delete(self):
        if self.resource_id is None:
            return

        client = self.cloud_server().servers
        try:
            server = client.get(self.resource_id)
        except pyrax.exceptions.ServerNotFound:
            pass
        else:
            server.delete()

        self.resource_id = None

    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        import pdb; pdb.set_trace()

        client = self.cloud_server().servers
        server = client.get(self.resource_id)

        if 'Metadata' in tmpl_diff:
            self.private_key = self.resource_private_key_get()

            files = [{'path': "/var/cache/heat-cfntools/last_metadata",
                      'data': str(json_snippet['Metadata'])}]
            self._sftp_files(server, files)

            command = "bash -x /var/lib/cloud/data/cfn-userdata > "
            "/root/cfn-userdata.log 2>&1"
            self._run_ssh_command(server, command)

        if 'Flavor' in prop_diff:
            server.resize(json_snippet['Properties']['Flavor'])
            new_server = server.get(server.id)
            if new_server.status == "CONFIRM_RESIZE":
                server.confirm_resize()
            else:
                server.revert_resize()
                raise exception.Error("Could not resize instance, reverting.")

        return True


def resource_mapping():
    return {
        'Rackspace::Cloud::Server': CloudServer
    }
