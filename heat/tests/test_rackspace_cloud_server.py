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

import mox
import pyrax

from heat.tests.v1_1 import fakes
from heat.common import template_format
from heat.engine import parser
from heat.engine import resource
from heat.engine import scheduler
from heat.openstack.common import uuidutils
from heat.tests.common import HeatTestCase
from heat.tests import utils
from heat.tests.utils import setup_dummy_db
from heat.engine.resources.rackspace import cloud_server


wp_template = '''
{
  "AWSTemplateFormatVersion" : "2010-09-09",
  "Description" : "WordPress",
  "Parameters" : {
    "Flavor" : {
      "Description" : "Rackspace Cloud Server flavor",
      "Type" : "String",
      "Default" : "2",
      "AllowedValues" : [ "2", "3", "4", "5", "6", "7", "8" ],
      "ConstraintDescription" : "must be a valid Rackspace Cloud Server flavor."
    },
  },
  "Resources" : {
    "WebServer": {
      "Type": "Rackspace::Cloud::Server",
      "Properties": {
        "ImageName"      : "F17",
        "InstanceName"   : "Heat test",
        "Flavor"         : "2",
        "UserData"       : "wordpress"
      }
    }
  }
}
'''


class RackspaceCloudServerTest(HeatTestCase):
    def setUp(self):
        super(RackspaceCloudServerTest, self).setUp()
        self.fc = fakes.FakeClient()
        setup_dummy_db()

    def _setup_test_instance(self, return_server, name):
        stack_name = '%s_stack' % name
        t = template_format.parse(wp_template)
        template = parser.Template(t)
        params = parser.Parameters(stack_name, template, {'Flavor': '2'})
        stack = parser.Stack(None, stack_name, template, params,
                             stack_id=uuidutils.generate_uuid())

        t['Resources']['WebServer']['Properties']['ImageName'] = 'F17'
        t['Resources']['WebServer']['Properties']['InstanceName'] = 'Heat test'
        t['Resources']['WebServer']['Properties']['Flavor'] = '2'

        instance = cloud_server.CloudServer('%s_name' % name,
                                            t['Resources']['WebServer'], stack)

        self.m.StubOutWithMock(pyrax, 'set_credential_file')
        pyrax.set_credential_file(mox.IgnoreArg()).AndReturn(True)
        self.m.StubOutWithMock(pyrax, 'connect_to_cloudservers')
        pyrax.connect_to_cloudservers().AndReturn(self.fc)

        instance.t = instance.stack.resolve_runtime_data(instance.t)

        instance_name = t['Resources']['WebServer']['Properties']['InstanceName']
        image_name = t['Resources']['WebServer']['Properties']['ImageName']
        image_id = instance.rackspace_images[image_name]
        flavor = t['Resources']['WebServer']['Properties']['Flavor']

        self.m.StubOutWithMock(self.fc.servers, 'create')
        self.fc.servers.create(instance_name, image_id, flavor,
                               files=mox.IgnoreArg()).AndReturn(return_server)
        return instance

    def _create_test_instance(self, return_server, name):
        instance = self._setup_test_instance(return_server, name)
        self.m.ReplayAll()
        scheduler.TaskRunner(instance.create)()
        return instance

    def test_instance_create(self):
        return_server = self.fc.servers.list()[1]
        instance = self._create_test_instance(return_server,
                                              'test_instance_create')
        # this makes sure the auto increment worked on instance creation
        self.assertTrue(instance.id > 0)

        expected_ip = return_server.networks['public'][0]
        self.assertEqual(instance.FnGetAtt('PublicIp'), expected_ip)
        self.assertEqual(instance.FnGetAtt('PrivateIp'), expected_ip)
        self.assertEqual(instance.FnGetAtt('PrivateDnsName'), expected_ip)
        self.assertEqual(instance.FnGetAtt('PrivateDnsName'), expected_ip)

        self.m.VerifyAll()
