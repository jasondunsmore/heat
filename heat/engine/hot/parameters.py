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

import itertools

import six

from heat.common import exception
from heat.common.i18n import _
from heat.engine import constraints as constr
from heat.engine import parameters


PARAM_CONSTRAINTS = (
    DESCRIPTION, LENGTH, RANGE, ALLOWED_VALUES, ALLOWED_PATTERN,
    CUSTOM_CONSTRAINT,
) = (
    'description', 'length', 'range', 'allowed_values', 'allowed_pattern',
    'custom_constraint',
)

RANGE_KEYS = (MIN, MAX) = ('min', 'max')


class HOTParamSchema(parameters.Schema):
    """HOT parameter schema."""

    KEYS = (
        TYPE, DESCRIPTION, DEFAULT, SCHEMA, CONSTRAINTS,
        HIDDEN, LABEL, UPDATABLE
    ) = (
        'type', 'description', 'default', 'schema', 'constraints',
        'hidden', 'label', 'updatable'
    )

    # For Parameters the type name for Schema.LIST is comma_delimited_list
    # and the type name for Schema.MAP is json
    TYPES = (
        STRING, NUMBER, LIST, MAP, BOOLEAN,
    ) = (
        'string', 'number', 'comma_delimited_list', 'json', 'boolean',
    )

    PARAMETER_KEYS = KEYS

    def __init__(self, data_type, description=None, default=None, schema=None,
                 constraints=None, hidden=False, label=None, updatable=True):
        super(HOTParamSchema, self).__init__(data_type=data_type,
                                             description=description,
                                             default=default,
                                             schema=schema,
                                             constraints=constraints,
                                             label=label)
        self.updatable = updatable

    @classmethod
    def from_dict(cls, param_name, schema_dict):
        """Return a Parameter Schema object from a legacy schema dictionary.

        :param param_name: name of the parameter owning the schema; used
               for more verbose logging
        :type  param_name: str
        """
        cls._validate_dict(param_name, schema_dict)

        def constraints():
            constraints = schema_dict.get(cls.CONSTRAINTS)
            if constraints is None:
                return

            if not isinstance(constraints, list):
                raise exception.InvalidSchemaError(
                    message=_("Invalid parameter constraints for parameter "
                              "%s, expected a list") % param_name)

            for constraint in constraints:
                cls._check_dict(constraint, PARAM_CONSTRAINTS,
                                'parameter constraints')
                desc = constraint.get(DESCRIPTION)
                if RANGE in constraint:
                    cdef = constraint.get(RANGE)
                    cls._check_dict(cdef, RANGE_KEYS, 'range constraint')
                    yield constr.Range(parameters.Schema.get_num(MIN, cdef),
                                       parameters.Schema.get_num(MAX, cdef),
                                       desc)
                elif LENGTH in constraint:
                    cdef = constraint.get(LENGTH)
                    cls._check_dict(cdef, RANGE_KEYS, 'length constraint')
                    yield constr.Length(parameters.Schema.get_num(MIN, cdef),
                                        parameters.Schema.get_num(MAX, cdef),
                                        desc)
                elif ALLOWED_VALUES in constraint:
                    cdef = constraint.get(ALLOWED_VALUES)
                    yield constr.AllowedValues(cdef, desc)
                elif ALLOWED_PATTERN in constraint:
                    cdef = constraint.get(ALLOWED_PATTERN)
                    yield constr.AllowedPattern(cdef, desc)
                elif CUSTOM_CONSTRAINT in constraint:
                    cdef = constraint.get(CUSTOM_CONSTRAINT)
                    yield constr.CustomConstraint(cdef, desc)
                else:
                    raise exception.InvalidSchemaError(
                        message=_("No constraint expressed"))

        # make update_allowed true by default on TemplateResources
        # as the template should deal with this.
        return cls(schema_dict[cls.TYPE],
                   description=schema_dict.get(HOTParamSchema.DESCRIPTION),
                   default=schema_dict.get(HOTParamSchema.DEFAULT),
                   constraints=list(constraints()),
                   hidden=schema_dict.get(HOTParamSchema.HIDDEN, False),
                   label=schema_dict.get(HOTParamSchema.LABEL),
                   updatable=schema_dict.get(HOTParamSchema.UPDATABLE, True))


