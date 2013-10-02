# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from heat.engine import clients
from heat.openstack.common import log as logging
from heat.engine.resources.neutron import neutron
from heat.engine import scheduler

if clients.neutronclient is not None:
    from neutronclient.common.exceptions import NeutronClientException

logger = logging.getLogger(__name__)


class Subnet(neutron.NeutronResource):

    allocation_schema = {'start': {'Type': 'String',
                                   'Required': True},
                         'end': {'Type': 'String',
                                 'Required': True}}

    properties_schema = {'network_id': {'Type': 'String',
                                        'Required': True},
                         'cidr': {'Type': 'String',
                                  'Required': True},
                         'value_specs': {'Type': 'Map',
                                         'Default': {}},
                         'name': {'Type': 'String'},
                         'ip_version': {'Type': 'Integer',
                                        'AllowedValues': [4, 6],
                                        'Default': 4},
                         'dns_nameservers': {'Type': 'List'},
                         'gateway_ip': {'Type': 'String'},
                         'enable_dhcp': {'Type': 'Boolean'},
                         'allocation_pools': {'Type': 'List',
                                              'Schema': {
                                              'Type': 'Map',
                                              'Schema': allocation_schema
                                              }},
                         'tenant_id': {'Type': 'String'}}
    attributes_schema = {
        "name": _("Friendly name of the subnet."),
        "network_id": _("Parent network of the subnet."),
        "tenant_id": _("Tenant owning the subnet."),
        "allocation_pools": _("Ip allocation pools and their ranges."),
        "gateway_ip": _("Ip of the subnet's gateway."),
        "ip_version": _("Ip version for the subnet."),
        "cidr": _("CIDR block notation for this subnet."),
        # dns_nameservers isn't in the api docs; is it right?
        "dns_nameservers": _("List of dns nameservers."),
        "enable_dhcp": _("'true' if DHCP is enabled for this subnet; 'false' "
                         "otherwise.")
    }

    @staticmethod
    def _null_gateway_ip(props):
        if 'gateway_ip' not in props:
            return
        # Specifying null in the gateway_ip will result in
        # a property containing an empty string.
        # A null gateway_ip has special meaning in the API
        # so this needs to be set back to None.
        # See bug https://bugs.launchpad.net/heat/+bug/1226666
        if props.get('gateway_ip') == '':
            props['gateway_ip'] = None

    def handle_create(self):
        props = self.prepare_properties(
            self.properties,
            self.physical_resource_name())

        self._null_gateway_ip(props)

        subnet = self.neutron().create_subnet({'subnet': props})['subnet']
        self.resource_id_set(subnet['id'])

    def handle_delete(self):
        client = self.neutron()
        try:
            client.delete_subnet(self.resource_id)
        except NeutronClientException as ex:
            if ex.status_code != 404:
                raise ex
        else:
            return scheduler.TaskRunner(self._confirm_delete)()

    def _show_resource(self):
        return self.neutron().show_subnet(self.resource_id)['subnet']


def resource_mapping():
    if clients.neutronclient is None:
        return {}

    return {
        'OS::Neutron::Subnet': Subnet,
    }
