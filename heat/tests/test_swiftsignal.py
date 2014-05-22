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

import uuid

import mock
import six

from heat.common import exception
from heat.common import template_format
from heat.engine import clients
from heat.engine import environment
from heat.engine import parser
from heat.engine.resources import swiftsignal
from heat.tests.common import HeatTestCase
from heat.tests import utils


swiftsignal_template = '''
heat_template_version: 2013-05-23

resources:
  test_wait_condition:
    type: "OS::Heat::SwiftSignal"
    properties:
      handle: { get_resource: test_wait_condition_handle }
      timeout: 1800

  test_wait_condition_handle:
    type: "OS::Heat::SwiftSignalHandle"
    properties:
      timeout: 18000
'''


class SwiftSignalTest(HeatTestCase):
    def setUp(self):
        super(SwiftSignalTest, self).setUp()
        utils.setup_dummy_db()

    def create_stack(self):
        tmpl = template_format.parse(swiftsignal_template)
        template = parser.Template(tmpl)
        ctx = utils.dummy_context(tenant_id='test_tenant')
        stack = parser.Stack(ctx, 'test_stack', template,
                             environment.Environment(),
                             disable_rollback=True)
        stack.id = str(uuid.uuid4())
        return stack

    @mock.patch.object(clients.OpenStackClients, 'swift')
    def test_create(self, mock_swift):
        stack = self.create_stack()

        mock_swift_object = mock.Mock()
        mock_swift.return_value = mock_swift_object
        mock_swift_object.url = "http://fake-host.com:8080/v1/AUTH_1234"
        mock_swift_object.head_account.return_value = {
            'x-account-meta-temp-url-key': '123456'
        }
        mock_swift_object.get_object.return_value = (None, "success")

        stack.create()
        self.assertEqual(('CREATE', 'COMPLETE'), stack.state)

    @mock.patch.object(clients.OpenStackClients, 'swift')
    def test_post_success_to_handle(self, mock_swift):
        stack = self.create_stack()

        mock_swift_object = mock.Mock()
        mock_swift.return_value = mock_swift_object
        mock_swift_object.url = "http://fake-host.com:8080/v1/AUTH_1234"
        mock_swift_object.head_account.return_value = {
            'x-account-meta-temp-url-key': '123456'
        }
        mock_swift_object.get_object.side_effect = [(None, "in progress"),
                                                    (None, "in progress"),
                                                    (None, "success")]

        stack.create()
        self.assertEqual(('CREATE', 'COMPLETE'), stack.state)

    @mock.patch.object(clients.OpenStackClients, 'swift')
    @mock.patch.object(swiftsignal, 'time')
    def test_handle_timeout(self, mock_time, mock_swift):
        stack = self.create_stack()

        mock_swift_object = mock.Mock()
        mock_swift.return_value = mock_swift_object
        mock_swift_object.url = "http://fake-host.com:8080/v1/AUTH_1234"
        mock_swift_object.head_account.return_value = {
            'x-account-meta-temp-url-key': '123456'
        }
        mock_swift_object.get_object.return_value = (None, "in progress")

        mock_time.time.side_effect = [1000, 2801]

        stack.create()
        self.assertIn('SwiftSignal wait condition timed out while waiting '
                      'for completion signal',
                      six.text_type(stack.status_reason))


# TODO(jason): Write more tests
