
The `heat.engine.service <../../api/heat.engine.service.rst#module-heat.engine.service>`_ Module
================================================================================================

**class heat.engine.service.EngineListener(host, engine_id,
thread_group_mgr)**

   Bases: ``oslo_service.service.Service``

   Listen on an AMQP queue named for the engine.

   Allows individual engines to communicate with each other for
   multi-engine support.

   ``ACTIONS = ('stop_stack', 'send')``

   ``SEND = 'send'``

   ``STOP_STACK = 'stop_stack'``

   **listening(*args, **kwargs)**

      Respond to a watchdog request.

      Respond affirmatively to confirm that the engine performing the
      action is still alive.

   **reset(*args, **kwargs)**

      Reset a service in case it received a SIGHUP.

   **send(*args, **kwargs)**

   **start(*args, **kwargs)**

   **stop(*args, **kwargs)**

      Stop a service.

      :Parameters:
         **graceful** -- indicates whether to wait for all threads to
         finish or terminate them instantly

   **stop_stack(*args, **kwargs)**

      Stop any active threads on a stack.

   **wait(*args, **kwargs)**

      Wait for a service to shut down.

**class heat.engine.service.EngineService(host, topic)**

   Bases: ``oslo_service.service.Service``

   Manages the running instances from creation to destruction.

   All the methods in here are called from the RPC backend.  This is
   all done dynamically so if a call is made via RPC that does not
   have a corresponding method here, an exception will be thrown when
   it attempts to call into this class.  Arguments to these methods
   are also dynamically added and will be named as keyword arguments
   by the RPC caller.

   ``RPC_API_VERSION = '1.18'``

   **abandon_stack(*args, **kwargs)**

      Abandon a given stack.

      :Parameters:
         * **cnxt** -- RPC context.

         * **stack_identity** -- Name of the stack you want to
           abandon.

   **authenticated_to_backend(*args, **kwargs)**

      Validate the credentials in the RPC context.

      Verify that the credentials in the RPC context are valid for the
      current cloud backend.

   **count_stacks(*args, **kwargs)**

      Return the number of stacks that match the given filters.

      :Parameters:
         * **cnxt** -- RPC context.

         * **filters** -- a dict of ATTR:VALUE to match against stacks

         * **tenant_safe** -- if true, scope the request by the
           current tenant

         * **show_deleted** -- if true, count will include the deleted
           stacks

         * **show_nested** -- if true, count will include nested
           stacks

         * **show_hidden** -- if true, count will include hidden
           stacks

         * **tags** -- count stacks containing these tags, combine
           multiple tags using the boolean AND expression

         * **tags_any** -- count stacks containing these tags, combine
           multiple tags using the boolean OR expression

         * **not_tags** -- count stacks not containing these tags,
           combine multiple tags using the boolean AND expression

         * **not_tags_any** -- count stacks not containing these tags,
           combine multiple tags using the boolean OR expression

      :Returns:
         a integer representing the number of matched stacks

   **create_periodic_tasks(*args, **kwargs)**

   **create_software_config(*args, **kwargs)**

   **create_software_deployment(*args, **kwargs)**

   **create_stack(*args, **kwargs)**

      Create a new stack using the template provided.

      Note that at this stage the template has already been fetched
      from the heat-api process if using a template-url.

      :Parameters:
         * **cnxt** -- RPC context.

         * **stack_name** -- Name of the stack you want to create.

         * **template** -- Template of stack you want to create.

         * **params** -- Stack Input Params

         * **files** -- Files referenced from the template

         * **args** -- Request parameters/args passed from API

         * **owner_id** -- parent stack ID for nested stacks, only
           expected when called from another heat-engine (not a user
           option)

         * **nested_depth** -- the nested depth for nested stacks,
           only expected when called from another heat-engine

         * **user_creds_id** -- the parent user_creds record for
           nested stacks

         * **stack_user_project_id** -- the parent
           stack_user_project_id for nested stacks

         * **parent_resource_name** -- the parent resource name

   **create_watch_data(*args, **kwargs)**

      Creates data for CloudWatch and WaitConditions.

      This could be used by CloudWatch and WaitConditions and treat HA
      service events like any other CloudWatch.

   **delete_snapshot(*args, **kwargs)**

   **delete_software_config(*args, **kwargs)**

   **delete_software_deployment(*args, **kwargs)**

   **delete_stack(*args, **kwargs)**

      Delete a given stack.

      :Parameters:
         * **cnxt** -- RPC context.

         * **stack_identity** -- Name of the stack you want to delete.

   **describe_stack_resource(*args, **kwargs)**

   **describe_stack_resources(*args, **kwargs)**

   **find_physical_resource(*args, **kwargs)**

      Return an identifier for the specified resource.

      :Parameters:
         * **cnxt** -- RPC context.

         * **physical_resource_id** -- The physical resource ID to
           look up.

   **generate_template(*args, **kwargs)**

      Generate a template based on the specified type.

      :Parameters:
         * **cnxt** -- RPC context.

         * **type_name** -- Name of the resource type to generate a
           template for.

         * **template_type** -- the template type to generate, cfn or
           hot.

   **get_revision(*args, **kwargs)**

   **get_template(*args, **kwargs)**

      Get the template.

      :Parameters:
         * **cnxt** -- RPC context.

         * **stack_identity** -- Name of the stack you want to see.

   **identify_stack(*args, **kwargs)**

      The full stack identifier for a single, live stack with
      stack_name.

      :Parameters:
         * **cnxt** -- RPC context.

         * **stack_name** -- Name or UUID of the stack to look up.

   **list_events(*args, **kwargs)**

      Lists all events associated with a given stack.

      It supports pagination (``limit`` and ``marker``), sorting
      (``sort_keys`` and ``sort_dir``) and filtering(filters) of the
      results.

      :Parameters:
         * **cnxt** -- RPC context.

         * **stack_identity** -- Name of the stack you want to get
           events for

         * **filters** -- a dict with attribute:value to filter the
           list

         * **limit** -- the number of events to list (integer or
           string)

         * **marker** -- the ID of the last event in the previous page

         * **sort_keys** -- an array of fields used to sort the list

         * **sort_dir** -- the direction of the sort ('asc' or
           'desc').

   **list_resource_types(*args, **kwargs)**

      Get a list of supported resource types.

      :Parameters:
         * **cnxt** -- RPC context.

         * **support_status** -- Support status of resource type

         * **type_name** -- Resource type's name (regular expression
           allowed)

         * **heat_version** -- Heat version

   **list_services(*args, **kwargs)**

   **list_software_configs(*args, **kwargs)**

   **list_software_deployments(*args, **kwargs)**

   **list_stack_resources(*args, **kwargs)**

   **list_stacks(*args, **kwargs)**

      Returns attributes of all stacks.

      It supports pagination (``limit`` and ``marker``), sorting
      (``sort_keys`` and ``sort_dir``) and filtering (``filters``) of
      the results.

      :Parameters:
         * **cnxt** -- RPC context

         * **limit** -- the number of stacks to list (integer or
           string)

         * **marker** -- the ID of the last item in the previous page

         * **sort_keys** -- an array of fields used to sort the list

         * **sort_dir** -- the direction of the sort ('asc' or 'desc')

         * **filters** -- a dict with attribute:value to filter the
           list

         * **tenant_safe** -- if true, scope the request by the
           current tenant

         * **show_deleted** -- if true, show soft-deleted stacks

         * **show_nested** -- if true, show nested stacks

         * **show_hidden** -- if true, show hidden stacks

         * **tags** -- show stacks containing these tags, combine
           multiple tags using the boolean AND expression

         * **tags_any** -- show stacks containing these tags, combine
           multiple tags using the boolean OR expression

         * **not_tags** -- show stacks not containing these tags,
           combine multiple tags using the boolean AND expression

         * **not_tags_any** -- show stacks not containing these tags,
           combine multiple tags using the boolean OR expression

      :Returns:
         a list of formatted stacks

   **list_template_functions(*args, **kwargs)**

   **list_template_versions(*args, **kwargs)**

   **metadata_software_deployments(*args, **kwargs)**

   **preview_stack(*args, **kwargs)**

      Simulate a new stack using the provided template.

      Note that at this stage the template has already been fetched
      from the heat-api process if using a template-url.

      :Parameters:
         * **cnxt** -- RPC context.

         * **stack_name** -- Name of the stack you want to create.

         * **template** -- Template of stack you want to create.

         * **params** -- Stack Input Params

         * **files** -- Files referenced from the template

         * **args** -- Request parameters/args passed from API

   **preview_update_stack(*args, **kwargs)**

      Show the resources that would be updated.

      The preview_update_stack method shows the resources that would
      be changed with an update to an existing stack based on the
      provided template and parameters. See update_stack for
      description of parameters.

      This method *cannot* guarantee that an update will have the
      actions specified because resource plugins can influence
      changes/replacements at runtime.

      Note that at this stage the template has already been fetched
      from the heat-api process if using a template-url.

   **reset(*args, **kwargs)**

   **reset_stack_status(*args, **kwargs)**

   **resource_schema(*args, **kwargs)**

      Return the schema of the specified type.

      :Parameters:
         * **cnxt** -- RPC context.

         * **type_name** -- Name of the resource type to obtain the
           schema of.

   **resource_signal(*args, **kwargs)**

      Calls resource's signal for the specified resource.

      :Parameters:
         **sync_call** -- indicates whether a synchronized call
         behavior is expected. This is reserved for CFN WaitCondition
         implementation.

   **service_manage_cleanup(*args, **kwargs)**

   **service_manage_report(*args, **kwargs)**

   **set_stack_and_resource_to_failed(*args, **kwargs)**

   **set_watch_state(*args, **kwargs)**

      Temporarily set the state of a given watch.

      :Parameters:
         * **cnxt** -- RPC context.

         * **watch_name** -- Name of the watch.

         * **state** -- State (must be one defined in WatchRule class.

   **show_snapshot(*args, **kwargs)**

   **show_software_config(*args, **kwargs)**

   **show_software_deployment(*args, **kwargs)**

   **show_stack(*args, **kwargs)**

      Return detailed information about one or all stacks.

      :Parameters:
         * **cnxt** -- RPC context.

         * **stack_identity** -- Name of the stack you want to show,
           or None to show all

   **show_watch(*args, **kwargs)**

      Return the attributes of one watch/alarm.

      :Parameters:
         * **cnxt** -- RPC context.

         * **watch_name** -- Name of the watch you want to see, or
           None to see all.

   **show_watch_metric(*args, **kwargs)**

      Return the datapoints for a metric.

      :Parameters:
         * **cnxt** -- RPC context.

         * **metric_namespace** -- Name of the namespace you want to
           see, or None to see all.

         * **metric_name** -- Name of the metric you want to see, or
           None to see all.

   **signal_software_deployment(*args, **kwargs)**

   **stack_cancel_update(*args, **kwargs)**

      Cancel currently running stack update.

      :Parameters:
         * **cnxt** -- RPC context.

         * **stack_identity** -- Name of the stack for which to cancel
           update.

         * **cancel_with_rollback** -- Force rollback when cancel
           update.

   **stack_check(*args, **kwargs)**

      Handle request to perform a check action on a stack.

   **stack_list_snapshots(*args, **kwargs)**

   **stack_restore(*args, **kwargs)**

   **stack_resume(*args, **kwargs)**

      Handle request to perform a resume action on a stack.

   **stack_snapshot(*args, **kwargs)**

   **stack_suspend(*args, **kwargs)**

      Handle request to perform suspend action on a stack.

   **start(*args, **kwargs)**

   **stop(*args, **kwargs)**

   **update_software_deployment(*args, **kwargs)**

   **update_stack(*args, **kwargs)**

      Update an existing stack based on the provided template and
      params.

      Note that at this stage the template has already been fetched
      from the heat-api process if using a template-url.

      :Parameters:
         * **cnxt** -- RPC context.

         * **stack_identity** -- Name of the stack you want to create.

         * **template** -- Template of stack you want to create.

         * **params** -- Stack Input Params

         * **files** -- Files referenced from the template

         * **args** -- Request parameters/args passed from API

   **validate_template(*args, **kwargs)**

      Check the validity of a template.

      Checks, so far as we can, that a template is valid, and returns
      information about the parameters suitable for producing a user
      interface through which to specify the parameter values.

      :Parameters:
         * **cnxt** -- RPC context.

         * **template** -- Template of stack you want to create.

         * **params** -- Stack Input Params

         * **files** -- Files referenced from the template

         * **show_nested** -- if True, any nested templates will be
           checked

   **wait(*args, **kwargs)**

      Wait for a service to shut down.

**class heat.engine.service.ThreadGroupManager**

   Bases: ``object``

   **add_event(stack_id, event)**

   **add_timer(stack_id, func, *args, **kwargs)**

      Define a periodic task in the stack threadgroups.

      The task is run in a separate greenthread.

      Periodicity is cfg.CONF.periodic_interval

   **remove_event(gt, stack_id, event)**

   **send(stack_id, message)**

   **start(stack_id, func, *args, **kwargs)**

      Run the given method in a sub-thread.

   **start_with_acquired_lock(stack, lock, func, *args, **kwargs)**

      Run the given method in a sub-thread with an existing stack
      lock.

      Release the provided lock when the thread finishes.

      :Parameters:
         * **stack** (*heat.engine.parser.Stack*) -- Stack to be
           operated on

         * **lock** (`heat.engine.stack_lock.StackLock
           <../../api/heat.engine.stack_lock.rst#heat.engine.stack_lock.StackLock>`_)
           -- The acquired stack lock

         * **func** (*function or instancemethod*) -- Callable to be
           invoked in sub-thread

         * **args** -- Args to be passed to func

         * **kwargs** -- Keyword-args to be passed to func

   **start_with_lock(cnxt, stack, engine_id, func, *args, **kwargs)**

      Run the method in sub-thread after acquiring the stack lock.

      Release the lock when the thread finishes.

      :Parameters:
         * **cnxt** -- RPC context

         * **stack** (*heat.engine.parser.Stack*) -- Stack to be
           operated on

         * **engine_id** -- The UUID of the engine/worker acquiring
           the lock

         * **func** (*function or instancemethod*) -- Callable to be
           invoked in sub-thread

         * **args** -- Args to be passed to func

         * **kwargs** -- Keyword-args to be passed to func.

   **stop(stack_id, graceful=False)**

      Stop any active threads on a stack.

   **stop_timers(stack_id)**
