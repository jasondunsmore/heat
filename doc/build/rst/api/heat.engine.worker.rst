
The ``heat.engine.worker`` Module
=================================

**class heat.engine.worker.WorkerService(host, topic, engine_id,
thread_group_mgr)**

   Bases: ``oslo_service.service.Service``

   Service that has 'worker' actor in convergence.

   This service is dedicated to handle internal messages to the
   'worker' (a.k.a. 'converger') actor in convergence. Messages on
   this bus will use the 'cast' rather than 'call' method to anycast
   the message to an engine that will handle it asynchronously. It
   won't wait for or expect replies from these messages.

   ``RPC_API_VERSION = '1.2'``

   **check_resource(*args, **kwargs)**

      Process a node in the dependency graph.

      The node may be associated with either an update or a cleanup of
      its associated resource.

   **reset(*args, **kwargs)**

      Reset a service in case it received a SIGHUP.

   **start(*args, **kwargs)**

   **stop(*args, **kwargs)**

   **wait(*args, **kwargs)**

      Wait for a service to shut down.

**heat.engine.worker.check_resource_cleanup(rsrc, template_id,
resource_data, engine_id, timeout)**

   Delete the Resource if appropriate.

**heat.engine.worker.check_resource_update(rsrc, template_id,
resource_data, engine_id, timeout)**

   Create or update the Resource if appropriate.

**heat.engine.worker.check_stack_complete(cnxt, stack,
current_traversal, sender_id, deps, is_update)**

   Mark the stack complete if the update is complete.

   Complete is currently in the sense that all desired resources are
   in service, not that superfluous ones have been cleaned up.

**heat.engine.worker.construct_input_data(rsrc)**

**heat.engine.worker.propagate_check_resource(cnxt, rpc_client,
next_res_id, current_traversal, predecessors, sender_key, sender_data,
is_update, adopt_stack_data)**

   Trigger processing of node if all of its dependencies are
   satisfied.
