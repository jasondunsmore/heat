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
import random
import re
import time
import urlparse

from heat.common import exception
from heat.common import identifier
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource
from heat.engine.resources import swift_utils
from heat.openstack.common.gettextutils import _
from heat.openstack.common import log as logging
from heat.openstack.common import uuidutils

LOG = logging.getLogger(__name__)

IN_PROGRESS = 'in progress'


class SwiftSignalHandle(resource.Resource):

    PROPERTIES = (TIMEOUT,) = ('timeout',)

    properties_schema = {
        TIMEOUT: properties.Schema(
            properties.Schema.NUMBER,
            description=_('The number of seconds that the TempURL will be '
                          'valid for.'),
            required=True,
            constraints=[
                constraints.Range(1, 43200),
            ]
        )
    }

    def handle_create(self):
        method = 'PUT'
        seconds = self.properties.get(self.TIMEOUT)
        container_name = 'heat-%s' % uuidutils.uuid.uuid4()
        obj_name = uuidutils.uuid.uuid4()
        path = '/v1/AUTH_%s/%s/%s' % (self.context.tenant_id, container_name,
                                      obj_name)

        self.swift().put_container(container_name)
        self.swift().put_object(container_name, obj_name, IN_PROGRESS)

        if 'x-account-meta-temp-url-key' in self.swift().head_account():
            key = self.swift().head_account()['x-account-meta-temp-url-key']
        else:
            key = hashlib.sha224(str(random.getrandbits(256))).hexdigest()[:32]
            self.swift().post_account({'x-account-meta-temp-url-key': key})

        path = swift_utils.generate_temp_url(method, seconds, path, key)
        sw_url = urlparse.urlparse(self.swift().url)
        tempurl = '%s://%s%s' % (sw_url.scheme, sw_url.netloc, path)

        self.resource_id_set(tempurl)

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
            description=_('The maximum number of seconds to wait for the '
                          'resource to signal completion.  Once the timeout '
                          'is reached, the wait condition will ...'),
            required=True,
            constraints=[
                constraints.Range(1, 43200),
            ]
        )
    }

    def __init__(self, name, json_snippet, stack):
        super(SwiftSignal, self).__init__(name, json_snippet, stack)
        self.timeout_time = None
        self.container_name = None
        self.obj_name = None

    def _validate_handle_url(self, url):
        parts = url.path.split('/')
        uuid_re = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        if (not swift_utils.valid_temp_url_path(url.path) or
                not parts[2].endswith(self.context.tenant_id) or
                not re.match('heat-' + uuid_re, parts[3]) or
                not re.match(uuid_re, parts[4])):
            raise ValueError(_('"%s" is not a valid SwiftSignalHandle') %
                             url.path)

    def handle_create(self):
        handle = self.properties[self.HANDLE]
        url = urlparse.urlparse(handle)
        self._validate_handle_url(url)

        self.container_name, self.obj_name = url.path.split('/')[3:]
        seconds = self.properties.get(self.TIMEOUT)
        self.timeout_time = time.time() + seconds

    def check_create_complete(self, signal):
        obj_head, obj_body = self.swift().get_object(self.container_name,
                                                     self.obj_name)
        timed_out = time.time() > self.timeout_time

        if obj_body == IN_PROGRESS and not timed_out:
            return False

        self.swift().delete_object(self.container_name, self.obj_name)
        self.swift().delete_container(self.container_name)

        if timed_out:
            raise exception.Error(_('SwiftSignal wait condition timed out '
                                    'while waiting for completion signal'))

        # TODO(jason): Need to support multiple signals the way
        # AWS::CloudFormation::WaitCondition does?
        return True


def resource_mapping():
    return {'OS::Heat::SwiftSignal': SwiftSignal,
            'OS::Heat::SwiftSignalHandle': SwiftSignalHandle}


def available_resource_mapping():
    return resource_mapping()
