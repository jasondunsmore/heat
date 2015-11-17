
The `heat.engine.parameters <../../api/heat.engine.parameters.rst#module-heat.engine.parameters>`_ Module
*********************************************************************************************************

**class heat.engine.parameters.BooleanParam(name, schema,
value=None)**

   Bases: `heat.engine.parameters.Parameter
   <../../api/heat.engine.parameters.rst#heat.engine.parameters.Parameter>`_

   A template parameter of type "Boolean".

   **value()**

**class heat.engine.parameters.CommaDelimitedListParam(name, schema,
value=None)**

   Bases: `heat.engine.parameters.ParsedParameter
   <../../api/heat.engine.parameters.rst#heat.engine.parameters.ParsedParameter>`_,
   ``_abcoll.Sequence``

   A template parameter of type "CommaDelimitedList".

   **parse(value)**

   **value()**

**class heat.engine.parameters.JsonParam(name, schema, value=None)**

   Bases: `heat.engine.parameters.ParsedParameter
   <../../api/heat.engine.parameters.rst#heat.engine.parameters.ParsedParameter>`_

   A template parameter who's value is map or list.

   **parse(value)**

   **value()**

**class heat.engine.parameters.NumberParam(name, schema, value=None)**

   Bases: `heat.engine.parameters.Parameter
   <../../api/heat.engine.parameters.rst#heat.engine.parameters.Parameter>`_

   A template parameter of type "Number".

   **value()**

**class heat.engine.parameters.Parameter(name, schema, value=None)**

   Bases: ``object``

   A template parameter.

   **default()**

      Return the default value of the parameter.

   **description()**

      Return the description of the parameter.

   **has_default()**

      Return whether the parameter has a default value.

   **has_value()**

      Parameter has a user or default value.

   **hidden()**

      Return whether the parameter is hidden.

      Hidden parameters should be sanitised in any output to the user.

   **label()**

      Return the label or param name.

   **set_default(value)**

   **validate(validate_value=True, context=None)**

      Validates the parameter.

      This method validates if the parameter's schema is valid, and if
      the default value - if present - or the user-provided value for
      the parameter comply with the schema.

   **value()**

      Get the parameter value, optionally sanitising it for output.

**class heat.engine.parameters.Parameters(stack_identifier, tmpl,
user_params=None, param_defaults=None)**

   Bases: ``_abcoll.Mapping``

   Parameters of a stack.

   The parameters of a stack, with type checking, defaults, etc.
   specified by the stack's template.

   ``PARAM_REGION = 'AWS::Region'``

   ``PARAM_STACK_ID = 'AWS::StackId'``

   ``PARAM_STACK_NAME = 'AWS::StackName'``

   ``PSEUDO_PARAMETERS = ('AWS::StackId', 'AWS::StackName',
   'AWS::Region')``

   **map(func, filter_func=<function <lambda> at 0x7ff2cbd7b938>)**

      Map the supplied function onto each Parameter.

      Map the supplied function onto each Parameter (with an optional
      filter function) and return the resulting dictionary.

   **set_stack_id(stack_identifier)**

      Set the StackId pseudo parameter value.

   **validate(validate_value=True, context=None)**

      Validates all parameters.

      This method validates if all user-provided parameters are
      actually defined in the template, and if all parameters are
      valid.

**class heat.engine.parameters.ParsedParameter(name, schema,
value=None)**

   Bases: `heat.engine.parameters.Parameter
   <../../api/heat.engine.parameters.rst#heat.engine.parameters.Parameter>`_

   A template parameter with cached parsed value.

   **set_default(value)**

**class heat.engine.parameters.Schema(data_type, description=None,
default=None, schema=None, constraints=None, hidden=False,
label=None)**

   Bases: `heat.engine.constraints.Schema
   <../../api/heat.engine.constraints.rst#heat.engine.constraints.Schema>`_

   Parameter schema.

   ``BOOLEAN = 'Boolean'``

   ``CONSTRAINTS = 'Constraints'``

   ``DEFAULT = 'Default'``

   ``DESCRIPTION = 'Description'``

   ``HIDDEN = 'NoEcho'``

   ``KEYS = ('Type', 'Descriptio ... ts', 'NoEcho', 'Label')``

   ``LABEL = 'Label'``

   ``LIST = 'CommaDelimitedList'``

   ``MAP = 'Json'``

   ``NUMBER = 'Number'``

   ``PARAMETER_KEYS = ('Type', 'Default',  ... tDescription',
   'Label')``

   ``SCHEMA = 'Schema'``

   ``STRING = 'String'``

   ``TYPE = 'Type'``

   ``TYPES = ('String', 'Number', 'CommaDelimitedList', 'Json',
   'Boolean')``

   ``classmethod from_dict(param_name, schema_dict)``

      Return a Parameter Schema object from a legacy schema
      dictionary.

      :Parameters:
         **param_name** (*str*) -- name of the parameter owning the
         schema; used for more verbose logging

   ``static get_num(key, context)``

   **set_default(default=None)**

   **validate_value(value, context=None)**

**class heat.engine.parameters.StringParam(name, schema, value=None)**

   Bases: `heat.engine.parameters.Parameter
   <../../api/heat.engine.parameters.rst#heat.engine.parameters.Parameter>`_

   A template parameter of type "String".
