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

import json
import urlparse

from swiftclient import client as swiftclient_client

from heat.common import exception
from heat.engine import attributes
from heat.engine.clients.os import swift
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource
from heat.engine.resources import wait_condition
from heat.engine import scheduler
from heat.openstack.common.gettextutils import _
from heat.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class SwiftSignalFailure(wait_condition.WaitConditionFailure):
    pass


class SwiftSignalTimeout(wait_condition.WaitConditionTimeout):
    pass


class SwiftSignalHandle(resource.Resource):

    properties_schema = {}

    ATTRIBUTES = (
        TOKEN,
        ENDPOINT,
        CURL_CLI,
    ) = (
        'token',
        'endpoint',
        'curl_cli',
    )

    attributes_schema = {
        TOKEN: attributes.Schema(
            _('Tokens are not needed for Swift TempURLs.  This attribute is '
              'being kept for compatibility with the '
              'OS::Heat::WaitConditionHandle resource'),
            cache_mode=attributes.Schema.CACHE_NONE
        ),
        ENDPOINT: attributes.Schema(
            _('Endpoint/url which can be used for signalling handle'),
            cache_mode=attributes.Schema.CACHE_NONE
        ),
        CURL_CLI: attributes.Schema(
            _('Convenience attribute, provides curl CLI command '
              'which can be used for signalling handle completion'),
            cache_mode=attributes.Schema.CACHE_NONE
        ),
    }

    WAIT_STATUSES = (
        STATUS_FAILURE,
        STATUS_SUCCESS,
    ) = (
        'FAILURE',
        'SUCCESS',
    )

    METADATA_KEYS = (
        DATA, REASON, STATUS, UNIQUE_ID
    ) = (
        'data', 'reason', 'status', 'id'
    )

    def handle_create(self):
        url = self.client_plugin('swift')._get_signal_url(self.stack, self.name)
        self.data_set('endpoint', url)
        self.resource_id_set(url)

    def get_signals(self):
        try:
            container = self.swift().get_container(self.stack.id)
        except swiftclient_client.ClientException as exc:
            if exc.http_status == 404:  # Swift container was deleted by user
                return None
            raise exc

        index = container[1]
        if not index:  # Swift objects were deleted by user
            return None

        # Remove objects in that are for other handle resources, since
        # multiple SwiftSignalHandle resources in the same stack share
        # a container
        obj_name = "%s-%s" % (self.stack.name, self.name)
        filtered = [obj for obj in index if obj_name in obj['name']]

        # Fetch objects from Swift and filter results
        obj_bodies = []
        for obj in filtered:
            try:
                signal = self.swift().get_object(self.stack.id, obj['name'])
            except swiftclient_client.ClientException as exc:
                if exc.http_status == 404:  # Swift object disappeared
                    continue
                raise exc

            body = signal[1]
            if body == swift.IN_PROGRESS:  # Ignore the initial object
                continue
            if body == "":
                obj_bodies.append({})
                continue
            try:
                obj_bodies.append(json.loads(body))
            except ValueError:
                raise exception.Error(_("Failed to parse JSON data: %s") %
                                      body)

        # Set default values on each signal
        signals = []
        signal_num = 1
        for signal in obj_bodies:

            # Remove previous signals with the same ID
            id = self.UNIQUE_ID
            ids = [s.get(id) for s in signals if id in s]
            if ids and id in signal and ids.count(signal[id]) > 0:
                [signals.remove(s) for s in signals if s.get(id) == signal[id]]

            # Make sure all fields are set, since all are optional
            signal.setdefault(self.DATA, None)
            unique_id = signal.setdefault(self.UNIQUE_ID, signal_num)
            reason = 'Signal %s recieved' % unique_id
            signal.setdefault(self.REASON, reason)
            signal.setdefault(self.STATUS, self.STATUS_SUCCESS)

            signals.append(signal)
            signal_num += 1

        return signals

    def get_status(self):
        return [s[self.STATUS] for s in self.get_signals()]

    def get_status_reason(self, status):
        return [s[self.REASON]
                for s in self.get_signals()
                if s[self.STATUS] == status]

    def get_data(self):
        signals = self.get_signals()
        if not signals:
            return None
        data = {}
        for signal in signals:
            data[signal[self.UNIQUE_ID]] = signal[self.DATA]
        return data

    def update(self, after, before=None, prev_resource=None):
        raise resource.UpdateReplace(self.name)

    def _resolve_attribute(self, key):
        if self.resource_id:
            if key == self.TOKEN:
                return ''  # HeatWaitConditionHandle compatibility
            elif key == self.ENDPOINT:
                return self.data().get('endpoint')
            elif key == self.CURL_CLI:
                return ('curl -i -X PUT \'%s\'' % self.data().get('endpoint'))


