
The ``heat.engine.cfn.functions`` Module
****************************************

**class heat.engine.cfn.functions.Base64(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <heat.engine.function.rst#heat.engine.function.Function>`_

   A placeholder function for converting to base64.

   Takes the form:

   ::

      { "Fn::Base64" : "<string>" }

   This function actually performs no conversion. It is included for
   the benefit of templates that convert UserData to Base64. Heat
   accepts UserData in plain text.

   **result()**

**class heat.engine.cfn.functions.FindInMap(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <heat.engine.function.rst#heat.engine.function.Function>`_

   A function for resolving keys in the template mappings.

   Takes the form:

   ::

      { "Fn::FindInMap" : [ "mapping",
                            "key",
                            "value" ] }

   **result()**

**class heat.engine.cfn.functions.GetAZs(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <heat.engine.function.rst#heat.engine.function.Function>`_

   A function for retrieving the availability zones.

   Takes the form:

   ::

      { "Fn::GetAZs" : "<region>" }

   **result()**

**class heat.engine.cfn.functions.GetAtt(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <heat.engine.function.rst#heat.engine.function.Function>`_

   A function for resolving resource attributes.

   Takes the form:

   ::

      { "Fn::GetAtt" : [ "<resource_name>",
                         "<attribute_name" ] }

   **dep_attrs(resource_name)**

   **dependencies(path)**

   **result()**

   **validate()**

**class heat.engine.cfn.functions.Join(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <heat.engine.function.rst#heat.engine.function.Function>`_

   A function for joining strings.

   Takes the form:

   ::

      { "Fn::Join" : [ "<delim>", [ "<string_1>", "<string_2>", ... ] ] }

   And resolves to:

   ::

      "<string_1><delim><string_2><delim>..."

   **result()**

**class heat.engine.cfn.functions.MemberListToMap(stack, fn_name,
args)**

   Bases: `heat.engine.function.Function
   <heat.engine.function.rst#heat.engine.function.Function>`_

   A function to convert lists with enumerated keys and values to
   mapping.

   Takes the form:

   ::

      { 'Fn::MemberListToMap' : [ 'Name',
                                  'Value',
                                  [ '.member.0.Name=<key_0>',
                                    '.member.0.Value=<value_0>',
                                    ... ] ] }

   And resolves to:

   ::

      { "<key_0>" : "<value_0>", ... }

   The first two arguments are the names of the key and value.

   **result()**

**class heat.engine.cfn.functions.ParamRef(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <heat.engine.function.rst#heat.engine.function.Function>`_

   A function for resolving parameter references.

   Takes the form:

   ::

      { "Ref" : "<param_name>" }

   **result()**

**heat.engine.cfn.functions.Ref(stack, fn_name, args)**

   A function for resolving parameters or resource references.

   Takes the form:

   ::

      { "Ref" : "<param_name>" }

   or:

   ::

      { "Ref" : "<resource_name>" }

**class heat.engine.cfn.functions.Replace(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <heat.engine.function.rst#heat.engine.function.Function>`_

   A function for performing string substitutions.

   Takes the form:

   ::

      { "Fn::Replace" : [
          { "<key_1>": "<value_1>", "<key_2>": "<value_2>", ... },
          "<key_1> <key_2>"
        ] }

   And resolves to:

   ::

      "<value_1> <value_2>"

   This is implemented using python str.replace on each key. The order
   in which replacements are performed is undefined.

   **result()**

**class heat.engine.cfn.functions.ResourceFacade(stack, fn_name,
args)**

   Bases: `heat.engine.function.Function
   <heat.engine.function.rst#heat.engine.function.Function>`_

   A function for retrieving data in a parent provider template.

   A function for obtaining data from the facade resource from within
   the corresponding provider template.

   Takes the form:

   ::

      { "Fn::ResourceFacade": "<attribute_type>" }

   where the valid attribute types are "Metadata", "DeletionPolicy"
   and "UpdatePolicy".

   ``DELETION_POLICY = 'DeletionPolicy'``

   ``METADATA = 'Metadata'``

   ``UPDATE_POLICY = 'UpdatePolicy'``

   **result()**

**class heat.engine.cfn.functions.ResourceRef(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <heat.engine.function.rst#heat.engine.function.Function>`_

   A function for resolving resource references.

   Takes the form:

   ::

      { "Ref" : "<resource_name>" }

   **dependencies(path)**

   **result()**

**class heat.engine.cfn.functions.Select(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <heat.engine.function.rst#heat.engine.function.Function>`_

   A function for selecting an item from a list or map.

   Takes the form (for a list lookup):

   ::

      { "Fn::Select" : [ "<index>", [ "<value_1>", "<value_2>", ... ] ] }

   Takes the form (for a map lookup):

   ::

      { "Fn::Select" : [ "<index>", { "<key_1>": "<value_1>", ... } ] }

   If the selected index is not found, this function resolves to an
   empty string.

   **result()**

**class heat.engine.cfn.functions.Split(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <heat.engine.function.rst#heat.engine.function.Function>`_

   A function for splitting strings.

   Takes the form:

   ::

      { "Fn::Split" : [ "<delim>", "<string_1><delim><string_2>..." ] }

   And resolves to:

   ::

      [ "<string_1>", "<string_2>", ... ]

   **result()**
