
The ``heat.engine.sync_point`` Module
=====================================

**exception heat.engine.sync_point.SyncPointNotFound(sync_point)**

   Bases: ``exceptions.Exception``

   Raised when resource update requires replacement.

**heat.engine.sync_point.create(context, entity_id, traversal_id,
is_update, stack_id)**

   Creates an sync point entry in DB.

**heat.engine.sync_point.delete_all(context, stack_id, traversal_id)**

   Deletes all sync points of a stack associated with a traversal_id.

**heat.engine.sync_point.deserialize_input_data(db_input_data)**

**heat.engine.sync_point.get(context, entity_id, traversal_id,
is_update)**

   Retrieves a sync point entry from DB.

**heat.engine.sync_point.make_key(*components)**

**heat.engine.sync_point.serialize_input_data(input_data)**

**heat.engine.sync_point.sync(cnxt, entity_id, current_traversal,
is_update, propagate, predecessors, new_data)**

**heat.engine.sync_point.update_input_data(context, entity_id,
current_traversal, is_update, atomic_key, input_data)**
