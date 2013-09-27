

from heat.engine import stack_resource
from heat.engine.resources import server
from heat.openstack.common import log as logging

logger = logging.getLogger(__name__)


class ResourceGroup(stack_resource.StackResource):

    properties_schema = {
        'count': {'Type': 'Number', 'Required': True},
        'resource_def': {'Type': 'Map', 'Required': True}
    }

    update_allowed_keys = ('properties')
    update_allowed_properties = ('resource_name')

    # TODO: Is there already global resource mapping?
    res_map = {'OS::Heat::Server': server.Server}

    def __init__(self, name, json_snippet, stack):
        super(ResourceGroup, self).__init__(name, json_snippet, stack)

        count = self.json_snippet['count']
        resource_def = self.json_snippet['resource_def']
        res_class = self.res_map[resource_def['type']]

        self.resources = []
        for resource_num in range(count):
            resource = res_class("test", resource_def, self.stack)
            resource.name = resource.name + str(resource_num)
            self.resources.append(resource)

    def validate(self):
        for resource in self.resources:
            resource.validate()



def resource_mapping():
    return {'OS::Heat::ResourceGroup': ResourceGroup}