class SwiftSignal(resource.Resource):

    PROPERTIES = (HANDLE, TIMEOUT, COUNT,) = ('handle', 'timeout', 'count',)

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
                          'is reached, creation of the wait condition '
                          'resource will fail.'),
            required=True,
            constraints=[
                constraints.Range(1, 43200),
            ]
        ),
        COUNT: properties.Schema(
            properties.Schema.NUMBER,
            description=_('The number of success signals that must be '
                          'received before the stack creation process '
                          'continues.'),
            default=1,
            constraints=[
                constraints.Range(1, 1000),
            ]
        )
    }

    ATTRIBUTES = (DATA) = 'data'

    attributes_schema = {
        DATA: attributes.Schema(
            _('JSON data that was uploaded via the SwiftSignalHandle.')
        )
    }

    def __init__(self, name, json_snippet, stack):
        super(SwiftSignal, self).__init__(name, json_snippet, stack)
        self._obj_name = None
        self._url = None

    @property
    def url(self):
        if not self._url:
            self._url = urlparse.urlparse(self.properties[self.HANDLE])
        return self._url

    @property
    def obj_name(self):
        if not self._obj_name:
            self._obj_name = self.url.path.split('/')[4]
        return self._obj_name

    def _validate_handle_url(self):
        parts = self.url.path.split('/')
        msg = _('"%(url)s" is not a valid SwiftSignalHandle.  The %(part)s '
                'is invalid')
        if not self.client_plugin('swift').valid_temp_url_path(self.url.path):
            raise ValueError(msg % {'url': self.url.path,
                                    'part': 'Swift TempURL path'})
        if not parts[2].endswith(self.context.tenant_id):
            raise ValueError(msg % {'url': self.url.path,
                                    'part': 'tenant'})
        if not parts[3] == self.stack.id:
            raise ValueError(msg % {'url': self.url.path,
                                    'part': 'container name'})

    def handle_create(self):
        self._validate_handle_url()
        runner = scheduler.TaskRunner(self._wait, self._get_handle_resource())
        runner.start(timeout=float(self.properties.get(self.TIMEOUT)))
        return runner

    def _wait(self, handle):
        while True:
            try:
                yield
            except scheduler.Timeout:
                count = self.properties.get(self.COUNT)
                raise SwiftSignalTimeout(self, handle)

            count = self.properties.get(self.COUNT)
            statuses = handle.get_status()
            if not statuses:
                continue

            for status in statuses:
                if status == handle.STATUS_FAILURE:
                    failure = SwiftSignalFailure(self, handle)
                    LOG.info(_('%(name)s Failed (%(failure)s)')
                             % {'name': str(self), 'failure': str(failure)})
                    raise failure
                elif status != handle.STATUS_SUCCESS:
                    raise exception.Error(_("Unknown status: %s") % status)

            if len(statuses) >= count:
                LOG.info(_("%s Succeeded") % str(self))
                return

    def _get_handle_resource(self):
        resource_name = self.obj_name.split('-')[1]
        if resource_name in self.stack.resources:
            return self.stack.resources[resource_name]

    def check_create_complete(self, runner):
        return runner.step()

    def _resolve_attribute(self, key):
        handle = self._get_handle_resource()
        if key == self.DATA:
            return unicode(json.dumps(handle.get_data()))


def resource_mapping():
    return {'OS::Heat::SwiftSignal': SwiftSignal,
            'OS::Heat::SwiftSignalHandle': SwiftSignalHandle}


def available_resource_mapping():
    return resource_mapping()
