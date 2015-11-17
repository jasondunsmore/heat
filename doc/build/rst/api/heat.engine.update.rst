
The ``heat.engine.update`` Module
*********************************

**class heat.engine.update.StackUpdate(existing_stack, new_stack,
previous_stack, rollback=False, error_wait_time=None)**

   Bases: ``object``

   A Task to perform the update of an existing stack to a new
   template.

   **dependencies()**

      Return the Dependencies graph for the update.

      Returns a Dependencies object representing the dependencies
      between update operations to move from an existing stack
      definition to a new one.

   **preview()**
