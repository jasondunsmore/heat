
The `heat.engine.hot.functions <../../api/heat.engine.hot.functions.rst#module-heat.engine.hot.functions>`_ Module
==================================================================================================================

**class heat.engine.hot.functions.Digest(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <../../api/heat.engine.function.rst#heat.engine.function.Function>`_

   A function for performing digest operations.

   Takes the form:

   ::

      digest:
        - <algorithm>
        - <value>

   Valid algorithms are the ones provided by natively by hashlib (md5,
   sha1, sha224, sha256, sha384, and sha512) or any one provided by
   OpenSSL.

   **digest(algorithm, value)**

   **result()**

   **validate_usage(args)**

**class heat.engine.hot.functions.GetAtt(stack, fn_name, args)**

   Bases: `heat.engine.hot.functions.GetAttThenSelect
   <../../api/heat.engine.hot.functions.rst#heat.engine.hot.functions.GetAttThenSelect>`_

   A function for resolving resource attributes.

   Takes the form:

   ::

      get_attr:
        - <resource_name>
        - <attribute_name>
        - <path1>
        - ...

   **result()**

**class heat.engine.hot.functions.GetAttAllAttributes(stack, fn_name,
args)**

   Bases: `heat.engine.hot.functions.GetAtt
   <../../api/heat.engine.hot.functions.rst#heat.engine.hot.functions.GetAtt>`_

   A function for resolving resource attributes.

   Takes the form:

   ::

      get_attr:
        - <resource_name>
        - <attributes_name>
        - <path1>
        - ...

   where <attributes_name> and <path1>, ... are optional arguments. If
   there is no <attributes_name>, result will be dict of all
   resource's attributes. Else function returns resolved resource's
   attribute.

   **dep_attrs(resource_name)**

      Check if there is no attribute_name defined, return empty chain.

   **result()**

**class heat.engine.hot.functions.GetAttThenSelect(stack, fn_name,
args)**

   Bases: `heat.engine.cfn.functions.GetAtt
   <../../api/heat.engine.cfn.functions.rst#heat.engine.cfn.functions.GetAtt>`_

   A function for resolving resource attributes.

   Takes the form:

   ::

      get_attr:
        - <resource_name>
        - <attribute_name>
        - <path1>
        - ...

   **dep_attrs(resource_name)**

   **result()**

**class heat.engine.hot.functions.GetFile(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <../../api/heat.engine.function.rst#heat.engine.function.Function>`_

   A function for including a file inline.

   Takes the form:

   ::

      get_file: <file_key>

   And resolves to the content stored in the files dictionary under
   the given key.

   **result()**

**class heat.engine.hot.functions.GetParam(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <../../api/heat.engine.function.rst#heat.engine.function.Function>`_

   A function for resolving parameter references.

   Takes the form:

   ::

      get_param: <param_name>

   or:

   ::

      get_param:
        - <param_name>
        - <path1>
        - ...

   **result()**

**class heat.engine.hot.functions.Join(stack, fn_name, args)**

   Bases: `heat.engine.cfn.functions.Join
   <../../api/heat.engine.cfn.functions.rst#heat.engine.cfn.functions.Join>`_

   A function for joining strings.

   Takes the form:

   ::

      { "list_join" : [ "<delim>", [ "<string_1>", "<string_2>", ... ] ] }

   And resolves to:

   ::

      "<string_1><delim><string_2><delim>..."

**class heat.engine.hot.functions.JoinMultiple(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <../../api/heat.engine.function.rst#heat.engine.function.Function>`_

   A function for joining one or more lists of strings.

   Takes the form:

   ::

      { "list_join" : [ "<delim>", [ "<string_1>", "<string_2>", ... ] ] }

   And resolves to:

   ::

      "<string_1><delim><string_2><delim>..."

   Optionally multiple lists may be specified, which will also be
   joined.

   **result()**

**class heat.engine.hot.functions.MapMerge(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <../../api/heat.engine.function.rst#heat.engine.function.Function>`_

   A function for merging maps.

   Takes the form:

   ::

      { "map_merge" : [{'k1': 'v1', 'k2': 'v2'}, {'k1': 'v2'}] }

   And resolves to:

   ::

      {'k1': 'v2', 'k2': 'v2'}

   **result()**

**class heat.engine.hot.functions.Removed(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <../../api/heat.engine.function.rst#heat.engine.function.Function>`_

   This function existed in previous versions of HOT, but has been
   removed.

   Check the HOT guide for an equivalent native function.

   **result()**

   **validate()**

**class heat.engine.hot.functions.Repeat(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <../../api/heat.engine.function.rst#heat.engine.function.Function>`_

   A function for iterating over a list of items.

   Takes the form:

   ::

      repeat:
          template:
              <body>
          for_each:
              <var>: <list>

   The result is a new list of the same size as <list>, where each
   element is a copy of <body> with any occurrences of <var> replaced
   with the corresponding item of <list>.

   **result()**

**class heat.engine.hot.functions.Replace(stack, fn_name, args)**

   Bases: `heat.engine.cfn.functions.Replace
   <../../api/heat.engine.cfn.functions.rst#heat.engine.cfn.functions.Replace>`_

   A function for performing string substitutions.

   Takes the form:

   ::

      str_replace:
        template: <key_1> <key_2>
        params:
          <key_1>: <value_1>
          <key_2>: <value_2>
          ...

   And resolves to:

   ::

      "<value_1> <value_2>"

   This is implemented using Python's str.replace on each key. The
   order in which replacements are performed is undefined.

**class heat.engine.hot.functions.ReplaceJson(stack, fn_name, args)**

   Bases: `heat.engine.hot.functions.Replace
   <../../api/heat.engine.hot.functions.rst#heat.engine.hot.functions.Replace>`_

   A function for performing string substitutions.

   Behaves the same as Replace, but tolerates non-string parameter
   values, e.g map/list - these are serialized as json before doing
   the string substitution.

   **result()**

**class heat.engine.hot.functions.ResourceFacade(stack, fn_name,
args)**

   Bases: `heat.engine.cfn.functions.ResourceFacade
   <../../api/heat.engine.cfn.functions.rst#heat.engine.cfn.functions.ResourceFacade>`_

   A function for retrieving data in a parent provider template.

   A function for obtaining data from the facade resource from within
   the corresponding provider template.

   Takes the form:

   ::

      resource_facade: <attribute_type>

   where the valid attribute types are "metadata", "deletion_policy"
   and "update_policy".

   ``DELETION_POLICY = 'deletion_policy'``

   ``METADATA = 'metadata'``

   ``UPDATE_POLICY = 'update_policy'``

**class heat.engine.hot.functions.StrSplit(stack, fn_name, args)**

   Bases: `heat.engine.function.Function
   <../../api/heat.engine.function.rst#heat.engine.function.Function>`_

   A function for splitting delimited strings into a list.

   Optionally extracting a specific list member by index.

   Takes the form:

   ::

      str_split: [delimiter, string, <index> ]

   or:

   ::

      str_split:
        - delimiter
        - string
        - <index>

   If <index> is specified, the specified list item will be returned
   otherwise, the whole list is returned, similar to get_attr with
   path based attributes accessing lists.

   **result()**
