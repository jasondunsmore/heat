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

import hashlib
import hmac

from swiftclient import client as sc

from heat.engine.clients import client_plugin
from heat.openstack.common.gettextutils import _


class SwiftClientPlugin(client_plugin.ClientPlugin):

    def _create(self):

        con = self.context
        endpoint_type = self._get_client_option('swift', 'endpoint_type')
        args = {
            'auth_version': '2.0',
            'tenant_name': con.tenant,
            'user': con.username,
            'key': None,
            'authurl': None,
            'preauthtoken': self.auth_token,
            'preauthurl': self.url_for(service_type='object-store',
                                       endpoint_type=endpoint_type),
            'os_options': {'endpoint_type': endpoint_type},
            'cacert': self._get_client_option('swift', 'ca_file'),
            'insecure': self._get_client_option('swift', 'insecure')
        }
        return sc.Connection(**args)

    def valid_temp_url_path(self, path):
        '''Return True if path is a valid Swift TempURL path, False otherwise.

        A Swift TempURL path must:
        - Be five parts, ['', 'v1', 'account', 'container', 'object']
        - Be a v1 request
        - Have account value that starts with "AUTH_"
        - Have container and object values
        - Have an object value with more than just '/'s

        :param path: The TempURL path
        :type path: string
        '''
        parts = path.split('/', 4)
        return bool(len(parts) == 5 and
                    not parts[0] and
                    parts[1] == 'v1' and
                    parts[2] and
                    parts[3] and
                    parts[4].strip('/'))


    def generate_temp_url(self, method, expires, path, key):
        '''Generate a Swift TempURL

        :param method: The HTTP method allowed with the TempURL
        :type method: string
        :param expires: The Unix timestamp indicating when the TempURL expires
        :type expires: integer
        :param path: The TempURL path
        :type path: string
        :param key: A secret key that will be used to generate the signature
        :type key: string
        '''
        expires = int(expires)

        if expires < 1:
            raise ValueError(_("'expires' must be a positive value"))

        if not valid_temp_url_path(path):
            raise ValueError(_("'%s' does not refer to an object "
                               "(e.g. /v1/account/container/object)") % path)

        sig = hmac.new(key, '%s\n%s\n%s' % (method, expires, path),
                       hashlib.sha1).hexdigest()
        return '%s?temp_url_sig=%s&temp_url_expires=%s' % (path, sig, expires)
