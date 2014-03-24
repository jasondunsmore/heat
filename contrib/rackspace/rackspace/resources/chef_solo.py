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

import os
import pickle
import psutil
import shlex
import subprocess
import tempfile
import uuid

from oslo_log import log as logging

from oslo.config import cfg

from heat.common import exception
from heat.common.i18n import _
from heat.engine import properties
from heat.engine import resource
from heat.engine import support
from heat.openstack.common.versionutils import deprecated


LOG = logging.getLogger(__name__)


# All of these options must have a default because they'll be passed
# as CLI options

chef_opts = [
    cfg.StrOpt('rubygem_path',
               default="/opt/chef/embedded/bin",
               help=_('Path where the gem binary is located.')),
    cfg.StrOpt('berkshelf_version',
               default="2.0.18",
               help=_('The version of berkshelf to install on the client '
                      'instance.')),
    cfg.StrOpt('librarian_chef_version',
               default="0.0.2",
               help=_('The version of librarian-chef to install on the client '
                      'instance.')),
    cfg.StrOpt('chef_solo_path',
               default="/tmp/heat_chef",
               help=_('Path to cache chef solo kitchens.')),
    cfg.IntOpt('sftp_retries',
               default=30,
               help=_('Number of times to retry SSH connection.')),
    cfg.BoolOpt('ssh_jump_enabled',
                default=False,
                help=_('Use jump host for SSH connections.')),
    cfg.StrOpt('ssh_jump_host',
               default='1.2.3.4',
               help=_('IP of jump host (not hostname).')),
    cfg.IntOpt('ssh_jump_port',
               default=22,
               help=_('SSH port of jump host.')),
    cfg.StrOpt('ssh_jump_user',
               default='heat',
               help=_('User to use for jump host.')),
    cfg.StrOpt('ssh_jump_key',
               default='/opt/heat/.ssh/id_rsa',
               help=_('Path to private SSH key to use for jump host.')),
]
cfg.CONF.register_opts(chef_opts)


