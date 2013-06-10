from heat.engine import resource
from heat.openstack.common import log as logging
import pyrax
from heat.common import short_id, exception
import json
from oslo.config import cfg
from email.mime.text import MIMEText
import pkgutil
import os
from urlparse import urlparse
from email.mime.multipart import MIMEMultipart
import paramiko
from Crypto.PublicKey import RSA
import tempfile

logger = logging.getLogger(__name__)


class CloudServer(resource.Resource):
    tags_schema = {'Key': {'Type': 'String',
                           'Required': True},
                   'Value': {'Type': 'String',
                             'Required': True}}
    properties_schema = {
        'ImageId': {'Type': 'String', 'Required': True},
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
        'InstanceType': {'Type': 'String', 'Required': True},
        'Tags': {'Type': 'List',
                 'Schema': {'Type': 'Map',
                            'Schema': tags_schema}}
    }

    def __init__(self, name, json_snippet, stack):
        super(CloudServer, self).__init__(name, json_snippet, stack)
        self.ipaddress = None
        self.mime_string = None

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

        Because Rackspace Cloud Servers do not have the metadata
        service running, we have to transfer the user-data file to the
        server.

        """
        pyrax.set_setting("identity_type", "rackspace")
        pyrax.set_credential_file("/opt/stack/heat/heat/engine/resources/rackspace/rs-pyrax-creds.txt")

        #name = self.properties['InstanceType']
        name = "cloud-server-vanilla"
        #image = self.properties['ImageId']
        image = "e4dbdba7-b2a4-4ee5-8e8f-4595b6d694ce"  # Ubuntu 12.04
        #flavor = self.properties['InstanceType']
        flavor = "2"
        rsa = RSA.generate(1024)
        private_key = rsa.exportKey()
        private_key_file = tempfile.NamedTemporaryFile()
        private_key_file.write(private_key)

        public_key = rsa.publickey().exportKey('OpenSSH')
        files={"/root/.ssh/authorized_keys": public_key}

        # Create server
        cs_ord = pyrax.connect_to_cloudservers(region="ORD")
        server = cs_ord.servers.create(name, image, flavor, files=files)
        complete = pyrax.utils.wait_until(server, "status",
                                          ["ACTIVE", "ERROR"], attempts=0)

        # Get public IP
        for public_ip in complete.addresses['public']:
            if public_ip['version'] == 4:
                ip = public_ip['addr']
        if not ip:
            raise exception.Error('Could not determine public IP of server')

        # Set up server
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key_file.seek(0)
        ssh.connect(ip,
                    username="root",
                    key_filename=private_key_file.name)

        # SFTP user-data file
        userdata = self.properties['UserData'] or ''
        userdata = self._build_userdata(userdata)
        userdata_file = tempfile.NamedTemporaryFile()
        userdata_file.write(userdata)
        private_key_file.seek(0)
        pkey = paramiko.RSAKey.from_private_key_file(private_key_file.name)
        transport = paramiko.Transport((ip, 22))
        transport.connect(hostkey=None, username="root", pkey=pkey)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(userdata_file.name, "/tmp/userdata")

        # SSH
        script = """echo "deb http://ppa.launchpad.net/steve-stevebaker/heat-cfntools/ubuntu precise main" >> /etc/apt/sources.list
gpg --keyserver keyserver.ubuntu.net --recv-keys 6D7D4795
apt-get update
apt-get install -y --force-yes cloud-init heat-cfntools
mkdir -p /var/lib/cloud/seed/nocloud-net
mv /tmp/userdata /var/lib/cloud/seed/nocloud-net/user-data
touch /var/lib/cloud/seed/nocloud-net/meta-data
date >> /var/log/cloud-init.log
cloud-init start >> /var/log/cloud-init.log
rm -f /root/.ssh/authorized_keys
"""
        stdin, stdout, stderr = ssh.exec_command(script)

        private_key_file.close()
        userdata_file.close()
        import pdb; pdb.set_trace()

    def handle_delete(self):
        raise NotImplementedError

    def handle_update(self):
        raise NotImplementedError


def resource_mapping():
    return {
        'Rackspace::CloudServer': CloudServer
    }
