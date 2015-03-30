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

import copy

import mock

from heat.common import template_format
from heat.engine import environment
from heat.engine import resource
from heat.engine import scheduler
from heat.engine import stack
from heat.engine import template
from heat.tests import common
from heat.tests import generic_resource as generic_rsrc
from heat.tests import utils

empty_template = template_format.parse('''{
  "HeatTemplateFormatVersion" : "2012-12-12",
}''')


class StackUpdateTest(common.HeatTestCase):
    def setUp(self):
        super(StackUpdateTest, self).setUp()

        self.tmpl = template.Template(copy.deepcopy(empty_template))
        self.ctx = utils.dummy_context()

        resource._register_class('GenericResourceType',
                                 generic_rsrc.GenericResource)
        resource._register_class('ResourceWithPropsType',
                                 generic_rsrc.ResourceWithProps)
        resource._register_class('ResWithComplexPropsAndAttrs',
                                 generic_rsrc.ResWithComplexPropsAndAttrs)

    def test_update_add(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl))
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {
                     'AResource': {'Type': 'GenericResourceType'},
                     'BResource': {'Type': 'GenericResourceType'}}}
        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertIn('BResource', self.stack)

    def test_update_remove(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {
                    'AResource': {'Type': 'GenericResourceType'},
                    'BResource': {'Type': 'GenericResourceType'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl))
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertNotIn('BResource', self.stack)

    def test_update_description(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Description': 'ATemplate',
                'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl))
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Description': 'BTemplate',
                 'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('BTemplate',
                         self.stack.t[self.stack.t.DESCRIPTION])

    def test_update_timeout(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Description': 'ATemplate',
                'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl), timeout_mins=60)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Description': 'ATemplate',
                 'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2), timeout_mins=30)
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual(30, self.stack.timeout_mins)

    def test_update_disable_rollback(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Description': 'ATemplate',
                'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=False)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Description': 'ATemplate',
                 'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2),
                                    disable_rollback=True)
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual(True, self.stack.disable_rollback)

    def test_update_tags(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Description': 'ATemplate',
                'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 tags=['tag1', 'tag2'])
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual(['tag1', 'tag2'], self.stack.tags)

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl),
                                    tags=['tag3', 'tag4'])
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual(['tag3', 'tag4'], self.stack.tags)

    def test_update_tags_remove_all(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Description': 'ATemplate',
                'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 tags=['tag1', 'tag2'])
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual(['tag1', 'tag2'], self.stack.tags)

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl))
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual(None, self.stack.tags)

    def test_update_modify_ok_replace(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                            'Properties': {'Foo': 'abc'}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl))
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                             'Properties': {'Foo': 'xyz'}}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))

        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('xyz', self.stack['AResource'].properties['Foo'])

        loaded_stack = stack.Stack.load(self.ctx, self.stack.id)
        stored_props = loaded_stack['AResource']._stored_properties_data
        self.assertEqual({'Foo': 'xyz'}, stored_props)

    def test_update_modify_ok_replace_int(self):
        # create
        # ========
        tmpl = {'heat_template_version': '2013-05-23',
                'resources': {'AResource': {
                    'type': 'ResWithComplexPropsAndAttrs',
                    'properties': {'an_int': 1}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl))
        self.stack.store()
        stack_id = self.stack.id
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        value1 = 2
        prop_diff1 = {'an_int': value1}
        value2 = 1
        prop_diff2 = {'an_int': value2}

        mock_upd = self.patchobject(generic_rsrc.ResWithComplexPropsAndAttrs,
                                    'handle_update')

        # update 1
        # ==========

        self.stack = stack.Stack.load(self.ctx, stack_id=stack_id)
        tmpl2 = {'heat_template_version': '2013-05-23',
                 'resources': {'AResource': {
                     'type': 'ResWithComplexPropsAndAttrs',
                     'properties': {'an_int': value1}}}}
        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))

        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        mock_upd.assert_called_once_with(mock.ANY, mock.ANY, prop_diff1)

        # update 2
        # ==========
        # reload the previous stack
        self.stack = stack.Stack.load(self.ctx, stack_id=stack_id)
        tmpl3 = {'heat_template_version': '2013-05-23',
                 'resources': {'AResource': {
                     'type': 'ResWithComplexPropsAndAttrs',
                     'properties': {'an_int': value2}}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl3))

        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)

        mock_upd.assert_called_with(mock.ANY, mock.ANY, prop_diff2)

    def test_update_modify_param_ok_replace(self):
        tmpl = {
            'HeatTemplateFormatVersion': '2012-12-12',
            'Parameters': {
                'foo': {'Type': 'String'}
            },
            'Resources': {
                'AResource': {
                    'Type': 'ResourceWithPropsType',
                    'Properties': {'Foo': {'Ref': 'foo'}}
                }
            }
        }

        self.stack = stack.Stack(
            self.ctx, 'update_test_stack',
            template.Template(
                tmpl, env=environment.Environment({'foo': 'abc'})))
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        env2 = environment.Environment({'foo': 'xyz'})
        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl, env=env2))

        def check_and_raise(*args):
            self.assertEqual('abc', self.stack['AResource'].properties['Foo'])
            raise resource.UpdateReplace

        mock_upd = self.patchobject(generic_rsrc.ResourceWithProps,
                                    'update_template_diff',
                                    side_effect=check_and_raise)

        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('xyz', self.stack['AResource'].properties['Foo'])
        mock_upd.assert_called_once_with(
            {'Type': 'ResourceWithPropsType',
             'Properties': {'Foo': 'xyz'}},
            {'Type': 'ResourceWithPropsType',
             'Properties': {'Foo': 'abc'}})

    def test_update_modify_update_failed(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                            'Properties': {'Foo': 'abc'}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=True)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        res = self.stack['AResource']
        res.update_allowed_properties = ('Foo',)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                             'Properties': {'Foo': 'xyz'}}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))

        mock_upd = self.patchobject(generic_rsrc.ResourceWithProps,
                                    'handle_update',
                                    side_effect=Exception("Foo"))

        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.FAILED),
                         self.stack.state)
        mock_upd.assert_called_once_with(
            tmpl2['Resources']['AResource'],
            {'Properties': {'Foo': 'xyz'}},
            {'Foo': 'xyz'})

    def test_update_modify_replace_failed_delete(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                            'Properties': {'Foo': 'abc'}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=True)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                             'Properties': {'Foo': 'xyz'}}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))

        # make the update fail deleting the existing resource
        mock_del = self.patchobject(generic_rsrc.ResourceWithProps,
                                    'handle_delete',
                                    side_effect=Exception)

        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.FAILED),
                         self.stack.state)
        mock_del.assert_called_once_with()
        # Unset here so destroy() is not stubbed for stack.delete cleanup
        self.m.UnsetStubs()

    def test_update_modify_replace_failed_create(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                            'Properties': {'Foo': 'abc'}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=True)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                             'Properties': {'Foo': 'xyz'}}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))

        # patch in a dummy handle_create making the replace fail creating
        mock_create = self.patchobject(generic_rsrc.ResourceWithProps,
                                       'handle_create',
                                       side_effect=Exception)

        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.FAILED),
                         self.stack.state)
        mock_create.assert_called_once_with()

    def test_update_modify_replace_failed_create_and_delete_1(self):
        resource._register_class('ResourceWithResourceIDType',
                                 generic_rsrc.ResourceWithResourceID)
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type':
                                            'ResourceWithResourceIDType',
                                            'Properties': {'ID': 'a_res'}},
                              'BResource': {'Type':
                                            'ResourceWithResourceIDType',
                                            'Properties': {'ID': 'b_res'},
                                            'DependsOn': 'AResource'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=True)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {'AResource': {'Type':
                                             'ResourceWithResourceIDType',
                                             'Properties': {'ID': 'xyz'}},
                               'BResource': {'Type':
                                             'ResourceWithResourceIDType',
                                             'Properties': {'ID': 'b_res'},
                                             'DependsOn': 'AResource'}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))

        # patch in a dummy handle_create making the replace fail creating
        mock_create = self.patchobject(generic_rsrc.ResourceWithResourceID,
                                       'handle_create', side_effect=Exception)
        mock_id = self.patchobject(generic_rsrc.ResourceWithResourceID,
                                   'mox_resource_id',
                                   return_value=None)

        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.FAILED),
                         self.stack.state)
        self.stack.delete()
        self.assertEqual((stack.Stack.DELETE, stack.Stack.COMPLETE),
                         self.stack.state)

        mock_create.assert_called_once_with()

        # Three calls in list: first is an attempt to delete backup_stack
        # where create(xyz) has failed, so no resource_id passed; the 2nd
        # and the 3rd calls are invoked by resource BResource deletion
        # followed by AResource deletion.
        mock_id.assert_has_calls(
            [mock.call(None), mock.call('b_res'), mock.call('a_res')])

    def test_update_modify_replace_failed_create_and_delete_2(self):
        resource._register_class('ResourceWithResourceIDType',
                                 generic_rsrc.ResourceWithResourceID)
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type':
                                            'ResourceWithResourceIDType',
                                            'Properties': {'ID': 'a_res'}},
                              'BResource': {'Type':
                                            'ResourceWithResourceIDType',
                                            'Properties': {'ID': 'b_res'},
                                            'DependsOn': 'AResource'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=True)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {'AResource': {'Type':
                                             'ResourceWithResourceIDType',
                                             'Properties': {'ID': 'c_res'}},
                               'BResource': {'Type':
                                             'ResourceWithResourceIDType',
                                             'Properties': {'ID': 'xyz'},
                                             'DependsOn': 'AResource'}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))

        # patch in a dummy handle_create making the replace fail creating
        mock_create = self.patchobject(generic_rsrc.ResourceWithResourceID,
                                       'handle_create',
                                       side_effect=[None, Exception])
        mock_id = self.patchobject(generic_rsrc.ResourceWithResourceID,
                                   'mox_resource_id', return_value=None)

        self.stack.update(updated_stack)
        # set resource_id for AResource because handle_create() is overwritten
        # by the mock.
        self.stack.resources['AResource'].resource_id_set('c_res')
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.FAILED),
                         self.stack.state)
        self.stack.delete()
        self.assertEqual((stack.Stack.DELETE, stack.Stack.COMPLETE),
                         self.stack.state)

        self.assertEqual(2, mock_create.call_count)
        # Four calls in chain: 1st is an attempt to delete backup_stack where
        # the create(xyz) failed with no resource_id, the other three are
        # derived from resource dependencies.
        mock_id.assert_has_calls(
            [mock.call(None), mock.call('c_res'), mock.call('b_res'),
             mock.call('a_res')])

    def test_update_modify_replace_create_in_progress_and_delete_1(self):
        resource._register_class('ResourceWithResourceIDType',
                                 generic_rsrc.ResourceWithResourceID)
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type':
                                            'ResourceWithResourceIDType',
                                            'Properties': {'ID': 'a_res'}},
                              'BResource': {'Type':
                                            'ResourceWithResourceIDType',
                                            'Properties': {'ID': 'b_res'},
                                            'DependsOn': 'AResource'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=True)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {'AResource': {'Type':
                                             'ResourceWithResourceIDType',
                                             'Properties': {'ID': 'xyz'}},
                               'BResource': {'Type':
                                             'ResourceWithResourceIDType',
                                             'Properties': {'ID': 'b_res'},
                                             'DependsOn': 'AResource'}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))

        # patch in a dummy handle_create making the replace fail creating
        mock_create = self.patchobject(generic_rsrc.ResourceWithResourceID,
                                       'handle_create', side_effect=Exception)
        mock_id = self.patchobject(generic_rsrc.ResourceWithResourceID,
                                   'mox_resource_id', return_value=None)

        self.stack.update(updated_stack)
        # Override stack status and resources status for emulating
        # IN_PROGRESS situation
        self.stack.state_set(
            stack.Stack.UPDATE, stack.Stack.IN_PROGRESS, None)
        self.stack.resources['AResource'].state_set(
            resource.Resource.CREATE, resource.Resource.IN_PROGRESS, None)
        self.stack.delete()
        self.assertEqual((stack.Stack.DELETE, stack.Stack.COMPLETE),
                         self.stack.state)

        mock_create.assert_called_once_with()
        # Three calls in chain: 1st is an attempt to delete backup_stack where
        # the create(xyz) failed with no resource_id, the other two ordered by
        # resource dependencies.
        mock_id.assert_has_calls(
            [mock.call(None), mock.call('b_res'), mock.call('a_res')])

    def test_update_modify_replace_create_in_progress_and_delete_2(self):
        resource._register_class('ResourceWithResourceIDType',
                                 generic_rsrc.ResourceWithResourceID)
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type':
                                            'ResourceWithResourceIDType',
                                            'Properties': {'ID': 'a_res'}},
                              'BResource': {'Type':
                                            'ResourceWithResourceIDType',
                                            'Properties': {'ID': 'b_res'},
                                            'DependsOn': 'AResource'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=True)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {'AResource': {'Type':
                                             'ResourceWithResourceIDType',
                                             'Properties': {'ID': 'c_res'}},
                               'BResource': {'Type':
                                             'ResourceWithResourceIDType',
                                             'Properties': {'ID': 'xyz'},
                                             'DependsOn': 'AResource'}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))

        # patch in a dummy handle_create making the replace fail creating
        mock_create = self.patchobject(generic_rsrc.ResourceWithResourceID,
                                       'handle_create',
                                       side_effect=[None, Exception])
        mock_id = self.patchobject(generic_rsrc.ResourceWithResourceID,
                                   'mox_resource_id', return_value=None)

        self.stack.update(updated_stack)
        # set resource_id for AResource because handle_create() is mocked
        self.stack.resources['AResource'].resource_id_set('c_res')
        # Override stack status and resources status for emulating
        # IN_PROGRESS situation
        self.stack.state_set(
            stack.Stack.UPDATE, stack.Stack.IN_PROGRESS, None)
        self.stack.resources['BResource'].state_set(
            resource.Resource.CREATE, resource.Resource.IN_PROGRESS, None)
        self.stack.delete()
        self.assertEqual((stack.Stack.DELETE, stack.Stack.COMPLETE),
                         self.stack.state)

        self.assertEqual(2, mock_create.call_count)
        # Four calls in chain: 1st is an attempt to delete backup_stack where
        # the create(xyz) failed with no resource_id, the other three are
        # derived from resource dependencies.
        mock_id.assert_has_calls(
            [mock.call(None), mock.call('c_res'), mock.call('b_res'),
             mock.call('a_res')])

    def test_update_add_signal(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl))
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {
                     'AResource': {'Type': 'GenericResourceType'},
                     'BResource': {'Type': 'GenericResourceType'}}}
        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))

        updater = scheduler.TaskRunner(self.stack.update_task, updated_stack)
        updater.start()
        while 'BResource' not in self.stack:
            self.assertFalse(updater.step())
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.IN_PROGRESS),
                         self.stack.state)

        # Reload the stack from the DB and prove that it contains the new
        # resource already
        re_stack = stack.Stack.load(utils.dummy_context(), self.stack.id)
        self.assertIn('BResource', re_stack)

        updater.run_to_completion()
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertIn('BResource', self.stack)

    def test_update_add_failed_create(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl))
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {
                     'AResource': {'Type': 'GenericResourceType'},
                     'BResource': {'Type': 'GenericResourceType'}}}
        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))

        # patch in a dummy handle_create making BResource fail creating
        mock_create = self.patchobject(generic_rsrc.GenericResource,
                                       'handle_create', side_effect=Exception)

        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.FAILED),
                         self.stack.state)
        self.assertIn('BResource', self.stack)

        # Reload the stack from the DB and prove that it contains the failed
        # resource (to ensure it will be deleted on stack delete)
        re_stack = stack.Stack.load(utils.dummy_context(), self.stack.id)
        self.assertIn('BResource', re_stack)
        mock_create.assert_called_once_with()

    def test_update_add_failed_create_rollback_failed(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl))
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {
                     'AResource': {'Type': 'GenericResourceType'},
                     'BResource': {'Type': 'GenericResourceType'}}}
        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2),
                                    disable_rollback=False)

        # patch handle_create/delete making BResource fail creation/deletion
        mock_create = self.patchobject(generic_rsrc.GenericResource,
                                       'handle_create', side_effect=Exception)
        mock_delete = self.patchobject(generic_rsrc.GenericResource,
                                       'handle_delete', side_effect=Exception)

        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.ROLLBACK, stack.Stack.FAILED),
                         self.stack.state)
        self.assertIn('BResource', self.stack)

        # Reload the stack from the DB and prove that it contains the failed
        # resource (to ensure it will be deleted on stack delete)
        re_stack = stack.Stack.load(utils.dummy_context(), self.stack.id)
        self.assertIn('BResource', re_stack)

        mock_create.assert_called_once_with()
        mock_delete.assert_called_once_with()

    def test_update_rollback(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                            'Properties': {'Foo': 'abc'}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=False)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                             'Properties': {'Foo': 'xyz'}}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2),
                                    disable_rollback=False)

        # patch in a dummy handle_create making the replace fail when creating
        # the replacement rsrc
        mock_create = self.patchobject(generic_rsrc.ResourceWithProps,
                                       'handle_create', side_effect=Exception)

        with mock.patch.object(self.stack, 'state_set',
                               side_effect=self.stack.state_set) as mock_state:
            self.stack.update(updated_stack)
            self.assertEqual((stack.Stack.ROLLBACK, stack.Stack.COMPLETE),
                             self.stack.state)
            self.assertEqual('abc', self.stack['AResource'].properties['Foo'])
            self.assertEqual(2, mock_state.call_count)
            self.assertEqual(('UPDATE', 'IN_PROGRESS'),
                             mock_state.call_args_list[0][0][:2])
            self.assertEqual(('ROLLBACK', 'IN_PROGRESS'),
                             mock_state.call_args_list[1][0][:2])

        mock_create.assert_called_once_with()

    def test_update_rollback_on_cancel_event(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                            'Properties': {'Foo': 'abc'}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=False)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                             'Properties': {'Foo': 'xyz'}},
                               }}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2),
                                    disable_rollback=False)
        evt_mock = mock.MagicMock()
        evt_mock.ready.return_value = True
        evt_mock.wait.return_value = 'cancel'

        self.stack.update(updated_stack, event=evt_mock)
        self.assertEqual((stack.Stack.ROLLBACK, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('abc', self.stack['AResource'].properties['Foo'])
        evt_mock.ready.assert_called_once_with()
        evt_mock.wait.assert_called_once_with()

    def test_update_rollback_fail(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Parameters': {'AParam': {'Type': 'String'}},
                'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                            'Properties': {'Foo': 'abc'}}}}

        env1 = environment.Environment({'parameters': {'AParam': 'abc'}})
        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl, env=env1),
                                 disable_rollback=False)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Parameters': {'BParam': {'Type': 'String'}},
                 'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                             'Properties': {'Foo': 'xyz'}}}}

        env2 = environment.Environment({'parameters': {'BParam': 'smelly'}})
        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2, env=env2),
                                    disable_rollback=False)

        # patch in a dummy handle_create making the replace fail when creating
        # the replacement rsrc, and again on the second call (rollback)
        mock_create = self.patchobject(generic_rsrc.ResourceWithProps,
                                       'handle_create', side_effect=Exception)
        mock_delete = self.patchobject(generic_rsrc.ResourceWithProps,
                                       'handle_delete', side_effect=Exception)

        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.ROLLBACK, stack.Stack.FAILED),
                         self.stack.state)

        mock_create.assert_called_once_with()
        mock_delete.assert_called_once_with()

    def test_update_rollback_add(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=False)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {
                     'AResource': {'Type': 'GenericResourceType'},
                     'BResource': {'Type': 'GenericResourceType'}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2),
                                    disable_rollback=False)

        # patch in a dummy handle_create making the replace fail when creating
        # the replacement rsrc, and succeed on the second call (rollback)
        mock_create = self.patchobject(generic_rsrc.GenericResource,
                                       'handle_create', side_effect=Exception)
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.ROLLBACK, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertNotIn('BResource', self.stack)

        mock_create.assert_called_once_with()

    def test_update_rollback_remove(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {
                    'AResource': {'Type': 'GenericResourceType'},
                    'BResource': {'Type': 'ResourceWithPropsType'}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=False)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {'AResource': {'Type': 'GenericResourceType'}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2),
                                    disable_rollback=False)

        # patch in a dummy delete making the destroy fail
        mock_create = self.patchobject(generic_rsrc.ResourceWithProps,
                                       'handle_create')
        mock_delete = self.patchobject(generic_rsrc.ResourceWithProps,
                                       'handle_delete',
                                       side_effect=[Exception, None])

        self.stack.update(updated_stack)

        self.assertEqual((stack.Stack.ROLLBACK, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertIn('BResource', self.stack)

        mock_create.assert_called_once_with()
        self.assertEqual(2, mock_delete.call_count)

        # Unset here so delete() is not stubbed for stack.delete cleanup
        self.m.UnsetStubs()

    def test_update_rollback_replace(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {
                    'AResource': {'Type': 'ResourceWithPropsType',
                                  'Properties': {'Foo': 'foo'}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=False)
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)

        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {'AResource': {'Type': 'ResourceWithPropsType',
                                             'Properties': {'Foo': 'bar'}}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2),
                                    disable_rollback=False)

        # patch in a dummy delete making the destroy fail
        mock_delete = self.patchobject(generic_rsrc.ResourceWithProps,
                                       'handle_delete',
                                       side_effect=[Exception, None, None])

        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.ROLLBACK, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual(3, mock_delete.call_count)

        # Unset here so delete() is not stubbed for stack.delete cleanup
        self.m.UnsetStubs()

    def test_update_replace_by_reference(self):
        '''
        assertion:
        changes in dynamic attributes, due to other resources been updated
        are not ignored and can cause dependent resources to be updated.
        '''
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {
                    'AResource': {'Type': 'ResourceWithPropsType',
                                  'Properties': {'Foo': 'abc'}},
                    'BResource': {'Type': 'ResourceWithPropsType',
                                  'Properties': {
                                      'Foo': {'Ref': 'AResource'}}}}}
        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {
                     'AResource': {'Type': 'ResourceWithPropsType',
                                   'Properties': {'Foo': 'smelly'}},
                     'BResource': {'Type': 'ResourceWithPropsType',
                                   'Properties': {
                                       'Foo': {'Ref': 'AResource'}}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl))

        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('abc', self.stack['AResource'].properties['Foo'])
        self.assertEqual('AResource',
                         self.stack['BResource'].properties['Foo'])

        self.ref_id_called = False

        def get_ref_id(*args):
            ref_id = 'inst-007' if self.ref_id_called else 'AResource'
            if self.ref_id_called is False:
                self.ref_id_called = True
            return ref_id

        mock_id = self.patchobject(generic_rsrc.ResourceWithProps,
                                   'FnGetRefId',
                                   side_effect=get_ref_id)

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('smelly', self.stack['AResource'].properties['Foo'])
        self.assertEqual('inst-007', self.stack['BResource'].properties['Foo'])

        # Note: mock_id is called 14 times!!!
        mock_id.assert_called_with()

    def test_update_with_new_resources_with_reference(self):
        '''
        assertion:
        check, that during update with new resources which one has
        reference on second, reference will be correct resolved.
        '''
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {
                    'CResource': {'Type': 'ResourceWithPropsType',
                                  'Properties': {'Foo': 'abc'}}}}
        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {
                     'CResource': {'Type': 'ResourceWithPropsType',
                                   'Properties': {'Foo': 'abc'}},
                     'AResource': {'Type': 'ResourceWithPropsType',
                                   'Properties': {'Foo': 'smelly'}},
                     'BResource': {'Type': 'ResourceWithPropsType',
                                   'Properties': {
                                       'Foo': {'Ref': 'AResource'}}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl))

        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('abc', self.stack['CResource'].properties['Foo'])
        self.assertEqual(1, len(self.stack.resources))

        mock_create = self.patchobject(generic_rsrc.ResourceWithProps,
                                       'handle_create', return_value=None)

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('smelly', self.stack['AResource'].properties['Foo'])
        self.assertEqual('AResource',
                         self.stack['BResource'].properties['Foo'])

        self.assertEqual(3, len(self.stack.resources))

        mock_create.assert_called_with()

    def test_update_by_reference_and_rollback_1(self):
        '''
        assertion:
        check that rollback still works with dynamic metadata
        this test fails the first instance
        '''
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {
                    'AResource': {'Type': 'ResourceWithPropsType',
                                  'Properties': {'Foo': 'abc'}},
                    'BResource': {'Type': 'ResourceWithPropsType',
                                  'Properties': {
                                      'Foo': {'Ref': 'AResource'}}}}}
        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {
                     'AResource': {'Type': 'ResourceWithPropsType',
                                   'Properties': {'Foo': 'smelly'}},
                     'BResource': {'Type': 'ResourceWithPropsType',
                                   'Properties': {
                                       'Foo': {'Ref': 'AResource'}}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=False)

        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('abc', self.stack['AResource'].properties['Foo'])
        self.assertEqual('AResource',
                         self.stack['BResource'].properties['Foo'])

        mock_id = self.patchobject(generic_rsrc.ResourceWithProps,
                                   'FnGetRefId', return_value='AResource')

        # mock to make the replace fail when creating the replacement resource
        mock_create = self.patchobject(generic_rsrc.ResourceWithProps,
                                       'handle_create', side_effect=Exception)

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2),
                                    disable_rollback=False)
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.ROLLBACK, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('abc', self.stack['AResource'].properties['Foo'])

        mock_id.assert_called_with()
        mock_create.assert_called_once_with()

    def test_update_by_reference_and_rollback_2(self):
        '''
        assertion:
        check that rollback still works with dynamic metadata
        this test fails the second instance
        '''

        class ResourceTypeA(generic_rsrc.ResourceWithProps):
            count = 0

            def handle_create(self):
                ResourceTypeA.count += 1
                self.resource_id_set('%s%d' % (self.name, self.count))

        resource._register_class('ResourceTypeA', ResourceTypeA)

        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {
                    'AResource': {'Type': 'ResourceTypeA',
                                  'Properties': {'Foo': 'abc'}},
                    'BResource': {'Type': 'ResourceWithPropsType',
                                  'Properties': {
                                      'Foo': {'Ref': 'AResource'}}}}}
        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {
                     'AResource': {'Type': 'ResourceTypeA',
                                   'Properties': {'Foo': 'smelly'}},
                     'BResource': {'Type': 'ResourceWithPropsType',
                                   'Properties': {
                                       'Foo': {'Ref': 'AResource'}}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=False)

        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('abc', self.stack['AResource'].properties['Foo'])
        self.assertEqual('AResource1',
                         self.stack['BResource'].properties['Foo'])

        # mock to make the replace fail when creating the second
        # replacement resource
        mock_create = self.patchobject(generic_rsrc.ResourceWithProps,
                                       'handle_create', side_effect=Exception)

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2),
                                    disable_rollback=False)
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.ROLLBACK, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('abc', self.stack['AResource'].properties['Foo'])
        self.assertEqual('AResource1',
                         self.stack['BResource'].properties['Foo'])
        mock_create.assert_called_once_with()

    def test_update_failure_recovery(self):
        '''
        assertion:
        check that rollback still works with dynamic metadata
        this test fails the second instance
        '''

        class ResourceTypeA(generic_rsrc.ResourceWithProps):
            count = 0

            def handle_create(self):
                ResourceTypeA.count += 1
                self.resource_id_set('%s%d' % (self.name, self.count))

            def handle_delete(self):
                return super(ResourceTypeA, self).handle_delete()

        resource._register_class('ResourceTypeA', ResourceTypeA)

        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {
                    'AResource': {'Type': 'ResourceTypeA',
                                  'Properties': {'Foo': 'abc'}},
                    'BResource': {'Type': 'ResourceWithPropsType',
                                  'Properties': {
                                      'Foo': {'Ref': 'AResource'}}}}}
        tmpl2 = {'HeatTemplateFormatVersion': '2012-12-12',
                 'Resources': {
                     'AResource': {'Type': 'ResourceTypeA',
                                   'Properties': {'Foo': 'smelly'}},
                     'BResource': {'Type': 'ResourceWithPropsType',
                                   'Properties': {
                                       'Foo': {'Ref': 'AResource'}}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl),
                                 disable_rollback=True)

        self.stack.store()
        self.stack.create()

        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('abc', self.stack['AResource'].properties['Foo'])
        self.assertEqual('AResource1',
                         self.stack['BResource'].properties['Foo'])

        # mock to make the replace fail when creating the second
        # replacement resource
        mock_create = self.patchobject(generic_rsrc.ResourceWithProps,
                                       'handle_create',
                                       side_effect=[Exception, None])
        mock_delete = self.patchobject(generic_rsrc.ResourceWithProps,
                                       'handle_delete')
        mock_delete_A = self.patchobject(ResourceTypeA, 'handle_delete')

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2),
                                    disable_rollback=True)
        self.stack.update(updated_stack)

        mock_create.assert_called_once_with()

        self.assertEqual((stack.Stack.UPDATE, stack.Stack.FAILED),
                         self.stack.state)
        self.assertEqual('smelly', self.stack['AResource'].properties['Foo'])

        self.stack = stack.Stack.load(self.ctx, self.stack.id)
        updated_stack2 = stack.Stack(self.ctx, 'updated_stack',
                                     template.Template(tmpl2),
                                     disable_rollback=True)

        self.stack.update(updated_stack2)

        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('smelly', self.stack['AResource'].properties['Foo'])
        self.assertEqual('AResource2',
                         self.stack['BResource'].properties['Foo'])

        self.assertEqual(2, mock_create.call_count)
        self.assertEqual(2, mock_delete.call_count)
        mock_delete_A.assert_called_once_with()

    def test_update_failure_recovery_new_param(self):
        '''
        assertion:
        check that rollback still works with dynamic metadata
        this test fails the second instance
        '''

        class ResourceTypeA(generic_rsrc.ResourceWithProps):
            count = 0

            def handle_create(self):
                ResourceTypeA.count += 1
                self.resource_id_set('%s%d' % (self.name, self.count))

            def handle_delete(self):
                return super(ResourceTypeA, self).handle_delete()

        resource._register_class('ResourceTypeA', ResourceTypeA)

        tmpl = {
            'HeatTemplateFormatVersion': '2012-12-12',
            'Parameters': {
                'abc-param': {'Type': 'String'}
            },
            'Resources': {
                'AResource': {'Type': 'ResourceTypeA',
                              'Properties': {'Foo': {'Ref': 'abc-param'}}},
                'BResource': {'Type': 'ResourceWithPropsType',
                              'Properties': {'Foo': {'Ref': 'AResource'}}}
            }
        }
        env1 = environment.Environment({'abc-param': 'abc'})
        tmpl2 = {
            'HeatTemplateFormatVersion': '2012-12-12',
            'Parameters': {
                'smelly-param': {'Type': 'String'}
            },
            'Resources': {
                'AResource': {'Type': 'ResourceTypeA',
                              'Properties': {'Foo': {'Ref': 'smelly-param'}}},
                'BResource': {'Type': 'ResourceWithPropsType',
                              'Properties': {'Foo': {'Ref': 'AResource'}}}
            }
        }
        env2 = environment.Environment({'smelly-param': 'smelly'})

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl, env=env1),
                                 disable_rollback=True)

        self.stack.store()
        self.stack.create()

        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('abc', self.stack['AResource'].properties['Foo'])
        self.assertEqual('AResource1',
                         self.stack['BResource'].properties['Foo'])

        mock_create = self.patchobject(generic_rsrc.ResourceWithProps,
                                       'handle_create',
                                       side_effect=[Exception, None])
        mock_delete = self.patchobject(generic_rsrc.ResourceWithProps,
                                       'handle_delete')
        mock_delete_A = self.patchobject(ResourceTypeA, 'handle_delete')

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2, env=env2),
                                    disable_rollback=True)
        self.stack.update(updated_stack)

        # creation was a failure
        mock_create.assert_called_once_with()
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.FAILED),
                         self.stack.state)
        self.assertEqual('smelly', self.stack['AResource'].properties['Foo'])

        self.stack = stack.Stack.load(self.ctx, self.stack.id)
        updated_stack2 = stack.Stack(self.ctx, 'updated_stack',
                                     template.Template(tmpl2, env=env2),
                                     disable_rollback=True)

        self.stack.update(updated_stack2)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)

        self.stack = stack.Stack.load(self.ctx, self.stack.id)
        self.assertEqual('smelly', self.stack['AResource'].properties['Foo'])
        self.assertEqual('AResource2',
                         self.stack['BResource'].properties['Foo'])

        self.assertEqual(2, mock_delete.call_count)
        mock_delete_A.assert_called_once_with()
        self.assertEqual(2, mock_create.call_count)

    def test_update_replace_parameters(self):
        '''
        assertion:
        changes in static environment parameters
        are not ignored and can cause dependent resources to be updated.
        '''
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Parameters': {'AParam': {'Type': 'String'}},
                'Resources': {
                    'AResource': {'Type': 'ResourceWithPropsType',
                                  'Properties': {'Foo': {'Ref': 'AParam'}}}}}

        env1 = environment.Environment({'parameters': {'AParam': 'abc'}})
        env2 = environment.Environment({'parameters': {'AParam': 'smelly'}})
        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl, env=env1))

        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('abc', self.stack['AResource'].properties['Foo'])

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl, env=env2))
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('smelly', self.stack['AResource'].properties['Foo'])

    def test_update_deletion_policy(self):
        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {
                    'AResource': {'Type': 'ResourceWithPropsType',
                                  'Properties': {'Foo': 'Bar'}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl))

        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)
        resource_id = self.stack['AResource'].id

        new_tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                    'Resources': {
                        'AResource': {'Type': 'ResourceWithPropsType',
                                      'DeletionPolicy': 'Retain',
                                      'Properties': {'Foo': 'Bar'}}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(new_tmpl))
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)

        self.assertEqual(resource_id, self.stack['AResource'].id)

    def test_update_deletion_policy_no_handle_update(self):

        class ResourceWithNoUpdate(resource.Resource):
            properties_schema = {'Foo': {'Type': 'String'}}

        resource._register_class('ResourceWithNoUpdate',
                                 ResourceWithNoUpdate)

        tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                'Resources': {
                    'AResource': {'Type': 'ResourceWithNoUpdate',
                                  'Properties': {'Foo': 'Bar'}}}}

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl))

        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)
        resource_id = self.stack['AResource'].id

        new_tmpl = {'HeatTemplateFormatVersion': '2012-12-12',
                    'Resources': {
                        'AResource': {'Type': 'ResourceWithNoUpdate',
                                      'DeletionPolicy': 'Retain',
                                      'Properties': {'Foo': 'Bar'}}}}

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(new_tmpl))
        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)

        self.assertEqual(resource_id, self.stack['AResource'].id)

    def test_update_template_format_version(self):
        tmpl = {
            'HeatTemplateFormatVersion': '2012-12-12',
            'Parameters': {
                'AParam': {'Type': 'String', 'Default': 'abc'}},
            'Resources': {
                'AResource': {
                    'Type': 'ResourceWithPropsType',
                    'Properties': {'Foo': {'Ref': 'AParam'}}
                },
            }
        }

        self.stack = stack.Stack(self.ctx, 'update_test_stack',
                                 template.Template(tmpl))
        self.stack.store()
        self.stack.create()
        self.assertEqual((stack.Stack.CREATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('abc', self.stack['AResource'].properties['Foo'])

        tmpl2 = {
            'heat_template_version': '2013-05-23',
            'parameters': {
                'AParam': {'type': 'string', 'default': 'foo'}},
            'resources': {
                'AResource': {
                    'type': 'ResourceWithPropsType',
                    'properties': {'Foo': {'get_param': 'AParam'}}
                }
            }
        }

        updated_stack = stack.Stack(self.ctx, 'updated_stack',
                                    template.Template(tmpl2))

        self.stack.update(updated_stack)
        self.assertEqual((stack.Stack.UPDATE, stack.Stack.COMPLETE),
                         self.stack.state)
        self.assertEqual('foo', self.stack['AResource'].properties['Foo'])
