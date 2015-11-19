
The `heat.api.openstack.v1.events <../../api/heat.api.openstack.v1.events.rst#module-heat.api.openstack.v1.events>`_ Module
===========================================================================================================================

**class heat.api.openstack.v1.events.EventController(options)**

   Bases: ``object``

   WSGI controller for Events in Heat v1 API.

   Implements the API actions.

   ``REQUEST_SCOPE = 'events'``

   **index(controller, req, tenant_id, **kwargs)**

      Lists summary information for all events.

   **show(controller, req, tenant_id, **kwargs)**

      Gets detailed information for an event.

**heat.api.openstack.v1.events.create_resource(options)**

   Events resource factory method.

**heat.api.openstack.v1.events.format_event(req, event, keys=None)**
