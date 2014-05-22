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
import random
import time
import urlparse

from heat.common import exception
from heat.engine import clients
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource
from heat.openstack.common.gettextutils import _
from heat.openstack.common import log as logging
from heat.openstack.common import uuidutils

LOG = logging.getLogger(__name__)


class SwiftSignalHandle(resource.Resource):

    PROPERTIES = (TIMEOUT,) = ('timeout',)

    properties_schema = {
        TIMEOUT: properties.Schema(
            properties.Schema.NUMBER,
            required=True,
            description=_('The number of seconds that the TempURL will be '
                          'valid for.')
            )
        }

    def handle_create(self):
        # Generate the Swift TempURL and store it as the resource ID
        method = 'GET'
        seconds = self.properties.get(self.TIMEOUT)
        expires = int(time.time() + seconds)
        container = 'heat-swiftsignal-%s' % uuidutils.uuid.uuid4()
        path = '/v1/%s/%s/object' % (self.context.tenant_id, container)

        if 'x-account-meta-temp-url-key' in self.swift().head_account():
            key = self.swift().head_account()['x-account-meta-temp-url-key']
        else:
            key = hashlib.sha224(str(random.getrandbits(256))).hexdigest()
            self.swift().post_account({'x-account-meta-temp-url-key': key})

        hmac_body = '%s\n%s\n%s' % (method, expires, path)
        sig = hmac.new(key, hmac_body, hashlib.sha1).hexdigest()

        uri = '%s?temp_url_sig=%s&temp_url_expires=%s' % (path, sig, expires)
        sw_url = urlparse.urlparse(self.swift().url)
        url = '%s://%s/%s' % (sw_url.scheme, sw_url.netloc, uri)

        self.resource_id_set(url)

    def FnGetRefId(self):
        return self.resource_id if self.resource_id else self.name


class SwiftSignal(resource.Resource):

    PROPERTIES = (HANDLE, TIMEOUT,) = ('handle', 'timeout',)

    properties_schema = {
        HANDLE: properties.Schema(
            properties.Schema.STRING,
            required=True,
            description=_('URL of TempURL where resource will signal '
                          'completion and optionally upload data.')
        ),
        TIMEOUT: properties.Schema(
            properties.Schema.NUMBER,
            required=True,
            description=_('The number of seconds to wait for the resource to '
                          'signal completion.')
        )
    }

    def _validate_handle_url(self):
        pass

    #def handle_create(self):
    #    pass

    def check_create_complete(self):
        import ipdb; ipdb.set_trace()
        self.swift()


def resource_mapping():
    return {'OS::Heat::SwiftSignal': SwiftSignal,
            'OS::Heat::SwiftSignalHandle': SwiftSignalHandle}

def available_resource_mapping():
    return resource_mapping()
