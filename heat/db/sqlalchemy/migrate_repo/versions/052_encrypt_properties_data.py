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

from migrate.versioning import util as migrate_util
from sqlalchemy import orm

from oslo.config import cfg
from oslo.utils import encodeutils

from heat.common import crypt
from heat.common.i18n import _
from heat.db.sqlalchemy import models


def upgrade(migrate_engine):

    if not cfg.CONF.encrypt_parameters_and_properties:
        return

    Session = orm.sessionmaker(bind=migrate_engine)
    session = Session()
    resources = session.query(models.Resource).all()

    for resource in resources:
        for prop_name, prop_value in resource.properties_data.items():
            encoded_value = encodeutils.safe_encode(prop_value)
            resource.properties_data[prop_name] = crypt.encrypt(encoded_value)
        session.commit()
    session.close()

def downgrade(migrate_engine):

    Session = orm.sessionmaker(bind=migrate_engine)
    session = Session()
    resources = session.query(models.Resource).all()

    for resource in resources:
        for prop_name, prop_value in resource.properties_data.items():
            decrypt_function_name = prop_value[0]
            decrypt_function = getattr(crypt, decrypt_function_name, None)
            msg = _('Decrypting %(resource)s property data: %(prop)s') % {
                'resource': resource.name, 'prop': prop_name}
            migrate_util.log.info(msg)
            decrypted_val = decrypt_function(prop_value[1])
            decoded_val = encodeutils.safe_decode(decrypted_val)
            resource.properties_data[prop_name] = decoded_val
        session.commit()
    session.close()
