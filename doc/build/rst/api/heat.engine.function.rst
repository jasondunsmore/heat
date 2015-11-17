
The ``heat.engine.function`` Module
***********************************

**class heat.engine.function.Function(stack, fn_name, args)**

   Bases: ``object``

   Abstract base class for template functions.

   **dep_attrs(resource_name)**

      Return the attributes of the specified resource that are
      referenced.

      Return an iterator over any attributes of the specified resource
      that this function references.

   **dependencies(path)**

   **result()**

      Return the result of resolving the function.

      Function subclasses must override this method to calculate their
      results.

   ``stack``

   **validate()**

      Validate arguments without resolving the function.

      Function subclasses must override this method to validate their
      args.

**heat.engine.function.dep_attrs(snippet, resource_name)**

   Iterator over dependent attrs of a resource in a template snippet.

   The snippet should be already parsed to insert Function objects
   where appropriate.

   :Returns:
      an iterator over the attributes of the specified resource that

   are referenced in the template snippet.

**heat.engine.function.dependencies(snippet, path='')**

   Return an iterator over Resource dependencies in a template
   snippet.

   The snippet should be already parsed to insert Function objects
   where appropriate.

**heat.engine.function.resolve(snippet)**

**heat.engine.function.validate(snippet)**
