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

from oslo_log import log as logging

from heat.common import exception
from heat.common.i18n import _
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource

LOG = logging.getLogger(__name__)


class PoolNode(resource.Resource):
    """A resource for RackConnect LoadBalancerPool node."""

    default_client_name = "rackconnect"

    PROPERTIES = (
        POOL, SERVER_ID
    ) = (
        "pool", "server_id",
    )

    properties_schema = {
        POOL: properties.Schema(
            properties.Schema.STRING,
            _("The id of the pool."),
            required=True,
            constraints=[
                constraints.CustomConstraint("rackconnect.pool")
            ]
        ),
        SERVER_ID: properties.Schema(
            properties.Schema.STRING,
            _("The id of the server to be added."),
            required=True,
            constraints=[
                constraints.CustomConstraint("nova.server")
            ]
        ),
    }

    def _get_pool_id(self):
        prop_pool = self.properties[self.POOL]
        if prop_pool:
            pools = [p.id for p in self.client().list_load_balancer_pools()
                     if p.id == prop_pool or p.name == prop_pool]
            if pools:
                return pools[0]

    def handle_create(self):
        try:
            pool_node = self.client().create_pool_node(
                self._get_pool_id(),
                self.properties[self.SERVER_ID]
                )

            if pool_node is not None:
                self.resource_id_set(pool_node.id)

            return pool_node

        except Exception as exc:
            if self.client_plugin().is_client_exception(exc):
                return None

    def check_create_complete(self, pool_node):
        if pool_node is None:
            # failed on intial call to rackconnect, so try again until
            # success in creating the resource is achieved
            pool_nodes = self.client().list_pool_nodes(self._get_pool_id())

            for pool_node in pool_nodes:
                server_id = pool_node.cloud_server['id']
                if server_id == self.properties[self.SERVER_ID]:
                    return self._check_status(pool_node)

            else:
                try:
                    pool_node = self.client().create_pool_node(
                        self._get_pool_id(),
                        self.properties[self.SERVER_ID]
                        )
                    if pool_node is not None:
                        self.resource_id_set(pool_node.id)
                    return self._check_status(pool_node)

                except Exception as exc:
                    if self.client_plugin().is_client_exception(exc):
                        return False

        else:
            # handle_create succeeded
            return self._check_status(pool_node)

    def handle_delete(self):
        if self.resource_id is None:
            return None
        try:
            return self.client().delete_pool_node(
                self._get_pool_id(),
                self.resource_id
            )
        except Exception as exc:
            self.client_plugin().ignore_not_found(exc)

    def check_delete_complete(self, pool_node):

        if pool_node is None:
            return True
        else:
            try:
                pool_node.get()
            except Exception as exc:
                self.client_plugin().ignore_not_found(exc)
                return True
            if pool_node.status == 'REMOVING':
                return False
            elif pool_node.status == 'REMOVE_FAILED':
                raise resource.ResourceInError(
                    resource_status=pool_node.status,
                    status_reason=pool_node.status_detail
                )
            else:
                raise resource.ResourceUnknownStatus(
                    resource_status=pool_node.status,
                    result=_('Pool node not removed.'))

    def validate(self):

        super(PoolNode, self).validate()

        pool_id = self._get_pool_id()
        server_id = self.properties[self.SERVER_ID]

        LOG.info("\n\nPOOL: %s\nSERVER: %s\n\n" % (pool_id, server_id))

        # check if the server is already in the pool
        if pool_id:
            pool = self.client().get_load_balancer_pool(pool_id)
            pool_node_ids = (
                node.cloud_server['id'] for node in pool.nodes()
            )

            if server_id in pool_node_ids:
                msg = _('Server %(server_id)s is already a member of '
                        'load balancer pool %(pool_id)s' %
                        {"pool_id": pool_id,
                         "server_id": server_id})
                raise exception.StackValidationFailed(message=msg)

    def _check_status(self, pool_node):
        pool_node.get()
        if pool_node.status == 'ACTIVE':
            return True
        elif pool_node.status == 'ADDING':
            return False
        elif pool_node.status == 'ADD_FAILED':
            raise resource.ResourceInError(
                resource_status=pool_node.status,
                status_reason=pool_node.status_detail
            )
        else:
            raise resource.ResourceUnknownStatus(
                resource_status=pool_node.status,
                result=_('Pool node not created.')
            )


class PublicIP(resource.Resource):
    """A resource for RackConnect public ips."""

    default_client_name = "rackconnect"

    PROPERTIES = (
        SERVER_ID
    ) = (
        "server_id"
    )

    properties_schema = {
        SERVER_ID: properties.Schema(
            properties.Schema.STRING,
            _("The id of the server to be added."),
            required=True,
            constraints=[
                constraints.CustomConstraint("nova.server")
            ]
        )
    }

    def handle_create(self):
        try:
            public_ip = self.client().create_public_ip(
                self.properties[self.SERVER_ID]
                )
        except Exception as exc:
            if self.client_plugin().is_client_exception(exc):
                return None

        if public_ip is not None:
            self.resource_id_set(public_ip.id)

        return public_ip

    def check_create_complete(self, public_ip):

        if public_ip is None:
            # failed on intial call to rackconnect, so try again until
            # success in creating the resource is achieved
            public_ips = self.client().get_public_ips_for_server(
                            self.properties[self.SERVER_ID]
                         )

            if public_ips:
                public_ip = public_ips[0]
                return self._check_status(public_ip)
            else:
                try:
                    public_ip = self.client().create_public_ip(
                        self.properties[self.SERVER_ID]
                        )
                    if public_ip is not None:
                        self.resource_id_set(public_ip.id)
                        return self._check_status(public_ip)

                except Exception as exc:
                    if self.client_plugin().is_client_exception(exc):
                        return False

        else:
            # handle_create succeeded
            return self._check_status(public_ip)

    def handle_delete(self):
        if self.resource_id is None:
            return
        try:
            return self.client().delete_public_ip(self.resource_id)
        except Exception as exc:
            self.client_plugin().ignore_not_found(exc)

    def check_delete_complete(self, public_ip):

        if public_ip is None:
            return True
        else:
            try:
                public_ip.get()
            except Exception as exc:
                self.client_plugin().ignore_not_found(exc)
                return True

            if public_ip.status == 'REMOVING':
                return False
            elif public_ip.status == 'REMOVE_FAILED':
                raise resource.ResourceInError(
                    resource_status=public_ip.status,
                    status_reason=public_ip.status_detail
                )
            else:
                raise resource.ResourceUnknownStatus(
                    resource_status=public_ip.status,
                    result=_('Public IP not removed.'))

    def _check_status(self, public_ip):
        public_ip.get()
        if public_ip.status == 'ACTIVE':
            return True
        elif public_ip.status == 'ADDING':
            return False
        elif public_ip.status == 'ADD_FAILED':
            raise resource.ResourceInError(
                resource_status=public_ip.status,
                status_reason=public_ip.status_detail
            )
        else:
            raise resource.ResourceUnknownStatus(
                resource_status=public_ip.status,
                result=_('Public IP not assigned.'))


def resource_mapping():
    return {'Rackspace::RackConnect::PoolNode': PoolNode,
            'Rackspace::RackConnect::PublicIP': PublicIP, }
