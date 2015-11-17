
The ``heat.engine.clients.os.cinder`` Module
********************************************

**class heat.engine.clients.os.cinder.CinderClientPlugin(context)**

   Bases: `heat.engine.clients.client_plugin.ClientPlugin
   <heat.engine.clients.client_plugin.rst#heat.engine.clients.client_plugin.ClientPlugin>`_

   ``VOLUME = 'volume'``

   ``VOLUME_V2 = 'volumev2'``

   **check_attach_volume_complete(vol_id)**

   **check_detach_volume_complete(vol_id)**

   ``exceptions_module = <module 'cinderclien ...
   client/exceptions.pyc'>``

   **get_volume(volume)**

   **get_volume_api_version()**

      Returns the most recent API version.

   **get_volume_backup(backup)**

   **get_volume_snapshot(snapshot)**

   **get_volume_type(volume_type)**

   **is_conflict(ex)**

   **is_not_found(ex)**

   **is_over_limit(ex)**

   ``service_types = ['volume', 'volumev2']``

**class heat.engine.clients.os.cinder.VolumeBackupConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.EntityNotFound'>,)``

   **validate_with_client(client, backup)**

**class heat.engine.clients.os.cinder.VolumeConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.EntityNotFound'>,)``

   **validate_with_client(client, volume)**

**class heat.engine.clients.os.cinder.VolumeSnapshotConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.EntityNotFound'>,)``

   **validate_with_client(client, snapshot)**

**class heat.engine.clients.os.cinder.VolumeTypeConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.EntityNotFound'>,)``

   **validate_with_client(client, volume_type)**
