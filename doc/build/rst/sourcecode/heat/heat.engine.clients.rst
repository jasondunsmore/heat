
The ``heat.engine.clients`` Module
**********************************

**class heat.engine.clients.ClientBackend**

   Bases: ``object``

   Class for delaying choosing the backend client module.

   Delay choosing the backend client module until the client's class
   needs to be initialized.

``heat.engine.clients.Clients``

   alias of ``ClientBackend``

**class heat.engine.clients.OpenStackClients(context)**

   Bases: ``object``

   Convenience class to create and cache client instances.

   ``auth_token``

   **client(name)**

   **client_plugin(name)**

   ``context``

**heat.engine.clients.has_client(name)**

**heat.engine.clients.initialise()**

**heat.engine.clients.list_opts()**
