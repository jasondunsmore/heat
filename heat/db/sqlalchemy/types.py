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
import six

from oslo_serialization import jsonutils
from sqlalchemy.dialects import mysql
from sqlalchemy import types

LOG = logging.getLogger(__name__)

dumps = jsonutils.dumps
loads = jsonutils.loads


class LongText(types.TypeDecorator):
    impl = types.Text

    def load_dialect_impl(self, dialect):
        if dialect.name == 'mysql':
            return dialect.type_descriptor(mysql.LONGTEXT())
        else:
            return self.impl


class Json(LongText):

    def process_bind_param(self, value, dialect):
        try:
            return dumps(value)
        except ValueError:
            val = {key: six.text_type(value[key]) for key in value.keys()}

            # Debugging a gate failure (unable to reproduce failure locally)
            if "Circular reference detected" in val.values():
                import pprint
                print "Debugging process_bind_param()"
                pprint.pprint(value)
                pprint.pprint(val)
                pprint.pprint(dumps(val))

            return dumps(val)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return loads(value)


class List(types.TypeDecorator):
    impl = types.Text

    def load_dialect_impl(self, dialect):
        if dialect.name == 'mysql':
            return dialect.type_descriptor(mysql.LONGTEXT())
        else:
            return self.impl

    def process_bind_param(self, value, dialect):
        return dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return loads(value)
