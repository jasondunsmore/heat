
The ``heat.engine.clients.os.glance`` Module
============================================

**class heat.engine.clients.os.glance.GlanceClientPlugin(context)**

   Bases: `heat.engine.clients.client_plugin.ClientPlugin
   <heat.engine.clients.client_plugin.rst#heat.engine.clients.client_plugin.ClientPlugin>`_

   ``IMAGE = 'image'``

   ``exceptions_module = <module 'glanceclien ...
   s/glanceclient/exc.py'>``

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

   **is_conflict(ex)**

   **is_not_found(ex)**

   **is_over_limit(ex)**

   ``service_types = ['image']``

**class heat.engine.clients.os.glance.ImageConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.EntityNotFound'>,)``

   **validate_with_client(client, value)**
