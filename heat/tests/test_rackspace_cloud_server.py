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
import paramiko

from heat.openstack.common import log as logging
from heat.tests.v1_1 import fakes
from heat.common import template_format, exception
from heat.engine import parser
from heat.engine import resource
from heat.engine import scheduler
from heat.openstack.common import uuidutils
from heat.tests.common import HeatTestCase
from heat.tests import utils
from heat.tests.utils import setup_dummy_db
from heat.engine.resources.rackspace import cloud_server, rackspace_resource

logger = logging.getLogger(__name__)

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

    def _setup_test_stack(self, stack_name):
        t = template_format.parse(wp_template)
        template = parser.Template(t)
        params = parser.Parameters(stack_name, template, {'Flavor': '2'})
        stack = parser.Stack(None, stack_name, template, params,
                             stack_id=uuidutils.generate_uuid())
        return (t, stack)

    def _setup_test_instance(self, return_server, name, image_name="F17"):
        stack_name = '%s_stack' % name
        (t, stack) = self._setup_test_stack(stack_name)

        t['Resources']['WebServer']['Properties']['ImageName'] = image_name
        t['Resources']['WebServer']['Properties']['InstanceName'] = 'Heat test'
        t['Resources']['WebServer']['Properties']['Flavor'] = '2'

        instance = cloud_server.CloudServer('%s_name' % name,
                                            t['Resources']['WebServer'], stack)
        #self.m.StubOutWithMock(logger, 'info')
        #logger.info(mox.IgnoreArg())

        instance.t = instance.stack.resolve_runtime_data(instance.t)

        instance_name = t['Resources']['WebServer']['Properties']['InstanceName']
        image_id = instance.rackspace_images[image_name]
        flavor = t['Resources']['WebServer']['Properties']['Flavor']

        self.m.StubOutWithMock(self.fc.servers, 'create')
        self.fc.servers.create(instance_name, image_id, flavor,
                               files=mox.IgnoreArg()).AndReturn(return_server)

        # SSH
        self.m.StubOutWithMock(paramiko, "SSHClient")
        self.m.StubOutWithMock(paramiko, "MissingHostKeyPolicy")
        ssh = self.m.CreateMockAnything()
        paramiko.SSHClient().AndReturn(ssh)
        paramiko.MissingHostKeyPolicy()
        ssh.set_missing_host_key_policy(None)
        ssh.connect(mox.IgnoreArg(),
                    key_filename=mox.IgnoreArg(),
                    username='root')
        stdin = self.m.CreateMockAnything()
        stdout = self.m.CreateMockAnything()
        stderr = self.m.CreateMockAnything()
        stdout.read().AndReturn("stdout")
        stderr.read().AndReturn("stderr")
        ssh.exec_command(mox.IgnoreArg()).AndReturn((stdin, stdout, stderr))

        # SFTP
        self.m.StubOutWithMock(paramiko, "Transport")
        transport = self.m.CreateMockAnything()
        paramiko.Transport((mox.IgnoreArg(), 22)).AndReturn(transport)
        transport.connect(hostkey=None, username="root", pkey=mox.IgnoreArg())
        sftp = self.m.CreateMockAnything()
        self.m.StubOutWithMock(paramiko, "SFTPClient")
        paramiko.SFTPClient.from_transport(transport).AndReturn(sftp)
        sftp_file = self.m.CreateMockAnything()
        sftp.open(mox.IgnoreArg(), 'w').AndReturn(sftp_file)
        sftp_file.write(mox.IgnoreArg())
        sftp_file.close()
        sftp_file = self.m.CreateMockAnything()
        sftp.open(mox.IgnoreArg(), 'w').AndReturn(sftp_file)
        sftp_file.write(mox.IgnoreArg())
        sftp_file.close()

        self.m.StubOutWithMock(rackspace_resource.RackspaceResource, "nova")
        rackspace_resource.RackspaceResource.nova().MultipleTimes().AndReturn(self.fc)

        return instance

    def _create_test_instance(self, return_server, name):
        instance = self._setup_test_instance(return_server, name)

        self.m.ReplayAll()
        scheduler.TaskRunner(instance.create)()
        return instance

    def _update_test_instance(self, return_server, name):
        instance = self._setup_test_instance(return_server, name)

        # SFTP
        transport = self.m.CreateMockAnything()
        paramiko.Transport((mox.IgnoreArg(), 22))
        transport.connect(hostkey=None, username="root", pkey=mox.IgnoreArg())
        sftp = self.m.CreateMockAnything()
        paramiko.SFTPClient.from_transport(transport).AndReturn(sftp)
        sftp_file = self.m.CreateMockAnything()
        sftp.open(mox.IgnoreArg(), 'w').AndReturn(sftp_file)
        sftp_file.write(mox.IgnoreArg())
        sftp_file.close()
        sftp_file = self.m.CreateMockAnything()
        sftp.open(mox.IgnoreArg(), 'w').AndReturn(sftp_file)
        sftp_file.write(mox.IgnoreArg())
        sftp_file.close()

    def test_instance_create(self):
        return_server = self.fc.servers.list()[1]
        instance = self._create_test_instance(return_server,
                                              'test_instance_create')
        # this makes sure the auto increment worked on instance creation
        self.assertTrue(instance.id > 0)

        expected_public = return_server.networks['public'][0]
        expected_private = return_server.networks['private'][0]
        self.assertEqual(instance.FnGetAtt('PublicIp'), expected_public)
        self.assertEqual(instance.FnGetAtt('PrivateIp'), expected_private)
        self.assertEqual(instance.FnGetAtt('PublicDnsName'), expected_public)
        self.assertEqual(instance.FnGetAtt('PrivateDnsName'), expected_public)

        self.m.VerifyAll()

    def test_instance_create_with_image_name(self):
        return_server = self.fc.servers.list()[1]
        instance = self._setup_test_instance(return_server,
                                             'test_instance_create_image_id',
                                             image_name='F18')

        self.m.ReplayAll()
        scheduler.TaskRunner(instance.create)()

        # this makes sure the auto increment worked on instance creation
        self.assertTrue(instance.id > 0)

        expected_public = return_server.networks['public'][0]
        expected_private = return_server.networks['private'][0]
        self.assertEqual(instance.FnGetAtt('PublicIp'), expected_public)
        self.assertEqual(instance.FnGetAtt('PrivateIp'), expected_private)
        self.assertEqual(instance.FnGetAtt('PublicDnsName'), expected_public)
        self.assertEqual(instance.FnGetAtt('PrivateDnsName'), expected_public)

        self.m.VerifyAll()

    def test_instance_create_image_name_err(self):
        stack_name = 'test_instance_create_image_name_err_stack'
        (t, stack) = self._setup_test_stack(stack_name)

        # create an instance with non exist image name
        t['Resources']['WebServer']['Properties']['ImageName'] = 'Slackware'
        instance = cloud_server.CloudServer('instance_create_image_err',
                                            t['Resources']['WebServer'], stack)

        self.assertRaises(exception.ImageNotFound, instance.handle_create)

        self.m.VerifyAll()

    def test_instance_create_flavor_err(self):
        stack_name = 'test_instance_create_flavor_err_stack'
        (t, stack) = self._setup_test_stack(stack_name)

        # create an instance with non exist image name
        t['Resources']['WebServer']['Properties']['Flavor'] = '1'
        instance = cloud_server.CloudServer('instance_create_flavor_err',
                                            t['Resources']['WebServer'], stack)

        self.assertRaises(exception.FlavorMissing, instance.handle_create)

        self.m.VerifyAll()

    def test_instance_create_delete(self):
        return_server = self.fc.servers.list()[1]
        instance = self._create_test_instance(return_server,
                                              'test_instance_create_delete')
        instance.resource_id = 1234

        # this makes sure the auto increment worked on instance creation
        self.assertTrue(instance.id > 0)

        instance.delete()
        self.assertTrue(instance.resource_id is None)
        self.assertEqual(instance.state, (instance.DELETE, instance.COMPLETE))
        self.m.VerifyAll()

    def test_instance_update_metadata(self):
        return_server = self.fc.servers.list()[1]
        instance = self._create_test_instance(return_server,
                                              'test_instance_update')
        self.m.UnsetStubs()
        self._update_test_instance(return_server, 'test_instance_update')
        self.m.ReplayAll()
        update_template = copy.deepcopy(instance.t)
        update_template['Metadata'] = {'test': 123}
        self.assertEqual(None, instance.update(update_template))
        self.assertEqual(instance.metadata, {'test': 123})

    def test_instance_update_replace(self):
        return_server = self.fc.servers.list()[1]
        instance = self._create_test_instance(return_server,
                                              'test_instance_update')

        update_template = copy.deepcopy(instance.t)
        update_template['Notallowed'] = {'test': 123}
        self.assertRaises(resource.UpdateReplace,
                          instance.update, update_template)

    def test_instance_update_properties(self):
        return_server = self.fc.servers.list()[1]
        instance = self._create_test_instance(return_server,
                                              'test_instance_update')

        update_template = copy.deepcopy(instance.t)
        update_template['Properties']['KeyName'] = 'mustreplace'
        self.assertRaises(resource.UpdateReplace,
                          instance.update, update_template)

    def test_instance_status_build(self):
        return_server = self.fc.servers.list()[0]
        instance = self._setup_test_instance(return_server,
                                             'test_instance_status_build')
        instance.resource_id = 1234

        # Bind fake get method which Instance.check_create_complete will call
        def activate_status(server):
            server.status = 'ACTIVE'
        return_server.get = activate_status.__get__(return_server)
        self.m.ReplayAll()

        scheduler.TaskRunner(instance.create)()
        self.assertEqual(instance.state, instance.CREATE_COMPLETE)

    def test_instance_status_hard_reboot(self):
        self._test_instance_status_not_build_active('HARD_REBOOT')

    def test_instance_status_password(self):
        self._test_instance_status_not_build_active('PASSWORD')

    def test_instance_status_reboot(self):
        self._test_instance_status_not_build_active('REBOOT')

    def test_instance_status_rescue(self):
        self._test_instance_status_not_build_active('RESCUE')

    def test_instance_status_resize(self):
        self._test_instance_status_not_build_active('RESIZE')

    def test_instance_status_revert_resize(self):
        self._test_instance_status_not_build_active('REVERT_RESIZE')

    def test_instance_status_shutoff(self):
        self._test_instance_status_not_build_active('SHUTOFF')

    def test_instance_status_suspended(self):
        self._test_instance_status_not_build_active('SUSPENDED')

    def test_instance_status_verify_resize(self):
        self._test_instance_status_not_build_active('VERIFY_RESIZE')

    def _test_instance_status_not_build_active(self, uncommon_status):
        return_server = self.fc.servers.list()[0]
        instance = self._setup_test_instance(return_server,
                                             'test_instance_status_build')
        instance.resource_id = 1234

        # Bind fake get method which Instance.check_create_complete will call
        def activate_status(server):
            if hasattr(server, '_test_check_iterations'):
                server._test_check_iterations += 1
            else:
                server._test_check_iterations = 1
            if server._test_check_iterations == 1:
                server.status = uncommon_status
            if server._test_check_iterations > 2:
                server.status = 'ACTIVE'
        return_server.get = activate_status.__get__(return_server)
        self.m.StubOutWithMock(scheduler.TaskRunner, '_sleep')
        scheduler.TaskRunner._sleep(mox.IsA(int)).AndReturn(None)
        scheduler.TaskRunner._sleep(mox.IsA(int)).AndReturn(None)
        self.m.ReplayAll()

        scheduler.TaskRunner(instance.create)()
        self.assertEqual(instance.state, instance.CREATE_COMPLETE)

        self.m.VerifyAll()

    def test_build_nics(self):
        return_server = self.fc.servers.list()[1]
        instance = self._create_test_instance(return_server,
                                              'test_build_nics')

        self.assertEqual(None, instance._build_nics([]))
        self.assertEqual(None, instance._build_nics(None))
        self.assertEqual([
            {'port-id': 'id3'}, {'port-id': 'id1'}, {'port-id': 'id2'}],
            instance._build_nics([
                'id3', 'id1', 'id2']))
        self.assertEqual([
            {'port-id': 'id1'},
            {'port-id': 'id2'},
            {'port-id': 'id3'}], instance._build_nics([
                {'NetworkInterfaceId': 'id3', 'DeviceIndex': '3'},
                {'NetworkInterfaceId': 'id1', 'DeviceIndex': '1'},
                {'NetworkInterfaceId': 'id2', 'DeviceIndex': 2},
            ]))
        self.assertEqual([
            {'port-id': 'id1'},
            {'port-id': 'id2'},
            {'port-id': 'id3'},
            {'port-id': 'id4'},
            {'port-id': 'id5'}
        ], instance._build_nics([
            {'NetworkInterfaceId': 'id3', 'DeviceIndex': '3'},
            {'NetworkInterfaceId': 'id1', 'DeviceIndex': '1'},
            {'NetworkInterfaceId': 'id2', 'DeviceIndex': 2},
            'id4',
            'id5'
        ]))

    def test_instance_without_ip_address(self):
        return_server = self.fc.servers.list()[3]
        instance = self._create_test_instance(return_server,
                                              'test_without_ip_address')

        self.assertEqual(instance.FnGetAtt('PrivateIp'), '0.0.0.0')
