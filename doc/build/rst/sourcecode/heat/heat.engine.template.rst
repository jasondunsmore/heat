
The `heat.engine.template <../../api/heat.engine.template.rst#module-heat.engine.template>`_ Module
***************************************************************************************************

**class heat.engine.template.Template(template, template_id=None,
files=None, env=None)**

   Bases: ``_abcoll.Mapping``

   A stack template.

   **add_resource(definition, name=None)**

      Add a resource to the template.

      The resource is passed as a ResourceDefinition object. If no
      name is specified, the name from the ResourceDefinition should
      be used.

   ``classmethod
   create_empty_template(version=('heat_template_version',
   '2015-04-30'))``

      Create an empty template.

      Creates a new empty template with given version. If version is
      not provided, a new empty HOT template of version "2015-04-30"
      is returned.

      :Parameters:
         **version** -- A tuple containing version header of the

      template: version key and value. E.g. ("heat_template_version",
      "2015-04-30") :returns: A new empty template.

   **get_section_name(section)**

      Return a correct section name.

   ``classmethod load(context, template_id, t=None)``

      Retrieve a Template with the given ID from the database.

   **param_schemata(param_defaults=None)**

      Return a dict of parameters.Schema objects for the parameters.

   **parameters(stack_identifier, user_params, param_defaults=None)**

      Return a parameters.Parameters object for the stack.

   **parse(stack, snippet)**

   **remove_resource(name)**

      Remove a resource from the template.

   **resource_definitions(stack)**

      Return a dictionary of ResourceDefinition objects.

   **store(context=None)**

      Store the Template in the database and return its ID.

   **validate()**

      Validate the template.

      Validates the top-level sections of the template as well as
      syntax inside select sections. Some sections are not checked
      here but in code parts that are responsible for working with the
      respective sections (e.g. parameters are check by parameters
      schema class).

   **validate_resource_definitions(stack)**

      Check section's type of ResourceDefinitions.

   ``classmethod validate_resource_key_type(key, valid_types,
   typename, allowed_keys, rsrc_name, rsrc_data)``

      Validation type of the specific resource key.

      Used in validate_resource_definition and check correctness of
      key's type.
