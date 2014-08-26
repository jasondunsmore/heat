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

import sqlalchemy

from migrate.versioning import util as migrate_util
from sqlalchemy import orm

from oslo.config import cfg
from oslo.utils import encodeutils

from heat.common import crypt
from heat.common.i18n import _
from heat.db.sqlalchemy import models
from heat.db.sqlalchemy import types
from heat.engine import template


def upgrade(migrate_engine):
    meta = sqlalchemy.MetaData(bind=migrate_engine)

    stack = sqlalchemy.Table('stack', meta, autoload=True)
    encrypted_params = sqlalchemy.Column('encrypted_params', types.Json,
                                         default={})
    encrypted_params.create(stack)

    if not cfg.CONF.encrypt_parameters_and_properties:
        return

    Session = orm.sessionmaker(bind=migrate_engine)
    session = Session()
    stacks = session.query(models.Stack).all()

    for stack in stacks:
        tmpl = template.Template.load(None,
                                      stack.raw_template_id,
                                      stack.raw_template)
        params = stack.parameters
        parameters = params['parameters']

        encrypted_params = []
        for param_name, param in tmpl.param_schemata().items():
            if not param.hidden or param_name in encrypted_params:
                continue

            msg = _('Encrypting stack %(stack)s parameter %(param)s.')
            migrate_util.log.info(msg % {'stack': stack.name,
                                         'param': param_name})

            try:
                param_val = parameters[param_name]
            except KeyError:
                param_val = param.default

            encoded_val = encodeutils.safe_encode(param_val)
            parameters[param_name] = crypt.encrypt(encoded_val)
            encrypted_params.append(param_name)

        stack.encrypted_params = {'parameters': encrypted_params}
        params['parameters'] = parameters

        if stack.resources:
            import ipdb; ipdb.set_trace()
        session.commit()


def downgrade(migrate_engine):

    # Decrypt data using encrypted_params column
    Session = orm.sessionmaker(bind=migrate_engine)
    session = Session()
    stacks = session.query(models.Stack).all()

    for stack in stacks:
        params = stack.parameters
        parameters = params['parameters']

        encrypted_params = stack.encrypted_params.get('parameters', {})
        for param_name in encrypted_params:
            decrypt_function_name = parameters[param_name][0]
            decrypt_function = getattr(crypt, decrypt_function_name, None)
            msg = _('Decrypting %(stack)s parameter %(param)s.') % {
                'stack': stack.name, 'param': param_name}
            migrate_util.log.info(msg)
            decrypted_val = decrypt_function(parameters[param_name][1])
            parameters[param_name] = encodeutils.safe_decode(decrypted_val)

        params['parameters'] = parameters
        session.commit()

    # Drop encrypted_params column
    meta = sqlalchemy.MetaData(bind=migrate_engine)

    stack = sqlalchemy.Table('stack', meta, autoload=True)
    stack.c.encrypted_params.drop()
