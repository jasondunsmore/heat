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
    tags_schema = {'Key': {'Type': 'String',
                           'Required': True},
                   'Value': {'Type': 'String',
                             'Required': True}}

    properties_schema = {'ImageId': {'Type': 'String',
                                     'Required': True},
                         'InstanceType': {'Type': 'String',
                                          'Required': True},
                         'KeyName': {'Type': 'String'},
                         'AvailabilityZone': {'Type': 'String'},
                         'DisableApiTermination': {'Type': 'String',
                                                   'Implemented': False},
                         'KernelId': {'Type': 'String',
                                      'Implemented': False},
                         'Monitoring': {'Type': 'Boolean',
                                        'Implemented': False},
                         'PlacementGroupName': {'Type': 'String',
                                                'Implemented': False},
                         'PrivateIpAddress': {'Type': 'String',
                                              'Implemented': False},
                         'RamDiskId': {'Type': 'String',
                                       'Implemented': False},
                         'SecurityGroups': {'Type': 'List'},
                         'SecurityGroupIds': {'Type': 'List'},
                         'NetworkInterfaces': {'Type': 'List'},
                         'SourceDestCheck': {'Type': 'Boolean',
                                             'Implemented': False},
                         'SubnetId': {'Type': 'String'},
                         'Tags': {'Type': 'List',
                                  'Schema': {'Type': 'Map',
                                             'Schema': tags_schema}},
                         'NovaSchedulerHints': {'Type': 'List',
                                                'Schema': {
                                                    'Type': 'Map',
                                                    'Schema': tags_schema
                                                }},
                         'Tenancy': {'Type': 'String',
                                     'AllowedValues': ['dedicated', 'default'],
                                     'Implemented': False},
                         'UserData': {'Type': 'String'},
                         'Volumes': {'Type': 'List'}}

    # template keys supported for handle_update
    update_allowed_keys = ('Metadata',)

    _deferred_server_statuses = ['BUILD',
                                 'HARD_REBOOT',
                                 'PASSWORD',
                                 'REBOOT',
                                 'RESCUE',
                                 'RESIZE',
                                 'REVERT_RESIZE',
                                 'SHUTOFF',
                                 'SUSPENDED',
                                 'VERIFY_RESIZE']

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
        flavor = self.properties['InstanceType']
        
        client = novaclient.Client(
            1.1,
            self.context.user,
            self.context.password,
            self.context.tenant,
            auth_url=self.context.auth_url,
            region_name="ORD"
        )
        result = client.servers.create(
            self.name,  # name of server
            "31e1b5ee-ef2f-4f2a-8cbc-9d0ae412231c",  # image
            "2",  # flavor
            config_drive=True  # metadata service alt
        )
        print "ID:", result.id
        print "Root pass:", result.adminPass

    def handle_delete(self):
        raise NotImplementedError

    def handle_update(self):
        raise NotImplementedError

