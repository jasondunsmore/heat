# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

import mox

from testtools import skipIf

from heat.engine import clients
from heat.common import exception
from heat.common import template_format
from heat.engine import properties
from heat.engine import resource
from heat.engine import scheduler
from heat.engine.resources.neutron import net
from heat.engine.resources.neutron import subnet
from heat.engine.resources.neutron import router
from heat.engine.resources.neutron.neutron import NeutronResource as qr
from heat.openstack.common.importutils import try_import
from heat.tests.common import HeatTestCase
from heat.tests import fakes
from heat.tests import utils

neutronclient = try_import('neutronclient.v2_0.client')
qe = try_import('neutronclient.common.exceptions')

neutron_template = '''
{
  "AWSTemplateFormatVersion" : "2010-09-09",
  "Description" : "Template to test Neutron resources",
  "Parameters" : {},
  "Resources" : {
    "network": {
      "Type": "OS::Neutron::Net",
      "Properties": {
        "name": "the_network"
      }
    },
    "unnamed_network": {
      "Type": "OS::Neutron::Net"
    },
    "admin_down_network": {
      "Type": "OS::Neutron::Net",
      "Properties": {
        "admin_state_up": false
      }
    },
    "subnet": {
      "Type": "OS::Neutron::Subnet",
      "Properties": {
        "network_id": { "Ref" : "network" },
        "ip_version": 4,
        "cidr": "10.0.3.0/24",
        "allocation_pools": [{"start": "10.0.3.20", "end": "10.0.3.150"}],
        "dns_nameservers": ["8.8.8.8"]
      }
    },
    "port": {
      "Type": "OS::Neutron::Port",
      "Properties": {
        "device_id": "d6b4d3a5-c700-476f-b609-1493dd9dadc0",
        "name": "port1",
        "network_id": { "Ref" : "network" },
        "fixed_ips": [{
          "subnet_id": { "Ref" : "subnet" },
          "ip_address": "10.0.3.21"
        }]
      }
    },
    "port2": {
      "Type": "OS::Neutron::Port",
      "Properties": {
        "name": "port2",
        "network_id": { "Ref" : "network" }
      }
    },
    "router": {
      "Type": "OS::Neutron::Router"
    },
    "router_interface": {
      "Type": "OS::Neutron::RouterInterface",
      "Properties": {
        "router_id": { "Ref" : "router" },
        "subnet_id": { "Ref" : "subnet" }
      }
    },
    "gateway": {
      "Type": "OS::Neutron::RouterGateway",
      "Properties": {
        "router_id": { "Ref" : "router" },
        "network_id": { "Ref" : "network" }
      }
    }
  }
}
'''

neutron_floating_template = '''
{
  "AWSTemplateFormatVersion" : "2010-09-09",
  "Description" : "Template to test Neutron resources",
  "Parameters" : {},
  "Resources" : {
    "port_floating": {
      "Type": "OS::Neutron::Port",
      "Properties": {
        "network_id": "xyz1234",
        "fixed_ips": [{
          "subnet_id": "12.12.12.0",
          "ip_address": "10.0.0.10"
        }]
      }
    },
    "floating_ip": {
      "Type": "OS::Neutron::FloatingIP",
      "Properties": {
        "floating_network_id": "abcd1234",
      }
    },
    "floating_ip_assoc": {
      "Type": "OS::Neutron::FloatingIPAssociation",
      "Properties": {
        "floatingip_id": { "Ref" : "floating_ip" },
        "port_id": { "Ref" : "port_floating" }
      }
    },
    "router": {
      "Type": "OS::Neutron::Router"
    },
    "gateway": {
      "Type": "OS::Neutron::RouterGateway",
      "Properties": {
        "router_id": { "Ref" : "router" },
        "network_id": "abcd1234"
      }
    }
  }
}
'''


