
The ``heat.engine.resource`` Module
===================================

**class heat.engine.resource.Resource(name, definition, stack)**

   Bases: ``object``

   ``ACTIONS = ('INIT', 'CREATE', ' ... ', 'SNAPSHOT', 'CHECK')``

   ``ADOPT = 'ADOPT'``

   ``BASE_ATTRIBUTES = ('show',)``

   ``CHECK = 'CHECK'``

   ``COMPLETE = 'COMPLETE'``

   ``CREATE = 'CREATE'``

   ``DELETE = 'DELETE'``

   ``FAILED = 'FAILED'``

   **FnBase64(data)**

      For the intrinsic function Fn::Base64.

      :Parameters:
         **data** -- the input data.

      :Returns:
         the Base64 representation of the input data.

   **FnGetAtt(key, *path)**

      For the intrinsic function Fn::GetAtt.

      :Parameters:
         * **key** -- the attribute key.

         * **path** -- a list of path components to select from the
           attribute.

      :Returns:
         the attribute value.

   **FnGetAtts()**

      For the intrinsic function get_attr which returns all
      attributes.

      :Returns:
         dict of all resource's attributes exclude "show" attribute.

   **FnGetRefId()**

      For the intrinsic function Ref.

      :Results:
         the id or name of the resource.

   ``INIT = 'INIT'``

   ``IN_PROGRESS = 'IN_PROGRESS'``

   ``RESUME = 'RESUME'``

   ``ROLLBACK = 'ROLLBACK'``

   ``SHOW = 'show'``

   ``SNAPSHOT = 'SNAPSHOT'``

   ``STATUSES = ('IN_PROGRESS', 'FAILED', 'COMPLETE')``

   ``SUSPEND = 'SUSPEND'``

   ``UPDATE = 'UPDATE'``

   **action_handler_task(action, args=[], action_prefix=None)**

      A task to call the Resource subclass's handler methods for
      action.

      Calls the handle_<ACTION>() method for the given action and then
      calls the check_<ACTION>_complete() method with the result in a
      loop until it returns True. If the methods are not provided, the
      call is omitted.

      Any args provided are passed to the handler.

      If a prefix is supplied, the handler method
      handle_<PREFIX>_<ACTION>() is called instead.

   **add_dependencies(deps)**

   **adopt(resource_data)**

      Adopt the existing resource.

      Resource subclasses can provide a handle_adopt() method to
      customise adopt.

   ``attributes_schema = {}``

   ``base_attributes_schema = {'show': <heat.engine.attributes.Schema
   object at 0x7f7147574310>}``

   ``static build_template_dict(res_name, res_type, tmpl_type, params,
   props, outputs, description)``

   **ceilometer()**

   **check()**

      Checks that the physical resource is in its expected state.

      Gets the current status of the physical resource and updates the
      database accordingly.  If check is not supported by the
      resource, default action is to fail and revert the resource's
      status to its original state with the added message that check
      was not performed.

   **cinder()**

   **clear_hook(hook)**

   **client(name=None)**

   **client_plugin(name=None)**

   **create(*args, **kwargs)**

      Create the resource.

      Subclasses should provide a handle_create() method to customise
      creation.

   **create_convergence(template_id, resource_data, engine_id,
   timeout)**

      Creates the resource by invoking the scheduler TaskRunner.

   **data()**

      Return the resource data for this resource.

      Use methods data_set and data_delete to modify the resource data
      for this resource.

      :Returns:
         a dict representing the resource data for this resource.

   **data_delete(key)**

      Remove a key from the resource data.

      :Returns:
         True if the key existed to delete.

   **data_set(key, value, redact=False)**

      Set a key in the resource data.

   ``default_client_name = None``

   **delete(*args, **kwargs)**

      A task to delete the resource.

      Subclasses should provide a handle_delete() method to customise
      deletion.

   **delete_convergence(template_id, input_data, engine_id, timeout)**

      Destroys the resource if it doesn't belong to given template.

      The given template is suppose to be the current template being
      provisioned.

      Also, since this resource is visited as part of clean-up phase,
      the needed_by should be updated. If this resource was replaced
      by more recent resource, then delete this and update the
      replacement resource's needed_by and replaces fields.

   **delete_snapshot(*args, **kwargs)**

   **dep_attrs(resource_name)**

   **destroy(*args, **kwargs)**

      A task to delete the resource and remove it from the database.

   ``entity = None``

   **frozen_definition()**

   **get_reference_id()**

   **glance()**

   **handle_adopt(resource_data=None)**

   **handle_delete()**

      Default implementation; should be overridden by resources.

   **handle_update(json_snippet=None, tmpl_diff=None,
   prop_diff=None)**

   **has_hook(hook)**

   **has_interface(resource_type)**

      Check if resource is mapped to resource_type or is
      "resource_type".

      Check to see if this resource is either mapped to resource_type
      or is a "resource_type".

   **has_nested()**

   **heat()**

   **identifier()**

      Return an identifier for this resource.

   **implementation_signature()**

      Return a tuple defining the implementation.

      This should be broken down into a definition and an
      implementation version.

   ``classmethod is_service_available(context)``

   **is_using_neutron()**

   **keystone()**

   ``classmethod load(context, resource_id, is_update, data)``

   **lock(*args, **kwds)**

   **make_replacement(new_tmpl_id)**

   **metadata_get(refresh=False)**

   **metadata_set(metadata)**

   **metadata_update(new_metadata=None)**

      No-op for resources which don't explicitly override this method.

   **neutron()**

   ``no_signal_actions = ('SUSPEND', 'DELETE')``

   **nova()**

   **parsed_template(section=None, default=None)**

      Return the parsed template data for the resource.

      May be limited to only one section of the data, in which case a
      default value may also be supplied.

   **physical_resource_name()**

   ``physical_resource_name_limit = 255``

   **physical_resource_name_or_FnGetRefId()**

   **prepare_abandon()**

   **prepare_for_replace()**

      Prepare resource for replacing.

      Some resources requires additional actions before replace them.
      If resource need to be changed before replacing, this method
      should be implemented in resource class.

   **preview()**

      Default implementation of Resource.preview.

      This method should be overridden by child classes for specific
      behavior.

   ``static reduce_physical_resource_name(name, limit)``

      Reduce length of physical resource name to a limit.

      The reduced name will consist of the following:

      * the first 2 characters of the name

      * a hyphen

      * the end of the name, truncated on the left to bring the name
        length within the limit

      :Parameters:
         * **name** -- The name to reduce the length of

         * **limit** -- The max length limit

      :Returns:
         A name whose length is less than or equal to the limit

   **regenerate_info_schema(definition)**

      Default implementation; should be overridden by resources.

      Should be overridden by resources that would require schema
      refresh during update, ex. TemplateResource.

      :Definition:
         Resource Definition

   **reparse()**

   **required_by()**

      List of resources that require this one as a dependency.

      Returns a list of names of resources that depend on this
      resource directly.

   ``required_service_extension = None``

   ``requires_deferred_auth = False``

   **resource_class()**

      Return the resource class.

      This is used to compare old and new resources when updating, to
      ensure that in-place updates are possible. This method shold
      return the highest common class in the hierarchy whose
      subclasses are all capable of converting to each other's types
      via handle_update().

      This mechanism may disappear again in future, so third-party
      resource types should not rely on it.

   **resource_id_set(inst)**

   ``classmethod resource_to_template(resource_type,
   template_type='cfn')``

      Generate a provider template that mirrors the resource.

      :Parameters:
         * **resource_type** -- The resource type to be displayed in
           the template

         * **template_type** -- the template type to generate, cfn or
           hot.

      :Returns:
         A template where the resource's properties_schema is mapped
         as parameters, and the resource's attributes_schema is mapped
         as outputs

   **restore_prev_rsrc(convergence=False)**

      Restore resource after rollback.

      Some resources requires additional actions after rollback. If
      resource need to be changed during rollback, this method should
      be implemented in resource class.

   **resume()**

      Return a task to resume the resource.

      Subclasses should provide a handle_resume() method to implement
      resume.

   **rpc_client()**

      Return a client for making engine RPC calls.

   ``classmethod set_needed_by(db_rsrc, needed_by,
   expected_engine_id=None)``

   ``classmethod set_requires(db_rsrc, requires)``

   **signal(details=None, need_check=True)**

      Signal the resource.

      Subclasses should provide a handle_signal() method to implement
      the signal. The base-class raise an exception if no handler is
      implemented.

   ``signal_needs_metadata_updates = True``

   **snapshot()**

      Snapshot the resource and return the created data, if any.

   ``stack``

   ``state``

      Returns state, tuple of action, status.

   **state_reset()**

      Reset state to (INIT, COMPLETE).

   **state_set(action, status, reason='state changed')**

   ``strict_dependency = True``

   ``support_status = <heat.engine.support.SupportStatus object at
   0x7f7147574390>``

   **suspend()**

      Return a task to suspend the resource.

      Subclasses should provide a handle_suspend() method to implement
      suspend.

   **swift()**

   **translate_properties()**

      Translates old properties to new ones.

   **translation_rules()**

      Return specified rules for resource.

   **trigger_hook(hook)**

   **trove()**

   **type()**

   **update(*args, **kwargs)**

      Return a task to update the resource.

      Subclasses should provide a handle_update() method to customise
      update, the base-class handle_update will fail by default.

   ``update_allowed_properties = ()``

   **update_convergence(template_id, resource_data, engine_id,
   timeout)**

      Update the resource synchronously.

      Persist the resource's current_template_id to template_id and
      resource's requires to list of the required resource ids from
      the given resource_data and existing resource's requires, then
      updates the resource by invoking the scheduler TaskRunner.

   ``update_policy_schema = {}``

   **update_template_diff(after, before)**

      Returns the difference between the before and after json
      snippets.

      If something has been removed in after which exists in before we
      set it to None.

   **update_template_diff_properties(after_props, before_props)**

      Return changed Properties between the before and after
      properties.

      If any property having immutable as True is updated, raises
      NotSupported error. If any properties have changed which are not
      in update_allowed_properties, raises UpdateReplace.

   **validate()**

      Validate the resource.

      This may be overridden by resource plugins to add extra
      validation logic specific to the resource implementation.

   ``classmethod validate_deletion_policy(policy)``

   **validate_template()**

      Validate structural/syntax aspects of the resource definition.

      Resource plugins should not override this, because this
      interface is expected to be called pre-create so things normally
      valid in an overridden validate() such as accessing properties
      may not work.
