
The ``heat.engine.clients.os.keystone`` Module
==============================================

**class
heat.engine.clients.os.keystone.KeystoneClientPlugin(context)**

   Bases: `heat.engine.clients.client_plugin.ClientPlugin
   <heat.engine.clients.client_plugin.rst#heat.engine.clients.client_plugin.ClientPlugin>`_

   ``IDENTITY = 'identity'``

   ``exceptions_module = <module 'keystonecli ...
   eclient/exceptions.py'>``

   **get_domain_id(domain)**

   **get_group_id(group)**

   **get_project_id(project)**

   **get_region_id(region)**

   **get_role_id(role)**

   **get_service_id(service)**

   **get_user_id(user)**

   **is_conflict(ex)**

   **is_not_found(ex)**

   **is_over_limit(ex)**

   ``service_types = ['identity']``

**class heat.engine.clients.os.keystone.KeystoneDomainConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.EntityNotFound'>,)``

   **validate_with_client(client, domain)**

**class heat.engine.clients.os.keystone.KeystoneGroupConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.EntityNotFound'>,)``

   **validate_with_client(client, group)**

**class heat.engine.clients.os.keystone.KeystoneProjectConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.EntityNotFound'>,)``

   **validate_with_client(client, project)**

**class heat.engine.clients.os.keystone.KeystoneRoleConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.EntityNotFound'>,)``

   **validate_with_client(client, role)**

**class heat.engine.clients.os.keystone.KeystoneServiceConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class 'heat.common ...
   eServiceNameConflict'>)``

   **validate_with_client(client, service)**

**class heat.engine.clients.os.keystone.KeystoneUserConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.EntityNotFound'>,)``

   **validate_with_client(client, user)**
