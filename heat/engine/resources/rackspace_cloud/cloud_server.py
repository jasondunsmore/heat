from heat.engine import resource
from heat.openstack.common import log as logging
from novaclient import client as novaclient
from heat.common import short_id

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

    def handle_create(self):
        """Create a container."""
        server_name = "testserver2"
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
        # TODO: build user_data and make it available via HTTP
        user_data_url = "http://dunsmor.com/pastebin/1370288963.txt"
        result = client.servers.create(
            server_name,  # name of server
            "4588a7fc-d199-4d12-98fb-bfe952035e05",  # image
            "2",  # flavor
            config_drive=True,  # metadata service alt
            files={"/tmp/user-data-url": user_data_url}
        )

        # /etc/init/cloud-init.conf:

        # start on mounted MOUNTPOINT=/ and stopped cloud-init-nonet
        #
        # task
        #
        # console output
        #
        # pre-start script
        #   user_data_url=$(cat /tmp/user-data-url)
        #   mkdir -p /var/lib/cloud/seed/nocloud-net
        #   curl $user_data_url > /var/lib/cloud/nocloud-net/heat/user-data
        # end script
        #
        # exec /usr/bin/cloud-init start

        print "ID:", result.id
        print "Root pass:", result.adminPass

    def handle_delete(self):
        raise NotImplementedError

    def handle_update(self):
        raise NotImplementedError

