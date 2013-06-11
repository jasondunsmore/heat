from heat.engine import resource
from heat.openstack.common import log as logging
import pyrax
from heat.common import short_id, exception
import json
from oslo.config import cfg
from email.mime.text import MIMEText
import pkgutil
import os
from email.mime.multipart import MIMEMultipart
import paramiko
from Crypto.PublicKey import RSA
import tempfile

logger = logging.getLogger(__name__)


class CloudServer(resource.Resource):
    tags_schema = {
        'Key': {'Type': 'String', 'Required': True},
        'Value': {'Type': 'String', 'Required': True}
    }

    properties_schema = {
        'UserData': {'Type': 'String'},
        'KeyName': {'Type': 'String'},
        'AvailabilityZone': {'Type': 'String'},
        'SecurityGroups': {'Type': 'List'},
        'SecurityGroupIds': {'Type': 'List'},
        'NovaSchedulerHints': {
            'Type': 'List', 'Schema': {'Type': 'Map', 'Schema': tags_schema}
        },
        'Volumes': {'Type': 'List'},
        'SubnetId': {'Type': 'String'},
        'NetworkInterfaces': {'Type': 'List'},
        'InstanceName': {'Type': 'String', 'Required': True},
        'Flavor': {'Type': 'String', 'Required': True},
        'ImageName': {'Type': 'String', 'Required': True},
        'Tags': {'Type': 'List',
                 'Schema': {'Type': 'Map',
                            'Schema': tags_schema}}
    }

    rackspace_images = {
        "F17": "76856c8b-e56e-4301-b454-c8cd1be22cfb",
        "U12.04": "e4dbdba7-b2a4-4ee5-8e8f-4595b6d694ce"
    }

    image_scripts = {
        "F17": """#!/bin/bash -e

# Install cloud-init and heat-cfntools
yum install -y cloud-init python-boto
curl http://repos.fedorapeople.org/repos/heat/heat-trunk/fedora-17/x86_64/heat\
-cfntools-1.0-20130118.fc17.noarch.rpm > heat-cfntools.rpm
rpm -i heat-cfntools.rpm

# Create data source for cloud-init
mkdir -p /var/lib/cloud/seed/nocloud-net
mv /tmp/userdata /var/lib/cloud/seed/nocloud-net/user-data
touch /var/lib/cloud/seed/nocloud-net/meta-data

# Run cloud-init & cfn-init
cloud-init start
bash /var/lib/cloud/data/cfn-userdata

# Clean up
rm -f /root/.ssh/authorized_keys
"""
    }

    def __init__(self, name, json_snippet, stack):
        super(CloudServer, self).__init__(name, json_snippet, stack)
        self.ipaddress = None
        self.mime_string = None

        # Retrieve auth info from file (temporary solution)
        pyrax.set_setting("identity_type", "rackspace")
        pyrax.set_credential_file("/opt/stack/heat/heat/engine/resources/"
                                  "rackspace/rs-pyrax-creds.txt")
        self.cs = pyrax.connect_to_cloudservers()

    def _create_container_name(self, name=None):
        return name or '%s-%s-%s' % (self.stack.name,
                                     self.name,
                                     short_id.generate_id())

    def _build_userdata(self, userdata):
        if not self.mime_string:
            # Build mime multipart data blob for cloudinit userdata

            def make_subpart(content, filename, subtype=None):
                if subtype is None:
                    subtype = os.path.splitext(filename)[0]
                msg = MIMEText(content, _subtype=subtype)
                msg.add_header('Content-Disposition', 'attachment',
                               filename=filename)
                return msg

            def read_cloudinit_file(fn):
                data = pkgutil.get_data('heat', 'cloudinit/%s' % fn)
                data = data.replace('@INSTANCE_USER@',
                                    cfg.CONF.instance_user)
                return data

            attachments = [(read_cloudinit_file('config'), 'cloud-config'),
                           (read_cloudinit_file('boothook.sh'), 'boothook.sh',
                            'cloud-boothook'),
                           (read_cloudinit_file('part-handler.py'),
                            'part-handler.py'),
                           (userdata, 'cfn-userdata', 'x-cfninitdata'),
                           (read_cloudinit_file('loguserdata.py'),
                            'loguserdata.py', 'x-shellscript')]

            if 'Metadata' in self.t:
                attachments.append((json.dumps(self.metadata),
                                    'cfn-init-data', 'x-cfninitdata'))

            subparts = [make_subpart(*args) for args in attachments]
            mime_blob = MIMEMultipart(_subparts=subparts)

            self.mime_string = mime_blob.as_string()

        return self.mime_string

    def handle_create(self):
        """Create a Rackspace Cloud Servers container.

        Rackspace Cloud Servers does not have the metadata service
        running, so we have to transfer the user-data file to the
        server and then trigger cloud-init.

        """

        def create_temp_file(data):
            temp_file = tempfile.NamedTemporaryFile()
            temp_file.write(data)
            temp_file.seek(0)
            return temp_file

        # Retrieve server creation parameters from properties
        name = self.properties['InstanceName']
        image_name = self.properties['ImageName']
        image_id = self.rackspace_images[image_name]
        script = self.image_scripts[image_name]
        flavor = self.properties['Flavor']
        raw_userdata = self.properties['UserData'] or ''
        userdata = self._build_userdata(raw_userdata)

        # Generate one-time-use SSH public/private keypair (public key
        # will be put on server using personalities)
        rsa = RSA.generate(1024)
        private_key = rsa.exportKey()
        public_key = rsa.publickey().exportKey('OpenSSH')
        files = {"/root/.ssh/authorized_keys": public_key}

        # Create server
        server = self.cs.servers.create(name, image_id, flavor, files=files)
        complete = pyrax.utils.wait_until(server, "status",
                                          ["ACTIVE", "ERROR"], attempts=0)

        # Get public IP
        for ip in complete.addresses['public']:
            if ip['version'] == 4:
                public_ip = ip['addr']
        if not public_ip:
            raise exception.Error('Could not determine public IP of server')

        # Create temp files for SFTP
        userdata_file = create_temp_file(userdata)
        script_file = create_temp_file(script)
        private_key_file = create_temp_file(private_key)

        # Transfer files to server via SFTP
        pkey = paramiko.RSAKey.from_private_key_file(private_key_file.name)
        transport = paramiko.Transport((public_ip, 22))
        transport.connect(hostkey=None, username="root", pkey=pkey)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(userdata_file.name, "/tmp/userdata")
        sftp.put(script_file.name, "/root/heat-script")

        # Connect via SSH and run script
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(public_ip,
                    username="root",
                    key_filename=private_key_file.name)
        stdin, stdout, stderr = ssh.exec_command("bash /root/heat-script")
        logger.debug(stdout.read())
        logger.debug(stderr.read())

        # Clean up temp files
        private_key_file.close()
        userdata_file.close()
        script_file.close()

    def handle_delete(self):
        raise NotImplementedError

    def handle_update(self):
        raise NotImplementedError


def resource_mapping():
    return {
        'Rackspace::CloudServer': CloudServer
    }
