from heat.engine import resource
from heat.openstack.common import log as logging
from novaclient import client as novaclient
from heat.common import short_id
import json
from oslo.config import cfg
from email.mime.text import MIMEText
import pkgutil
import os
from urlparse import urlparse
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

def resource_mapping():
    return {
        'Rackspace::CloudServer': CloudServer
    }

def read_value(filename):
    with open(filename, 'r') as f:
        return f.read()

class CloudServer(resource.Resource):
    properties_schema = {
        'name': {'Type': 'String'}}

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

    def handle_create(self):
        """Create a container."""
        server_name = "testserver2"
        auth_url = "https://identity.api.rackspacecloud.com/v2.0/"
        password = read_value("/tmp/.p")
        tenant = read_value("/tmp/.a")
        user = read_value("/tmp/.u")
        #raw_userdata = self.properties['UserData'] or ''
        #userdata = _build_user_data(raw_userdata)
        client = novaclient.Client(
            1.1,
            user,
            password,
            tenant,
            auth_url=auth_url,
            region_name="ORD"
        )
        # TODO: build user_data and make it available via HTTP
        # TODO: create empty meta_data file
        user_data_url = "http://dunsmor.com/pastebin/1370288963.txt"
        result = client.servers.create(
            server_name,  # name of server
            "82f4a4ee-0266-48f6-a328-0681f893229d",  # image
            "2",  # flavor
            files={"/tmp/user-data-url": user_data_url}
        )

        print "ID:", result.id
        print "Root pass:", result.adminPass

    def handle_delete(self):
        raise NotImplementedError

    def handle_update(self):
        raise NotImplementedError