class NeutronTest(HeatTestCase):

    def test_validate_properties(self):
        vs = {'router:external': True}
        data = {'admin_state_up': False,
                'value_specs': vs}
        p = properties.Properties(net.Net.properties_schema, data)
        self.assertEqual(None, qr.validate_properties(p))

        vs['shared'] = True
        self.assertEqual('shared not allowed in value_specs',
                         qr.validate_properties(p))
        vs.pop('shared')

        vs['name'] = 'foo'
        self.assertEqual('name not allowed in value_specs',
                         qr.validate_properties(p))
        vs.pop('name')

        vs['tenant_id'] = '1234'
        self.assertEqual('tenant_id not allowed in value_specs',
                         qr.validate_properties(p))
        vs.pop('tenant_id')

        vs['foo'] = '1234'
        self.assertEqual(None, qr.validate_properties(p))

    def test_prepare_properties(self):
        data = {'admin_state_up': False,
                'value_specs': {'router:external': True}}
        p = properties.Properties(net.Net.properties_schema, data)
        props = qr.prepare_properties(p, 'resource_name')
        self.assertEqual({'name': 'resource_name',
                          'router:external': True,
                          'admin_state_up': False}, props)

    def test_is_built(self):
        self.assertTrue(qr.is_built({
            'name': 'the_net',
            'status': 'ACTIVE'
        }))
        self.assertTrue(qr.is_built({
            'name': 'the_net',
            'status': 'DOWN'
        }))
        self.assertFalse(qr.is_built({
            'name': 'the_net',
            'status': 'BUILD'
        }))
        self.assertRaises(exception.Error, qr.is_built, {
            'name': 'the_net',
            'status': 'FROBULATING'
        })


