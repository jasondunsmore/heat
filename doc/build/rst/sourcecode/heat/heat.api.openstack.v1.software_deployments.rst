
The `heat.api.openstack.v1.software_deployments <../../api/heat.api.openstack.v1.software_deployments.rst#module-heat.api.openstack.v1.software_deployments>`_ Module
=====================================================================================================================================================================

**class
heat.api.openstack.v1.software_deployments.SoftwareDeploymentController(options)**

   Bases: ``object``

   WSGI controller for Software deployments in Heat v1 API.

   Implements the API actions.

   ``REQUEST_SCOPE = 'software_deployments'``

   **create(controller, req, tenant_id, **kwargs)**

      Create a new software deployment.

   **default(req, **args)**

   **delete(controller, req, tenant_id, **kwargs)**

      Delete an existing software deployment.

   **index(controller, req, tenant_id, **kwargs)**

      List software deployments.

   **metadata(controller, req, tenant_id, **kwargs)**

      List software deployments grouped by the group name.

      This is done for the requested server.

   **show(controller, req, tenant_id, **kwargs)**

      Gets detailed information for a software deployment.

   **update(controller, req, tenant_id, **kwargs)**

      Update an existing software deployment.

**heat.api.openstack.v1.software_deployments.create_resource(options)**

   Software deployments resource factory method.
