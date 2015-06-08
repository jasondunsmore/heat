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


from tempest.api.orchestration import base
from tempest.common.utils import data_utils
from tempest import test


class UpdatePreviewTest(base.BaseOrchestrationTest):
    _tpl_type = 'yaml'
    _resource = 'resources'
    _type = 'type'

    @classmethod
    def resource_setup(cls):
        super(UpdatePreviewTest, cls).resource_setup()
        cls.stack_name = data_utils.rand_name('heat')
        template = cls.read_template('update_preview', ext=cls._tpl_type)

        # create the stack, avoid any duplicated key.
        cls.stack_identifier = cls.create_stack(
            cls.stack_name,
            template,
            parameters={
                'KeyPairName1': cls.stack_name + '_1',
                'KeyPairName2': cls.stack_name + '_2',
                'BucketName': cls.stack_name + '_bucket',
            })

        cls.stack_id = cls.stack_identifier.split('/')[1]
        cls.client.wait_for_stack_status(cls.stack_id, 'CREATE_COMPLETE')
        _, resources = cls.client.list_resources(cls.stack_identifier)
        cls.test_resources = {}
        for resource in resources:
            cls.test_resources[resource['logical_resource_id']] = resource

    @test.attr(type='gate')
    def test_created_resources(self):
        """Verifies created keypair resource."""

        test_template = self.load_template('update_preview',
                                           ext=self._tpl_type)
        resources = [('KeyPairSavePrivate',
                      test_template[self._resource][
                          'KeyPairSavePrivate'][self._type]),
                     ('KeyPairDontSavePrivate',
                      test_template[self._resource][
                          'KeyPairDontSavePrivate'][self._type]),
                     ('SwiftContainerWebsite',
                      test_template[self._resource][
                          'SwiftContainerWebsite'][self._type]),
                     ]

        for resource_name, resource_type in resources:
            resource = self.test_resources.get(resource_name, None)
            self.assertIsInstance(resource, dict)
            self.assertEqual(resource_name, resource['logical_resource_id'])
            self.assertEqual(resource_type, resource['resource_type'])
            self.assertEqual('CREATE_COMPLETE', resource['resource_status'])

    @test.attr(type='gate')
    def test_preview_no_changes(self):
        template = self.read_template('update_preview', ext=self._tpl_type)

        resp, update_actions = self.client.preview_update_stack(
            self.stack_identifier,
            self.stack_name,
            template=template,
            parameters={
                'KeyPairName1': self.stack_name + '_1',
                'KeyPairName2': self.stack_name + '_2',
                'BucketName': self.stack_name + '_bucket',
            })

        self.assertIsInstance(update_actions, dict)
        self.assertIsInstance(update_actions.get('resource_changes'), dict)

        changes = update_actions['resource_changes']

        self.assertEqual(4, len(changes['unchanged']))
        changes.pop('unchanged')
        for k in changes.keys():
            self.assertFalse(changes[k])

    def test_preview_update_replace(self):
        template = self.read_template('update_preview', ext=self._tpl_type)

        resp, update_actions = self.client.preview_update_stack(
            self.stack_identifier,
            self.stack_name,
            template=template,
            parameters={
                # change keypair1 name
                'KeyPairName1': self.stack_name + '_3',
                'KeyPairName2': self.stack_name + '_2',
                # change bucket name
                'BucketName': self.stack_name + '_bucket1',
            })

        self.assertIsInstance(update_actions, dict)
        self.assertIsInstance(update_actions.get('resource_changes'), dict)

        changes = update_actions['resource_changes']

        self.assertEqual(2, len(changes['unchanged']))
        changes.pop('unchanged')

        self.assertEqual(2, len(changes['replaced']))
        changes.pop('replaced')

        for k in changes.keys():
            self.assertFalse(changes[k])
