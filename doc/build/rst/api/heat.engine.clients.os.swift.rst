
The ``heat.engine.clients.os.swift`` Module
*******************************************

**class heat.engine.clients.os.swift.SwiftClientPlugin(context)**

   Bases: `heat.engine.clients.client_plugin.ClientPlugin
   <heat.engine.clients.client_plugin.rst#heat.engine.clients.client_plugin.ClientPlugin>`_

   ``OBJECT_STORE = 'object-store'``

   ``exceptions_module = <module 'swiftclient ...
   client/exceptions.pyc'>``

   **get_signal_url(container_name, obj_name, timeout=None)**

      Turn on object versioning.

      We can use a single TempURL for multiple signals and return a
      Swift TempURL.

   **get_temp_url(container_name, obj_name, timeout=None,
   method='PUT')**

      Return a Swift TempURL.

   **is_client_exception(ex)**

   **is_conflict(ex)**

   **is_not_found(ex)**

   **is_over_limit(ex)**

   **is_valid_temp_url_path(path)**

      Return True if path is a valid Swift TempURL path, False
      otherwise.

      A Swift TempURL path must: - Be five parts, ['', 'v1',
      'account', 'container', 'object'] - Be a v1 request - Have
      account, container, and object values - Have an object value
      with more than just '/'s

      :Parameters:
         **path** (*string*) -- The TempURL path

   **parse_last_modified(lm)**

      Parses the last-modified value.

      For example, last-modified values from a swift object header.
      Returns the datetime.datetime of that value.

      :Parameters:
         **lm** (*string*) -- The last-modified value (or None)

      :Returns:
         An offset-naive UTC datetime of the value (or None)

   ``service_types = ['object-store']``