@skipIf(neutronclient is None, 'neutronclient unavailable')
class NeutronNetTest(HeatTestCase):

    def setUp(self):
        super(NeutronNetTest, self).setUp()
        self.m.StubOutWithMock(neutronclient.Client, 'create_network')
        self.m.StubOutWithMock(neutronclient.Client, 'delete_network')
        self.m.StubOutWithMock(neutronclient.Client, 'show_network')
        self.m.StubOutWithMock(clients.OpenStackClients, 'keystone')
        utils.setup_dummy_db()

    def create_net(self, t, stack, resource_name):
        rsrc = net.Net('test_net', t['Resources'][resource_name], stack)
        scheduler.TaskRunner(rsrc.create)()
        self.assertEqual((rsrc.CREATE, rsrc.COMPLETE), rsrc.state)
        return rsrc

    def test_net(self):
        clients.OpenStackClients.keystone().AndReturn(
            fakes.FakeKeystoneClient())
        neutronclient.Client.create_network({
            'network': {'name': u'the_network', 'admin_state_up': True}
        }).AndReturn({"network": {
            "status": "BUILD",
            "subnets": [],
            "name": "name",
            "admin_state_up": False,
            "shared": False,
            "tenant_id": "c1210485b2424d48804aad5d39c61b8f",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})

        neutronclient.Client.show_network(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndReturn({"network": {
            "status": "BUILD",
            "subnets": [],
            "name": "name",
            "admin_state_up": False,
            "shared": False,
            "tenant_id": "c1210485b2424d48804aad5d39c61b8f",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})

        neutronclient.Client.show_network(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndReturn({"network": {
            "status": "ACTIVE",
            "subnets": [],
            "name": "name",
            "admin_state_up": False,
            "shared": False,
            "tenant_id": "c1210485b2424d48804aad5d39c61b8f",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})

        neutronclient.Client.show_network(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndRaise(qe.NeutronClientException(status_code=404))

        neutronclient.Client.show_network(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndReturn({"network": {
            "status": "ACTIVE",
            "subnets": [],
            "name": "name",
            "admin_state_up": False,
            "shared": False,
            "tenant_id": "c1210485b2424d48804aad5d39c61b8f",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})

        neutronclient.Client.show_network(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndReturn({"network": {
            "status": "ACTIVE",
            "subnets": [],
            "name": "name",
            "admin_state_up": False,
            "shared": False,
            "tenant_id": "c1210485b2424d48804aad5d39c61b8f",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})

        neutronclient.Client.delete_network(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndReturn(None)

        neutronclient.Client.show_network(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndRaise(qe.NeutronClientException(status_code=404))

        neutronclient.Client.delete_network(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndRaise(qe.NeutronClientException(status_code=404))

        self.m.ReplayAll()
        t = template_format.parse(neutron_template)
        stack = utils.parse_stack(t)
        rsrc = self.create_net(t, stack, 'network')

        # assert the implicit dependency between the gateway and the interface
        deps = stack.dependencies[stack['router_interface']]
        self.assertIn(stack['gateway'], deps)

        # assert the implicit dependency between the gateway and the subnet
        deps = stack.dependencies[stack['subnet']]
        self.assertIn(stack['gateway'], deps)

        rsrc.validate()

        ref_id = rsrc.FnGetRefId()
        self.assertEqual('fc68ea2c-b60b-4b4f-bd82-94ec81110766', ref_id)

        self.assertEqual(None, rsrc.FnGetAtt('status'))
        self.assertEqual('ACTIVE', rsrc.FnGetAtt('status'))
        try:
            rsrc.FnGetAtt('Foo')
            raise Exception('Expected InvalidTemplateAttribute')
        except exception.InvalidTemplateAttribute:
            pass

        self.assertEqual('fc68ea2c-b60b-4b4f-bd82-94ec81110766',
                         rsrc.FnGetAtt('id'))

        self.assertRaises(resource.UpdateReplace,
                          rsrc.handle_update, {}, {}, {})

        scheduler.TaskRunner(rsrc.delete)()
        rsrc.state_set(rsrc.CREATE, rsrc.COMPLETE, 'to delete again')
        scheduler.TaskRunner(rsrc.delete)()
        self.m.VerifyAll()


@skipIf(neutronclient is None, 'neutronclient unavailable')
class NeutronSubnetTest(HeatTestCase):

    def setUp(self):
        super(NeutronSubnetTest, self).setUp()
        self.m.StubOutWithMock(neutronclient.Client, 'create_subnet')
        self.m.StubOutWithMock(neutronclient.Client, 'delete_subnet')
        self.m.StubOutWithMock(neutronclient.Client, 'show_subnet')
        self.m.StubOutWithMock(clients.OpenStackClients, 'keystone')
        utils.setup_dummy_db()

    def create_subnet(self, t, stack, resource_name):
        rsrc = subnet.Subnet('test_subnet', t['Resources'][resource_name],
                             stack)
        scheduler.TaskRunner(rsrc.create)()
        self.assertEqual((rsrc.CREATE, rsrc.COMPLETE), rsrc.state)
        return rsrc

    def test_subnet(self):

        clients.OpenStackClients.keystone().AndReturn(
            fakes.FakeKeystoneClient())
        neutronclient.Client.create_subnet({
            'subnet': {
                'name': utils.PhysName('test_stack', 'test_subnet'),
                'network_id': u'None',
                'dns_nameservers': [u'8.8.8.8'],
                'allocation_pools': [
                    {'start': u'10.0.3.20', 'end': u'10.0.3.150'}],
                'ip_version': 4,
                'cidr': u'10.0.3.0/24'
            }
        }).AndReturn({
            "subnet": {
                "allocation_pools": [
                    {"start": "10.0.3.20", "end": "10.0.3.150"}],
                "cidr": "10.0.3.0/24",
                "dns_nameservers": ["8.8.8.8"],
                "enable_dhcp": True,
                "gateway_ip": "10.0.3.1",
                "id": "91e47a57-7508-46fe-afc9-fc454e8580e1",
                "ip_version": 4,
                "name": "name",
                "network_id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766",
                "tenant_id": "c1210485b2424d48804aad5d39c61b8f"
            }
        })
        neutronclient.Client.show_subnet(
            '91e47a57-7508-46fe-afc9-fc454e8580e1').AndRaise(
                qe.NeutronClientException(status_code=404))
        sn = {
            "subnet": {
                "name": "name",
                "network_id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766",
                "tenant_id": "c1210485b2424d48804aad5d39c61b8f",
                "allocation_pools": [
                    {"start": "10.0.3.20", "end": "10.0.3.150"}],
                "gateway_ip": "10.0.3.1",
                "ip_version": 4,
                "cidr": "10.0.3.0/24",
                "dns_nameservers": ["8.8.8.8"],
                "id": "91e47a57-7508-46fe-afc9-fc454e8580e1",
                "enable_dhcp": True,
            }
        }
        neutronclient.Client.show_subnet(
            '91e47a57-7508-46fe-afc9-fc454e8580e1').AndReturn(sn)
        neutronclient.Client.show_subnet(
            '91e47a57-7508-46fe-afc9-fc454e8580e1').AndReturn(sn)
        neutronclient.Client.show_subnet(
            '91e47a57-7508-46fe-afc9-fc454e8580e1').AndReturn(sn)

        neutronclient.Client.delete_subnet(
            '91e47a57-7508-46fe-afc9-fc454e8580e1'
        ).AndReturn(None)

        neutronclient.Client.show_subnet(
            '91e47a57-7508-46fe-afc9-fc454e8580e1'
        ).AndRaise(qe.NeutronClientException(status_code=404))

        neutronclient.Client.delete_subnet(
            '91e47a57-7508-46fe-afc9-fc454e8580e1'
        ).AndRaise(qe.NeutronClientException(status_code=404))

        self.m.ReplayAll()
        t = template_format.parse(neutron_template)
        stack = utils.parse_stack(t)
        rsrc = self.create_subnet(t, stack, 'subnet')

        rsrc.validate()

        ref_id = rsrc.FnGetRefId()
        self.assertEqual('91e47a57-7508-46fe-afc9-fc454e8580e1', ref_id)
        self.assertEqual(None,
                         rsrc.FnGetAtt('network_id'))
        self.assertEqual('fc68ea2c-b60b-4b4f-bd82-94ec81110766',
                         rsrc.FnGetAtt('network_id'))
        self.assertEqual('8.8.8.8', rsrc.FnGetAtt('dns_nameservers')[0])
        self.assertEqual('91e47a57-7508-46fe-afc9-fc454e8580e1',
                         rsrc.FnGetAtt('id'))

        # assert the dependency (implicit or explicit) between the ports
        # and the subnet
        self.assertIn(stack['port'], stack.dependencies[stack['subnet']])
        self.assertIn(stack['port2'], stack.dependencies[stack['subnet']])

        self.assertRaises(resource.UpdateReplace,
                          rsrc.handle_update, {}, {}, {})

        self.assertEqual(scheduler.TaskRunner(rsrc.delete)(), None)
        rsrc.state_set(rsrc.CREATE, rsrc.COMPLETE, 'to delete again')
        self.assertEqual(scheduler.TaskRunner(rsrc.delete)(), None)
        self.m.VerifyAll()

    def test_subnet_disable_dhcp(self):

        clients.OpenStackClients.keystone().AndReturn(
            fakes.FakeKeystoneClient())
        neutronclient.Client.create_subnet({
            'subnet': {
                'name': utils.PhysName('test_stack', 'test_subnet'),
                'network_id': u'None',
                'dns_nameservers': [u'8.8.8.8'],
                'allocation_pools': [
                    {'start': u'10.0.3.20', 'end': u'10.0.3.150'}],
                'ip_version': 4,
                'enable_dhcp': False,
                'cidr': u'10.0.3.0/24'
            }
        }).AndReturn({
            "subnet": {
                "allocation_pools": [
                    {"start": "10.0.3.20", "end": "10.0.3.150"}],
                "cidr": "10.0.3.0/24",
                "dns_nameservers": ["8.8.8.8"],
                "enable_dhcp": False,
                "gateway_ip": "10.0.3.1",
                "id": "91e47a57-7508-46fe-afc9-fc454e8580e1",
                "ip_version": 4,
                "name": "name",
                "network_id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766",
                "tenant_id": "c1210485b2424d48804aad5d39c61b8f"
            }
        })

        neutronclient.Client.show_subnet(
            '91e47a57-7508-46fe-afc9-fc454e8580e1').AndReturn({
                "subnet": {
                    "name": "name",
                    "network_id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766",
                    "tenant_id": "c1210485b2424d48804aad5d39c61b8f",
                    "allocation_pools": [
                        {"start": "10.0.3.20", "end": "10.0.3.150"}],
                    "gateway_ip": "10.0.3.1",
                    "ip_version": 4,
                    "cidr": "10.0.3.0/24",
                    "dns_nameservers": ["8.8.8.8"],
                    "id": "91e47a57-7508-46fe-afc9-fc454e8580e1",
                    "enable_dhcp": False,
                }
            })

        neutronclient.Client.delete_subnet(
            '91e47a57-7508-46fe-afc9-fc454e8580e1'
        ).AndReturn(None)

        neutronclient.Client.show_subnet(
            '91e47a57-7508-46fe-afc9-fc454e8580e1'
        ).AndRaise(qe.NeutronClientException(status_code=404))

        self.m.ReplayAll()
        t = template_format.parse(neutron_template)
        t['Resources']['subnet']['Properties']['enable_dhcp'] = 'False'
        stack = utils.parse_stack(t)
        rsrc = self.create_subnet(t, stack, 'subnet')

        rsrc.validate()

        ref_id = rsrc.FnGetRefId()
        self.assertEqual('91e47a57-7508-46fe-afc9-fc454e8580e1', ref_id)
        self.assertEqual(False, rsrc.FnGetAtt('enable_dhcp'))
        scheduler.TaskRunner(rsrc.delete)()
        self.m.VerifyAll()


@skipIf(neutronclient is None, 'neutronclient unavailable')
class NeutronRouterTest(HeatTestCase):
    @skipIf(router.neutronV20 is None, "Missing Neutron v2_0")
    def setUp(self):
        super(NeutronRouterTest, self).setUp()
        self.m.StubOutWithMock(neutronclient.Client, 'create_router')
        self.m.StubOutWithMock(neutronclient.Client, 'delete_router')
        self.m.StubOutWithMock(neutronclient.Client, 'show_router')
        self.m.StubOutWithMock(neutronclient.Client, 'add_interface_router')
        self.m.StubOutWithMock(neutronclient.Client, 'remove_interface_router')
        self.m.StubOutWithMock(neutronclient.Client, 'add_gateway_router')
        self.m.StubOutWithMock(neutronclient.Client, 'remove_gateway_router')
        self.m.StubOutWithMock(router.neutronV20,
                               'find_resourceid_by_name_or_id')
        self.m.StubOutWithMock(clients.OpenStackClients, 'keystone')
        utils.setup_dummy_db()

    def create_router(self, t, stack, resource_name):
        rsrc = router.Router('router', t['Resources'][resource_name], stack)
        scheduler.TaskRunner(rsrc.create)()
        self.assertEqual((rsrc.CREATE, rsrc.COMPLETE), rsrc.state)
        return rsrc

    def create_router_interface(self, t, stack, resource_name, properties={}):
        t['Resources'][resource_name]['Properties'] = properties
        rsrc = router.RouterInterface(
            'router_interface',
            t['Resources'][resource_name],
            stack)
        scheduler.TaskRunner(rsrc.create)()
        self.assertEqual((rsrc.CREATE, rsrc.COMPLETE), rsrc.state)
        return rsrc

    def create_gateway_router(self, t, stack, resource_name, properties={}):
        t['Resources'][resource_name]['Properties'] = properties
        rsrc = router.RouterGateway(
            'gateway',
            t['Resources'][resource_name],
            stack)
        scheduler.TaskRunner(rsrc.create)()
        self.assertEqual((rsrc.CREATE, rsrc.COMPLETE), rsrc.state)
        return rsrc

    def test_router(self):
        clients.OpenStackClients.keystone().AndReturn(
            fakes.FakeKeystoneClient())
        neutronclient.Client.create_router({
            'router': {
                'name': utils.PhysName('test_stack', 'router'),
                'admin_state_up': True,
            }
        }).AndReturn({
            "router": {
                "status": "BUILD",
                "external_gateway_info": None,
                "name": utils.PhysName('test_stack', 'router'),
                "admin_state_up": True,
                "tenant_id": "3e21026f2dc94372b105808c0e721661",
                "id": "3e46229d-8fce-4733-819a-b5fe630550f8"
            }
        })
        neutronclient.Client.show_router(
            '3e46229d-8fce-4733-819a-b5fe630550f8').AndReturn({
                "router": {
                    "status": "BUILD",
                    "external_gateway_info": None,
                    "name": utils.PhysName('test_stack', 'router'),
                    "admin_state_up": True,
                    "tenant_id": "3e21026f2dc94372b105808c0e721661",
                    "routes": [],
                    "id": "3e46229d-8fce-4733-819a-b5fe630550f8"
                }
            })
        neutronclient.Client.show_router(
            '3e46229d-8fce-4733-819a-b5fe630550f8').AndReturn({
                "router": {
                    "status": "ACTIVE",
                    "external_gateway_info": None,
                    "name": utils.PhysName('test_stack', 'router'),
                    "admin_state_up": True,
                    "tenant_id": "3e21026f2dc94372b105808c0e721661",
                    "routes": [],
                    "id": "3e46229d-8fce-4733-819a-b5fe630550f8"
                }
            })

        neutronclient.Client.show_router(
            '3e46229d-8fce-4733-819a-b5fe630550f8').AndRaise(
                qe.NeutronClientException(status_code=404))
        neutronclient.Client.show_router(
            '3e46229d-8fce-4733-819a-b5fe630550f8').AndReturn({
                "router": {
                    "status": "ACTIVE",
                    "external_gateway_info": None,
                    "name": utils.PhysName('test_stack', 'router'),
                    "admin_state_up": True,
                    "tenant_id": "3e21026f2dc94372b105808c0e721661",
                    "routes": [],
                    "id": "3e46229d-8fce-4733-819a-b5fe630550f8"
                }
            })
        neutronclient.Client.show_router(
            '3e46229d-8fce-4733-819a-b5fe630550f8').AndReturn({
                "router": {
                    "status": "ACTIVE",
                    "external_gateway_info": None,
                    "name": utils.PhysName('test_stack', 'router'),
                    "admin_state_up": True,
                    "tenant_id": "3e21026f2dc94372b105808c0e721661",
                    "routes": [],
                    "id": "3e46229d-8fce-4733-819a-b5fe630550f8"
                }
            })

        neutronclient.Client.delete_router(
            '3e46229d-8fce-4733-819a-b5fe630550f8'
        ).AndReturn(None)

        neutronclient.Client.show_router(
            '3e46229d-8fce-4733-819a-b5fe630550f8'
        ).AndRaise(qe.NeutronClientException(status_code=404))

        neutronclient.Client.delete_router(
            '3e46229d-8fce-4733-819a-b5fe630550f8'
        ).AndRaise(qe.NeutronClientException(status_code=404))

        self.m.ReplayAll()
        t = template_format.parse(neutron_template)
        stack = utils.parse_stack(t)
        rsrc = self.create_router(t, stack, 'router')

        rsrc.validate()

        ref_id = rsrc.FnGetRefId()
        self.assertEqual('3e46229d-8fce-4733-819a-b5fe630550f8', ref_id)
        self.assertEqual(None,
                         rsrc.FnGetAtt('tenant_id'))
        self.assertEqual('3e21026f2dc94372b105808c0e721661',
                         rsrc.FnGetAtt('tenant_id'))
        self.assertEqual('3e46229d-8fce-4733-819a-b5fe630550f8',
                         rsrc.FnGetAtt('id'))

        self.assertRaises(resource.UpdateReplace,
                          rsrc.handle_update, {}, {}, {})

        self.assertEqual(scheduler.TaskRunner(rsrc.delete)(), None)
        rsrc.state_set(rsrc.CREATE, rsrc.COMPLETE, 'to delete again')
        self.assertEqual(scheduler.TaskRunner(rsrc.delete)(), None)
        self.m.VerifyAll()

    def test_router_interface(self):
        clients.OpenStackClients.keystone().AndReturn(
            fakes.FakeKeystoneClient())
        neutronclient.Client.add_interface_router(
            '3e46229d-8fce-4733-819a-b5fe630550f8',
            {'subnet_id': '91e47a57-7508-46fe-afc9-fc454e8580e1'}
        ).AndReturn(None)
        neutronclient.Client.remove_interface_router(
            '3e46229d-8fce-4733-819a-b5fe630550f8',
            {'subnet_id': '91e47a57-7508-46fe-afc9-fc454e8580e1'}
        ).AndReturn(None)
        neutronclient.Client.remove_interface_router(
            '3e46229d-8fce-4733-819a-b5fe630550f8',
            {'subnet_id': '91e47a57-7508-46fe-afc9-fc454e8580e1'}
        ).AndRaise(qe.NeutronClientException(status_code=404))
        self.m.ReplayAll()
        t = template_format.parse(neutron_template)
        stack = utils.parse_stack(t)

        rsrc = self.create_router_interface(
            t, stack, 'router_interface', properties={
                'router_id': '3e46229d-8fce-4733-819a-b5fe630550f8',
                'subnet_id': '91e47a57-7508-46fe-afc9-fc454e8580e1'
            })

        scheduler.TaskRunner(rsrc.delete)()
        rsrc.state_set(rsrc.CREATE, rsrc.COMPLETE, 'to delete again')
        scheduler.TaskRunner(rsrc.delete)()
        self.m.VerifyAll()

    def test_gateway_router(self):
        clients.OpenStackClients.keystone().AndReturn(
            fakes.FakeKeystoneClient())
        router.neutronV20.find_resourceid_by_name_or_id(
            mox.IsA(neutronclient.Client),
            'network',
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndReturn('fc68ea2c-b60b-4b4f-bd82-94ec81110766')
        neutronclient.Client.add_gateway_router(
            '3e46229d-8fce-4733-819a-b5fe630550f8',
            {'network_id': 'fc68ea2c-b60b-4b4f-bd82-94ec81110766'}
        ).AndReturn(None)
        neutronclient.Client.remove_gateway_router(
            '3e46229d-8fce-4733-819a-b5fe630550f8'
        ).AndReturn(None)
        neutronclient.Client.remove_gateway_router(
            '3e46229d-8fce-4733-819a-b5fe630550f8'
        ).AndRaise(qe.NeutronClientException(status_code=404))
        self.m.ReplayAll()
        t = template_format.parse(neutron_template)
        stack = utils.parse_stack(t)

        rsrc = self.create_gateway_router(
            t, stack, 'gateway', properties={
                'router_id': '3e46229d-8fce-4733-819a-b5fe630550f8',
                'network_id': 'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
            })

        scheduler.TaskRunner(rsrc.delete)()
        rsrc.state_set(rsrc.CREATE, rsrc.COMPLETE, 'to delete again')
        scheduler.TaskRunner(rsrc.delete)()
        self.m.VerifyAll()


@skipIf(neutronclient is None, 'neutronclient unavailable')
class NeutronFloatingIPTest(HeatTestCase):
    @skipIf(net.clients.neutronclient is None, "Missing Neutron Client")
    def setUp(self):
        super(NeutronFloatingIPTest, self).setUp()
        self.m.StubOutWithMock(neutronclient.Client, 'create_floatingip')
        self.m.StubOutWithMock(neutronclient.Client, 'delete_floatingip')
        self.m.StubOutWithMock(neutronclient.Client, 'show_floatingip')
        self.m.StubOutWithMock(neutronclient.Client, 'update_floatingip')
        self.m.StubOutWithMock(neutronclient.Client, 'create_port')
        self.m.StubOutWithMock(neutronclient.Client, 'delete_port')
        self.m.StubOutWithMock(neutronclient.Client, 'show_port')
        self.m.StubOutWithMock(clients.OpenStackClients, 'keystone')
        utils.setup_dummy_db()

    def test_floating_ip(self):

        clients.OpenStackClients.keystone().AndReturn(
            fakes.FakeKeystoneClient())
        neutronclient.Client.create_floatingip({
            'floatingip': {'floating_network_id': u'abcd1234'}
        }).AndReturn({'floatingip': {
            "status": "ACTIVE",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})

        neutronclient.Client.show_floatingip(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndRaise(qe.NeutronClientException(status_code=404))
        neutronclient.Client.show_floatingip(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).MultipleTimes().AndReturn({'floatingip': {
            "status": "ACTIVE",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})

        neutronclient.Client.delete_floatingip(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766').AndReturn(None)
        neutronclient.Client.delete_floatingip(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766').AndRaise(
                qe.NeutronClientException(status_code=404))
        self.m.ReplayAll()

        t = template_format.parse(neutron_floating_template)
        stack = utils.parse_stack(t)

        # assert the implicit dependency between the floating_ip
        # and the gateway
        deps = stack.dependencies[stack['gateway']]
        self.assertIn(stack['floating_ip'], deps)

        fip = stack['floating_ip']
        scheduler.TaskRunner(fip.create)()
        self.assertEqual((fip.CREATE, fip.COMPLETE), fip.state)
        fip.validate()

        fip_id = fip.FnGetRefId()
        self.assertEqual('fc68ea2c-b60b-4b4f-bd82-94ec81110766', fip_id)

        self.assertEqual(None, fip.FnGetAtt('status'))
        self.assertEqual('ACTIVE', fip.FnGetAtt('status'))
        try:
            fip.FnGetAtt('Foo')
            raise Exception('Expected InvalidTemplateAttribute')
        except exception.InvalidTemplateAttribute:
            pass

        self.assertEqual('fc68ea2c-b60b-4b4f-bd82-94ec81110766',
                         fip.FnGetAtt('id'))
        self.assertRaises(resource.UpdateReplace,
                          fip.handle_update, {}, {}, {})
        scheduler.TaskRunner(fip.delete)()
        fip.state_set(fip.CREATE, fip.COMPLETE, 'to delete again')
        scheduler.TaskRunner(fip.delete)()

        self.m.VerifyAll()

    def test_port(self):

        clients.OpenStackClients.keystone().AndReturn(
            fakes.FakeKeystoneClient())
        neutronclient.Client.create_port({'port': {
            'network_id': u'xyz1234',
            'fixed_ips': [
                {'subnet_id': u'12.12.12.0', 'ip_address': u'10.0.0.10'}
            ],
            'name': utils.PhysName('test_stack', 'port_floating'),
            'admin_state_up': True}}
        ).AndReturn({'port': {
            "status": "BUILD",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})
        neutronclient.Client.show_port(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndReturn({'port': {
            "status": "BUILD",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})
        neutronclient.Client.show_port(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndReturn({'port': {
            "status": "ACTIVE",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})
        neutronclient.Client.show_port(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndRaise(qe.NeutronClientException(status_code=404))
        neutronclient.Client.show_port(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).MultipleTimes().AndReturn({'port': {
            "status": "ACTIVE",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})

        self.m.ReplayAll()

        t = template_format.parse(neutron_floating_template)
        stack = utils.parse_stack(t)

        p = stack['port_floating']
        scheduler.TaskRunner(p.create)()
        self.assertEqual((p.CREATE, p.COMPLETE), p.state)
        p.validate()

        port_id = p.FnGetRefId()
        self.assertEqual('fc68ea2c-b60b-4b4f-bd82-94ec81110766', port_id)

        self.assertEqual(None, p.FnGetAtt('status'))
        self.assertEqual('ACTIVE', p.FnGetAtt('status'))
        try:
            p.FnGetAtt('Foo')
            raise Exception('Expected InvalidTemplateAttribute')
        except exception.InvalidTemplateAttribute:
            pass

        self.assertEqual('fc68ea2c-b60b-4b4f-bd82-94ec81110766',
                         p.FnGetAtt('id'))

        self.assertRaises(resource.UpdateReplace,
                          p.handle_update, {}, {}, {})

        self.m.VerifyAll()

    def test_floatip_port(self):

        clients.OpenStackClients.keystone().AndReturn(
            fakes.FakeKeystoneClient())
        neutronclient.Client.create_floatingip({
            'floatingip': {'floating_network_id': u'abcd1234'}
        }).AndReturn({'floatingip': {
            "status": "ACTIVE",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})

        neutronclient.Client.create_port({'port': {
            'network_id': u'xyz1234',
            'fixed_ips': [
                {'subnet_id': u'12.12.12.0', 'ip_address': u'10.0.0.10'}
            ],
            'name': utils.PhysName('test_stack', 'port_floating'),
            'admin_state_up': True}}
        ).AndReturn({'port': {
            "status": "BUILD",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})
        neutronclient.Client.show_port(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndReturn({'port': {
            "status": "ACTIVE",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})
        neutronclient.Client.update_floatingip(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766',
            {
                'floatingip': {
                    'port_id': u'fc68ea2c-b60b-4b4f-bd82-94ec81110766'}}
        ).AndReturn({'floatingip': {
            "status": "ACTIVE",
            "id": "fc68ea2c-b60b-4b4f-bd82-94ec81110766"
        }})

        neutronclient.Client.update_floatingip(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766',
            {'floatingip': {
                'port_id': None
            }}).AndReturn(None)

        neutronclient.Client.delete_port(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndReturn(None)

        neutronclient.Client.show_port(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndRaise(qe.NeutronClientException(status_code=404))

        neutronclient.Client.delete_floatingip(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndReturn(None)

        neutronclient.Client.update_floatingip(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766',
            {'floatingip': {
                'port_id': None
            }}).AndRaise(qe.NeutronClientException(status_code=404))

        neutronclient.Client.delete_port(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndRaise(qe.NeutronClientException(status_code=404))

        neutronclient.Client.delete_floatingip(
            'fc68ea2c-b60b-4b4f-bd82-94ec81110766'
        ).AndRaise(qe.NeutronClientException(status_code=404))

        self.m.ReplayAll()

        t = template_format.parse(neutron_floating_template)
        stack = utils.parse_stack(t)

        fip = stack['floating_ip']
        scheduler.TaskRunner(fip.create)()
        self.assertEqual((fip.CREATE, fip.COMPLETE), fip.state)

        p = stack['port_floating']
        scheduler.TaskRunner(p.create)()
        self.assertEqual((p.CREATE, p.COMPLETE), p.state)

        fipa = stack['floating_ip_assoc']
        scheduler.TaskRunner(fipa.create)()
        self.assertEqual((fipa.CREATE, fipa.COMPLETE), fipa.state)

        fipa.validate()

        fipa_id = fipa.FnGetRefId()
        fip_id = fip.FnGetRefId()
        port_id = p.FnGetRefId()
        self.assertEqual('%s:%s' % (fip_id, port_id), fipa_id)
        self.assertRaises(resource.UpdateReplace,
                          fipa.handle_update, {}, {}, {})

        scheduler.TaskRunner(fipa.delete)()
        scheduler.TaskRunner(p.delete)()
        scheduler.TaskRunner(fip.delete)()

        fipa.state_set(fipa.CREATE, fipa.COMPLETE, 'to delete again')
        fip.state_set(fip.CREATE, fip.COMPLETE, 'to delete again')
        p.state_set(p.CREATE, p.COMPLETE, 'to delete again')

        scheduler.TaskRunner(fipa.delete)()
        self.assertEqual(scheduler.TaskRunner(p.delete)(), None)
        scheduler.TaskRunner(fip.delete)()

        self.m.VerifyAll()
