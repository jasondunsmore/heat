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

from heat.engine.resources import swift_utils
from heat.tests.common import HeatTestCase


class SwiftUtilsTests(HeatTestCase):

    def test_valid_temp_url_path(self):
        valids = [
            "/v1/AUTH_demo/c/o",
            "/v1/AUTH_demo/c/o/",
            "/v1/TEST_demo/c/o",
            "/v1/AUTH_demo/c/pseudo_folder/o",
        ]
        for url in valids:
            self.assertTrue(swift_utils.valid_temp_url_path(url))

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
