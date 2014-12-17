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


import mock

import uuid

from heat.common import exception
from heat.engine import resource
from heat.engine import rsrc_defn
from heat.tests import common

from .. import clients
from ..resources import rackconnect  # noqa



class PoolNodeTest(common.HeatTestCase):

    def setUp(self):
        super(PoolNodeTest, self).setUp()
        resource._register_class("Rackspace::RackConnect::PoolNode",
                                 rackconnect.PoolNode)

        # create fake variables to construct the resource
        self._name = str(uuid.uuid4())
        self._definition = mock.Mock(spec=rsrc_defn.ResourceDefinition)
        properties = {}
        properties[rackconnect.PoolNode.SERVER_ID] = uuid.uuid4()
        properties[rackconnect.PoolNode.POOL] = uuid.uuid4()

        self._definition.properties.return_value = properties
        # set up a stack object
        self._stack = mock.Mock()
        self._stack.context.return_value = mock.Mock()
        self._stack.context.clients.return_value = mock.Mock()
        self._stack.context.clients.get.return_value = mock.Mock()
        self._stack.db_resource_get.return_value = None

    def test_handle_create(self):

        self._pool_node = rackconnect.PoolNode(
            self._name, self._definition, self._stack
        )
        self._pool_node._get_pool_id = mock.Mock(return_value='2343')
        mock_client = mock.Mock()
        mock_client.create_pool_node.return_value = mock.Mock(
            cloud_server={'id': 'Harry Potter'},
            id='random id'
        )
        self._pool_node.client = mock.Mock(return_value=mock_client)

        # call the method under test
        resp = self._pool_node.handle_create()

        # test if the method behaves as expected
        self.assertEqual('random id', resp.id)
        self.assertEqual('Harry Potter', resp.cloud_server['id'])

        # add methods to test exceptions
        mock_client.create_pool_node = mock.Mock(side_effect=Exception)
        mock_check = mock.Mock(return_value=True)
        mock_check.is_client_exception.return_value = True
        self._pool_node.client_plugin = mock.Mock(return_value=mock_check)

        # call the method under test
        resp = self._pool_node.handle_create()

        self.assertEqual(resp, None)

    def test_check_create_complete(self):

        self._pool_node = rackconnect.PoolNode(
            self._name, self._definition, self._stack
        )
        self._pool_node._get_pool_id = mock.Mock(return_value='an id')

        mock_node = mock.Mock()
        mock_check_status = mock.Mock(return_value='Au Revoir')
        self._pool_node._check_status = mock_check_status

        resp = self._pool_node.check_create_complete(mock_node)
        self.assertEqual(resp, 'Au Revoir')

        mock_node = None
        mock_client = mock.Mock()
        mock_nodes = [
            mock.Mock(cloud_server={"id": self._pool_node.SERVER_ID})
        ]
        mock_client.list_pool_nodes.return_value = mock_nodes
        self._pool_node.client = mock.Mock(return_value=mock_client)

        resp = self._pool_node.check_create_complete(mock_node)
        self.assertEqual(resp, 'Au Revoir')

        mock_client.list_pool_nodes.return_value = []
        self._pool_node.client = mock.Mock(return_value=mock_client)

        resp = self._pool_node.check_create_complete(mock_node)
        self.assertEqual(resp, 'Au Revoir')

        mock_client.create_pool_node = mock.Mock(side_effect=Exception)
        mock_check = mock.Mock(return_value=True)
        mock_check.is_client_exception.return_value = True
        self._pool_node.client_plugin = mock.Mock(return_value=mock_check)
        self._pool_node.client = mock.Mock(return_value=mock_client)

        # call the method under test
        resp = self._pool_node.check_create_complete(mock_node)
        self.assertEqual(resp, False)

    def test_check_status(self):

        self._pool_node = rackconnect.PoolNode(
            self._name, self._definition, self._stack
        )

        mock_node = mock.Mock()

        mock_node.status = 'ACTIVE'
        ret = self._pool_node._check_status(mock_node)
        self.assertTrue(ret)

        mock_node.status = 'ADDING'
        ret = self._pool_node._check_status(mock_node)
        self.assertFalse(ret)

        mock_node.status = 'ADD_FAILED'
        self.assertRaises(
            resource.ResourceInError,
            self._pool_node._check_status,
            mock_node
        )

        mock_node.status = 'gibberish'
        self.assertRaises(
            resource.ResourceUnknownStatus,
            self._pool_node._check_status,
            mock_node
        )

    def test_handle_delete(self):

        self._pool_node = rackconnect.PoolNode(
            self._name, self._definition, self._stack
        )

        mock_client = mock.Mock()
        mock_resp = mock.Mock()

        mock_client.delete_pool_node.return_value = mock_resp
        mock_client.list_load_balancer_pools.return_value = [self._pool_node]
        self._pool_node.client = mock.Mock()
        self._pool_node.client.return_value = mock_client
        self._pool_node.resource_id = None

        resp = self._pool_node.handle_delete()

        self.assertIsNone(resp)

        self._pool_node.resource_id = 'somethingNotNone'
        resp = self._pool_node.handle_delete()

        self.assertIsNotNone(resp)

    def test_check_delete_complete(self):

        self._pool_node = rackconnect.PoolNode(
            self._name, self._definition, self._stack
        )

        mock_node = None

        ret = self._pool_node.check_delete_complete(mock_node)
        self.assertTrue(ret)

        mock_node = mock.Mock()

        mock_node.status = 'REMOVING'
        ret = self._pool_node.check_delete_complete(mock_node)
        self.assertFalse(ret)

        mock_node.status = 'REMOVE_FAILED'
        self.assertRaises(
            resource.ResourceInError,
            self._pool_node.check_delete_complete,
            mock_node
        )

        mock_node.status = 'gibberish'
        self.assertRaises(
            resource.ResourceUnknownStatus,
            self._pool_node.check_delete_complete,
            mock_node
        )

    @mock.patch.object(resource.Resource, 'validate')
    def test_validate(self, mock_validate):

        mock_validate.return_value = None

        self._pool_node = rackconnect.PoolNode(
            self._name, self._definition, self._stack
        )

        mock_client = mock.Mock()
        self._pool_node.client = mock.Mock(return_value=mock_client)

        mock_pool = mock.Mock()
        mock_pool.id = self._pool_node.properties[self._pool_node.POOL]
        mock_node = mock.Mock()
        server_id = self._pool_node.properties[self._pool_node.SERVER_ID]
        mock_node.cloud_server = {"id": server_id}
        mock_pool.nodes.return_value = [mock_node]
        mock_client.list_load_balancer_pools.return_value = [mock_pool]
        mock_client.get_load_balancer_pool.return_value = mock_pool

        self.assertRaises(
            exception.StackValidationFailed,
            self._pool_node.validate
        )


