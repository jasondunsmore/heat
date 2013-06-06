from heat.engine import resource
from heat.openstack.common import log as logging
from novaclient import client as novaclient
from heat.common import short_id, exception
import json
from oslo.config import cfg
from email.mime.text import MIMEText
import pkgutil
import os
from urlparse import urlparse
from email.mime.multipart import MIMEMultipart
import BaseHTTPServer
from socket import AF_INET, SOCK_STREAM, socket
import urllib2

logger = logging.getLogger(__name__)

def read_value(filename):
    with open(filename, 'r') as f:
        return f.read()

class UserDataHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        with open("/tmp/user-data", 'r') as f:
            userdata = f.read()
        self.send_response(200)
        self.send_header("Content-type", type)
        self.send_header("Content-length", str(len(userdata)))
        self.end_headers()
        self.wfile.write(userdata)

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

            attachments.append((cfg.CONF.heat_watch_server_url,
                                'cfn-watch-server', 'x-cfninitdata'))

            attachments.append((cfg.CONF.heat_metadata_server_url,
                                'cfn-metadata-server', 'x-cfninitdata'))

            # Create a boto config which the cfntools on the host use to know
            # where the cfn and cw API's are to be accessed
            cfn_url = urlparse(cfg.CONF.heat_metadata_server_url)
            cw_url = urlparse(cfg.CONF.heat_watch_server_url)
            is_secure = cfg.CONF.instance_connection_is_secure
            vcerts = cfg.CONF.instance_connection_https_validate_certificates
            boto_cfg = "\n".join(["[Boto]",
                                  "debug = 0",
                                  "is_secure = %s" % is_secure,
                                  "https_validate_certificates = %s" % vcerts,
                                  "cfn_region_name = heat",
                                  "cfn_region_endpoint = %s" %
                                  cfn_url.hostname,
                                  "cloudwatch_region_name = heat",
                                  "cloudwatch_region_endpoint = %s" %
                                  cw_url.hostname])
            attachments.append((boto_cfg,
                                'cfn-boto-cfg', 'x-cfninitdata'))

            subparts = [make_subpart(*args) for args in attachments]
            mime_blob = MIMEMultipart(_subparts=subparts)

            self.mime_string = mime_blob.as_string()

        return self.mime_string

    def _serve_userdata(self, port):
        raw_userdata = self.properties['UserData'] or ''
        userdata = self._build_userdata(raw_userdata)
        with open("/tmp/user-data", 'w') as f:
            f.write(userdata)
        httpd = BaseHTTPServer.HTTPServer(('', port), UserDataHandler)
        httpd.timeout = 600
        httpd.handle_request()  # wait for server to fetch userdata
        httpd.server_close()

    def _find_available_port(self, start, end):
        port = start
        s = socket(AF_INET, SOCK_STREAM)
        while True:
            result = s.connect_ex(("127.0.0.1", port))
            if result != 0:  # 0 means the port is open
                s.close()
                return port
            elif port >= end:
                s.close()
                raise exception.Error("No open ports between %s and %s"
                                      % (start, end))
            else:
                port += 1

    def handle_create(self):
        """Create a container.

        Because Rackspace Cloud Servers do not have the metadata
        service running, we have to transfer the user-data file to the
        server.  This is done via an HTTP call to the Heat server from
        the Cloud Server, so the ports 9000-9100 must be accessible
        from the Cloud Server.

        """
        auth_url = "https://identity.api.rackspacecloud.com/v2.0/"
        password = read_value("/tmp/.p")
        tenant = read_value("/tmp/.a")
        user = read_value("/tmp/.u")
        client = novaclient.Client(
            1.1,
            user,
            password,
            tenant,
            auth_url=auth_url,
            region_name="ORD"
        )

        server_name = "cloud-init-build-userdata-debugging3"
        image = "dd979f2c-2805-422f-af31-ef6b63ef9f5e"
        flavor = "2"
        # TODO(jason): Find a better way to obtain public IP address
        ip = urllib2.urlopen('http://ip.42.pl/raw').read()
        port = self._find_available_port(9000, 9100)
        userdata_url = "http://" + ip + ":" + str(port)
        files={"/tmp/user-data-url": userdata_url}
        result = client.servers.create(server_name, image, flavor, files=files)
        self._serve_userdata(port)

        print "ID:", result.id
        print "Root pass:", result.adminPass

    def handle_delete(self):
        raise NotImplementedError

    def handle_update(self):
        raise NotImplementedError


def resource_mapping():
    return {
        'Rackspace::CloudServer': CloudServer
    }
