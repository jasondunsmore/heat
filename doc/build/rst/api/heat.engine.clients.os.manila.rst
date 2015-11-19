
The ``heat.engine.clients.os.manila`` Module
============================================

**class heat.engine.clients.os.manila.ManilaClientPlugin(context)**

   Bases: `heat.engine.clients.client_plugin.ClientPlugin
   <heat.engine.clients.client_plugin.rst#heat.engine.clients.client_plugin.ClientPlugin>`_

   ``SHARE = 'share'``

   ``exceptions_module = <module 'manilaclien ...
   aclient/exceptions.py'>``

   **get_security_service(service_identity)**

   **get_share_network(share_network_identity)**

   **get_share_snapshot(snapshot_identity)**

   **get_share_type(share_type_identity)**

   **is_conflict(ex)**

   **is_not_found(ex)**

   **is_over_limit(ex)**

   ``service_types = ['share']``

**class heat.engine.clients.os.manila.ManilaShareBaseConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class 'manilaclien ...
   ptions.NoUniqueMatch'>)``

   **validate_with_client(client, resource_id)**

**class heat.engine.clients.os.manila.ManilaShareNetworkConstraint**

   Bases: ``heat.engine.clients.os.manila.ManilaShareBaseConstraint``

   ``resource_getter_name = 'get_share_network'``

**class heat.engine.clients.os.manila.ManilaShareSnapshotConstraint**

   Bases: ``heat.engine.clients.os.manila.ManilaShareBaseConstraint``

   ``resource_getter_name = 'get_share_snapshot'``

**class heat.engine.clients.os.manila.ManilaShareTypeConstraint**

   Bases: ``heat.engine.clients.os.manila.ManilaShareBaseConstraint``

   ``resource_getter_name = 'get_share_type'``
