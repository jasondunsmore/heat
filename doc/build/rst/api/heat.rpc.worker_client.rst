
The ``heat.rpc.worker_client`` Module
=====================================

Client side of the heat worker RPC API.

**class heat.rpc.worker_client.WorkerClient**

   Bases: ``object``

   Client side of the heat worker RPC API.

   API version history:

   ::

      1.0 - Initial version.
      1.1 - Added check_resource.
      1.2 - Add adopt data argument to check_resource.

   ``BASE_RPC_API_VERSION = '1.0'``

   **cast(ctxt, msg, version=None)**

   **check_resource(ctxt, resource_id, current_traversal, data,
   is_update, adopt_stack_data)**

   ``static make_msg(method, **kwargs)``