class PublicIPTest(common.HeatTestCase):

    def setUp(self):
        super(PublicIPTest, self).setUp()
        resource._register_class("Rackspace::RackConnect::PublicIP",
                                 rackconnect.PublicIP)

        # create fake variables to construct the resource
        self._name = str(uuid.uuid4())
        self._definition = mock.Mock(spec=rsrc_defn.ResourceDefinition)
        properties = {}
        properties[rackconnect.PublicIP.SERVER_ID] = uuid.uuid4()

        self._definition.properties.return_value = properties

        # set up a stack object
        self._stack = mock.Mock()
        self._stack.context.return_value = mock.Mock()
        self._stack.context.clients.return_value = mock.Mock()
        self._stack.context.clients.get.return_value = mock.Mock()
        self._stack.db_resource_get.return_value = None

    def test_handle_create(self):

        self._public_ip = rackconnect.PublicIP(
            self._name, self._definition, self._stack
        )

        mock_client = mock.Mock()
        mock_resp = mock.Mock()
        self._public_ip.client = mock.Mock()
        self._public_ip.client.return_value = mock_client
        mock_client.create_public_ip.return_value = mock_resp

        mock_resp.id = uuid.uuid4()

        resp = self._public_ip.handle_create()

        self.assertEqual(resp, mock_resp)

        # add methods to test exceptions
        mock_client.create_public_ip = mock.Mock(side_effect=Exception)
        mock_check = mock.Mock(return_value=True)
        mock_check.is_client_exception.return_value = True
        self._public_ip.client_plugin = mock.Mock(return_value=mock_check)

        # call the method under test
        resp = self._public_ip.handle_create()
        self.assertEqual(resp, None)

    def test_check_status(self):

        self._public_ip = rackconnect.PublicIP(
            self._name, self._definition, self._stack
        )

        mock_public_ip = mock.Mock()

        mock_public_ip.status = 'ACTIVE'
        ret = self._public_ip._check_status(mock_public_ip)
        self.assertTrue(ret)

        mock_public_ip.status = 'ADDING'
        ret = self._public_ip._check_status(mock_public_ip)
        self.assertFalse(ret)

        mock_public_ip.status = 'ADD_FAILED'
        self.assertRaises(
            resource.ResourceInError,
            self._public_ip._check_status,
            mock_public_ip
        )

        mock_public_ip.status = 'gibberish'
        self.assertRaises(
            resource.ResourceUnknownStatus,
            self._public_ip._check_status,
            mock_public_ip
        )

    def test_check_create_complete(self):

        self._public_ip = rackconnect.PublicIP(
            self._name, self._definition, self._stack
        )

        mock_node = mock.Mock()
        mock_check_status = mock.Mock(return_value='Au Revoir')
        self._public_ip._check_status = mock_check_status

        resp = self._public_ip.check_create_complete(mock_node)
        self.assertEqual(resp, 'Au Revoir')

        mock_node = None
        mock_client = mock.Mock()
        mock_client.get_public_ips_for_server.return_value = [mock.Mock()]
        self._public_ip.client = mock.Mock(return_value=mock_client)

        resp = self._public_ip.check_create_complete(mock_node)
        self.assertEqual(resp, 'Au Revoir')

        mock_client.get_public_ips_for_server.return_value = []
        self._public_ip.client = mock.Mock(return_value=mock_client)

        resp = self._public_ip.check_create_complete(mock_node)
        self.assertEqual(resp, 'Au Revoir')

        mock_client.create_public_ip = mock.Mock(side_effect=Exception)
        mock_check = mock.Mock(return_value=True)
        mock_check.is_client_exception.return_value = True
        self._public_ip.client_plugin = mock.Mock(return_value=mock_check)
        self._public_ip.client = mock.Mock(return_value=mock_client)

        # call the method under test
        resp = self._public_ip.check_create_complete(mock_node)
        self.assertEqual(resp, False)


    def test_handle_delete(self):

        self._public_ip = rackconnect.PublicIP(
            self._name, self._definition, self._stack
        )

        mock_resp = mock.Mock()
        mock_client = mock.Mock()
        self._public_ip.resource_id = mock.Mock()
        self._public_ip.client = mock.Mock()
        self._public_ip.client.return_value = mock_client
        mock_client.delete_public_ip.return_value = mock_resp

        resp = self._public_ip.handle_delete()

        self.assertEqual(resp, mock_resp)

    def test_check_delete_complete(self):

        self._public_ip = rackconnect.PublicIP(
            self._name, self._definition, self._stack
        )

        mock_public_ip = None

        ret = self._public_ip.check_delete_complete(mock_public_ip)
        self.assertTrue(ret)

        mock_public_ip = mock.Mock()

        mock_public_ip.status = 'REMOVING'
        ret = self._public_ip.check_delete_complete(mock_public_ip)
        self.assertFalse(ret)

        mock_public_ip.status = 'REMOVE_FAILED'
        self.assertRaises(
            resource.ResourceInError,
            self._public_ip.check_delete_complete,
            mock_public_ip
        )

        mock_public_ip.status = 'gibberish'
        self.assertRaises(
            resource.ResourceUnknownStatus,
            self._public_ip.check_delete_complete,
            mock_public_ip
        )


