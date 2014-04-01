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

import socket
import time

import mock
from oslo.config import cfg
import paramiko

from heat.common import exception
from heat.common import template_format
from heat.engine import parser
from heat.engine import resource
from heat.engine import scheduler
from heat.tests.common import HeatTestCase
from heat.tests.v1_1 import fakes as fakes_v1_1
from heat.tests import utils

from ..resources import cloud_server  # noqa
from ..resources import wait_condition  # noqa


raw_template = '''
{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Description": "Hello world",
  "Resources": {
    "TestWaitCondition": {
      "Type": "Rackspace::Server::SSHWaitCondition",
      "Properties": {
        "ip_addresses": [ '1.2.3.4' ],
        "private_key": "1234",
        "timeout": "30",
        "user": "root",
        "script": "[[ -e /root/hello-world.txt ]]"
      }
    }
  }
}
'''


class SSHWaitConditionTest(HeatTestCase):

    def setUp(self):
        super(SSHWaitConditionTest, self).setUp()
        self.fc = fakes_v1_1.FakeClient()
        utils.setup_dummy_db()
        # Test environment may not have pyrax client library installed and if
        # pyrax is not installed resource class would not be registered.
        # So register resource provider class explicitly for unit testing.
        resource._register_class("Rackspace::Server::SSHWaitCondition",
                                 wait_condition.SSHWaitCondition)
        resource._register_class("Rackspace::Cloud::Server",
                                 cloud_server.CloudServer)

    @mock.patch.object(paramiko, 'SSHClient')
    def test_successful_with_script(self, mock_ssh_class):
        t = template_format.parse(raw_template)
        stack = utils.parse_stack(t)

        mock_ssh, mock_chan, mock_transport = (mock.Mock(),) * 3
        mock_ssh_class.return_value = mock_ssh
        mock_ssh.get_transport.return_value = mock_transport
        mock_transport.open_session.return_value = mock_chan
        mock_chan.recv_exit_status.return_value = 0

        wait_cond = wait_condition.SSHWaitCondition(
            'test', t['Resources']['TestWaitCondition'], stack)

        self.assertIsNone(scheduler.TaskRunner(wait_cond.create)())
        self.assertEqual(1, mock_chan.recv_exit_status.call_count)

    @mock.patch.object(paramiko, 'SSHClient')
    def test_custom_check_retry(self, mock_ssh_class):
        t = template_format.parse(raw_template)
        stack = utils.parse_stack(t)

        mock_ssh, mock_chan, mock_transport = (mock.Mock(),) * 3
        mock_ssh_class.return_value = mock_ssh
        mock_ssh.get_transport.return_value = mock_transport
        mock_transport.open_session.return_value = mock_chan
        mock_chan.recv_exit_status.side_effect = [4, 0]

        wait_cond = wait_condition.SSHWaitCondition(
            'test', t['Resources']['TestWaitCondition'], stack)

        self.assertIsNone(scheduler.TaskRunner(wait_cond.create)())
        self.assertEqual(2, mock_chan.recv_exit_status.call_count)

    @mock.patch.object(paramiko, 'SSHClient')
    def test_custom_check_failed(self, mock_ssh_class):
        t = template_format.parse(raw_template)
        stack = utils.parse_stack(t)

        mock_ssh, mock_chan, mock_transport = (mock.Mock(),) * 3
        mock_ssh_class.return_value = mock_ssh
        mock_ssh.get_transport.return_value = mock_transport
        mock_transport.open_session.return_value = mock_chan
        mock_chan.recv_exit_status.return_value = 1

        wait_cond = wait_condition.SSHWaitCondition(
            'test', t['Resources']['TestWaitCondition'], stack)

        exc = self.assertRaises(exception.ResourceFailure,
                                scheduler.TaskRunner(wait_cond.create))
        self.assertIn("Script failed on server", str(exc))
        self.assertEqual(1, mock_chan.recv_exit_status.call_count)

    @mock.patch.object(paramiko, 'SSHClient')
    def test_multiple_ips(self, mock_ssh_class):
        t = template_format.parse(raw_template)
        t['Resources']['TestWaitCondition']['Properties']['ip_addresses'] = \
            ['1.2.3.4', '5.6.7.8']
        stack = utils.parse_stack(t)

        mock_ssh, mock_chan, mock_transport = (mock.Mock(),) * 3
        mock_ssh_class.return_value = mock_ssh
        mock_ssh.get_transport.return_value = mock_transport
        mock_transport.open_session.return_value = mock_chan
        mock_chan.recv_exit_status.return_value = 0

        wait_cond = wait_condition.SSHWaitCondition(
            'test', t['Resources']['TestWaitCondition'], stack)

        self.assertIsNone(scheduler.TaskRunner(wait_cond.create)())
        self.assertEqual(2, mock_chan.recv_exit_status.call_count)

    @mock.patch.object(paramiko, 'SSHClient')
    def test_ssh_connection_refused(self, mock_ssh_class):
        t = template_format.parse(raw_template)
        stack = utils.parse_stack(t)

        mock_ssh, mock_chan, mock_transport = (mock.Mock(),) * 3
        mock_ssh_class.return_value = mock_ssh
        exc = socket.error()
        exc.errno = 111
        mock_ssh.connect.side_effect = [exc, None]
        mock_ssh.get_transport.return_value = mock_transport
        mock_transport.open_session.return_value = mock_chan
        mock_chan.recv_exit_status.return_value = 0

        wait_cond = wait_condition.SSHWaitCondition(
            'test', t['Resources']['TestWaitCondition'], stack)

        self.assertIsNone(scheduler.TaskRunner(wait_cond.create)())
        self.assertEqual(2, mock_ssh.connect.call_count)

    @mock.patch.object(paramiko, 'SSHClient')
    def test_ssh_other_socket_error(self, mock_ssh_class):
        t = template_format.parse(raw_template)
        stack = utils.parse_stack(t)

        mock_ssh, mock_chan, mock_transport = (mock.Mock(),) * 3
        mock_ssh_class.return_value = mock_ssh
        exc = socket.error()
        exc.errno = 123
        mock_ssh.connect.side_effect = [exc, None]
        mock_ssh.get_transport.return_value = mock_transport
        mock_transport.open_session.return_value = mock_chan
        mock_chan.recv_exit_status.return_value = 0

        wait_cond = wait_condition.SSHWaitCondition(
            'test', t['Resources']['TestWaitCondition'], stack)

        self.assertRaises(exception.ResourceFailure,
                          scheduler.TaskRunner(wait_cond.create))
        self.assertEqual(1, mock_ssh.connect.call_count)

    @mock.patch.object(paramiko, 'SSHClient')
    @mock.patch.object(scheduler, 'wallclock')
    @mock.patch.object(parser.Stack, 'timeout_secs')
    def test_timeout_runner(self, mock_timeout, mock_wallclock,
                            mock_ssh_class):
        t = template_format.parse(raw_template)
        t['Resources']['TestWaitCondition']['Properties']['timeout'] = 5
        stack = utils.parse_stack(t)

        mock_ssh, mock_chan, mock_transport = (mock.Mock(),) * 3
        mock_ssh_class.return_value = mock_ssh
        mock_ssh.get_transport.return_value = mock_transport
        mock_transport.open_session.return_value = mock_chan
        mock_chan.recv_exit_status.return_value = 4

        now = time.time()
        mock_wallclock.side_effect = [now + x for x in range(10)]

        wait_cond = wait_condition.SSHWaitCondition(
            'test', t['Resources']['TestWaitCondition'], stack)

        exc = self.assertRaises(exception.ResourceFailure,
                                scheduler.TaskRunner(wait_cond.create))
        self.assertIn("timed out after 5 seconds", str(exc))
        self.assertEqual(5, mock_chan.recv_exit_status.call_count)

    @mock.patch.object(paramiko, 'SSHClient')
    def test_timeout_ssh(self, mock_ssh_class):
        t = template_format.parse(raw_template)
        t['Resources']['TestWaitCondition']['Properties']['timeout'] = 5
        stack = utils.parse_stack(t)

        mock_ssh, mock_chan, mock_transport = (mock.Mock(),) * 3
        mock_ssh_class.return_value = mock_ssh
        mock_ssh.get_transport.return_value = mock_transport
        mock_transport.open_session.return_value = mock_chan
        mock_chan.exit_status_ready.return_value = False
        mock_chan.recv.side_effect = socket.timeout()

        wait_cond = wait_condition.SSHWaitCondition(
            'test', t['Resources']['TestWaitCondition'], stack)

        exc = self.assertRaises(exception.ResourceFailure,
                                scheduler.TaskRunner(wait_cond.create))
        self.assertIn("SSH command timed out after 5 seconds", str(exc))

    @mock.patch.object(paramiko, 'SSHClient')
    def test_custom_user(self, mock_ssh_class):
        t = template_format.parse(raw_template)
        t['Resources']['TestWaitCondition']['Properties']['user'] = 'heat'
        t['Resources']['TestWaitCondition']['Properties']['script'] = None
        stack = utils.parse_stack(t)

        mock_ssh, mock_chan, mock_transport = (mock.Mock(),) * 3
        mock_ssh_class.return_value = mock_ssh
        mock_ssh.get_transport.return_value = mock_transport
        mock_transport.open_session.return_value = mock_chan
        mock_chan.recv_exit_status.return_value = 0

        wait_cond = wait_condition.SSHWaitCondition(
            'test', t['Resources']['TestWaitCondition'], stack)

        self.assertIsNone(scheduler.TaskRunner(wait_cond.create)())
        mock_ssh.connect.assert_called_once_with(mock.ANY,
                                                 username='heat',
                                                 key_filename=mock.ANY)

    @mock.patch.object(paramiko, 'SSHClient')
    def test_max_bytes(self, mock_ssh_class):
        t = template_format.parse(raw_template)
        stack = utils.parse_stack(t)

        mock_ssh, mock_chan, mock_transport = (mock.Mock(),) * 3
        mock_ssh_class.return_value = mock_ssh
        mock_ssh.get_transport.return_value = mock_transport
        mock_transport.open_session.return_value = mock_chan
        mock_socket_err = mock.Mock()
        mock_socket_err.errno = 111
        mock_ssh.connect.side_effect = mock_socket_err()
        mock_chan.recv.return_value = "1" * 1024
        mock_chan.exit_status_ready.return_value = False
        cfg.CONF.set_override('max_json_body_size', 1048576)

        wait_cond = wait_condition.SSHWaitCondition(
            'test', t['Resources']['TestWaitCondition'], stack)

        exc = self.assertRaises(exception.ResourceFailure,
                                scheduler.TaskRunner(wait_cond.create))
        self.assertIn("Received more than 1048576 bytes of output", str(exc))
        self.assertEqual(0, mock_chan.recv_exit_status.call_count)
        self.assertEqual(1025, mock_chan.exit_status_ready.call_count)
