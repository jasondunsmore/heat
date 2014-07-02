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

import six
from testtools.matchers import MatchesRegex

from heat.engine.clients.os import swift
from heat.tests.common import HeatTestCase
from heat.tests import utils


class SwiftClientPluginTests(HeatTestCase):
    def setUp(self):
        super(SwiftClientPluginTests, self).setUp()
        con = utils.dummy_context()

        import ipdb; ipdb.set_trace()
        c = con.clients
        self.nova_plugin = c.client_plugin('swift')
        self.swift = swift.SwiftClientPlugin('swift')

    def test_valid_temp_url_path(self):
        valids = [
            "/v1/AUTH_demo/c/o",
            "/v1/AUTH_demo/c/o/",
            "/v1/TEST_demo/c/o",
            "/v1/AUTH_demo/c/pseudo_folder/o",
        ]
        for url in valids:
            self.assertTrue(self.swift.valid_temp_url_path(url))

        invalids = [
            "/v2/AUTH_demo/c/o",
            "/v1/AUTH_demo/c//",
            "/v1/AUTH_demo/c/",
            "/AUTH_demo/c//",
            "//AUTH_demo/c/o",
            "//v1/AUTH_demo/c/o",
            "/v1/AUTH_demo/o",
            "/v1/AUTH_demo//o",
            "/v1//c/o",
            "/v1/c/o",
        ]
        for url in invalids:
            self.assertFalse(swift_utils.valid_temp_url_path(url))

    def test_generate_temp_url(self):
        tempurl = swift_utils.generate_temp_url("PUT", 1404325431,
                                                "/v1/AUTH_demo/c/o", "1" * 32)
        regexp = ("/v1/AUTH_demo/c/o\?temp_url_sig=[0-9a-f]{40}&"
                  "temp_url_expires=1404325431")
        self.assertThat(tempurl, MatchesRegex(regexp))

    def test_generate_temp_url_expires_negative_value(self):
        exc = self.assertRaises(ValueError, swift_utils.generate_temp_url,
                                "PUT", -1404325431, "/v1/AUTH_demo/c/o",
                                "1" * 32)
        self.assertEqual("'expires' must be a positive value",
                         six.text_type(exc))

    def test_generate_temp_url_invalid_path(self):
        exc = self.assertRaises(ValueError, swift_utils.generate_temp_url,
                                "PUT", 1404325431, "/v2/AUTH_demo/c/o",
                                "1" * 32)
        self.assertEqual("'/v2/AUTH_demo/c/o' does not refer to an object "
                         "(e.g. /v1/account/container/object)",
                         six.text_type(exc))
