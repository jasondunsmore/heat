
The `heat.engine.attributes <../../api/heat.engine.attributes.rst#module-heat.engine.attributes>`_ Module
=========================================================================================================

**class heat.engine.attributes.Attribute(attr_name, schema)**

   Bases: ``object``

   An Attribute schema.

   **as_output(resource_name, template_type='cfn')**

      Output entry for a provider template with the given resource
      name.

      :Parameters:
         * **resource_name** -- the logical name of the provider
           resource

         * **template_type** -- the template type to generate

      :Returns:
         This attribute as a template 'Output' entry for cfn template
         and 'output' entry for hot template

   **support_status()**

**class heat.engine.attributes.Attributes(res_name, schema,
resolver)**

   Bases: ``_abcoll.Mapping``

   Models a collection of Resource Attributes.

   ``static as_outputs(resource_name, resource_class,
   template_type='cfn')``

      Dict of Output entries for a provider template with resource
      name.

      :Parameters:
         * **resource_name** -- logical name of the resource

         * **resource_class** -- resource implementation class

      :Returns:
         The attributes of the specified resource_class as a template
         Output map

   **reset_resolved_values()**

   ``static schema_from_outputs(json_snippet)``

**class heat.engine.attributes.DynamicSchemeAttributes(res_name,
schema, resolver)**

   Bases: `heat.engine.attributes.Attributes
   <../../api/heat.engine.attributes.rst#heat.engine.attributes.Attributes>`_

   The collection of attributes for resources without static attr
   scheme.

   The class defines collection of attributes for such entities as
   Resource Group, Software Deployment and so on that doesn't have
   static attribute scheme. The attribute scheme for such kind of
   resources can contain attribute from attribute scheme (like other
   resources) and dynamic attributes (nested stack attrs or API
   response attrs).

**class heat.engine.attributes.Schema(description=None,
support_status=<heat.engine.support.SupportStatus object at
0x7f71491e55d0>, cache_mode='cache_local', type=None)**

   Bases: `heat.engine.constraints.Schema
   <../../api/heat.engine.constraints.rst#heat.engine.constraints.Schema>`_

   Simple schema class for attributes.

   Schema objects are serializable to dictionaries following a
   superset of the HOT input Parameter schema using dict().

   ``BOOLEAN = 'Boolean'``

   ``CACHE_LOCAL = 'cache_local'``

   ``CACHE_MODES = ('cache_local', 'cache_none')``

   ``CACHE_NONE = 'cache_none'``

   ``DESCRIPTION = 'description'``

   ``INTEGER = 'Integer'``

   ``KEYS = ('description', 'type')``

   ``LIST = 'List'``

   ``MAP = 'Map'``

   ``STRING = 'String'``

   ``TYPE = 'type'``

   ``TYPES = ('String', 'Map', 'List', 'Integer', 'Boolean')``

   ``classmethod from_attribute(schema_dict)``

      Return a Property Schema corresponding to a Attribute Schema.

**heat.engine.attributes.schemata(schema)**

   Return dictionary of Schema objects for given dictionary of
   schemata.

**heat.engine.attributes.select_from_attribute(attribute_value,
path)**

   Select an element from an attribute value.

   :Parameters:
      * **attribute_value** -- the attribute value.

      * **path** -- a list of path components to select from the
        attribute.

   :Returns:
      the selected attribute component value.
