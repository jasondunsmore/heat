
The ``heat.engine.clients.os.trove`` Module
*******************************************

**class heat.engine.clients.os.trove.FlavorConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.FlavorMissing'>,)``

   **validate_with_client(client, flavor)**

**class heat.engine.clients.os.trove.TroveClientPlugin(context)**

   Bases: `heat.engine.clients.client_plugin.ClientPlugin
   <heat.engine.clients.client_plugin.rst#heat.engine.clients.client_plugin.ClientPlugin>`_

   ``DATABASE = 'rax:database'``

   ``exceptions_module = <module 'troveclient ...
   client/exceptions.pyc'>``

   **get_flavor_id(flavor)**

      Get the ID for the specified flavor name.

      If the specified value is flavor id, just return it.

      :Parameters:
         **flavor** -- the name of the flavor to find

      :Returns:
         the id of :flavor:

      :Raises:
         exception.FlavorMissing

   **is_conflict(ex)**

   **is_not_found(ex)**

   **is_over_limit(ex)**

   ``service_types = ['rax:database']``

   **validate_datastore(datastore_type, datastore_version,
   ds_type_key, ds_version_key)**
