
The ``heat.engine.clients.os.nova`` Module
==========================================

**class heat.engine.clients.os.nova.FlavorConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.FlavorMissing'>,)``

   **validate_with_client(client, flavor)**

**class heat.engine.clients.os.nova.HostConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.EntityNotFound'>,)``

   **validate_with_client(client, host_name)**

**class heat.engine.clients.os.nova.KeypairConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.UserKeyPairMissing'>,)``

   **validate_with_client(client, key_name)**

**class heat.engine.clients.os.nova.NetworkConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class 'heat.common ...
   esourceNameAmbiguity'>)``

   **validate_with_client(client, network)**

**class heat.engine.clients.os.nova.NovaClientPlugin(context)**

   Bases: `heat.engine.clients.client_plugin.ClientPlugin
   <heat.engine.clients.client_plugin.rst#heat.engine.clients.client_plugin.ClientPlugin>`_

   ``COMPUTE = 'compute'``

   **absolute_limits()**

      Return the absolute limits as a dictionary.

   **attach_volume(server_id, volume_id, device)**

   **build_userdata(metadata, userdata=None, instance_user=None,
   user_data_format='HEAT_CFNTOOLS')**

      Build multipart data blob for CloudInit.

      Data blob includes user-supplied Metadata, user data, and the
      required Heat in-instance configuration.

      :Parameters:
         * **resource** (*heat.engine.Resource*) -- the resource
           implementation

         * **userdata** (*str or None*) -- user data string

         * **instance_user** (*string*) -- the user to create on the
           server

         * **user_data_format** (*string*) -- Format of user data to
           return

      :Returns:
         multipart mime as a string

   **check_delete_server_complete(server_id)**

      Wait for server to disappear from Nova.

   **check_detach_volume_complete(server_id, attach_id)**

      Check that nova server lost attachment.

      This check is needed for immediate reattachment when updating:
      there might be some time between cinder marking volume as
      'available' and nova removing attachment from its own objects,
      so we check that nova already knows that the volume is detached.

   **check_rebuild(server_id)**

      Verify that a rebuilding server is rebuilt.

      Raise error if it ends up in an ERROR state.

   **check_resize(server_id, flavor_id, flavor)**

      Verify that a resizing server is properly resized.

      If that's the case, confirm the resize, if not raise an error.

   **check_verify_resize(server_id)**

   ``deferred_server_statuses = ['BUILD', 'HARD_REBO ... NDED',
   'VERIFY_RESIZE']``

   **detach_volume(server_id, attach_id)**

   ``exceptions_module = <module 'novaclient. ...
   aclient/exceptions.py'>``

   **fetch_server(server_id)**

      Fetch fresh server object from Nova.

      Log warnings and return None for non-critical API errors. Use
      this method in various ``check_*_complete`` resource methods,
      where intermittent errors can be tolerated.

   **get_console_urls(server)**

      Return dict-like structure of server's console urls.

      The actual console url is lazily resolved on access.

   **get_flavor_id(flavor)**

      Get the id for the specified flavor name.

      If the specified value is flavor id, just return it.

      :Parameters:
         **flavor** -- the name of the flavor to find

      :Returns:
         the id of :flavor:

      :Raises:
         exception.FlavorMissing

   **get_host(host_name)**

      Get the host id specified by name.

      :Parameters:
         **host_name** -- the name of host to find

      :Returns:
         the list of match hosts

      :Raises:
         exception.EntityNotFound

   **get_ip(server, net_type, ip_version)**

      Return the server's IP of the given type and version.

   **get_keypair(key_name)**

      Get the public key specified by :key_name:

      :Parameters:
         **key_name** -- the name of the key to look for

      :Returns:
         the keypair (name, public_key) for :key_name:

      :Raises:
         exception.UserKeyPairMissing

   **get_net_id_by_label(label)**

   **get_nova_network_id(net_identifier)**

   **get_server(server)**

      Return fresh server object.

      Substitutes Nova's NotFound for Heat's EntityNotFound, to be
      returned to user as HTTP error.

   **get_status(server)**

      Return the server's status.

      :Parameters:
         **server** -- server object

      :Returns:
         status as a string

   **has_extension(alias)**

      Check if specific extension is present.

   **interface_attach(server_id, port_id=None, net_id=None,
   fip=None)**

   **interface_detach(server_id, port_id)**

   **is_bad_request(ex)**

   **is_conflict(ex)**

   **is_not_found(ex)**

   **is_over_limit(ex)**

   **is_unprocessable_entity(ex)**

   **meta_serialize(metadata)**

      Serialize non-string metadata values before sending them to
      Nova.

   **meta_update(server, metadata)**

      Delete/Add the metadata in nova as needed.

   **rebuild(server_id, image_id, password=None,
   preserve_ephemeral=False)**

      Rebuild the server and call check_rebuild to verify.

   **refresh_server(server)**

      Refresh server's attributes.

      Also log warnings for non-critical API errors.

   **rename(server, name)**

      Update the name for a server.

   **resize(server_id, flavor_id)**

      Resize the server.

   **server_to_ipaddress(server)**

      Return the server's IP address, fetching it from Nova.

   ``service_types = ['compute']``

   **verify_resize(server_id)**

**class heat.engine.clients.os.nova.ServerConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.EntityNotFound'>,)``

   **validate_with_client(client, server)**
