
The `heat.api.openstack.v1.software_configs <../../api/heat.api.openstack.v1.software_configs.rst#module-heat.api.openstack.v1.software_configs>`_ Module
=========================================================================================================================================================

**class
heat.api.openstack.v1.software_configs.SoftwareConfigController(options)**

   Bases: ``object``

   WSGI controller for Software config in Heat v1 API.

   Implements the API actions.

   ``REQUEST_SCOPE = 'software_configs'``

   **create(controller, req, tenant_id, **kwargs)**

      Create a new software config.

   **default(req, **args)**

   **delete(controller, req, tenant_id, **kwargs)**

      Delete an existing software config.

   **global_index(controller, req, tenant_id, **kwargs)**

   **index(controller, req, tenant_id, **kwargs)**

      Lists summary information for all software configs.

   **show(controller, req, tenant_id, **kwargs)**

      Gets detailed information for a software config.

**heat.api.openstack.v1.software_configs.create_resource(options)**

   Software configs resource factory method.
