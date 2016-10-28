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

import mock
import six
import uuid

from heat.common import template_format
from heat.engine.clients import client_plugin
from heat.engine import resource
from heat.engine import rsrc_defn
from heat.engine import scheduler
from heat.engine import stack
from heat.engine import template
from heat.tests import common
from heat.tests import utils

wp_template = '''
{
  "AWSTemplateFormatVersion" : "2010-09-09",
  "Description" : "openstack Zaqar queue service as a resource",
  "Resources" : {
    "MyQueue2" : {
      "Type" : "OS::Zaqar::Queue",
      "Properties" : {
        "name" : "myqueue",
        "metadata" : { "key1" : { "key2" : "value", "key3" : [1, 2] } }
      }
    },
    "MySubscription" : {
      "Type" : "OS::Zaqar::Subscription",
      "Properties" : {
        "name" : "myqueue",
        "subscriber" : "mailto:name@domain.com",
        "ttl" : "3600",
        "options" : { "key1" : "value1" }
      }
    }
  },
  "Outputs" : {
    "queue_id": {
      "Value": { "Ref" : "MyQueue2" },
      "Description": "queue name"
    },
    "queue_href": {
      "Value": { "Fn::GetAtt" : [ "MyQueue2", "href" ]},
      "Description": "queue href"
    }
  }
}
'''


class FakeSubscription(object):
    def __init__(self, name, id, auto_create=True):
        self.id = id
        self._auto_create = auto_create
        self._exists = False

    def delete(self):
        pass


@mock.patch.object(resource.Resource, "client_plugin")
@mock.patch.object(resource.Resource, "client")
class ZaqarSubscriptionTest(common.HeatTestCase):
    def setUp(self):
        super(ZaqarSubscriptionTest, self).setUp()
        self.fc = self.m.CreateMockAnything()
        self.ctx = utils.dummy_context()

    def parse_stack(self, t):
        stack_name = 'test_stack'
        tmpl = template.Template(t)
        self.stack = stack.Stack(self.ctx, stack_name, tmpl)
        self.stack.validate()
        self.stack.store()

    def test_create(self, mock_client, mock_plugin):
        t = template_format.parse(wp_template)
        self.parse_stack(t)

        subscription = self.stack['MySubscription']
        id = "58138648c1e2eb7355d62137"

        self.m.StubOutWithMock(subscription, 'client')
        subscription.client().MultipleTimes().AndReturn(self.fc)

        fake_subscription = FakeSubscription(subscription.properties['name'],
            id, auto_create=False)
        self.m.StubOutWithMock(self.fc, 'subscription')
        self.fc.subscription(subscription.properties['name'],
                             options={'key1': 'value1'},
                             subscriber=u'mailto:name@domain.com', ttl=3600,
                             auto_create=False).AndReturn(fake_subscription)

        self.m.ReplayAll()

        scheduler.TaskRunner(subscription.create)()
        self.assertEqual(id, subscription.FnGetAtt('subscription_id'))

    def test_delete(self):
        pass

    def test_update_in_place(self):
        pass

    def test_update_replace(self):
        pass

    def test_show_resource(self):
        pass

    def test_parse_live_resource_data(self):
        pass