class HOTParameter(parameters.Parameter):

    def __new__(cls, name, schema, value=None):
        if cls is not HOTParameter:
            return super(HOTParameter, cls).__new__(cls, name, schema,
                                                    value=value)

        # Check for fully-fledged Schema objects
        if not isinstance(schema, HOTParamSchema):
            schema = HOTParamSchema.from_dict(name, schema)

        if schema.type == schema.STRING:
            ParamClass = HOTStringParam
        elif schema.type == schema.NUMBER:
            ParamClass = HOTNumberParam
        elif schema.type == schema.LIST:
            ParamClass = HOTCommaDelimitedListParam
        elif schema.type == schema.MAP:
            ParamClass = HOTJsonParam
        elif schema.type == schema.BOOLEAN:
            ParamClass = HOTBooleanParam
        else:
            raise ValueError(_('Invalid Parameter type "%s"') % schema.type)

        return ParamClass(name, schema, value)

    def updatable(self):
        """Return whether the parameter is updatable."""
        return self.schema.updatable


class HOTStringParam(HOTParameter, parameters.StringParam):
    pass


class HOTNumberParam(HOTParameter, parameters.NumberParam):
    pass


class HOTCommaDelimitedListParam(HOTParameter,
                                 parameters.CommaDelimitedListParam):
    pass


class HOTJsonParam(HOTParameter, parameters.JsonParam):
    pass


class HOTBooleanParam(HOTParameter, parameters.BooleanParam):
    pass


class HOTParameters(parameters.Parameters):
    PSEUDO_PARAMETERS = (
        PARAM_STACK_ID, PARAM_STACK_NAME, PARAM_REGION, PARAM_PROJECT_ID
    ) = (
        'OS::stack_id', 'OS::stack_name', 'OS::region', 'OS::project_id'
    )

    def __init__(self, stack_identifier, tmpl, user_params=None,
                 param_defaults=None):

        user_params = user_params or {}
        param_defaults = param_defaults or {}

        def user_parameter(schema_item):
            name, schema = schema_item
            return HOTParameter(name, schema,
                                user_params.get(name))

        self.tmpl = tmpl
        self.user_params = user_params

        schemata = self.tmpl.param_schemata()
        user_parameters = (user_parameter(si) for si in
                           six.iteritems(schemata))
        pseudo_parameters = self._pseudo_parameters(stack_identifier)

        self.params = dict((p.name,
                            p) for p in itertools.chain(pseudo_parameters,
                                                        user_parameters))

        for pd in six.iterkeys(param_defaults):
            if pd in self.params:
                self.params[pd].set_default(param_defaults[pd])

    def set_stack_id(self, stack_identifier):
        """Set the StackId pseudo parameter value."""
        if stack_identifier is not None:
            self.params[self.PARAM_STACK_ID].schema.set_default(
                stack_identifier.stack_id)
            return True
        return False

    def _pseudo_parameters(self, stack_identifier):
        stack_id = getattr(stack_identifier, 'stack_id', '')
        stack_name = getattr(stack_identifier, 'stack_name', '')
        tenant = getattr(stack_identifier, 'tenant', '')

        yield HOTParameter(
            self.PARAM_STACK_ID,
            HOTParamSchema(HOTParamSchema.STRING, _('Stack ID'),
                           default=str(stack_id)))
        yield HOTParameter(
            self.PARAM_PROJECT_ID,
            HOTParamSchema(HOTParamSchema.STRING, _('Project ID'),
                           default=str(tenant)))
        if stack_name:
            yield HOTParameter(
                self.PARAM_STACK_NAME,
                HOTParamSchema(HOTParamSchema.STRING, _('Stack Name'),
                               default=stack_name))
