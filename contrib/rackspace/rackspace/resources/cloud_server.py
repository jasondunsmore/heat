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

from heat.common import exception
from heat.engine.resources import nova_utils
from heat.engine.resources import server
from heat.openstack.common.gettextutils import _
from heat.openstack.common import log as logging

try:
    import pyrax  # noqa
    PYRAX_INSTALLED = True
except ImportError:
    PYRAX_INSTALLED = False

logger = logging.getLogger(__name__)


class CloudServer(server.Server):
    """Resource for Rackspace Cloud Servers."""

    # Managed Cloud automation statuses
    MC_STATUS_IN_PROGRESS = 'In Progress'
    MC_STATUS_COMPLETE = 'Complete'
    MC_STATUS_BUILD_ERROR = 'Build Error'

    # RackConnect automation statuses
    RC_STATUS_DEPLOYING = 'DEPLOYING'
    RC_STATUS_DEPLOYED = 'DEPLOYED'
    RC_STATUS_FAILED = 'FAILED'
    RC_STATUS_UNPROCESSABLE = 'UNPROCESSABLE'

    attributes_schema = copy.deepcopy(server.Server.attributes_schema)
    attributes_schema.update(
        {
            'distro': _('The Linux distribution on the server.'),
            'privateIPv4': _('The private IPv4 address of the server.'),
        }
    )

    def __init__(self, name, json_snippet, stack):
        super(CloudServer, self).__init__(name, json_snippet, stack)
        self._server = None
        self._distro = None
        self._image = None
        self._managed_cloud_started_event_sent = False
        self._rack_connect_started_event_sent = False

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
            self._distro = image_data.metadata['os_distro']
        return self._distro

    @property
    def image(self):
        """Return the server's image ID."""
        image = self.properties.get(self.IMAGE)
        if image and self._image is None:
            self._image = nova_utils.get_image_id(self.nova(), image)
        return self._image

    def _config_drive(self):
        return True

    def _check_managed_cloud_complete(self, server):
        if not self._managed_cloud_started_event_sent:
            msg = _("Waiting for Managed Cloud automation to complete")
            self._add_event(self.action, self.status, msg)
            self._managed_cloud_started_event_sent = True

        if 'rax_service_level_automation' not in server.metadata:
            logger.debug(_("Managed Cloud server does not have the "
                           "rax_service_level_automation metadata tag yet"))
            return False

        mc_status = server.metadata['rax_service_level_automation']
        logger.debug(_("Managed Cloud automation status: %s") % mc_status)

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
            logger.debug(_("RackConnect server does not have the "
                           "rackconnect_automation_status metadata tag yet"))
            return False

        rc_status = server.metadata['rackconnect_automation_status']
        logger.debug(_("RackConnect automation status: %s") % rc_status)

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
                logger.warning(_("RackConnect unprocessable reason: %s") %
                               reason)

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
        if not self._check_active(server):
            return False

        nova_utils.refresh_server(server)

        if 'rack_connect' in self.context.roles and not \
           self._check_rack_connect_complete(server):
            return False

        if 'rax_managed' in self.context.roles and not \
           self._check_managed_cloud_complete(server):
            return False

        return True

    def _resolve_attribute(self, name):
        if name == 'distro':
            return self.distro
        if name == 'privateIPv4':
            return nova_utils.get_ip(self.server, 'private', 4)
        return super(CloudServer, self)._resolve_attribute(name)

    def FnGetRefId(self):
        return self.resource_id


def resource_mapping():
    return {'Rackspace::Cloud::Server': CloudServer}


def available_resource_mapping():
    if PYRAX_INSTALLED:
        return resource_mapping()
    return {}
