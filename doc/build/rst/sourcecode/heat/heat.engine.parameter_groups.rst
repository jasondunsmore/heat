
The `heat.engine.parameter_groups <../../api/heat.engine.parameter_groups.rst#module-heat.engine.parameter_groups>`_ Module
===========================================================================================================================

**class heat.engine.parameter_groups.ParameterGroups(tmpl)**

   Bases: ``object``

   The ParameterGroups specified by the stack's template.

   **validate()**

      Validate the parameter group.

      Validate that each parameter belongs to only one Parameter Group
      and that each parameter name in the group references a valid
      parameter.
