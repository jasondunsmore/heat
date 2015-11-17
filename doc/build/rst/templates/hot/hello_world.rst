
Hello World HOT Template
************************

https://git.openstack.org/cgit/openstack/heat-templates/tree/hot/hello_world.yaml


Description
***********

Hello world HOT template that just defines a single compute instance.
Contains just base features to verify base HOT support.


Parameters
**********

*key_name* ``(required)``
   *type*
      *string*

   *description*
      Name of an existing key pair to use for the instance

*flavor* ``(optional)``
   *type*
      *string*

   *description*
      Flavor for the instance to be created

*image* ``(required)``
   *type*
      *string*

   *description*
      Image *ID* or image name to use for the instance

*admin_pass* ``(required)``
   *type*
      *string*

   *description*
      The admin password for the instance

*db_port* ``(optional)``
   *type*
      *number*

   *description*
      The database port number