class MockNotFound(Exception):

    def __init__(self, code, message):
        self.code = code
        super(MockNotFound, self).__init__(message)


@mock.patch.object(clients, 'pyrax')
class ConstraintTests(common.HeatTestCase):

    def _build_mock_clients(self, mocked_module):
        mockclients = mock.Mock()
        mockclient = mock.Mock()
        mockclients.client.return_value = mockclient
        mocked_module.exceptions.NotFound = MockNotFound
        return (mockclients, mockclient)

    def test_network_constraint(self, mocked_module):

        mockclients, mockclient = self._build_mock_clients(mocked_module)
        net_constraint = clients.RackconnectNetworkConstraint()

        # test happy path
        uid = uuid.uuid4()
        mocknet = mock.Mock()
        mocknet.id = uid
        mocknet.name = 'testnet'
        mockclient.list_networks.return_value = [mocknet]

        # happy path by id
        self.assertIsNone(net_constraint.validate_with_client(mockclients, uid))

        # happy path by name
        self.assertIsNone(net_constraint.validate_with_client(mockclients,
                                                              'testnet'))

        # test not found
        mockclient.list_networks.return_value = []
        exc = self.assertRaises(MockNotFound,
                                net_constraint.validate_with_client,
                                mockclients, uid)
        self.assertIn("%s is not a valid Rackconnect V3 network"
                      % uid, str(exc))

    def test_pool_validator(self, mocked_module):

        mockclients, mockclient = self._build_mock_clients(mocked_module)
        pool_constraint = clients.RackconnectPoolConstraint()

        # test happy path
        uid = uuid.uuid4()
        mockpool = mock.Mock()
        mockpool.id = uid
        mockpool.name = 'testpool'
        mockclient.list_load_balancer_pools.return_value = [mockpool]

        # happy path by id
        self.assertIsNone(pool_constraint.validate_with_client(mockclients, uid))

        # happy path by name
        self.assertIsNone(pool_constraint.validate_with_client(mockclients,
                                                              'testpool'))

        # test not found
        mockclient.list_load_balancer_pools.return_value = []
        exc = self.assertRaises(Exception,
                                pool_constraint.validate_with_client,
                                mockclients, uid)
        self.assertIn("%s is not a valid Rackconnect V3 load balancer pool"
                      % uid, str(exc))
