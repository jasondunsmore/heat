
The `heat.engine.api <../../api/heat.engine.api.rst#module-heat.engine.api>`_ Module
====================================================================================

**heat.engine.api.extract_args(params)**

   Extract arguments passed as parameters and return them as a
   dictionary.

   Extract any arguments passed as parameters through the API and
   return them as a dictionary. This allows us to filter the passed
   args and do type conversion where appropriate

**heat.engine.api.format_event(event)**

**heat.engine.api.format_notification_body(stack)**

**heat.engine.api.format_resource_attributes(resource,
with_attr=None)**

**heat.engine.api.format_resource_properties(resource)**

**heat.engine.api.format_snapshot(snapshot)**

**heat.engine.api.format_software_config(sc, detail=True)**

**heat.engine.api.format_software_deployment(sd)**

**heat.engine.api.format_stack(stack, preview=False)**

   Return a representation of the given stack.

   Return a representation of the given stack that matches the API
   output expectations.

**heat.engine.api.format_stack_outputs(stack, outputs)**

   Return a representation of the given output template.

   Return a representation of the given output template for the given
   stack that matches the API output expectations.

**heat.engine.api.format_stack_preview(stack)**

**heat.engine.api.format_stack_resource(resource, detail=True,
with_props=False, with_attr=None)**

   Return a representation of the given resource.

   Return a representation of the given resource that matches the API
   output expectations.

**heat.engine.api.format_validate_parameter(param)**

   Format a template parameter for validate template API call.

   Formats a template parameter and its schema information from the
   engine's internal representation (i.e. a Parameter object and its
   associated Schema object) to a representation expected by the
   current API (for example to be compatible to CFN syntax).

**heat.engine.api.format_watch(watch)**

**heat.engine.api.format_watch_data(wd)**

**heat.engine.api.translate_filters(params)**

   Translate filter names to their corresponding DB field names.

   :Parameters:
      **params** -- A dictionary containing keys from
      engine.api.STACK_KEYS and other keys previously leaked to users.

   :Returns:
      A dict containing only valid DB filed names.
