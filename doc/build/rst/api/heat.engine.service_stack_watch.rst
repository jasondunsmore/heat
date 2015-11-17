
The ``heat.engine.service_stack_watch`` Module
**********************************************

**class heat.engine.service_stack_watch.StackWatch(thread_group_mgr)**

   Bases: ``object``

   **check_stack_watches(sid)**

   **periodic_watcher_task(sid)**

      Evaluate all watch-rules defined for stack ID.

      Periodic task, created for each stack, triggers watch-rule
      evaluation for all rules defined for the stack sid = stack ID.

   **start_watch_task(stack_id, cnxt)**
