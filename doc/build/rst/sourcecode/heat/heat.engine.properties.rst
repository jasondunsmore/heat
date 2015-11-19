
The `heat.engine.properties <../../api/heat.engine.properties.rst#module-heat.engine.properties>`_ Module
=========================================================================================================

**class heat.engine.properties.Properties(schema, data,
resolver=<function <lambda> at 0x7f7149148c08>, parent_name=None,
context=None, section=None)**

   Bases: ``_abcoll.Mapping``

   **get_user_value(key, validate=False)**

   ``static schema_from_params(params_snippet)``

      Create properties schema from the parameters section of a
      template.

      :Parameters:
         **params_snippet** -- parameter definition from a template

      :Returns:
         equivalent properties schemata for the specified parameters

   ``classmethod schema_to_parameters_and_properties(schema,
   template_type='cfn')``

      Convert a schema to template parameters and properties.

      This can be used to generate a provider template that matches
      the given properties schemata.

      :Parameters:
         **schema** -- A resource type's properties_schema

      :Returns:
         A tuple of params and properties dicts

      ex: input:  {'foo': {'Type': 'List'}}
         output: {'foo': {'Type': 'CommaDelimitedList'}},
            {'foo': {'Fn::Split': {'Ref': 'foo'}}}

      ex: input:  {'foo': {'Type': 'String'}, 'bar': {'Type': 'Map'}}
         output: {'foo': {'Type': 'String'}, 'bar': {'Type': 'Json'}},
            {'foo': {'Ref': 'foo'}, 'bar': {'Ref': 'bar'}}

   **validate(with_value=True)**

**class heat.engine.properties.Property(schema, name=None,
context=None)**

   Bases: ``object``

   **default()**

   **get_value(value, validate=False)**

      Get value from raw value and sanitize according to data type.

   **has_default()**

   **immutable()**

   **implemented()**

   **required()**

   **support_status()**

   **type()**

   **update_allowed()**

**class heat.engine.properties.Schema(data_type, description=None,
default=None, schema=None, required=False, constraints=None,
implemented=True, update_allowed=False, immutable=False,
support_status=<heat.engine.support.SupportStatus object at
0x7f7149145510>, allow_conversion=False)**

   Bases: `heat.engine.constraints.Schema
   <../../api/heat.engine.constraints.rst#heat.engine.constraints.Schema>`_

   Schema class for validating resource properties.

   This class is used for defining schema constraints for resource
   properties. It inherits generic validation features from the base
   Schema class and add processing that is specific to resource
   properties.

   ``CONSTRAINTS = 'constraints'``

   ``DEFAULT = 'default'``

   ``DESCRIPTION = 'description'``

   ``IMMUTABLE = 'immutable'``

   ``KEYS = ('type', 'descriptio ... _allowed', 'immutable')``

   ``REQUIRED = 'required'``

   ``SCHEMA = 'schema'``

   ``TYPE = 'type'``

   ``UPDATE_ALLOWED = 'update_allowed'``

   **allowed_param_prop_type()**

      Return allowed type of Property Schema converted from parameter.

      Especially, when generating Schema from parameter, Integer
      Property Schema will be supplied by Number parameter.

   ``classmethod from_legacy(schema_dict)``

      Return a Property Schema object from a legacy schema dictionary.

   ``classmethod from_parameter(param)``

      Return a Property Schema corresponding to a Parameter Schema.

      Convert a parameter schema from a provider template to a
      property Schema for the corresponding resource facade.

**class heat.engine.properties.TranslationRule(properties, rule,
source_path, value=None, value_name=None, value_path=None)**

   Bases: ``object``

   Translating mechanism one properties to another.

   Mechanism uses list of rules, each defines by this class, and can
   be executed. Working principe: during resource creating after
   properties defining resource take list of rules, specified by
   method translation_rules, which should be overloaded for each
   resource, if it's needed, and execute each rule using
   translate_properties method. Next operations are allowed:

   * ADD. This rule allows to add some value to list-type properties.
     Only
        list-type values can be added to such properties. Using for
        other cases is prohibited and will be returned with error.

   * REPLACE. This rule allows to replace some property value to
     another. Used
        for all types of properties. Note, that if property has list
        type, then value will be replaced for all elements of list,
        where it needed. If element in such property must be replaced
        by value of another element of this property, value_name must
        be defined.

   * DELETE. This rule allows to delete some property. If property has
     list
        type, then deleting affects value in all list elements.

   ``ADD = 'Add'``

   ``DELETE = 'Delete'``

   ``REPLACE = 'Replace'``

   ``RULE_KEYS = ('Add', 'Replace', 'Delete')``

   **execute_rule()**

   **get_data_from_source_path(path)**

   **validate()**

**heat.engine.properties.schemata(schema_dicts)**

   Return dictionary of Schema objects for given dictionary of
   schemata.

   The input schemata are converted from the legacy (dictionary-based)
   format to Schema objects where necessary.
