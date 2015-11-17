
The ``heat.engine.clients.os.sahara`` Module
********************************************

**class heat.engine.clients.os.sahara.ImageConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class 'heat.common ...
   esourceNameAmbiguity'>)``

   **validate_with_client(client, value)**

**class heat.engine.clients.os.sahara.PluginConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.EntityNotFound'>,)``

   **validate_with_client(client, value)**

**class heat.engine.clients.os.sahara.SaharaClientPlugin(context)**

   Bases: `heat.engine.clients.client_plugin.ClientPlugin
   <heat.engine.clients.client_plugin.rst#heat.engine.clients.client_plugin.ClientPlugin>`_

   ``DATA_PROCESSING = 'data-processing'``

   ``exceptions_module = <module 'saharaclien ...
   raclient/api/base.pyc'>``

   **get_image_id(image_identifier)**

      Return the ID for the specified image name or identifier.

      :Parameters:
         **image_identifier** -- image name or a UUID-like identifier

      :Returns:
         the id of the requested :image_identifier:

      :Raises:
         exception.EntityNotFound,
         exception.PhysicalResourceNameAmbiguity

   **get_image_id_by_name(image_identifier)**

      Return the ID for the specified image name.

      :Parameters:
         **image_identifier** -- image name

      :Returns:
         the id of the requested :image_identifier:

      :Raises:
         exception.EntityNotFound,
         exception.PhysicalResourceNameAmbiguity

   **get_plugin_id(plugin_name)**

      Get the id for the specified plugin name.

      :Parameters:
         **plugin_name** -- the name of the plugin to find

      :Returns:
         the id of :plugin:

      :Raises:
         exception.EntityNotFound

   **is_conflict(ex)**

   **is_not_found(ex)**

   **is_not_registered(ex)**

   **is_over_limit(ex)**

   ``service_types = ['data-processing']``

   **validate_hadoop_version(plugin_name, hadoop_version)**
