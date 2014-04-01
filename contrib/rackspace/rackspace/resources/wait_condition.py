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
import tempfile

import paramiko

from heat.common import exception
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource
from heat.engine import scheduler
from heat.openstack.common.gettextutils import _
from heat.openstack.common import log as logging

logger = logging.getLogger(__name__)


class SSHConnectionRefused(Exception):
    pass


class SSHWaitCondition(resource.Resource):
    PROPERTIES = (
        RESOURCE_IDS, SCRIPT, USER, PRIVATE_KEY, TIMEOUT
    ) = (
        'resource_ids', 'script', 'user', 'private_key', 'timeout'
    )

    properties_schema = {
        RESOURCE_IDS: properties.Schema(
            properties.Schema.LIST,
            description=_('List of resource IDs to wait on'),
            required=True
        ),
        PRIVATE_KEY: properties.Schema(
            properties.Schema.STRING,
            required=True,
            description=_('The private SSH key that will be used to connect.')
        ),
        TIMEOUT: properties.Schema(
            properties.Schema.NUMBER,
            description=_('The number of seconds to wait for cloud-init '
                          'and the optional script to finish.'),
            required=True,
            constraints=[
                constraints.Range(1, 3600),
            ]
        ),
        SCRIPT: properties.Schema(
            properties.Schema.STRING,
            default='',
            description=_('Script to test if cloud-init was successful. '
                          'A non-zero exit status will result in a failed '
                          'stack.')
        ),
        USER: properties.Schema(
            properties.Schema.STRING,
            default='root',
            description=_('The user to SSH to the server as.')
        ),
    }

    def handle_create(self):
        checkers = []
        for resource_id in self.properties.get(self.RESOURCE_IDS):
            checker = scheduler.TaskRunner(self._check_resource, resource_id)
            checker.start(timeout=float(self.properties[self.TIMEOUT]))
            checkers.append(checker)
        return checkers

    def _check_resource(self, resource_id):
        server = self.nova().servers.get(resource_id)

        def ssh_command(command):
            with tempfile.NamedTemporaryFile() as private_key_file:
                private_key = self.properties.get(self.PRIVATE_KEY)
                private_key_file.write(private_key)
                private_key_file.seek(0)
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(
                    paramiko.MissingHostKeyPolicy())
                try:
                    ssh.connect(server.accessIPv4,
                                username=self.properties.get(self.USER),
                                key_filename=private_key_file.name)
                except socket.error as exc:
                    if exc.errno == 111:
                        raise SSHConnectionRefused()
                    raise
            try:
                stdin, stdout, stderr = ssh.exec_command(command)
                bytes_read = 0
                max_bytes = 1048576
                while not stdout.channel.exit_status_ready():
                    if bytes_read >= max_bytes:
                        msg = _("Received more than %(max_bytes)s bytes of "
                                "output from the SSH command: %(command)s") % \
                              {'max_bytes': max_bytes, 'command': command}
                        raise exception.Error(msg)
                    # If too much output is buffered, the exit status
                    # may never be ready (recv_exit_status will hang
                    # forever), so read output until the exit status
                    # is ready.
                    stdout.read(1024)
                    bytes_read += 1024
                exit_code = stdout.channel.recv_exit_status()
                if exit_code == 0:
                    return True
                else:
                    return False
            finally:
                ssh.close()

        def cloud_init_finished():
            bt_fin = '/var/lib/cloud/instances/%s/boot-finished' % resource_id
            try:
                return ssh_command('[ -e %s ]' % bt_fin)
            except SSHConnectionRefused:
                # Sometimes SSH becomes unavailable while cloud-init
                # is running.  Try again later.
                return False

        while not cloud_init_finished():
            try:
                yield
            except scheduler.Timeout:
                msg = _('%(server)s timed out after %(secs)s seconds') % \
                      {'server': server.name,
                       'secs': self.properties[self.TIMEOUT]}
                raise exception.Error(msg)

        script = self.properties.get(self.SCRIPT)
        if not script:
            return

        custom_check_successful = ssh_command(script)
        if custom_check_successful:
            return
        else:
            msg = _('Script failed on server: %s') % server.name
            raise exception.Error(msg)

    def check_create_complete(self, checkers):
        for checker in checkers:
            if not checker.started():
                checker.start()
            if not checker.step():
                return False
        return True


def resource_mapping():
    return {'Rackspace::Cloud::SSHWaitCondition': SSHWaitCondition}


def available_resource_mapping():
    return resource_mapping()
