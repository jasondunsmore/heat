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
import json

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
                'wait_secs': 0,
                'action_wait_secs': {'create': 1},
                'client_name': 'nova',
                'entity_name': 'servers',
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
                'wait_secs': 0,
                'action_wait_secs': {'update': 1}
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


class CreateStackTest(functional_base.FunctionalTestsBase):
    def setUp(self):
        super(CreateStackTest, self).setUp()

    def test_create_rollback(self):
        values = {'fail': True, 'value': 'test_create_rollback'}
        template = _change_rsrc_properties(test_template_one_resource,
                                           ['test1'], values)

        self.stack_create(
            template=template,
            expected_status='ROLLBACK_COMPLETE',
            disable_rollback=False)


class UpdateStackTest(functional_base.FunctionalTestsBase):

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
parameters:
  count:
    type: number
    default: 2
resources:
  test_group:
    type: OS::Heat::ResourceGroup
    properties:
      count: {get_param: count}
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

    fail_param_template = '''
heat_template_version: 2014-10-16
parameters:
  do_fail:
    type: boolean
    default: False
resources:
  aresource:
    type: OS::Heat::TestResource
    properties:
      value: Test
      fail: {get_param: do_fail}
      wait_secs: 1
'''

    def setUp(self):
        super(UpdateStackTest, self).setUp()

    def test_stack_update_nochange(self):
        template = _change_rsrc_properties(test_template_one_resource,
                                           ['test1'],
                                           {'value': 'test_no_change'})
        stack_identifier = self.stack_create(
            template=template)
        expected_resources = {'test1': 'OS::Heat::TestResource'}
        self.assertEqual(expected_resources,
                         self.list_resources(stack_identifier))

        # Update with no changes, resources should be unchanged
        self.update_stack(stack_identifier, template)
        self.assertEqual(expected_resources,
                         self.list_resources(stack_identifier))

    def test_stack_in_place_update(self):
        template = _change_rsrc_properties(test_template_one_resource,
                                           ['test1'],
                                           {'value': 'test_in_place'})
        stack_identifier = self.stack_create(
            template=template)
        expected_resources = {'test1': 'OS::Heat::TestResource'}
        self.assertEqual(expected_resources,
                         self.list_resources(stack_identifier))
        resource = self.client.resources.list(stack_identifier)
        initial_phy_id = resource[0].physical_resource_id

        tmpl_update = _change_rsrc_properties(
            test_template_one_resource, ['test1'],
            {'value': 'test_in_place_update'})
        # Update the Value
        self.update_stack(stack_identifier, tmpl_update)
        resource = self.client.resources.list(stack_identifier)
        # By default update_in_place
        self.assertEqual(initial_phy_id,
                         resource[0].physical_resource_id)

    def test_stack_update_replace(self):
        template = _change_rsrc_properties(test_template_one_resource,
                                           ['test1'],
                                           {'value': 'test_replace'})
        stack_identifier = self.stack_create(
            template=template)
        expected_resources = {'test1': 'OS::Heat::TestResource'}
        self.assertEqual(expected_resources,
                         self.list_resources(stack_identifier))
        resource = self.client.resources.list(stack_identifier)
        initial_phy_id = resource[0].physical_resource_id

        # Update the value and also set update_replace prop
        tmpl_update = _change_rsrc_properties(
            test_template_one_resource, ['test1'],
            {'value': 'test_in_place_update', 'update_replace': True})
        self.update_stack(stack_identifier, tmpl_update)
        resource = self.client.resources.list(stack_identifier)
        # update Replace
        self.assertNotEqual(initial_phy_id,
                            resource[0].physical_resource_id)

    def test_stack_update_add_remove(self):
        template = _change_rsrc_properties(test_template_one_resource,
                                           ['test1'],
                                           {'value': 'test_add_remove'})
        stack_identifier = self.stack_create(
            template=template)
        initial_resources = {'test1': 'OS::Heat::TestResource'}
        self.assertEqual(initial_resources,
                         self.list_resources(stack_identifier))

        tmpl_update = _change_rsrc_properties(
            test_template_two_resource, ['test1', 'test2'],
            {'value': 'test_add_remove_update'})
        # Add one resource via a stack update
        self.update_stack(stack_identifier, tmpl_update)
        updated_resources = {'test1': 'OS::Heat::TestResource',
                             'test2': 'OS::Heat::TestResource'}
        self.assertEqual(updated_resources,
                         self.list_resources(stack_identifier))

        # Then remove it by updating with the original template
        self.update_stack(stack_identifier, template)
        self.assertEqual(initial_resources,
                         self.list_resources(stack_identifier))

    def test_stack_update_rollback(self):
        template = _change_rsrc_properties(test_template_one_resource,
                                           ['test1'],
                                           {'value': 'test_update_rollback'})
        stack_identifier = self.stack_create(
            template=template)
        initial_resources = {'test1': 'OS::Heat::TestResource'}
        self.assertEqual(initial_resources,
                         self.list_resources(stack_identifier))

        tmpl_update = _change_rsrc_properties(
            test_template_two_resource, ['test1', 'test2'],
            {'value': 'test_update_rollback', 'fail': True})
        # stack update, also set failure
        self.update_stack(stack_identifier, tmpl_update,
                          expected_status='ROLLBACK_COMPLETE',
                          disable_rollback=False)
        # since stack update failed only the original resource is present
        updated_resources = {'test1': 'OS::Heat::TestResource'}
        self.assertEqual(updated_resources,
                         self.list_resources(stack_identifier))

    def test_stack_update_from_failed(self):
        # Prove it's possible to update from an UPDATE_FAILED state
        template = _change_rsrc_properties(test_template_one_resource,
                                           ['test1'],
                                           {'value': 'test_update_failed'})
        stack_identifier = self.stack_create(
            template=template)
        initial_resources = {'test1': 'OS::Heat::TestResource'}
        self.assertEqual(initial_resources,
                         self.list_resources(stack_identifier))

        tmpl_update = _change_rsrc_properties(
            test_template_one_resource, ['test1'], {'fail': True})
        # Update with bad template, we should fail
        self.update_stack(stack_identifier, tmpl_update,
                          expected_status='UPDATE_FAILED')
        # but then passing a good template should succeed
        self.update_stack(stack_identifier, test_template_two_resource)
        updated_resources = {'test1': 'OS::Heat::TestResource',
                             'test2': 'OS::Heat::TestResource'}
        self.assertEqual(updated_resources,
                         self.list_resources(stack_identifier))

    def test_stack_update_from_failed_resolve_invalid_type(self):
        """Test for bug 1588431.

        Whenever a stack has a resource with a property that
        resolves to an incorrect type, we should be able to update
        the stack with a valid template.
        """
        invalid_template = '''
heat_template_version: 2014-10-16
resources:
  random-string-grp:
    type: OS::Heat::ResourceGroup
    properties:
      count: 4
      resource_def:
        type: OS::Heat::RandomString
  single-random-string:
      type: OS::Heat::RandomString
      properties:
        length:
          str_replace:
            params:
              foo: {get_attr: [random-string-grp, value]}
            template: |
              foo1
'''
        valid_template = '''
heat_template_version: 2014-10-16
resources:
  random-string-grp:
    type: OS::Heat::ResourceGroup
    properties:
      count: 4
      resource_def:
        type: OS::Heat::RandomString
  single-random-string:
      type: OS::Heat::RandomString
      properties:
        length: 8
'''
        stack_identifier = self.stack_create(template=invalid_template,
                                             expected_status='CREATE_FAILED')
        self.update_stack(stack_identifier, template=valid_template,
                          expected_status='UPDATE_COMPLETE')

    def test_stack_update_provider(self):
        template = _change_rsrc_properties(
            test_template_one_resource, ['test1'],
            {'value': 'test_provider_template'})
        files = {'provider.template': json.dumps(template)}
        env = {'resource_registry':
               {'My::TestResource': 'provider.template'}}
        stack_identifier = self.stack_create(
            template=self.provider_template,
            files=files,
            environment=env
        )

        initial_resources = {'test1': 'My::TestResource'}
        self.assertEqual(initial_resources,
                         self.list_resources(stack_identifier))

        # Prove the resource is backed by a nested stack, save the ID
        nested_identifier = self.assert_resource_is_a_stack(stack_identifier,
                                                            'test1')
        nested_id = nested_identifier.split('/')[-1]

        # Then check the expected resources are in the nested stack
        nested_resources = {'test1': 'OS::Heat::TestResource'}
        self.assertEqual(nested_resources,
                         self.list_resources(nested_identifier))
        tmpl_update = _change_rsrc_properties(
            test_template_two_resource, ['test1', 'test2'],
            {'value': 'test_provider_template'})
        # Add one resource via a stack update by changing the nested stack
        files['provider.template'] = json.dumps(tmpl_update)
        self.update_stack(stack_identifier, self.provider_template,
                          environment=env, files=files)

        # Parent resources should be unchanged and the nested stack
        # should have been updated in-place without replacement
        self.assertEqual(initial_resources,
                         self.list_resources(stack_identifier))
        rsrc = self.client.resources.get(stack_identifier, 'test1')
        self.assertEqual(rsrc.physical_resource_id, nested_id)

        # Then check the expected resources are in the nested stack
        nested_resources = {'test1': 'OS::Heat::TestResource',
                            'test2': 'OS::Heat::TestResource'}
        self.assertEqual(nested_resources,
                         self.list_resources(nested_identifier))

    def test_stack_update_alias_type(self):
        env = {'resource_registry':
               {'My::TestResource': 'OS::Heat::RandomString',
                'My::TestResource2': 'OS::Heat::RandomString'}}
        stack_identifier = self.stack_create(
            template=self.provider_template,
            environment=env
        )
        p_res = self.client.resources.get(stack_identifier, 'test1')
        self.assertEqual('My::TestResource', p_res.resource_type)

        initial_resources = {'test1': 'My::TestResource'}
        self.assertEqual(initial_resources,
                         self.list_resources(stack_identifier))
        res = self.client.resources.get(stack_identifier, 'test1')
        # Modify the type of the resource alias to My::TestResource2
        tmpl_update = copy.deepcopy(self.provider_template)
        tmpl_update['resources']['test1']['type'] = 'My::TestResource2'
        self.update_stack(stack_identifier, tmpl_update, environment=env)
        res_a = self.client.resources.get(stack_identifier, 'test1')
        self.assertEqual(res.physical_resource_id, res_a.physical_resource_id)
        self.assertEqual(res.attributes['value'], res_a.attributes['value'])

    def test_stack_update_alias_changes(self):
        env = {'resource_registry':
               {'My::TestResource': 'OS::Heat::RandomString'}}
        stack_identifier = self.stack_create(
            template=self.provider_template,
            environment=env
        )
        p_res = self.client.resources.get(stack_identifier, 'test1')
        self.assertEqual('My::TestResource', p_res.resource_type)

        initial_resources = {'test1': 'My::TestResource'}
        self.assertEqual(initial_resources,
                         self.list_resources(stack_identifier))
        res = self.client.resources.get(stack_identifier, 'test1')
        # Modify the resource alias to point to a different type
        env = {'resource_registry':
               {'My::TestResource': 'OS::Heat::TestResource'}}
        self.update_stack(stack_identifier, template=self.provider_template,
                          environment=env)
        res_a = self.client.resources.get(stack_identifier, 'test1')
        self.assertNotEqual(res.physical_resource_id,
                            res_a.physical_resource_id)

    def test_stack_update_provider_type(self):
        template = _change_rsrc_properties(
            test_template_one_resource, ['test1'],
            {'value': 'test_provider_template'})
        files = {'provider.template': json.dumps(template)}
        env = {'resource_registry':
               {'My::TestResource': 'provider.template',
                'My::TestResource2': 'provider.template'}}
        stack_identifier = self.stack_create(
            template=self.provider_template,
            files=files,
            environment=env
        )
        p_res = self.client.resources.get(stack_identifier, 'test1')
        self.assertEqual('My::TestResource', p_res.resource_type)

        initial_resources = {'test1': 'My::TestResource'}
        self.assertEqual(initial_resources,
                         self.list_resources(stack_identifier))

        # Prove the resource is backed by a nested stack, save the ID
        nested_identifier = self.assert_resource_is_a_stack(stack_identifier,
                                                            'test1')
        nested_id = nested_identifier.split('/')[-1]

        # Then check the expected resources are in the nested stack
        nested_resources = {'test1': 'OS::Heat::TestResource'}
        self.assertEqual(nested_resources,
                         self.list_resources(nested_identifier))
        n_res = self.client.resources.get(nested_identifier, 'test1')

        # Modify the type of the provider resource to My::TestResource2
        tmpl_update = copy.deepcopy(self.provider_template)
        tmpl_update['resources']['test1']['type'] = 'My::TestResource2'
        self.update_stack(stack_identifier, tmpl_update,
                          environment=env, files=files)
        p_res = self.client.resources.get(stack_identifier, 'test1')
        self.assertEqual('My::TestResource2', p_res.resource_type)

        # Parent resources should be unchanged and the nested stack
        # should have been updated in-place without replacement
        self.assertEqual({u'test1': u'My::TestResource2'},
                         self.list_resources(stack_identifier))
        rsrc = self.client.resources.get(stack_identifier, 'test1')
        self.assertEqual(rsrc.physical_resource_id, nested_id)

        # Then check the expected resources are in the nested stack
        self.assertEqual(nested_resources,
                         self.list_resources(nested_identifier))
        n_res2 = self.client.resources.get(nested_identifier, 'test1')
        self.assertEqual(n_res.physical_resource_id,
                         n_res2.physical_resource_id)

    def test_stack_update_provider_group(self):
        """Test two-level nested update."""

        # Create a ResourceGroup (which creates a nested stack),
        # containing provider resources (which create a nested
        # stack), thus exercising an update which traverses
        # two levels of nesting.
        template = _change_rsrc_properties(
            test_template_one_resource, ['test1'],
            {'value': 'test_provider_group_template'})
        files = {'provider.template': json.dumps(template)}
        env = {'resource_registry':
               {'My::TestResource': 'provider.template'}}

        stack_identifier = self.stack_create(
            template=self.provider_group_template,
            files=files,
            environment=env
        )

        initial_resources = {'test_group': 'OS::Heat::ResourceGroup'}
        self.assertEqual(initial_resources,
                         self.list_resources(stack_identifier))

        # Prove the resource is backed by a nested stack, save the ID
        nested_identifier = self.assert_resource_is_a_stack(stack_identifier,
                                                            'test_group')

        # Then check the expected resources are in the nested stack
        nested_resources = {'0': 'My::TestResource',
                            '1': 'My::TestResource'}
        self.assertEqual(nested_resources,
                         self.list_resources(nested_identifier))

        for n_rsrc in nested_resources:
            rsrc = self.client.resources.get(nested_identifier, n_rsrc)
            provider_stack = self.client.stacks.get(rsrc.physical_resource_id)
            provider_identifier = '%s/%s' % (provider_stack.stack_name,
                                             provider_stack.id)
            provider_resources = {u'test1': u'OS::Heat::TestResource'}
            self.assertEqual(provider_resources,
                             self.list_resources(provider_identifier))

        tmpl_update = _change_rsrc_properties(
            test_template_two_resource, ['test1', 'test2'],
            {'value': 'test_provider_group_template'})
        # Add one resource via a stack update by changing the nested stack
        files['provider.template'] = json.dumps(tmpl_update)
        self.update_stack(stack_identifier, self.provider_group_template,
                          environment=env, files=files)

        # Parent resources should be unchanged and the nested stack
        # should have been updated in-place without replacement
        self.assertEqual(initial_resources,
                         self.list_resources(stack_identifier))

        # Resource group stack should also be unchanged (but updated)
        nested_stack = self.client.stacks.get(nested_identifier)
        self.assertEqual('UPDATE_COMPLETE', nested_stack.stack_status)
        self.assertEqual(nested_resources,
                         self.list_resources(nested_identifier))

        for n_rsrc in nested_resources:
            rsrc = self.client.resources.get(nested_identifier, n_rsrc)
            provider_stack = self.client.stacks.get(rsrc.physical_resource_id)
            provider_identifier = '%s/%s' % (provider_stack.stack_name,
                                             provider_stack.id)
            provider_resources = {'test1': 'OS::Heat::TestResource',
                                  'test2': 'OS::Heat::TestResource'}
            self.assertEqual(provider_resources,
                             self.list_resources(provider_identifier))

    def test_stack_update_with_replacing_userdata(self):
        """Test case for updating userdata of instance.

        Confirm that we can update userdata of instance during updating stack
        by the user of member role.

        Make sure that a resource that inherits from StackUser can be deleted
        during updating stack.
        """
        if not self.conf.minimal_image_ref:
            raise self.skipException("No minimal image configured to test")
        if not self.conf.minimal_instance_type:
            raise self.skipException("No flavor configured to test")

        parms = {'flavor': self.conf.minimal_instance_type,
                 'image': self.conf.minimal_image_ref,
                 'network': self.conf.fixed_network_name,
                 'user_data': ''}

        stack_identifier = self.stack_create(
            template=self.update_userdata_template,
            parameters=parms
        )

        parms_updated = parms
        parms_updated['user_data'] = 'two'
        self.update_stack(
            stack_identifier,
            template=self.update_userdata_template,
            parameters=parms_updated)

    def test_stack_update_provider_group_patch(self):
        '''Test two-level nested update with PATCH'''
        template = _change_rsrc_properties(
            test_template_one_resource, ['test1'],
            {'value': 'test_provider_group_template'})
        files = {'provider.template': json.dumps(template)}
        env = {'resource_registry':
               {'My::TestResource': 'provider.template'}}

        stack_identifier = self.stack_create(
            template=self.provider_group_template,
            files=files,
            environment=env
        )

        initial_resources = {'test_group': 'OS::Heat::ResourceGroup'}
        self.assertEqual(initial_resources,
                         self.list_resources(stack_identifier))

        # Prove the resource is backed by a nested stack, save the ID
        nested_identifier = self.assert_resource_is_a_stack(stack_identifier,
                                                            'test_group')

        # Then check the expected resources are in the nested stack
        nested_resources = {'0': 'My::TestResource',
                            '1': 'My::TestResource'}
        self.assertEqual(nested_resources,
                         self.list_resources(nested_identifier))

        # increase the count, pass only the paramter, no env or template
        params = {'count': 3}
        self.update_stack(stack_identifier, parameters=params, existing=True)

        # Parent resources should be unchanged and the nested stack
        # should have been updated in-place without replacement
        self.assertEqual(initial_resources,
                         self.list_resources(stack_identifier))

        # Resource group stack should also be unchanged (but updated)
        nested_stack = self.client.stacks.get(nested_identifier)
        self.assertEqual('UPDATE_COMPLETE', nested_stack.stack_status)
        # Add a resource, as we should have added one
        nested_resources['2'] = 'My::TestResource'
        self.assertEqual(nested_resources,
                         self.list_resources(nested_identifier))

    def test_stack_update_from_failed_patch(self):
        '''Test PATCH update from a failed state.'''

        # Start with empty template
        stack_identifier = self.stack_create(
            template='heat_template_version: 2014-10-16')

        # Update with a good template, but bad parameter
        self.update_stack(stack_identifier,
                          template=self.fail_param_template,
                          parameters={'do_fail': True},
                          expected_status='UPDATE_FAILED')

        # PATCH update, only providing the parameter
        self.update_stack(stack_identifier,
                          parameters={'do_fail': False},
                          existing=True)
        self.assertEqual({u'aresource': u'OS::Heat::TestResource'},
                         self.list_resources(stack_identifier))

    def test_stack_update_with_new_env(self):
        """Update handles new resource types in the environment.

        If a resource type appears during an update and the update fails,
        retrying the update is able to find the type properly in the
        environment.
        """
        stack_identifier = self.stack_create(
            template=test_template_one_resource)

        # Update with a new resource and make the update fails
        template = _change_rsrc_properties(test_template_one_resource,
                                           ['test1'], {'fail': True})
        template['resources']['test2'] = {'type': 'My::TestResource'}
        template['resources']['test1']['depends_on'] = 'test2'
        env = {'resource_registry':
               {'My::TestResource': 'OS::Heat::TestResource'}}
        self.update_stack(stack_identifier,
                          template=template,
                          environment=env,
                          expected_status='UPDATE_FAILED')

        # Fixing the template should fix the stack
        template = _change_rsrc_properties(template,
                                           ['test1'], {'fail': False})
        self.update_stack(stack_identifier,
                          template=template,
                          environment=env)
        self.assertEqual({'test1': 'OS::Heat::TestResource',
                          'test2': 'My::TestResource'},
                         self.list_resources(stack_identifier))
