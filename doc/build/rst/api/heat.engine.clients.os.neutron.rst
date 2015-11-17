
The ``heat.engine.clients.os.neutron`` Module
*********************************************

**class heat.engine.clients.os.neutron.NeutronClientPlugin(context)**

   Bases: `heat.engine.clients.client_plugin.ClientPlugin
   <heat.engine.clients.client_plugin.rst#heat.engine.clients.client_plugin.ClientPlugin>`_

   ``NETWORK = 'network'``

   ``exceptions_module = <module 'neutronclie ...
   common/exceptions.pyc'>``

   **find_neutron_resource(props, key, key_type)**

   **get_secgroup_uuids(security_groups)**

      Returns a list of security group UUIDs.

      Args: security_groups: List of security group names or UUIDs

   **has_extension(alias)**

      Check if specific extension is present.

   **is_conflict(ex)**

   **is_no_unique(ex)**

   **is_not_found(ex)**

   **is_over_limit(ex)**

   **network_id_from_subnet_id(subnet_id)**

   **resolve_network(props, net_key, net_id_key)**

   **resolve_port(props, port_key, port_id_key)**

   **resolve_router(props, router_key, router_id_key)**

   **resolve_subnet(props, subnet_key, subnet_id_key)**

   ``service_types = ['network']``
