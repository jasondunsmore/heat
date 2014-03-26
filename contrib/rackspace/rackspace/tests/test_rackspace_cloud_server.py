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

import mox

from heat.common import exception
from heat.common import template_format
from heat.engine import clients
from heat.engine import environment
from heat.engine import parser
from heat.engine import resource
from heat.engine import scheduler
from heat.openstack.common import uuidutils
from heat.tests.common import HeatTestCase
from heat.tests import utils
from heat.tests.v1_1 import fakes

from ..resources import cloud_server  # noqa


wp_template = '''
{
  "AWSTemplateFormatVersion" : "2010-09-09",
  "Description" : "WordPress",
  "Parameters" : {
    "key_name" : {
      "Description" : "key_name",
      "Type" : "String",
      "Default" : "test"
    }
  },
  "Resources" : {
    "WebServer": {
      "Type": "Rackspace::Cloud::Server",
      "Properties": {
        "image" : "CentOS 5.2",
        "flavor"   : "256 MB Server",
        "key_name"   : "test",
        "user_data"       : "wordpress"
      }
    }
  }
}
'''


class CloudServersTest(HeatTestCase):
    def setUp(self):
        super(CloudServersTest, self).setUp()
        self.fc = fakes.FakeClient()
        utils.setup_dummy_db()
        # Test environment may not have pyrax client library installed and if
        # pyrax is not installed resource class would not be registered.
        # So register resource provider class explicitly for unit testing.
        resource._register_class("Rackspace::Cloud::Server",
                                 cloud_server.CloudServer)

    def _setup_test_stack(self, stack_name):
        t = template_format.parse(wp_template)
        template = parser.Template(t)
        stack = parser.Stack(utils.dummy_context(), stack_name, template,
                             environment.Environment({'key_name': 'test'}),
                             stack_id=uuidutils.generate_uuid())
        return (t, stack)

    def _setup_test_server(self, return_server, name, image_id=None,
                           override_name=False, stub_create=True, exit_code=0):
        stack_name = '%s_s' % name
        (t, stack) = self._setup_test_stack(stack_name)

        t['Resources']['WebServer']['Properties']['image'] = \
            image_id or 'CentOS 5.2'
        t['Resources']['WebServer']['Properties']['flavor'] = \
            '256 MB Server'

        server_name = '%s' % name
        if override_name:
            t['Resources']['WebServer']['Properties']['name'] = \
                server_name

        server = cloud_server.CloudServer(server_name,
                                          t['Resources']['WebServer'], stack)

        self.m.StubOutWithMock(cloud_server.CloudServer, "nova")
        cloud_server.CloudServer.nova().MultipleTimes().AndReturn(self.fc)
        self.m.StubOutWithMock(clients.OpenStackClients, 'nova')
        clients.OpenStackClients.nova().MultipleTimes().AndReturn(self.fc)

        return_server.adminPass = "foobar"
        server.t = server.stack.resolve_runtime_data(server.t)

        if stub_create:
            self.m.StubOutWithMock(self.fc.servers, 'create')
            self.fc.servers.create(
                image=1,
                flavor=1,
                key_name='test',
                name=override_name and server.name or utils.PhysName(
                    stack_name, server.name),
                security_groups=[],
                userdata=mox.IgnoreArg(),
                scheduler_hints=None,
                meta=None,
                nics=None,
                availability_zone=None,
                block_device_mapping=None,
                config_drive=True,
                disk_config=None,
                reservation_id=None,
                files=mox.IgnoreArg(),
                admin_pass=None).AndReturn(return_server)

        return server

    def _create_test_server(self, return_server, name, override_name=False,
                            stub_create=True, exit_code=0):
        server = self._setup_test_server(return_server, name,
                                         stub_create=stub_create,
                                         exit_code=exit_code)
        self.m.ReplayAll()
        scheduler.TaskRunner(server.create)()
        return server

    def _update_test_server(self, return_server, name, exit_code=0):
        self.m.StubOutWithMock(cloud_server.CloudServer, "nova")
        cloud_server.CloudServer.nova().MultipleTimes().AndReturn(self.fc)

    def _mock_metadata_os_distro(self):
        image_data = self.m.CreateMockAnything()
        image_data.metadata = {'os_distro': 'centos'}
        self.m.StubOutWithMock(self.fc.images, 'get')
        self.fc.images.get(mox.IgnoreArg()).MultipleTimes().\
            AndReturn(image_data)

    def test_rackconnect_deployed(self):
        return_server = self.fc.servers.list()[1]
        return_server.metadata = {'rackconnect_automation_status': 'DEPLOYED'}
        self.m.StubOutWithMock(return_server, 'get')
        return_server.get()
        server = self._setup_test_server(return_server,
                                         'test_rackconnect_deployed')
        server.context.roles = ['rack_connect']
        self.m.ReplayAll()
        scheduler.TaskRunner(server.create)()
        self.assertEqual('CREATE', server.action)
        self.assertEqual('COMPLETE', server.status)
        self.m.VerifyAll()

    def test_rackconnect_failed(self):
        return_server = self.fc.servers.list()[1]
        return_server.metadata = {'rackconnect_automation_status': 'FAILED'}
        self.m.StubOutWithMock(return_server, 'get')
        return_server.get()
        server = self._setup_test_server(return_server,
                                         'test_rackconnect_failed')
        server.context.roles = ['rack_connect']
        self.m.ReplayAll()
        create = scheduler.TaskRunner(server.create)
        exc = self.assertRaises(exception.ResourceFailure, create)
        self.assertEqual('Error: RackConnect automation FAILED', str(exc))

    def test_rackconnect_unprocessable(self):
        return_server = self.fc.servers.list()[1]
        return_server.metadata = {'rackconnect_automation_status':
                                  'UNPROCESSABLE',
                                  'rackconnect_unprocessable_reason':
                                  'Fake reason'}
        self.m.StubOutWithMock(return_server, 'get')
        return_server.get()
        server = self._setup_test_server(return_server,
                                         'test_rackconnect_unprocessable')
        server.context.roles = ['rack_connect']
        self.m.ReplayAll()
        scheduler.TaskRunner(server.create)()
        self.assertEqual('CREATE', server.action)
        self.assertEqual('COMPLETE', server.status)
        self.m.VerifyAll()

    def test_rackconnect_unknown(self):
        return_server = self.fc.servers.list()[1]
        return_server.metadata = {'rackconnect_automation_status': 'FOO'}
        self.m.StubOutWithMock(return_server, 'get')
        return_server.get()
        server = self._setup_test_server(return_server,
                                         'test_rackconnect_unknown')
        server.context.roles = ['rack_connect']
        self.m.ReplayAll()
        create = scheduler.TaskRunner(server.create)
        exc = self.assertRaises(exception.ResourceFailure, create)
        self.assertEqual('Error: Unknown RackConnect automation status: FOO',
                         str(exc))

    def test_rackconnect_deploying(self):
        return_server = self.fc.servers.list()[0]
        server = self._setup_test_server(return_server,
                                         'srv_sts_bld')
        server.resource_id = 1234
        server.context.roles = ['rack_connect']

        check_iterations = [0]

        # Bind fake get method which check_create_complete will call
        def activate_status(server):
            check_iterations[0] += 1
            if check_iterations[0] == 1:
                server.metadata['rackconnect_automation_status'] = 'DEPLOYING'
            if check_iterations[0] == 2:
                server.status = 'ACTIVE'
            if check_iterations[0] > 3:
                server.metadata['rackconnect_automation_status'] = 'DEPLOYED'
        return_server.get = activate_status.__get__(return_server)
        self.m.ReplayAll()

        scheduler.TaskRunner(server.create)()
        self.assertEqual((server.CREATE, server.COMPLETE), server.state)

        self.m.VerifyAll()

    def test_rackconnect_no_status(self):
        return_server = self.fc.servers.list()[0]
        server = self._setup_test_server(return_server,
                                         'srv_sts_bld')
        server.resource_id = 1234
        server.context.roles = ['rack_connect']

        check_iterations = [0]

        # Bind fake get method which check_create_complete will call
        def activate_status(server):
            check_iterations[0] += 1
            if check_iterations[0] == 1:
                server.status = 'ACTIVE'
            if check_iterations[0] == 2:
                server.metadata = {}
            if check_iterations[0] > 2:
                server.metadata['rackconnect_automation_status'] = 'DEPLOYED'
        return_server.get = activate_status.__get__(return_server)
        self.m.ReplayAll()

        scheduler.TaskRunner(server.create)()
        self.assertEqual((server.CREATE, server.COMPLETE), server.state)

        self.m.VerifyAll()

    def test_managed_cloud_lifecycle(self):
        return_server = self.fc.servers.list()[0]
        server = self._setup_test_server(return_server,
                                         'srv_sts_bld')
        server.resource_id = 1234
        server.context.roles = ['rack_connect', 'rax_managed']

        check_iterations = [0]

        # Bind fake get method which check_create_complete will call
        def activate_status(server):
            check_iterations[0] += 1
            if check_iterations[0] == 1:
                server.status = 'ACTIVE'
            if check_iterations[0] == 2:
                server.metadata = {'rackconnect_automation_status': 'DEPLOYED'}
            if check_iterations[0] == 3:
                server.metadata = {
                    'rackconnect_automation_status': 'DEPLOYED',
                    'rax_service_level_automation': 'In Progress'}
            if check_iterations[0] > 3:
                server.metadata = {
                    'rackconnect_automation_status': 'DEPLOYED',
                    'rax_service_level_automation': 'Complete'}
        return_server.get = activate_status.__get__(return_server)
        self.m.ReplayAll()

        scheduler.TaskRunner(server.create)()
        self.assertEqual((server.CREATE, server.COMPLETE), server.state)

        self.m.VerifyAll()

    def test_managed_cloud_build_error(self):
        return_server = self.fc.servers.list()[1]
        return_server.metadata = {'rax_service_level_automation':
                                  'Build Error'}
        self.m.StubOutWithMock(return_server, 'get')
        return_server.get()
        server = self._setup_test_server(return_server,
                                         'test_managed_cloud_build_error')
        server.context.roles = ['rax_managed']
        self.m.ReplayAll()
        create = scheduler.TaskRunner(server.create)
        exc = self.assertRaises(exception.ResourceFailure, create)
        self.assertEqual('Error: Managed Cloud automation failed', str(exc))

    def test_managed_cloud_unknown(self):
        return_server = self.fc.servers.list()[1]
        return_server.metadata = {'rax_service_level_automation': 'FOO'}
        self.m.StubOutWithMock(return_server, 'get')
        return_server.get()
        server = self._setup_test_server(return_server,
                                         'test_managed_cloud_unknown')
        server.context.roles = ['rax_managed']
        self.m.ReplayAll()
        create = scheduler.TaskRunner(server.create)
        exc = self.assertRaises(exception.ResourceFailure, create)
        self.assertEqual('Error: Unknown Managed Cloud automation status: FOO',
                         str(exc))
