
The ``heat.scaling.template`` Module
====================================

**heat.scaling.template.make_template(resource_definitions,
version=('heat_template_version', '2015-04-30'), child_env=None)**

   Return a Template object containing the given resource definitions.

   By default, the template will be in the HOT format. A different
   format can be specified by passing a (version_type, version_string)
   tuple matching any of the available template format plugins.

**heat.scaling.template.member_definitions(old_resources,
new_definition, num_resources, num_new, get_new_id,
customise=<function _identity at 0x7f71475a82a8>)**

   Iterate over resource definitions for a scaling group

   Generates the definitions for the next change to the scaling group.
   Each item is a (name, definition) tuple.

   The input is a list of (name, definition) tuples for existing
   resources in the group, sorted in the order that they should be
   replaced or removed (i.e. the resource that should be the first to
   be replaced (on update) or removed (on scale down) appears at the
   beginning of the list.) New resources are added or old resources
   removed as necessary to ensure a total of num_resources.

   The number of resources to have their definition changed to the new
   one is controlled by num_new. This value includes any new resources
   to be added, with any shortfall made up by modifying the
   definitions of existing resources.
