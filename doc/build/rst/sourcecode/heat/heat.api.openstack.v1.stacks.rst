
The `heat.api.openstack.v1.stacks <../../api/heat.api.openstack.v1.stacks.rst#module-heat.api.openstack.v1.stacks>`_ Module
***************************************************************************************************************************

Stack endpoint for Heat v1 REST API.

**class heat.api.openstack.v1.stacks.InstantiationData(data,
patch=False)**

   Bases: ``object``

   The data to create or update a stack.

   The data accompanying a PUT or POST request.

   ``PARAMS = ('stack_name', 'temp ... 'environment', 'files')``

   ``PARAM_ENVIRONMENT = 'environment'``

   ``PARAM_FILES = 'files'``

   ``PARAM_STACK_NAME = 'stack_name'``

   ``PARAM_TEMPLATE = 'template'``

   ``PARAM_TEMPLATE_URL = 'template_url'``

   ``PARAM_USER_PARAMS = 'parameters'``

   **args()**

      Get any additional arguments supplied by the user.

   **environment()**

      Get the user-supplied environment for the stack in YAML format.

      If the user supplied Parameters then merge these into the
      environment global options.

   **files()**

   ``static parse_error_check(*args, **kwds)``

   **stack_name()**

      Return the stack name.

   **template()**

      Get template file contents.

      Get template file contents, either inline, from stack adopt data
      or from a URL, in JSON or YAML format.

**class heat.api.openstack.v1.stacks.StackController(options)**

   Bases: ``object``

   WSGI controller for stacks resource in Heat v1 API.

   Implements the API actions.

   ``REQUEST_SCOPE = 'stacks'``

   **abandon(controller, req, tenant_id, **kwargs)**

      Abandons specified stack.

      Abandons specified stack by deleting the stack and it's
      resources from the database, but underlying resources will not
      be deleted.

   **create(controller, req, tenant_id, **kwargs)**

      Create a new stack.

   **default(req, **args)**

   **delete(controller, req, tenant_id, **kwargs)**

      Delete the specified stack.

   **delete_snapshot(controller, req, tenant_id, **kwargs)**

   **detail(controller, req, tenant_id, **kwargs)**

      Lists detailed information for all stacks.

   **generate_template(controller, req, tenant_id, **kwargs)**

      Generates a template based on the specified type.

   **global_index(controller, req, tenant_id, **kwargs)**

   **index(controller, req, tenant_id, **kwargs)**

      Lists summary information for all stacks.

   **list_resource_types(controller, req, tenant_id, **kwargs)**

      Returns a resource types list which may be used in template.

   **list_snapshots(controller, req, tenant_id, **kwargs)**

   **list_template_functions(controller, req, tenant_id, **kwargs)**

      Returns a list of available functions in a given template.

   **list_template_versions(controller, req, tenant_id, **kwargs)**

      Returns a list of available template versions.

   **lookup(controller, req, tenant_id, **kwargs)**

      Redirect to the canonical URL for a stack.

   **prepare_args(data)**

   **preview(controller, req, tenant_id, **kwargs)**

      Preview the outcome of a template and its params.

   **preview_update(controller, req, tenant_id, **kwargs)**

      Preview update for existing stack with a new
      template/parameters.

   **preview_update_patch(controller, req, tenant_id, **kwargs)**

      Preview PATCH update for existing stack.

   **resource_schema(controller, req, tenant_id, **kwargs)**

      Returns the schema of the given resource type.

   **restore_snapshot(controller, req, tenant_id, **kwargs)**

   **show(controller, req, tenant_id, **kwargs)**

      Gets detailed information for a stack.

   **show_snapshot(controller, req, tenant_id, **kwargs)**

   **snapshot(controller, req, tenant_id, **kwargs)**

   **template(controller, req, tenant_id, **kwargs)**

      Get the template body for an existing stack.

   **update(controller, req, tenant_id, **kwargs)**

      Update an existing stack with a new template and/or parameters.

   **update_patch(controller, req, tenant_id, **kwargs)**

      Update an existing stack with a new template.

      Update an existing stack with a new template by patching the
      parameters Add the flag patch to the args so the engine code can
      distinguish

   **validate_template(controller, req, tenant_id, **kwargs)**

      Implements the ValidateTemplate API action.

      Validates the specified template.

**class heat.api.openstack.v1.stacks.StackSerializer**

   Bases: ``heat.common.serializers.JSONResponseSerializer``

   Handles serialization of specific controller method responses.

   **create(response, result)**

**heat.api.openstack.v1.stacks.create_resource(options)**

   Stacks resource factory method.
