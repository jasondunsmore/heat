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

import copy
import os
import psutil
import shlex
import subprocess
import tempfile

from Crypto.PublicKey import RSA

from oslo_config import cfg

from oslo_log import log as logging

from heat.common import exception
from heat.common.i18n import _
from heat.common.i18n import _LW
from heat.engine import attributes
from heat.engine import properties
from heat.engine.resources.openstack.nova import server
from heat.engine import support


try:
    import pyrax  # noqa
    PYRAX_INSTALLED = True
except ImportError:
    PYRAX_INSTALLED = False

LOG = logging.getLogger(__name__)


class CloudServer(server.Server):
    """Resource for Rackspace Cloud Servers."""

    support_status = support.SupportStatus(
        support.DEPRECATED,
        _('Use OS::Nova::Server instead.'),
    )

    SCRIPT_INSTALL_REQUIREMENTS = {
        'ubuntu': """
apt-get update
export DEBIAN_FRONTEND=noninteractive
apt-get install -y -o Dpkg::Options::="--force-confdef" -o \
  Dpkg::Options::="--force-confold" python-boto python-pip gcc python-dev
pip install pbr==0.5.21
pip install heat-cfntools
cfn-create-aws-symlinks --source /usr/local/bin
""",
        ('fedora', '21'): """
yum install -y python-boto python-pip gcc python-devel
pip install pbr==0.5.21
pip install heat-cfntools
cfn-create-aws-symlinks
""",
        'fedora': """
yum install -y python-boto python-pip gcc python-devel
pip-python install pbr==0.5.21
pip-python install heat-cfntools
cfn-create-aws-symlinks
""" ,
        'centos': """
if ! (yum repolist 2> /dev/null | egrep -q "^[\!\*]?epel ");
then
 rpm -ivh http://mirror.rackspace.com/epel/6/i386/epel-release-6-8.noarch.rpm
fi
yum install -y python-boto python-pip gcc python-devel python-argparse
pip-python install pbr==0.5.21
pip-python install heat-cfntools
""",
        ('centos', '7'): """
yum install -y python-boto python-pip gcc python-devel python-argparse
pip install pbr==0.5.21
pip install heat-cfntools
""",
        'rhel': """
if ! (yum repolist 2> /dev/null | egrep -q "^[\!\*]?epel ");
then
 rpm -ivh http://mirror.rackspace.com/epel/6/i386/epel-release-6-8.noarch.rpm
fi
# The RPM DB stays locked for a few secs
while fuser /var/lib/rpm/*; do sleep 1; done
yum install -y python-boto python-pip gcc python-devel python-argparse
pip-python install pbr==0.5.21
pip-python install heat-cfntools
cfn-create-aws-symlinks
""",
        ('rhel', '7'): """
yum install -y python-boto python-pip gcc python-devel python-argparse
pip install pbr==0.5.21
pip install heat-cfntools
cfn-create-aws-symlinks
""",
        'debian': """
echo "deb http://mirror.rackspace.com/debian wheezy-backports main" >> \
  /etc/apt/sources.list
apt-get update
apt-get -t wheezy-backports install -y cloud-init
export DEBIAN_FRONTEND=noninteractive
apt-get install -y -o Dpkg::Options::="--force-confdef" -o \
  Dpkg::Options::="--force-confold" python-pip gcc python-dev
pip install pbr==0.5.21
pip install heat-cfntools
"""}

    SCRIPT_CREATE_DATA_SOURCE = """
sed -i 's/ConfigDrive/NoCloud/' /etc/cloud/cloud.cfg.d/*
rm -rf /var/lib/cloud
mkdir -p /var/lib/cloud/seed/nocloud-net
mv /tmp/userdata /var/lib/cloud/seed/nocloud-net/user-data
touch /var/lib/cloud/seed/nocloud-net/meta-data
chmod 600 /var/lib/cloud/seed/nocloud-net/*
"""

    SCRIPT_RUN_CLOUD_INIT = """
cloud-init start || cloud-init init
"""

    SCRIPT_RUN_CFN_USERDATA = """
bash -x /var/lib/cloud/data/cfn-userdata > /root/cfn-userdata.log 2>&1 ||
  exit 42
"""

    # Managed Cloud automation statuses
    MC_STATUS_IN_PROGRESS = 'In Progress'
    MC_STATUS_COMPLETE = 'Complete'
    MC_STATUS_BUILD_ERROR = 'Build Error'

    # RackConnect automation statuses
    RC_STATUS_DEPLOYING = 'DEPLOYING'
    RC_STATUS_DEPLOYED = 'DEPLOYED'
    RC_STATUS_FAILED = 'FAILED'
    RC_STATUS_UNPROCESSABLE = 'UNPROCESSABLE'

    # Admin Pass Properties
    SAVE_ADMIN_PASS = 'save_admin_pass'

    properties_schema = copy.deepcopy(server.Server.properties_schema)
    properties_schema.update(
        {
            SAVE_ADMIN_PASS: properties.Schema(
                properties.Schema.BOOLEAN,
                _('True if the system should remember the admin password; '
                  'False otherwise.'),
                default=False
            ),
        }
    )

    NEW_ATTRIBUTES = (
        DISTRO, PRIVATE_IP_V4, ADMIN_PASS_ATTR,
    ) = (
        'distro', 'privateIPv4', 'admin_pass',
    )

    ATTRIBUTES = copy.deepcopy(server.Server.ATTRIBUTES)
    ATTRIBUTES += NEW_ATTRIBUTES

    attributes_schema = copy.deepcopy(server.Server.attributes_schema)
    attributes_schema.update(
        {
            DISTRO: attributes.Schema(
                _('The Linux distribution on the server.')
            ),
            PRIVATE_IP_V4: attributes.Schema(
                _('The private IPv4 address of the server.')
            ),
            ADMIN_PASS_ATTR: attributes.Schema(
                _('The administrator password for the server.'),
                cache_mode=attributes.Schema.CACHE_NONE
            ),
        }
    )

    def __init__(self, name, json_snippet, stack):
        super(CloudServer, self).__init__(name, json_snippet, stack)
        self.stack = stack
        self._server = None
        self._distro = None
        self._image = None
        self._retry_iterations = 0
        self._managed_cloud_started_event_sent = False
        self._rack_connect_started_event_sent = False
        self._proc = None

    @property
    def server(self):
        """Return the Cloud Server object."""
        if self._server is None:
            self._server = self.nova().servers.get(self.resource_id)
        return self._server

    @property
    def distro(self):
        """Return the Linux distribution for this server."""
        image = self.properties.get(self.IMAGE)
        if self._distro is None and image:
            image_data = self.nova().images.get(self.image)
            dis = 'unknown'
            ver = 'default'
            if 'os_distro' in image_data.metadata:
                dis = image_data.metadata['os_distro']
            if "org.openstack__1__os_version" in image_data.metadata:
                ver = image_data.metadata["org.openstack__1__os_version"]
            self._distro = (dis, ver)
        return self._distro

    @property
    def script(self):
        """
        Return the config script for the Cloud Server image.

        The config script performs the following steps:
        1) Install cloud-init
        2) Create cloud-init data source
        3) Run cloud-init
        4) If user_data_format is 'HEAT_CFNTOOLS', run cfn-userdata script
        """
        baseinstall = (self.SCRIPT_INSTALL_REQUIREMENTS.get(self.distro) or
                       self.SCRIPT_INSTALL_REQUIREMENTS.get(self.distro[0]))
        if not baseinstall:
            return
        base_script = (baseinstall + self.SCRIPT_CREATE_DATA_SOURCE +
                       self.SCRIPT_RUN_CLOUD_INIT)
        userdata_format = self.properties.get(self.USER_DATA_FORMAT)
        if userdata_format == 'HEAT_CFNTOOLS':
            return base_script + self.SCRIPT_RUN_CFN_USERDATA
        elif userdata_format == 'RAW':
            return base_script

    @property
    def image(self):
        """Return the server's image ID."""
        image = self.properties.get(self.IMAGE)
        if image and self._image is None:
            self._image = self.client_plugin('glance').get_image_id(image)
        return self._image

    @property
    def private_key(self):
        """Return the private SSH key for the resource."""
        return self.data().get('private_key')

    @private_key.setter
    def private_key(self, private_key):
        """Save the resource's private SSH key to the database."""
        if self.id is not None:
            self.data_set('private_key', private_key, True)

    @property
    def has_userdata(self):
        """Return True if the server has user_data, False otherwise."""
        user_data = self.properties.get(self.USER_DATA)
        if user_data or self.metadata_get() != {}:
            return True
        else:
            return False

    def validate(self):
        """Validate user parameters."""
        image = self.properties.get(self.IMAGE)

        # It's okay if there's no script, as long as user_data and
        # metadata are both empty
        if image and self.script is None and self.has_userdata:
            msg = _("user_data is not supported for image %s.") % image
            raise exception.StackValidationFailed(message=msg)

        # Validate that the personality does not contain a reserved
        # key and that the number of personalities does not exceed the
        # Rackspace limit.
        personality = self.properties.get(self.PERSONALITY)
        if personality:
            limits = self.client_plugin().absolute_limits()

            # One personality will be used for an SSH key
            personality_limit = limits['maxPersonality'] - 1

            if "/root/.ssh/authorized_keys" in personality:
                msg = _('The personality property may not contain a key '
                        'of "/root/.ssh/authorized_keys"')
                raise exception.StackValidationFailed(message=msg)

            elif len(personality) > personality_limit:
                msg = _("The personality property may not contain greater "
                        "than %s entries.") % personality_limit
                raise exception.StackValidationFailed(message=msg)

        super(CloudServer, self).validate()

        # Validate that user_data is passed for servers with bootable
        # volumes AFTER validating that the server has either an image
        # or a bootable volume in Server.validate()
        if not image and self.has_userdata:
            msg = _("user_data scripts are not supported with bootable "
                    "volumes.")
            raise exception.StackValidationFailed(message=msg)

    def _personality(self):
        # Generate SSH public/private keypair for the engine to use
        if self.private_key is not None:
            rsa = RSA.importKey(self.private_key)
        else:
            rsa = RSA.generate(1024)
        self.private_key = rsa.exportKey()
        public_keys = [rsa.publickey().exportKey('OpenSSH')]

        # Add the user-provided key_name to the authorized_keys file
        key_name = self.properties.get(self.KEY_NAME)
        if key_name:
            user_keypair = self.client_plugin().get_keypair(key_name)
            public_keys.append(user_keypair.public_key)
        personality = {"/root/.ssh/authorized_keys": '\n'.join(public_keys)}

        # Add any user-provided personality files
        user_personality = self.properties.get(self.PERSONALITY)
        if user_personality:
            personality.update(user_personality)

        return personality

    def _key_name(self):
        return None

    def _check_managed_cloud_complete(self, server):
        if not self._managed_cloud_started_event_sent:
            msg = _("Waiting for Managed Cloud automation to complete")
            self._add_event(self.action, self.status, msg)
            self._managed_cloud_started_event_sent = True

        if 'rax_service_level_automation' not in server.metadata:
            LOG.debug("Managed Cloud server does not have the "
                      "rax_service_level_automation metadata tag yet")
            return False

        mc_status = server.metadata['rax_service_level_automation']
        LOG.debug("Managed Cloud automation status: %s" % mc_status)

        if mc_status == self.MC_STATUS_IN_PROGRESS:
            return False

        elif mc_status == self.MC_STATUS_COMPLETE:
            msg = _("Managed Cloud automation has completed")
            self._add_event(self.action, self.status, msg)
            return True

        elif mc_status == self.MC_STATUS_BUILD_ERROR:
            raise exception.Error(_("Managed Cloud automation failed"))

        else:
            raise exception.Error(_("Unknown Managed Cloud automation "
                                    "status: %s") % mc_status)

    def _check_rack_connect_complete(self, server):
        if not self._rack_connect_started_event_sent:
            msg = _("Waiting for RackConnect automation to complete")
            self._add_event(self.action, self.status, msg)
            self._rack_connect_started_event_sent = True

        if 'rackconnect_automation_status' not in server.metadata:
            LOG.debug("RackConnect server does not have the "
                      "rackconnect_automation_status metadata tag yet")
            return False

        rc_status = server.metadata['rackconnect_automation_status']
        LOG.debug("RackConnect automation status: %s" % rc_status)

        if rc_status == self.RC_STATUS_DEPLOYING:
            return False

        elif rc_status == self.RC_STATUS_DEPLOYED:
            self._server = None  # The public IP changed, forget old one
            return True

        elif rc_status == self.RC_STATUS_UNPROCESSABLE:
            # UNPROCESSABLE means the RackConnect automation was not
            # attempted (eg. Cloud Server in a different DC than
            # dedicated gear, so RackConnect does not apply).  It is
            # okay if we do not raise an exception.
            reason = server.metadata.get('rackconnect_unprocessable_reason',
                                         None)
            if reason is not None:
                LOG.warn(_LW("RackConnect unprocessable reason: %s"), reason)

            msg = _("RackConnect automation has completed")
            self._add_event(self.action, self.status, msg)
            return True

        elif rc_status == self.RC_STATUS_FAILED:
            raise exception.Error(_("RackConnect automation FAILED"))

        else:
            msg = _("Unknown RackConnect automation status: %s") % rc_status
            raise exception.Error(msg)

    def check_create_complete(self, server):
        """Check if server creation is complete and handle server configs."""
        if self._proc:  # subprocess has already been started
            ret_cd = self._proc.poll()
            if ret_cd is None:
                return False
            elif ret_cd == 0:
                msg = _("user_data run complete")
                self._add_event(self.action, self.status, msg)
                return True

            stdout, stderr = self._proc.communicate()
            LOG.error("Server user_data run failed [STDOUT]: %s" % stdout)
            LOG.error("Server user_data run failed [STDERR]: %s" % stderr)
            raise exception.Error("User data script exited with code %s" % ret_cd)

        if not self._check_active(server):
            return False

        self.client_plugin().refresh_server(server)

        if ('rack_connect' in self.context.roles and not
                self._check_rack_connect_complete(server)):
            return False

        if ('rax_managed' in self.context.roles and not
                self._check_managed_cloud_complete(server)):
            return False

        if self.has_userdata:
            path = (os.path.dirname(os.path.realpath(__file__)) +
                    "/run_user_data.py")
            with tempfile.NamedTemporaryFile(delete=False) as key_file:
                key_file.write(self.private_key)

            raw_userdata = self.properties[self.USER_DATA]
            userdata = self.client_plugin().build_userdata(self.metadata_get(),
                                                           raw_userdata)
            with tempfile.NamedTemporaryFile(delete=False) as userdata_file:
                userdata_file.write(userdata)
            with tempfile.NamedTemporaryFile(delete=False) as script_file:
                script_file.write(self.script)

            cmd = ("nice timeout -k 5 %s "
                   "python %s "
                   "--userdata-file %s "
                   "--script-file %s "
                   "--ip %s "
                   "--key-file %s "
                   "--timeout %s "
                   "--sftp-retries %s "
                   "--jump-enabled %s "
                   "--jump-host %s "
                   "--jump-port %s "
                   "--jump-user %s "
                   "--jump-key %s" % (
                       self.stack.timeout_secs(),
                       path,
                       userdata_file.name,
                       script_file.name,
                       self.server.accessIPv4,
                       key_file.name,
                       self.stack.timeout_secs(),
                       cfg.CONF.sftp_retries,
                       cfg.CONF.ssh_jump_enabled,
                       cfg.CONF.ssh_jump_host,
                       cfg.CONF.ssh_jump_port,
                       cfg.CONF.ssh_jump_user,
                       cfg.CONF.ssh_jump_key))
            LOG.info(cmd)

            msg = _("Running user_data")
            self._add_event(self.action, self.status, msg)

            self._proc = subprocess.Popen(shlex.split(cmd),
                                          stderr=subprocess.PIPE,
                                          stdout=subprocess.PIPE)
            LOG.info("PID of spawned run_user_data.py process: %s" %
                     self._proc.pid)
            self.data_set('process_id', self._proc.pid)
            return False

        return True

    def _resolve_attribute(self, name):
        if name == self.DISTRO:
            return self.distro[0]
        if name == self.PRIVATE_IP_V4:
            return self.client_plugin().get_ip(self.server, 'private', 4)
        if name == self.ADMIN_PASS_ATTR:
            return self.data().get(self.ADMIN_PASS_ATTR, '')
        return super(CloudServer, self)._resolve_attribute(name)

    def handle_create(self):
        
        # reset values for our own purposes
        self.properties.data[self.PERSONALITY] = self._personality()
        self.properties.data[self.KEY_NAME] = None

        server = super(CloudServer, self).handle_create()

        #  Server will not have an adminPass attribute if Nova's
        #  "enable_instance_password" config option is turned off
        if (self.properties.get(self.SAVE_ADMIN_PASS) and
                hasattr(server, 'adminPass') and server.adminPass):
            self.data_set(self.ADMIN_PASS,
                          server.adminPass,
                          redact=True)

        return server

    def handle_delete(self):
        deleter = super(CloudServer, self).handle_delete()
        pid = self.data().get('process_id')
        if pid is None:
            return deleter, None
        try:
            proc = psutil.Process(int(pid))
        except psutil.NoSuchProcess:
            return deleter, None
        LOG.info("Killing PID %s" % pid)
        proc.terminate()
        return deleter, proc

    def check_delete_complete(self, token):
        deleter, proc = token

        ret_val = super(CloudServer, self).check_delete_complete(deleter)
        if not ret_val:
            return False

        if proc is None:
            return True
        try:
            proc.wait(timeout=0)
        except psutil.TimeoutExpired:
            return False
        else:
            return True


def resource_mapping():
    return {'Rackspace::Cloud::Server': CloudServer}


def available_resource_mapping():
    if PYRAX_INSTALLED:
        return resource_mapping()
    return {}
