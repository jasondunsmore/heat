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

import base64

from Crypto.Cipher import AES
from oslo_config import cfg

from heat.common.i18n import _
from heat.openstack.common.crypto import utils


auth_opts = [
    cfg.StrOpt('auth_encryption_key',
               default='notgood but just long enough i t',
               help=_('Encryption key used for authentication '
                      'info in database. Length of this key '
                      'must be 16, 24 or 32'))
]

cfg.CONF.register_opts(auth_opts)


def encrypt(auth_info, encryption_key=None):
    if auth_info is None:
        return None, None

    encryption_key = get_valid_encryption_key(encryption_key)
    sym = utils.SymmetricCrypto()
    res = sym.encrypt(encryption_key,
                      auth_info, b64encode=True)
    return 'oslo_decrypt_v1', res


def oslo_decrypt_v1(auth_info, encryption_key=None):
    if auth_info is None:
        return None

    encryption_key = get_valid_encryption_key(encryption_key)
    sym = utils.SymmetricCrypto()
    return sym.decrypt(encryption_key,
                       auth_info, b64decode=True)


def get_valid_encryption_key(encryption_key):
    if encryption_key is None:
        encryption_key = cfg.CONF.auth_encryption_key[:32]
    else:
        encryption_key = encryption_key[0:32]
    return encryption_key


def heat_decrypt(auth_info, encryption_key=None):
    """Decrypt function for data that has been encrypted using an older
    version of Heat.
    Note: the encrypt function returns the function that is needed to
    decrypt the data. The database then stores this. When the data is
    then retrieved (potentially by a later version of Heat) the decrypt
    function must still exist. So whilst it may seem that this function
    is not referenced, it will be referenced from the database.
    """
    if auth_info is None:
        return None

    encryption_key = get_valid_encryption_key(encryption_key)
    auth = base64.b64decode(auth_info)
    iv = auth[:AES.block_size]
    cipher = AES.new(encryption_key, AES.MODE_CFB, iv)
    res = cipher.decrypt(auth[AES.block_size:])
    return res


def list_opts():
    yield None, auth_opts
