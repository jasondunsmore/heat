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

from oslo.config import cfg
import paramiko

from heat.common import exception
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource
from heat.engine import scheduler
from heat.openstack.common.gettextutils import _

cfg.CONF.import_opt('max_json_body_size', 'heat.common.config')


class SSHWaitCondition(resource.Resource):
    PROPERTIES = (
        IP_ADDRESSES, PATH, USER, PRIVATE_KEY, TIMEOUT
    ) = (
        'ip_addresses', 'path', 'user', 'private_key', 'timeout'
    )

    properties_schema = {
        IP_ADDRESSES: properties.Schema(
            properties.Schema.LIST,
            description=_('List of server IP addresses to wait on'),
            required=True
        ),
        PRIVATE_KEY: properties.Schema(
            properties.Schema.STRING,
            required=True,
            description=_('The private SSH key that will be used to connect.')
        ),
        TIMEOUT: properties.Schema(
            properties.Schema.NUMBER,
            description=_('The number of seconds to wait for the script to '
                          'run successfully.'),
            required=True,
            constraints=[
                constraints.Range(1, 300),
            ]
        ),
        PATH: properties.Schema(
            properties.Schema.STRING,
            required=True,
            description=_('A custom shell script to wait on. An exit code of '
                          '0 signals a successful check. An exit code of 4 '
                          'will result in a retry. Any other non-zero exit '
                          'status will result in a failed stack.')
        ),
        USER: properties.Schema(
            properties.Schema.STRING,
            default='root',
            description=_('The user to SSH to the server as.')
        ),
    }

    def handle_create(self):
        checkers = []
        for ip in self.properties.get(self.IP_ADDRESSES):
            checker = scheduler.TaskRunner(self._check_resource, ip)
            checker.start(timeout=float(self.properties[self.TIMEOUT]))
            checkers.append(checker)
        return checkers

    def _check_resource(self, ip):
        timeout = self.properties[self.TIMEOUT]
        path = self.properties.get(self.PATH)

        def ssh_command(path):
            with tempfile.NamedTemporaryFile() as private_key_file:
                private_key = self.properties.get(self.PRIVATE_KEY)
                private_key_file.write(private_key)
                private_key_file.seek(0)
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(
                    paramiko.MissingHostKeyPolicy())
                try:
                    ssh.connect(ip, username=self.properties.get(self.USER),
                                key_filename=private_key_file.name)
                except socket.error as exc:
                    # Sometimes SSH becomes unavailable while cloud-init
                    # is running.  Try again later.
                    if exc.errno == 111:  # Connection refused
                        return 4
                    raise
            try:
                chan = ssh.get_transport().open_session()
                chan.settimeout(timeout)
                chan.exec_command(path)
                max_bytes = cfg.CONF.max_json_body_size
                bytes_read = 0
                while not chan.exit_status_ready():
                    if bytes_read >= max_bytes:
                        msg = _("Received more than %(max_bytes)s bytes of "
                                "output from the SSH command: %(path)s") % \
                            {'max_bytes': max_bytes, 'path': path}
                        raise exception.Error(msg)
                    try:
                        # If too much output is buffered, the exit status
                        # may never be ready (recv_exit_status can hang
                        # forever), so read output until the exit status
                        # is ready.
                        chan.recv(1024)
                    except socket.timeout:
                        raise exception.Error(_("SSH command timed out after "
                                                "%(timeout)s seconds") %
                                              {'timeout': timeout})
                    bytes_read += 1024
                exit_code = chan.recv_exit_status()
                return exit_code
            finally:
                chan.close()
                ssh.close()

        while True:
            exit_code = ssh_command(path)
            if exit_code == 0:
                return
            elif exit_code == 4:
                try:
                    yield
                except scheduler.Timeout:
                    msg = _('Server at %(ip)s timed out after %(secs)s '
                            'seconds') % {'ip': ip, 'secs': timeout}
                    raise exception.Error(msg)
            else:
                msg = _('Script failed on server at %s') % ip
                raise exception.Error(msg)

    def check_create_complete(self, checkers):
        ret_status = True
        for checker in checkers:
            if not checker.started():
                checker.start()
            if not checker.step():
                ret_status = False
        return ret_status


def resource_mapping():
    return {'Rackspace::Cloud::SSHWaitCondition': SSHWaitCondition}


def available_resource_mapping():
    return resource_mapping()
