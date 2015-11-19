
The `heat.engine.environment <../../api/heat.engine.environment.rst#module-heat.engine.environment>`_ Module
============================================================================================================

**class heat.engine.environment.ClassResourceInfo(registry, path,
value)**

   Bases: `heat.engine.environment.ResourceInfo
   <../../api/heat.engine.environment.rst#heat.engine.environment.ResourceInfo>`_

   Store the mapping of resource name to python class implementation.

   ``description = 'Plugin'``

   **get_class(files=None)**

**class heat.engine.environment.Environment(env=None, user_env=True)**

   Bases: ``object``

   **get_class(resource_type, resource_name=None, files=None)**

   **get_constraint(name)**

   **get_resource_info(resource_type, resource_name=None,
   registry_type=None, ignore=None)**

   **get_stack_lifecycle_plugins()**

   **get_types(cnxt=None, support_status=None, type_name=None,
   version=None)**

   **load(env_snippet)**

   **register_class(resource_type, resource_class, path=None)**

   **register_constraint(constraint_name, constraint)**

   **register_stack_lifecycle_plugin(stack_lifecycle_name,
   stack_lifecycle_class)**

   **user_env_as_dict()**

      Get the environment as a dict, ready for storing in the db.

**class heat.engine.environment.GlobResourceInfo(registry, path,
value)**

   Bases: `heat.engine.environment.MapResourceInfo
   <../../api/heat.engine.environment.rst#heat.engine.environment.MapResourceInfo>`_

   Store the mapping (with wild cards) of one resource type to
   another.

   like: OS::Networking::* -> OS::Neutron::*

   ``description = 'Wildcard Mapping'``

   **get_resource_info(resource_type=None, resource_name=None)**

   **matches(resource_type)**

**class heat.engine.environment.MapResourceInfo(registry, path,
value)**

   Bases: `heat.engine.environment.ResourceInfo
   <../../api/heat.engine.environment.rst#heat.engine.environment.ResourceInfo>`_

   Store the mapping of one resource type to another.

   like: OS::Networking::FloatingIp -> OS::Neutron::FloatingIp

   ``description = 'Mapping'``

   **get_class(files=None)**

   **get_resource_info(resource_type=None, resource_name=None)**

**class heat.engine.environment.ResourceInfo(registry, path, value)**

   Bases: ``object``

   Base mapping of resource type to implementation.

   **get_resource_info(resource_type=None, resource_name=None)**

   **matches(resource_type)**

**class heat.engine.environment.ResourceRegistry(global_registry,
env)**

   Bases: ``object``

   By looking at the environment, find the resource implementation.

   **as_dict()**

      Return user resources in a dict format.

   **get_class(resource_type, resource_name=None, files=None)**

   **get_resource_info(resource_type, resource_name=None,
   registry_type=None, ignore=None)**

      Find possible matches to the resource type and name.

      Chain the results from the global and user registry to find a
      match.

   **get_types(cnxt=None, support_status=None, type_name=None,
   version=None)**

      Return a list of valid resource types.

   **iterable_by(resource_type, resource_name=None)**

   **load(json_snippet)**

   **log_resource_info(show_all=False, prefix=None)**

   **matches_hook(resource_name, hook)**

      Return whether a resource have a hook set in the environment.

      For a given resource and a hook type, we check to see if the the
      passed group of resources has the right hook associated with the
      name.

      Hooks are set in this format via *resources*:

      {
         "res_name": {
            "hooks": [pre-create, pre-update]

         }, ">>*<<_suffix": {

         "hooks": pre-create

         }, "prefix_*": {

         "hooks": pre-update

         }

      }

      A hook value is either *pre-create*, *pre-update* or a list of
      those values. Resources support wildcard matching. The asterisk
      sign matches everything.

   **register_class(resource_type, resource_class, path=None)**

   **remove_item(info)**

   **remove_resources_except(resource_name)**

**class heat.engine.environment.TemplateResourceInfo(registry, path,
value)**

   Bases: `heat.engine.environment.ResourceInfo
   <../../api/heat.engine.environment.rst#heat.engine.environment.ResourceInfo>`_

   Store the info needed to start a TemplateResource.

   ``description = 'Template'``

   **get_class(files=None)**

**heat.engine.environment.get_child_environment(parent_env,
child_params, item_to_remove=None, child_resource_name=None)**

   Build a child environment using the parent environment and params.

   This is built from the child_params and the parent env so some
   resources can use user-provided parameters as if they come from an
   environment.

   1. resource_registry must be merged (child env should be loaded
      after the parent env to take precedence).

   2. child parameters must overwrite the parent's as they won't be
      relevant in the child template.

   If *child_resource_name* is provided, resources in the registry
   will be replaced with the contents of the matching child resource
   plus anything that passes a wildcard match.

**heat.engine.environment.is_hook_definition(key, value)**

**heat.engine.environment.read_global_environment(env, env_dir=None)**

**heat.engine.environment.valid_hook_type(hook)**
