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


import copy

from heat_integrationtests.functional import functional_base

test_template_one_resource = {
    'heat_template_version': '2013-05-23',
    'description': 'Test template to create one instance.',
    'resources': {
        'test1': {
            'type': 'OS::Heat::TestResource',
            'properties': {
                'value': 'Test1',
                'fail': False,
                'update_replace': False,
                'wait_secs': 0
            }
        }
    }
}

test_template_two_resource = {
    'heat_template_version': '2013-05-23',
    'description': 'Test template to create two instance.',
    'resources': {
        'test1': {
            'type': 'OS::Heat::TestResource',
            'properties': {
                'value': 'Test1',
                'fail': False,
                'update_replace': False,
                'wait_secs': 0
            }
        },
        'test2': {
            'type': 'OS::Heat::TestResource',
            'properties': {
                'value': 'Test1',
                'fail': False,
                'update_replace': False,
                'wait_secs': 0
            }
        }
    }
}


def _change_rsrc_properties(template, rsrcs, values):
        modified_template = copy.deepcopy(template)
        for rsrc_name in rsrcs:
            rsrc_prop = modified_template['resources'][
                rsrc_name]['properties']
            for prop in rsrc_prop:
                if prop in values:
                    rsrc_prop[prop] = values[prop]
        return modified_template


class UpdatePreviewStackTest(functional_base.FunctionalTestsBase):

    provider_template = {
        'heat_template_version': '2013-05-23',
        'description': 'foo',
        'resources': {
            'test1': {
                'type': 'My::TestResource'
            }
        }
    }

    provider_group_template = '''
heat_template_version: 2013-05-23
resources:
  test_group:
    type: OS::Heat::ResourceGroup
    properties:
      count: 2
      resource_def:
        type: My::TestResource
'''

    update_userdata_template = '''
heat_template_version: 2014-10-16
parameters:
  flavor:
    type: string
  user_data:
    type: string
  image:
    type: string
  network:
    type: string

resources:
  server:
    type: OS::Nova::Server
    properties:
      image: {get_param: image}
      flavor: {get_param: flavor}
      networks: [{network: {get_param: network} }]
      user_data_format: SOFTWARE_CONFIG
      user_data: {get_param: user_data}
'''

    def test_add_resource(self):
        stack_identifier = self.stack_create(
            template=test_template_one_resource)
        expected_resources = {'test1': 'OS::Heat::TestResource'}
        self.assertEqual(expected_resources,
                         self.list_resources(stack_identifier))

        # Update with no changes, resources should be unchanged
        self.preview_update_stack(stack_identifier, test_template_two_resource)
        self.assertEqual(expected_resources,
                         self.list_resources(stack_identifier))

    def test_no_change(self):
        pass
