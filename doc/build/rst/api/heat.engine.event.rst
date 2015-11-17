
The ``heat.engine.event`` Module
********************************

**class heat.engine.event.Event(context, stack, action, status,
reason, physical_resource_id, resource_properties, resource_name,
resource_type, uuid=None, timestamp=None, id=None)**

   Bases: ``object``

   Class representing a Resource state change.

   **identifier()**

      Return a unique identifier for the event.

   ``classmethod load(context, event_id, event=None, stack=None)``

      Retrieve an Event from the database.

   **store()**

      Store the Event in the database.
