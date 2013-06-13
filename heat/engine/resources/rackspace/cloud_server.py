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
from heat.openstack.common import log as logging
from heat.common import exception

logger = logging.getLogger(__name__)


class CloudServer(instance.Instance):
    """"""
    properties_schema = {
        'UserData': {'Type': 'String'},
        'InstanceName': {'Type': 'String', 'Required': True},
        'Flavor': {'Type': 'String', 'Required': True},
        'ImageName': {'Type': 'String', 'Required': True}
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
bash /var/lib/cloud/data/cfn-userdata
"""

    image_scripts = {
        "F17": fedora_script,
        "F18": fedora_script
    }

    def validate(self):
        return self.properties.validate()

    def handle_create(self):
        """Create a Rackspace Cloud Servers container.

        Rackspace Cloud Servers does not have the metadata service
        running, so we have to transfer the user-data file to the
        server and then trigger cloud-init.

        """

        # TODO(jason): Authenticate via Rackspace base class
        pyrax.set_setting("identity_type", "rackspace")
        pyrax.set_credential_file("/opt/stack/heat/heat/engine/resources/"
                                  "rackspace/rs-pyrax-creds.txt")

        # Retrieve server creation parameters from properties
        name = self.properties['InstanceName']
        image_name = self.properties['ImageName']
        image_id = self.rackspace_images[image_name]
        self.script = self.image_scripts[image_name]
        flavor = self.properties['Flavor']
        raw_userdata = self.properties['UserData'] or ''
        self.userdata = self._build_userdata(raw_userdata)

        # Generate SSH public/private keypair
        rsa = RSA.generate(1024)
        self.private_key = rsa.exportKey()
        self.public_key = rsa.publickey().exportKey('OpenSSH')
        files = {"/root/.ssh/authorized_keys": self.public_key}

        # Create server
        cs = pyrax.connect_to_cloudservers()
        server = cs.servers.create(name, image_id, flavor, files=files)
        return server

    def check_create_complete(self, server):
        server.get()  # Update server attributes
        if server.status in self._deferred_server_statuses:
            return False
        elif server.status == 'ERROR':
            raise exception.Error('Server build failed.')

        self.resource_id_set(server.id)  # Save resource ID to db

        # Get public IP
        if 'public' not in server.addresses:
            raise exception.Error('Could not determine public IP of server')
        for ip in server.addresses['public']:
            if ip['version'] == 4:
                public_ip = ip['addr']
                break
        if not public_ip:
            raise exception.Error('Could not determine public IP of server')

        # Create temp file for private key
        private_key_file = tempfile.NamedTemporaryFile()
        private_key_file.write(self.private_key)
        private_key_file.seek(0)

        # Create heat-script and userdata files on server
        pkey = paramiko.RSAKey.from_private_key_file(private_key_file.name)
        private_key_file.seek(0)
        transport = paramiko.Transport((public_ip, 22))
        transport.connect(hostkey=None, username="root", pkey=pkey)
        sftp = paramiko.SFTPClient.from_transport(transport)
        remote_userdata = sftp.open("/tmp/userdata", 'w')
        remote_userdata.write(self.userdata)
        remote_userdata.close()
        remote_script = sftp.open("/root/heat-script.sh", 'w')
        remote_script.write(self.script)
        remote_script.close()

        # Connect via SSH and run script
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        ssh.connect(public_ip,
                    username="root",
                    key_filename=private_key_file.name)
        private_key_file.close()  # Delete temp file
        command = "bash -ex /root/heat-script.sh > /root/heat-script.log 2>&1"
        stdin, stdout, stderr = ssh.exec_command(command)
        logger.debug(stdout.read())
        logger.debug(stderr.read())

        return True

    def handle_delete(self):
        if self.resource_id is None:
            return

        # TODO(jason): Authenticate via Rackspace base class
        pyrax.set_setting("identity_type", "rackspace")
        pyrax.set_credential_file("/opt/stack/heat/heat/engine/resources/"
                                  "rackspace/rs-pyrax-creds.txt")

        cs = pyrax.connect_to_cloudservers()
        try:
            server = cs.servers.get(self.resource_id)
        except pyrax.exceptions.ServerNotFound:
            pass
        else:
            server.delete()

        self.resource_id = None


def resource_mapping():
    return {
        'Rackspace::Cloud::Server': CloudServer
    }
