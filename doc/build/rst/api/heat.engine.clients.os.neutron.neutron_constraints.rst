
The ``heat.engine.clients.os.neutron.neutron_constraints`` Module
=================================================================

**class
heat.engine.clients.os.neutron.neutron_constraints.NetworkConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class 'neutronclie ...
   esourceNameAmbiguity'>)``

   **validate_with_client(client, value)**

**class
heat.engine.clients.os.neutron.neutron_constraints.PortConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'neutronclient.common.exceptions.NeutronClientException'>,)``

   **validate_with_client(client, value)**

**class
heat.engine.clients.os.neutron.neutron_constraints.RouterConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'neutronclient.common.exceptions.NeutronClientException'>,)``

   **validate_with_client(client, value)**

**class
heat.engine.clients.os.neutron.neutron_constraints.SubnetConstraint**

   Bases: `heat.engine.constraints.BaseCustomConstraint
   <heat.engine.constraints.rst#heat.engine.constraints.BaseCustomConstraint>`_

   ``expected_exceptions = (<class
   'neutronclient.common.exceptions.NeutronClientException'>,)``

   **validate_with_client(client, value)**
