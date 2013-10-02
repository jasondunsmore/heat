
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

from oslo.config import cfg

cfg.CONF.import_opt('db_lock_timeout', 'heat.common.config')
cfg.CONF.import_opt('distributed_lock_driver', 'heat.common.config')
cfg.CONF.import_opt('engine_id', 'heat.common.config')
cfg.CONF.import_opt('zk_hosts', 'heat.common.config')
cfg.CONF.import_opt('zk_lock_acquire_timeout', 'heat.common.config')

from heat.openstack.common.gettextutils import _

from heat.common import exception
from heat.db import api as db_api

from heat.openstack.common import log as logging

if cfg.CONF.distributed_lock_driver == 'zookeeper':
    from kazoo import exceptions as kazoo_exceptions
    from kazoo.client import KazooClient
    from kazoo.recipe.lock import Lock as KazooLock

logger = logging.getLogger(__name__)


class ZookeeperConnectionTimeout(exception.HeatException):
    message = _("Unable to connect to Zookeeper on: %(hosts)s")


# TODO(jason): Split the Zookeeper lock into another patch for final review

class StackZKLock(object):
    def __init__(self, context, stack):
        self.context = context
        self.stack = stack
        self.engine_id = cfg.CONF.engine_id
        zk_hosts = ",".join(cfg.CONF.zk_hosts)
        self.zk = KazooClient(hosts=zk_hosts)
        # TODO(jason): Look into/address issue brought up by Joshua:
        # What should we do when the connection is lost (but the lock
        # was acquired)? Probably want to add those listeners?
        # https://github.com/python-zk/kazoo/blob/master/kazoo/recipe/lock.py#L3
        try:
            self.zk.start()
        except kazoo_exceptions.TimeoutError as exc:
            logger.exception(exc)
            raise ZookeeperConnectionTimeout(hosts=zk_hosts)
        # TODO(jason): Look into/address issue brought up by Joshua:
        # Why not separate this into a path instead of a string?
        # Zookeeper is path based and it seems logical that a tenant
        # would be a top level path and the stack name would be a file
        # in that directory. This will aid using existing zookeeper
        # tooling to examine those directories.
        # In particular:
        #   zkcli ls path
        # If its just a string combination, then it makes it hard to
        # look at what is currently locked.
        self.lock_name = "%s_%s" % (self.context.tenant, self.stack.name)
        self.lock = KazooLock(self.zk, self.lock_name)

    def acquire(self):
        """Acquire a lock on the stack"""
        try:
            existing_lock = self.zk.get(self.lock_name)[1]
        except kazoo_exceptions.NoNodeError:
            existing_lock = None

        # acquire() will return True if the engine that has the lock
        # asks for the lock.  To keep stacks with an active lock from
        # being worked on, check that the number of children for the
        # lock is zero before trying to acquire the lock.
        if existing_lock is None or existing_lock.numChildren == 0:
            try:
                self.lock.acquire(blocking=True,
                                  timeout=cfg.CONF.zk_lock_acquire_timeout)
                return
            except kazoo_exceptions.LockTimeout as exc:
                logger.exception(exc)
        raise exception.ActionInProgress(stack_name=self.stack.name,
                                         action=self.stack.action)

    def release(self):
        """Release a stack lock"""
        self.lock.release()

    def _gt_callback_release(self, gt, **kwargs):
        gt.wait()
        self.release()


class StackDBLock(object):
    def __init__(self, context, stack):
        self.context = context
        self.stack = stack
        self.engine_id = cfg.CONF.engine_id

    def acquire(self):
        """Acquire a lock on the stack"""
        existing_lock = db_api.stack_lock_get(self.context, self.stack.id)
        if existing_lock:
            if db_api.stack_lock_age(existing_lock) > cfg.CONF.db_lock_timeout:
                logger.info("Lock expired.  Engine %s is stealing the lock"
                            % existing_lock.engine_id)
                db_api.stack_lock_steal(self.context, self.stack.id,
                                        self.engine_id)
            else:
                logger.debug("Stack lock is owned by engine %s"
                             % existing_lock.engine_id)
                raise exception.ActionInProgress(stack_name=self.stack.name,
                                                 action=self.stack.action)
        else:
            db_api.stack_lock_create(self.context, self.stack.id,
                                     self.engine_id)

    def release(self):
        """Release a stack lock"""
        db_api.stack_lock_release(self.context, self.stack.id)

    def _gt_callback_release(self, gt, *args, **kwargs):
        gt.wait()
        self.release()


if cfg.CONF.distributed_lock_driver == 'zookeeper':
    StackLock = StackZKLock
elif cfg.CONF.distributed_lock_driver == 'database':
    StackLock = StackDBLock
else:
    raise exception.Error("Engine is configured to use an unknown distributed "
                          "lock driver: %s" % cfg.CONF.distributed_lock_driver)
