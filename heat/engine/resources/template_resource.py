# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
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

from heat.common import template_format

from heat.engine import attributes
from heat.engine import properties
from heat.engine import resource
from heat.engine import stack_resource

from heat.openstack.common import log as logging

logger = logging.getLogger(__name__)


class TemplateResource(stack_resource.StackResource):
    '''
    A resource implemented by a nested stack.

    This implementation passes resource properties as parameters to the nested
    stack. Outputs of the nested stack are exposed as attributes of this
    resource.
    '''

    def __init__(self, name, json_snippet, stack):
        self.template_name = stack.env.get_resource_type(json_snippet['Type'],
                                                         name)
        self.__parsed = None
        self.stack = stack
        # on purpose don't pass in the environment so we get
        # the official/facade class in case we need to copy it's schema.
        cls_facade = resource.get_class(json_snippet['Type'])
        # if we're not overriding via the environment, mirror the template as
        # a new resource
        if cls_facade == self.__class__:
            self.properties_schema = (properties.Properties
                .schema_from_params(self.parsed_nested.get('Parameters')))
            self.attributes_schema = (attributes.Attributes
                .schema_from_outputs(self.parsed_nested.get('Outputs')))
        # otherwise we are overriding a resource type via the environment
        # and should mimic that type
        else:
            self.properties_schema = cls_facade.properties_schema
            self.attributes_schema = cls_facade.attributes_schema

        super(TemplateResource, self).__init__(name, json_snippet, stack)

    def _to_parameters(self):
        '''
        :return: parameter values for our nested stack based on our properties
        '''
        params = {}
        for n, v in iter(self.properties.props.items()):
            if not v.implemented():
                continue
            elif v.type() == properties.LIST:
                # take a list and create a CommaDelimitedList
                val = self.properties[n]
                if val:
                    params[n] = ','.join(val)
            else:
                # for MAP, the JSON param takes either a collection or string,
                # so just pass it on and let the param validate as appropriate
                params[n] = self.properties[n]

        return params

    @property
    def parsed_nested(self):
        if not self.__parsed:
            self.__parsed = template_format.parse(self.template_data)
        return self.__parsed

    @property
    def template_data(self):
        t_data = self.stack.t.files.get(self.template_name)
        if not t_data and self.template_name.endswith((".yaml", ".template")):
            # late import since these can be expensive
            import urllib2
            from heat.common import urlfetch
            try:
                t_data = urlfetch.get(self.template_name)
            except urllib2.URLError as urle:
                raise ValueError("Could not fetch remote template '%s': %s" %
                                 (self.template_name, str(urle)))
            else:
                self.stack.t.files[self.template_name] = t_data
        return t_data

    def handle_create(self):
        return self.create_with_template(self.parsed_nested,
                                         self._to_parameters())

    def handle_delete(self):
        self.delete_nested()

    def FnGetRefId(self):
        if not self.nested():
            return unicode(self.name)
        return self.nested().identifier().arn()


resource.register_template_class(TemplateResource)
