
The `heat.api.openstack.v1.actions <../../api/heat.api.openstack.v1.actions.rst#module-heat.api.openstack.v1.actions>`_ Module
==============================================================================================================================

**class heat.api.openstack.v1.actions.ActionController(options)**

   Bases: ``object``

   WSGI controller for Actions in Heat v1 API.

   Implements the API for stack actions

   ``ACTIONS = ('suspend', 'resume', 'check', 'cancel_update')``

   ``CANCEL_UPDATE = 'cancel_update'``

   ``CHECK = 'check'``

   ``REQUEST_SCOPE = 'actions'``

   ``RESUME = 'resume'``

   ``SUSPEND = 'suspend'``

   **action(controller, req, tenant_id, **kwargs)**

      Performs a specified action on a stack.

      The body is expecting to contain exactly one item whose key
      specifies the action.

**heat.api.openstack.v1.actions.create_resource(options)**

   Actions action factory method.
