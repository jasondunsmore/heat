
The `heat.rpc.client <../../api/heat.rpc.client.rst#module-heat.rpc.client>`_ Module
====================================================================================

Client side of the heat engine RPC API.

**class heat.rpc.client.EngineClient**

   Bases: ``object``

   Client side of the heat engine rpc API.

   API version history:

   ::

      1.0 - Initial version.
      1.1 - Add support_status argument to list_resource_types()
      1.4 - Add support for service list
      1.9 - Add template_type option to generate_template()
      1.10 - Add support for software config list
      1.11 - Add support for template versions list
      1.12 - Add with_detail option for stack resources list
      1.13 - Add support for template functions list
      1.14 - Add cancel_with_rollback option to stack_cancel_update
      1.15 - Add preview_update_stack() call
      1.16 - Adds version, type_name to list_resource_types()
      1.17 - Add files to validate_template
      1.18 - Add show_nested to validate_template

   ``BASE_RPC_API_VERSION = '1.0'``

   **abandon_stack(ctxt, stack_identity)**

      Deletes a given stack but resources would not be deleted.

      :Parameters:
         * **ctxt** -- RPC context.

         * **stack_identity** -- Name of the stack you want to
           abandon.

   **authenticated_to_backend(ctxt)**

      Validate the credentials in the RPC context.

      Verify that the credentials in the RPC context are valid for the
      current cloud backend.

      :Parameters:
         **ctxt** -- RPC context.

   **call(ctxt, msg, version=None)**

   **cast(ctxt, msg, version=None)**

   **count_stacks(ctxt, filters=None, tenant_safe=True,
   show_deleted=False, show_nested=False, show_hidden=False,
   tags=None, tags_any=None, not_tags=None, not_tags_any=None)**

      Returns the number of stacks that match the given filters.

      :Parameters:
         * **ctxt** -- RPC context.

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

   **create_software_config(cnxt, group, name, config, inputs=None,
   outputs=None, options=None)**

   **create_software_deployment(cnxt, server_id, config_id=None,
   input_values=None, action='INIT', status='COMPLETE',
   status_reason='', stack_user_project_id=None)**

   **create_stack(ctxt, stack_name, template, params, files, args)**

      Creates a new stack using the template provided.

      Note that at this stage the template has already been fetched
      from the heat-api process if using a template-url.

      :Parameters:
         * **ctxt** -- RPC context.

         * **stack_name** -- Name of the stack you want to create.

         * **template** -- Template of stack you want to create.

         * **params** -- Stack Input Params/Environment

         * **files** -- files referenced from the environment.

         * **args** -- Request parameters/args passed from API

   **create_watch_data(ctxt, watch_name, stats_data)**

      Creates data for CloudWatch and WaitConditions.

      This could be used by CloudWatch and WaitConditions and treat HA
      service events like any other CloudWatch.

      :Parameters:
         * **ctxt** -- RPC context.

         * **watch_name** -- Name of the watch/alarm

         * **stats_data** -- The data to post.

   **delete_snapshot(cnxt, stack_identity, snapshot_id)**

   **delete_software_config(cnxt, config_id)**

   **delete_software_deployment(cnxt, deployment_id)**

   **delete_stack(ctxt, stack_identity, cast=True)**

      Deletes a given stack.

      :Parameters:
         * **ctxt** -- RPC context.

         * **stack_identity** -- Name of the stack you want to delete.

         * **cast** -- cast the message or use call (default: True)

   **describe_stack_resource(ctxt, stack_identity, resource_name,
   with_attr=None)**

      Get detailed resource information about a particular resource.

      :Parameters:
         * **ctxt** -- RPC context.

         * **stack_identity** -- Name of the stack.

         * **resource_name** -- the Resource.

   **describe_stack_resources(ctxt, stack_identity, resource_name)**

      Get detailed resource information about one or more resources.

      :Parameters:
         * **ctxt** -- RPC context.

         * **stack_identity** -- Name of the stack.

         * **resource_name** -- the Resource.

   **find_physical_resource(ctxt, physical_resource_id)**

      Return an identifier for the resource.

      :param ctxt RPC context. :param physcial_resource_id The
      physical resource ID to look up.

   **generate_template(ctxt, type_name, template_type='cfn')**

      Generate a template based on the specified type.

      :Parameters:
         * **ctxt** -- RPC context.

         * **type_name** -- The resource type name to generate a
           template for.

         * **template_type** -- the template type to generate, cfn or
           hot.

   **get_revision(ctxt)**

   **get_template(ctxt, stack_identity)**

      Get the template.

      :Parameters:
         * **ctxt** -- RPC context.

         * **stack_name** -- Name of the stack you want to see.

   **identify_stack(ctxt, stack_name)**

      Returns the full stack identifier for a single, live stack.

      :Parameters:
         * **ctxt** -- RPC context.

         * **stack_name** -- Name of the stack you want to see, or
           None to see all

   **ignore_error_named(error, name)**

      Raises the error unless its local name matches the supplied
      name.

      :Parameters:
         * **error** -- Remote raised error to derive the local name
           from.

         * **name** -- Name to compare local name to.

   **list_events(ctxt, stack_identity, filters=None, limit=None,
   marker=None, sort_keys=None, sort_dir=None)**

      Lists all events associated with a given stack.

      It supports pagination (``limit`` and ``marker``), sorting
      (``sort_keys`` and ``sort_dir``) and filtering(filters) of the
      results.

      :Parameters:
         * **ctxt** -- RPC context.

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

   **list_resource_types(ctxt, support_status=None, type_name=None,
   heat_version=None)**

      Get a list of valid resource types.

      :Parameters:
         * **ctxt** -- RPC context.

         * **support_status** -- Support status of resource type

         * **type_name** -- Resource type's name (regular expression
           allowed)

         * **version** -- Heat version

   **list_services(cnxt)**

   **list_software_configs(cnxt, limit=None, marker=None,
   tenant_safe=True)**

   **list_software_deployments(cnxt, server_id=None)**

   **list_stack_resources(ctxt, stack_identity, nested_depth=0,
   with_detail=False)**

      List the resources belonging to a stack.

      :Parameters:
         * **ctxt** -- RPC context.

         * **stack_identity** -- Name of the stack.

         * **nested_depth** -- Levels of nested stacks of which list
           resources.

         * **with_detail** -- show detail for resoruces in list.

   **list_stacks(ctxt, limit=None, marker=None, sort_keys=None,
   sort_dir=None, filters=None, tenant_safe=True, show_deleted=False,
   show_nested=False, show_hidden=False, tags=None, tags_any=None,
   not_tags=None, not_tags_any=None)**

      Returns attributes of all stacks.

      It supports pagination (``limit`` and ``marker``), sorting
      (``sort_keys`` and ``sort_dir``) and filtering (``filters``) of
      the results.

      :Parameters:
         * **ctxt** -- RPC context.

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
         a list of stacks

   **list_template_functions(ctxt, template_version)**

      Get a list of available functions in a given template.

      :Parameters:
         **ctxt** -- RPC context

      :param template_name : name of the template which function list
      you
         want to get

   **list_template_versions(ctxt)**

      Get a list of available template versions.

      :Parameters:
         **ctxt** -- RPC context.

   **local_error_name(error)**

      Returns the name of the error with any _Remote postfix removed.

      :Parameters:
         **error** -- Remote raised error to derive the name from.

   ``static make_msg(method, **kwargs)``

   **metadata_software_deployments(cnxt, server_id)**

   **preview_stack(ctxt, stack_name, template, params, files, args)**

      Simulates a new stack using the provided template.

      Note that at this stage the template has already been fetched
      from the heat-api process if using a template-url.

      :Parameters:
         * **ctxt** -- RPC context.

         * **stack_name** -- Name of the stack you want to create.

         * **template** -- Template of stack you want to create.

         * **params** -- Stack Input Params/Environment

         * **files** -- files referenced from the environment.

         * **args** -- Request parameters/args passed from API

   **preview_update_stack(ctxt, stack_identity, template, params,
   files, args)**

      Returns the resources that would be changed in an update.

      Based on the provided template and parameters.

      Requires RPC version 1.15 or above.

      :Parameters:
         * **ctxt** -- RPC context.

         * **stack_identity** -- Name of the stack you wish to update.

         * **template** -- New template for the stack.

         * **params** -- Stack Input Params/Environment

         * **files** -- files referenced from the environment.

         * **args** -- Request parameters/args passed from API

   **resource_schema(ctxt, type_name)**

      Get the schema for a resource type.

      :Parameters:
         **ctxt** -- RPC context.

   **resource_signal(ctxt, stack_identity, resource_name, details,
   sync_call=False)**

      Generate an alarm on the resource.

      :Parameters:
         * **ctxt** -- RPC context.

         * **stack_identity** -- Name of the stack.

         * **resource_name** -- the Resource.

         * **details** -- the details of the signal.

   **set_watch_state(ctxt, watch_name, state)**

      Temporarily set the state of a given watch.

      :Parameters:
         * **ctxt** -- RPC context.

         * **watch_name** -- Name of the watch

         * **state** -- State (must be one defined in WatchRule class)

   **show_snapshot(cnxt, stack_identity, snapshot_id)**

   **show_software_config(cnxt, config_id)**

   **show_software_deployment(cnxt, deployment_id)**

   **show_stack(ctxt, stack_identity)**

      Returns detailed information about one or all stacks.

      :Parameters:
         * **ctxt** -- RPC context.

         * **stack_identity** -- Name of the stack you want to show,
           or None to

      show all

   **show_watch(ctxt, watch_name)**

      Returns the attributes of one watch/alarm.

      The show_watch method returns the attributes of one watch or all
      watches if no watch_name is passed.

      :Parameters:
         * **ctxt** -- RPC context.

         * **watch_name** -- Name of the watch/alarm you want to see,
           or None to see all

   **show_watch_metric(ctxt, metric_namespace=None,
   metric_name=None)**

      Returns the datapoints for a metric.

      The show_watch_metric method returns the datapoints associated
      with a specified metric, or all metrics if no metric_name is
      passed.

      :Parameters:
         * **ctxt** -- RPC context.

         * **metric_namespace** -- Name of the namespace you want to
           see, or None to see all

         * **metric_name** -- Name of the metric you want to see, or
           None to see all

   **signal_software_deployment(cnxt, deployment_id, details,
   updated_at=None)**

   **stack_cancel_update(ctxt, stack_identity,
   cancel_with_rollback=True)**

   **stack_check(ctxt, stack_identity)**

   **stack_list_snapshots(cnxt, stack_identity)**

   **stack_restore(cnxt, stack_identity, snapshot_id)**

   **stack_resume(ctxt, stack_identity)**

   **stack_snapshot(ctxt, stack_identity, name)**

   **stack_suspend(ctxt, stack_identity)**

   **update_software_deployment(cnxt, deployment_id, config_id=None,
   input_values=None, output_values=None, action=None, status=None,
   status_reason=None, updated_at=None)**

   **update_stack(ctxt, stack_identity, template, params, files,
   args)**

      Updates an existing stack based on the provided template and
      params.

      Note that at this stage the template has already been fetched
      from the heat-api process if using a template-url.

      :Parameters:
         * **ctxt** -- RPC context.

         * **stack_name** -- Name of the stack you want to create.

         * **template** -- Template of stack you want to create.

         * **params** -- Stack Input Params/Environment

         * **files** -- files referenced from the environment.

         * **args** -- Request parameters/args passed from API

   **validate_template(ctxt, template, params=None, files=None,
   show_nested=False)**

      Uses the stack parser to check the validity of a template.

      :Parameters:
         * **ctxt** -- RPC context.

         * **template** -- Template of stack you want to create.

         * **params** -- Stack Input Params/Environment

         * **files** -- files referenced from the
           environment/template.

         * **show_nested** -- if True nested templates will be
           validated
