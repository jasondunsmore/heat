
The ``heat.engine.clients.os.designate`` Module
===============================================

**class
heat.engine.clients.os.designate.DesignateClientPlugin(context)**

   Bases: `heat.engine.clients.client_plugin.ClientPlugin
   <heat.engine.clients.client_plugin.rst#heat.engine.clients.client_plugin.ClientPlugin>`_

   ``DNS = 'dns'``

   **domain_create(**kwargs)**

   **domain_update(**kwargs)**

   ``exceptions_module = [<module 'designatec ...
   client/exceptions.py'>]``

   **get_domain_id(domain_id_or_name)**

   **is_not_found(ex)**

   **record_create(**kwargs)**

   **record_delete(**kwargs)**

   **record_update(**kwargs)**

   ``service_types = ['dns']``

**class heat.engine.clients.os.designate.DesignateDomainConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'heat.common.exception.EntityNotFound'>,)``

   **validate_with_client(client, domain)**
