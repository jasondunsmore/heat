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
import time

from heat.openstack.common.gettextutils import _


def valid_temp_url_path(path):
    '''Return True if path is a valid Swift TempURL path.

    A Swift TempURL path must:
    - Be five parts, ['', 'v1', 'account', 'container', 'object']
    - Be a v1 request
    - Have account value that starts with "AUTH_"
    - Have container and object values
    - Have an object value with more than just '/'s
    '''
    parts = path.split('/', 4)
    return bool(len(parts) == 5 and
                not parts[0] and
                parts[1] == 'v1' and
                parts[2].startswith('AUTH_') and
                parts[3] and
                parts[4].strip('/'))


def generate_temp_url(method, seconds, path, key):
    '''Generate a Swift TempURL'''
    try:
        expires = int(time.time() + int(seconds))
    except ValueError:
        expires = 0
    if expires < 1:
        raise ValueError(_("'seconds' must be a positive value"))

    if not valid_temp_url_path(path):
        raise ValueError(_('"%s" does not refer to an object '
                           '(e.g. /v1/account/container/object)') % path)

    sig = hmac.new(key, '%s\n%s\n%s' % (method, expires, path),
                   hashlib.sha1).hexdigest()
    return '%s?temp_url_sig=%s&temp_url_expires=%s' % (path, sig, expires)
