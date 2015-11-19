
The ``heat.engine.stack`` Module
================================

**exception heat.engine.stack.ForcedCancel(with_rollback=True)**

   Bases: ``exceptions.BaseException``

   Exception raised to cancel task execution.

**class heat.engine.stack.Stack(context, stack_name, tmpl,
stack_id=None, action=None, status=None, status_reason='',
timeout_mins=None, resolve_data=True, disable_rollback=True,
parent_resource=None, owner_id=None, adopt_stack_data=None,
stack_user_project_id=None, created_time=None, updated_time=None,
user_creds_id=None, tenant_id=None, use_stored_context=False,
username=None, nested_depth=0, strict_validate=True,
convergence=False, current_traversal=None, tags=None,
prev_raw_template_id=None, current_deps=None, cache_data=None,
resource_validate=True)**

   Bases: ``_abcoll.Mapping``

   ``ACTIONS = ('CREATE', 'DELETE', ... T', 'CHECK', 'RESTORE')``

   ``ADOPT = 'ADOPT'``

   ``CHECK = 'CHECK'``

   ``COMPLETE = 'COMPLETE'``

   ``CREATE = 'CREATE'``

   ``DELETE = 'DELETE'``

   ``FAILED = 'FAILED'``

   ``IN_PROGRESS = 'IN_PROGRESS'``

   ``RESTORE = 'RESTORE'``

   ``RESUME = 'RESUME'``

   ``ROLLBACK = 'ROLLBACK'``

   ``SNAPSHOT = 'SNAPSHOT'``

   ``STATUSES = ('IN_PROGRESS', 'FAILED', 'COMPLETE')``

   ``SUSPEND = 'SUSPEND'``

   ``UPDATE = 'UPDATE'``

   **access_allowed(credential_id, resource_name)**

      Is credential_id authorised to access resource by resource_name.

   **add_resource(resource)**

      Insert the given resource into the stack.

   **adopt(*args, **kwargs)**

      Adopt existing resources into a new stack.

   **cache_data_reference_id(resource_name)**

   **cache_data_resource_all_attributes(resource_name)**

   **cache_data_resource_attribute(resource_name, attribute_key)**

   **check(*args, **kwargs)**

   **converge_stack(*args, **kwargs)**

      Update the stack template and trigger convergence for resources.

   ``convergence_dependencies``

   **create(*args, **kwargs)**

      Create the stack and all of the resources.

   **create_stack_user_project_id(*args, **kwargs)**

   **db_resource_get(name)**

   **delete(*args, **kwargs)**

      Delete all of the resources, and then the stack itself.

      The action parameter is used to differentiate between a user
      initiated delete and an automatic stack rollback after a failed
      create, which amount to the same thing, but the states are
      recorded differently.

      Note abandon is a delete where all resources have been set to a
      RETAIN deletion policy, but we also don't want to delete
      anything required for those resources, e.g the
      stack_user_project.

   **delete_snapshot(*args, **kwargs)**

      Remove a snapshot from the backends.

   ``dependencies``

   ``env``

      This is a helper to allow resources to access stack.env.

   **get_availability_zones()**

   ``static get_dep_attrs(resources, outputs, resource_name)``

      Return the attributes of the specified resource that are
      referenced.

      Return an iterator over any attributes of the specified resource
      that are referenced.

   **get_kwargs_for_cloning(keep_status=False, only_db=False)**

      Get common kwargs for calling Stack() for cloning.

      The point of this method is to reduce the number of places that
      we need to update when a kwarg to Stack.__init__() is modified.
      It is otherwise easy to forget an option and cause some
      unexpected error if this option is lost.

      Note: - This doesn't return the args(name, template) but only
      the kwargs. - We often want to start 'fresh' so don't want to
      maintain the old

      status, action and status_reason.

      * We sometimes only want the DB attributes.

   **has_cache_data(resource_name)**

   **has_timed_out()**

      Returns True if this stack has timed-out.

   **identifier()**

      Return an identifier for this stack.

   **iter_resources(nested_depth=0)**

      Iterates over all the resources in a stack.

      Iterating includes nested stacks up to *nested_depth* levels
      below.

   ``classmethod load(context, stack_id=None, stack=None,
   show_deleted=True, use_stored_context=False, force_reload=False,
   cache_data=None)``

      Retrieve a Stack from the database.

   ``classmethod load_all(context, limit=None, marker=None,
   sort_keys=None, sort_dir=None, filters=None, tenant_safe=True,
   show_deleted=False, resolve_data=True, show_nested=False,
   show_hidden=False, tags=None, tags_any=None, not_tags=None,
   not_tags_any=None)``

   **mark_complete(traversal_id)**

      Mark the update as complete.

      This currently occurs when all resources have been updated;
      there may still be resources being cleaned up, but the Stack
      should now be in service.

   **object_path_in_stack()**

      Return stack resources and stacks in path from the root stack.

      If this is not nested return (None, self), else return stack
      resources and stacks in path from the root stack and including
      this stack.

      :Returns:
         a list of (stack_resource, stack) tuples.

   **output(*args, **kwargs)**

      Get the value of the specified stack output.

   ``parent_resource``

      Dynamically load up the parent_resource.

      Note: this should only be used by "Fn::ResourceFacade"

   **path_in_stack()**

      Return tuples of names in path from the root stack.

      If this is not nested return (None, self.name), else return
      tuples of names (stack_resource.name, stack.name) in path from
      the root stack and including this stack.

      :Returns:
         a list of (string, string) tuples.

   **persist_state_and_release_lock(engine_id)**

      Persist stack state to database and release stack lock

   **prepare_abandon(*args, **kwargs)**

   **preview_resources()**

      Preview the stack with all of the resources.

   **purge_db()**

      Cleanup database after stack has completed/failed.

      1. Delete previous raw template if stack completes successfully.

      2. Deletes all sync points. They are no longer needed after
         stack has completed/failed.

      3. Delete the stack if the action is DELETE.

   **register_access_allowed_handler(credential_id, handler)**

      Register an authorization handler function.

      Register a function which determines whether the credentials
      with a given ID can have access to a named resource.

   **remove_resource(resource_name)**

      Remove the resource with the specified name.

   **requires_deferred_auth()**

      Determine whether to perform API requests with deferred auth.

      Returns whether this stack may need to perform API requests
      during its lifecycle using the configured deferred
      authentication method.

   **reset_dependencies()**

   **reset_resource_attributes()**

   **resolve_static_data(snippet)**

   **resource_by_refid(refid)**

      Return the resource in this stack with the specified refid.

      :Returns:
         resource in this stack with the specified refid, or None if
         not found.

   ``resources``

   **restart_resource(resource_name)**

      Restart the resource specified by resource_name.

      stop resource_name and all that depend on it start resource_name
      and all that depend on it

   **restore(*args, **kwargs)**

      Restore the given snapshot.

      Invokes handle_restore on all resources.

   **resume(*args, **kwargs)**

      Resume the stack.

      Invokes handle_resume for all stack resources.

      Waits for all resources to become RESUME_COMPLETE then declares
      the stack RESUME_COMPLETE. Note the default implementation for
      all resources is to do nothing other than move to
      RESUME_COMPLETE, so the resources must implement handle_resume
      for this to have any effect.

   **rollback()**

   **root_stack_id()**

   **set_stack_user_project_id(project_id)**

   **snapshot(*args, **kwargs)**

      Snapshot the stack, invoking handle_snapshot on all resources.

   **stack_task(*args, **kwargs)**

      A task to perform an action on the stack.

      All of the resources are traversed in forward or reverse
      dependency order.

      :param action action that should be executed with stack
      resources :param reverse defines if action on the resources need
      to be executed

      in reverse order (resources - first and then res dependencies )

      :param post_func function that need to be executed after action
      complete on the stack :param error_wait_time time to wait before
      cancelling all execution threads when an error occurred :param
      aggregate_exceptions defines if exceptions should be aggregated
      :param pre_completion_func function that need to be executed
      right before action completion. Uses stack ,action, status and
      reason as input parameters

   ``state``

      Returns state, tuple of action, status.

   **state_set(*args, **kwargs)**

      Update the stack state.

   **store(*args, **kwargs)**

      Store the stack in the database and return its ID.

      If self.id is set, we update the existing stack.

   **stored_context()**

   **supports_check_action()**

   **suspend(*args, **kwargs)**

      Suspend the stack.

      Invokes handle_suspend for all stack resources.

      Waits for all resources to become SUSPEND_COMPLETE then declares
      the stack SUSPEND_COMPLETE. Note the default implementation for
      all resources is to do nothing other than move to
      SUSPEND_COMPLETE, so the resources must implement handle_suspend
      for this to have any effect.

   **time_elapsed()**

      Time elapsed in seconds since the stack operation started.

   **time_remaining()**

      Time left before stack times out.

   **timeout_secs()**

      Return the stack action timeout in seconds.

   **total_resources(stack_id=None)**

      Return the total number of resources in a stack.

      Includes nested stacks below.

   **update(*args, **kwargs)**

      Update the stack.

      Compare the current stack with newstack, and where necessary
      create/update/delete the resources until this stack aligns with
      newstack.

      Note update of existing stack resources depends on update being
      implemented in the underlying resource types

      Update will fail if it exceeds the specified timeout. The
      default is 60 minutes, set in the constructor

   **update_task(*args, **kwargs)**

   **validate(*args, **kwargs)**

      Validates the stack.

   ``worker_client``

      Return a client for making engine RPC calls.