class ChefSolo(resource.Resource):

    PROPERTIES = (
        BERKSFILE, BERKSFILE_LOCK, CHEFFILE, USERNAME, HOST, PRIVATE_KEY,
        DATA_BAGS, NODE, ROLES, USERS, ENVIRONMENTS, CLIENTS, CHEF_VERSION,
        KITCHEN
    ) = (
        'Berksfile', 'Berksfile.lock', 'Cheffile', 'username', 'host',
        'private_key', 'data_bags', 'node', 'roles', 'users', 'environments',
        'clients', 'chef_version', 'kitchen'
    )

    properties_schema = {
        BERKSFILE_LOCK: properties.Schema(
            properties.Schema.STRING,
            _('The Berksfile.lock to use with berkshelf to specify cookbook '
              'versions for the chef run.')
        ),
        BERKSFILE: properties.Schema(
            properties.Schema.STRING,
            _('The Berksfile to use with berkshelf to download cookbooks on '
              'the host for the chef run.'),
            support_status=support.SupportStatus(
                support.DEPRECATED,
                _('Use property %s.') % KITCHEN),
        ),
        CHEFFILE: properties.Schema(
            properties.Schema.STRING,
            _('The Cheffile to use with librarian-chef to download cookbooks '
              'on the host for the chef run.'),
            support_status=support.SupportStatus(
                support.DEPRECATED,
                _('Use property %s.') % KITCHEN),
        ),
        KITCHEN: properties.Schema(
            properties.Schema.STRING,
            _('A git url to the kitchen to clone. This can be used in place '
              'of a Berks or Chef file to install cookbooks on the host.'),
        ),
        USERNAME: properties.Schema(
            properties.Schema.STRING,
            _('The username to connect to the host with.'),
            default="root",
            required=True
        ),
        HOST: properties.Schema(
            properties.Schema.STRING,
            _('The host to run chef-solo on.'),
            required=True
        ),
        PRIVATE_KEY: properties.Schema(
            properties.Schema.STRING,
            _('The ssh key to connect to the host with.'),
            required=True
        ),
        DATA_BAGS: properties.Schema(
            properties.Schema.MAP,
            _('Data_bags to write to the kitchen during the chef run.'),
        ),
        NODE: properties.Schema(
            properties.Schema.MAP,
            _('The node file for the chef run. May have a run_list, '
              'attributes, etc.'),
        ),
        ROLES: properties.Schema(
            properties.Schema.MAP,
            _('Roles to be written to the kitchen for the chef run.'),
        ),
        USERS: properties.Schema(
            properties.Schema.MAP,
            _('Users to be written to the kitchen for the chef run.'),
        ),
        ENVIRONMENTS: properties.Schema(
            properties.Schema.MAP,
            _('Environments to be written to the kitchen for the chef run.'),
        ),
        CLIENTS: properties.Schema(
            properties.Schema.MAP,
            _('Clients to be written to the kitchen for the chef run.'),
        ),
        CHEF_VERSION: properties.Schema(
            properties.Schema.STRING,
            _('The version of chef to install on the host.'),
        )
    }

    def __init__(self, name, json_snippet, stack):
        super(ChefSolo, self).__init__(name, json_snippet, stack)

    def handle_create(self):
        self.resource_id_set(str(uuid.uuid4()))

        path = os.path.dirname(os.path.realpath(__file__)) + "/create_chef.py"
        with tempfile.NamedTemporaryFile(delete=False) as prop_file:
            pickle.dump(self.properties.items(), prop_file)
        cmd = ("nice timeout -k 5 %s "
               "python %s "
               "--prop-file %s "
               "--chef-solo-path %s "
               "--resource-id %s "
               "--sftp-retries %s "
               "--jump-enabled %s "
               "--jump-host %s "
               "--jump-port %s "
               "--jump-user %s "
               "--jump-key %s "
               "--rubygem-path %s "
               "--berkshelf-version %s "
               "--librarian-chef-version %s" % (
                   self.stack.timeout_secs(),
                   path,
                   prop_file.name,
                   cfg.CONF.chef_solo_path,
                   self.resource_id,
                   cfg.CONF.sftp_retries,
                   cfg.CONF.ssh_jump_enabled,
                   cfg.CONF.ssh_jump_host,
                   cfg.CONF.ssh_jump_port,
                   cfg.CONF.ssh_jump_user,
                   cfg.CONF.ssh_jump_key,
                   cfg.CONF.rubygem_path,
                   cfg.CONF.berkshelf_version,
                   cfg.CONF.librarian_chef_version))
        LOG.info(cmd)
        proc = subprocess.Popen(shlex.split(cmd), stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        LOG.info("PID of spawned create_chef.py process: %s" % proc.pid)
        self.data_set('process_id', proc.pid)
        return proc

    def check_create_complete(self, proc):
        if proc is None:
            return True
        ret_code = proc.poll()
        if ret_code is None:
            return False
        elif ret_code == 0:
            return True

        stdout, stderr = proc.communicate()
        LOG.error("Chef run failed [STDOUT]: %s" % stdout)
        LOG.error("Chef run failed [STDERR]: %s" % stderr)
        raise exception.Error("Script exited with code %s" % ret_code)

    def handle_delete(self):
        pid = self.data().get('process_id')
        if pid is None:
            return None
        try:
            proc = psutil.Process(int(pid))
        except psutil.NoSuchProcess:
            return None
        LOG.info("Killing PID %s" % pid)
        proc.terminate()
        return proc

    def check_delete_complete(self, proc):
        if proc is None:
            return True
        try:
            proc.wait(timeout=0)
        except psutil.TimeoutExpired:
            return False
        else:
            return True


def approved_mapping():
    return ('Rackspace::Cloud::ChefSolo', ChefSolo)


@deprecated(as_of=deprecated.ICEHOUSE, in_favor_of=str(approved_mapping()))
def deprecated_mapping():
    return ('OS::Heat::ChefSolo', ChefSolo)


def resource_mapping():
    approved = approved_mapping()
    deprecated = deprecated_mapping()
    return {
        approved[0]: approved[1],
        deprecated[0]: deprecated[1]
    }
