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

from oslo_log import log as logging
from oslo.config import cfg

from heat.common.i18n import _LE

LOG = logging.getLogger(__name__)

try:
    from zaqarclient.queues.v1 import client as zaqarclient
    from zaqarclient.transport import errors as zaqar_errors
except ImportError:
    zaqarclient = None
    zaqar_errors = None

from heat.engine.clients import client_plugin


class ZaqarClientPlugin(client_plugin.ClientPlugin):

    exception_module = zaqar_errors

    def _create(self):

        con = self.context
        if self.auth_token is None:
            LOG.error(_LE("Zaqar connection failed, no auth_token!"))
            return None

        opts = {
            'os_auth_token': con.auth_token,
            'os_auth_url': con.auth_url,
            'os_project_id': con.tenant,
            'os_service_type': 'messaging',
        }
        auth_opts = {'backend': 'keystone',
                     'options': opts}
        conf = {'auth_opts': auth_opts}
        endpoint = self.url_for(service_type='rax:queues',
                                region_name=cfg.CONF.region_name_for_services)
        
        endpoint = endpoint.rsplit('v1')[0]

        client = zaqarclient.Client(url=endpoint, conf=conf)

        return client

    def is_not_found(self, ex):
        return isinstance(ex, zaqar_errors.ResourceNotFound)
