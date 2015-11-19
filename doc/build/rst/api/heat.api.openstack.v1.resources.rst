
The ``heat.api.openstack.v1.resources`` Module
==============================================

**class heat.api.openstack.v1.resources.ResourceController(options)**

   Bases: ``object``

   WSGI controller for Resources in Heat v1 API.

   Implements the API actions.

   ``REQUEST_SCOPE = 'resource'``

   **index(controller, req, tenant_id, **kwargs)**

      Lists information for all resources.

   **metadata(controller, req, tenant_id, **kwargs)**

      Gets metadata information for a resource.

   **show(controller, req, tenant_id, **kwargs)**

      Gets detailed information for a resource.

   **signal(controller, req, tenant_id, **kwargs)**

**heat.api.openstack.v1.resources.create_resource(options)**

   Resources resource factory method.

**heat.api.openstack.v1.resources.format_resource(req, res,
keys=None)**
