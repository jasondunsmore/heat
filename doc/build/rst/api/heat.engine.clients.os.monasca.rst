
The ``heat.engine.clients.os.monasca`` Module
*********************************************

**class heat.engine.clients.os.monasca.MonascaClientPlugin(context)**

   Bases: `heat.engine.clients.client_plugin.ClientPlugin
   <heat.engine.clients.client_plugin.rst#heat.engine.clients.client_plugin.ClientPlugin>`_

   ``MONITORING = 'monitoring'``

   ``VERSION = '2_0'``

   ``exceptions_module = [None]``

   **get_notification(notification)**

   ``static is_available()``

   **is_not_found(ex)**

   **is_un_processable(ex)**

   ``service_types = ['monitoring']``

**class heat.engine.clients.os.monasca.MonascaNotificationConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions``

      alias of ``EntityNotFound``

   **validate_with_client(client, notification)**
