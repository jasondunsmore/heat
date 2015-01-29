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

from heat.common import crypt
from heat.common.i18n import _
from heat.db.sqlalchemy import models
from heat.engine import template

from migrate.versioning import util as migrate_util
from oslo.config import cfg
from oslo.utils import encodeutils
from sqlalchemy import orm


def upgrade(migrate_engine):

    if not cfg.CONF.encrypt_parameters_and_properties:
        return

    Session = orm.sessionmaker(bind=migrate_engine)
    session = Session()
    raw_templates = session.query(models.RawTemplate).all()

    for raw_template in raw_templates:
        tmpl = template.Template.load(None, raw_template.id, raw_template)

        encrypted_params = []
        for param_name, param in tmpl.param_schemata().items():
            if (param_name in encrypted_params) or (not param.hidden):
                continue

            msg = _('Encrypting raw template %(id)s parameter %(param)s.')
            migrate_util.log.info(msg % {'id': raw_template.id,
                                         'param': param_name})

            try:
                param_val = raw_template.environment['parameters'][param_name]
            except KeyError:
                param_val = param.default

            encoded_val = encodeutils.safe_encode(param_val)
            encrypted_val = crypt.encrypt(encoded_val)
            raw_template.environment['parameters'][param_name] = encrypted_val
            encrypted_params.append(param_name)

        raw_template.environment['encrypted_param_names'] = encrypted_params

    session.commit()
    session.close()


def downgrade(migrate_engine):

    Session = orm.sessionmaker(bind=migrate_engine)
    session = Session()
    raw_templates = session.query(models.RawTemplate).all()

    for raw_template in raw_templates:
        parameters = raw_template.environment['parameters']
        encrypted_params = raw_template.environment['encrypted_param_names']
        for param_name in encrypted_params:
            decrypt_function_name = parameters[param_name][0]
            decrypt_function = getattr(crypt, decrypt_function_name, None)
            msg = _('Decrypting raw template %(id)s parameter %(param)s.') % {
                'id': raw_template.id, 'param': param_name}
            migrate_util.log.info(msg)
            decrypted_val = decrypt_function(parameters[param_name][1])
            parameters[param_name] = encodeutils.safe_decode(decrypted_val)

    print "raw_templates[0].environment: %s" % raw_templates[0].environment
    print "DB value before committing: %s" % session.query(models.RawTemplate).all()[0].environment
    session.commit()
    print "DB value after committing: %s" % session.query(models.RawTemplate).all()[0].environment
    session.close()
