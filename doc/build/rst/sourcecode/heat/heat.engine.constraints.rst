
The `heat.engine.constraints <../../api/heat.engine.constraints.rst#module-heat.engine.constraints>`_ Module
************************************************************************************************************

**class heat.engine.constraints.AllowedPattern(pattern,
description=None)**

   Bases: `heat.engine.constraints.Constraint
   <../../api/heat.engine.constraints.rst#heat.engine.constraints.Constraint>`_

   Constrain values to a predefined regular expression pattern.

   Serializes to JSON as:

   ::

      {
          'allowed_pattern': <pattern>,
          'description': <description>
      }

   ``valid_types = ('STRING',)``

**class heat.engine.constraints.AllowedValues(allowed,
description=None)**

   Bases: `heat.engine.constraints.Constraint
   <../../api/heat.engine.constraints.rst#heat.engine.constraints.Constraint>`_

   Constrain values to a predefined set.

   Serializes to JSON as:

   ::

      {
          'allowed_values': [<allowed1>, <allowed2>, ...],
          'description': <description>
      }

   ``valid_types = ('STRING', 'INTEGER', 'NUMBER', 'BOOLEAN',
   'LIST')``

**class heat.engine.constraints.AnyIndexDict(value)**

   Bases: ``_abcoll.Mapping``

   A Mapping that returns the same value for any integer index.

   Used for storing the schema for a list. When converted to a
   dictionary, it contains a single item with the key '*'.

   ``ANYTHING = '*'``

**class heat.engine.constraints.BaseCustomConstraint**

   Bases: ``object``

   A base class for validation using API clients.

   It will provide a better error message, and reduce a bit of
   duplication. Subclass must provide *expected_exceptions* and
   implement *validate_with_client*.

   **error(value)**

   ``expected_exceptions = ()``

   **validate(value, context)**

**class heat.engine.constraints.Constraint(description=None)**

   Bases: ``_abcoll.Mapping``

   Parent class for constraints on allowable values for a Property.

   Constraints are serializable to dictionaries following the HOT
   input Parameter constraints schema using dict().

   ``DESCRIPTION = 'description'``

   **validate(value, schema=None, context=None)**

**class heat.engine.constraints.CustomConstraint(name,
description=None, environment=None)**

   Bases: `heat.engine.constraints.Constraint
   <../../api/heat.engine.constraints.rst#heat.engine.constraints.Constraint>`_

   A constraint delegating validation to an external class.

   ``custom_constraint``

   ``valid_types = ('STRING', 'INTEGER', 'NUMBER', 'BOOLEAN',
   'LIST')``

**class heat.engine.constraints.Length(min=None, max=None,
description=None)**

   Bases: `heat.engine.constraints.Range
   <../../api/heat.engine.constraints.rst#heat.engine.constraints.Range>`_

   Constrain the length of values within a range.

   Serializes to JSON as:

   ::

      {
          'length': {'min': <min>, 'max': <max>},
          'description': <description>
      }

   ``valid_types = ('STRING', 'LIST', 'MAP')``

**class heat.engine.constraints.Range(min=None, max=None,
description=None)**

   Bases: `heat.engine.constraints.Constraint
   <../../api/heat.engine.constraints.rst#heat.engine.constraints.Constraint>`_

   Constrain values within a range.

   Serializes to JSON as:

   ::

      {
          'range': {'min': <min>, 'max': <max>},
          'description': <description>
      }

   ``MAX = 'max'``

   ``MIN = 'min'``

   ``valid_types = ('INTEGER', 'NUMBER')``

**class heat.engine.constraints.Schema(data_type, description=None,
default=None, schema=None, required=False, constraints=None,
label=None)**

   Bases: ``_abcoll.Mapping``

   Schema base class for validating properties or parameters.

   Schema objects are serializable to dictionaries following a
   superset of the HOT input Parameter schema using dict().

   Serialises to JSON in the form:

   ::

      {
          'type': 'list',
          'required': False
          'constraints': [
              {
                  'length': {'min': 1},
                  'description': 'List must not be empty'
              }
          ],
          'schema': {
              '*': {
                  'type': 'string'
              }
          },
          'description': 'An example list property.'
      }

   ``BOOLEAN = 'Boolean'``

   ``BOOLEAN_TYPE = 'BOOLEAN'``

   ``CONSTRAINTS = 'constraints'``

   ``DEFAULT = 'default'``

   ``DESCRIPTION = 'description'``

   ``INTEGER = 'Integer'``

   ``INTEGER_TYPE = 'INTEGER'``

   ``KEYS = ('type', 'descriptio ... quired', 'constraints')``

   ``LIST = 'List'``

   ``LIST_TYPE = 'LIST'``

   ``MAP = 'Map'``

   ``MAP_TYPE = 'MAP'``

   ``NUMBER = 'Number'``

   ``NUMBER_TYPE = 'NUMBER'``

   ``REQUIRED = 'required'``

   ``SCHEMA = 'schema'``

   ``STRING = 'String'``

   ``STRING_TYPE = 'STRING'``

   ``TYPE = 'type'``

   ``TYPES = ('Integer', 'String', 'Number', 'Boolean', 'Map',
   'List')``

   ``TYPE_KEYS = ('INTEGER', 'STRING', 'NUMBER', 'BOOLEAN', 'MAP',
   'LIST')``

   **set_default(default=None)**

      Set the default value for this Schema object.

   ``static str_to_num(value)``

      Convert a string representation of a number into a numeric type.

   **to_schema_type(value)**

      Returns the value in the schema's data type.

   **validate(context=None)**

      Validates the schema.

      This method checks if the schema itself is valid, and if the
      default value - if present - complies to the schema's
      constraints.

   **validate_constraints(value, context=None, skipped=None)**
