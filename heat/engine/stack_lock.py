
import time

from oslo.config import cfg

cfg.CONF.import_opt('db_lock_timeout', 'heat.common.config')
cfg.CONF.import_opt('distributed_lock_driver', 'heat.common.config')
cfg.CONF.import_opt('engine_id', 'heat.common.config')
cfg.CONF.import_opt('zk_hosts', 'heat.common.config')
cfg.CONF.import_opt('zk_lock_acquire_timeout', 'heat.common.config')

from heat.common import exception
from heat.db import api as db_api

from heat.openstack.common import log as logging

logger = logging.getLogger(__name__)

if cfg.CONF.distributed_lock_driver == 'zookeeper':
    from kazoo.client import KazooClient
    from kazoo.recipe.lock import Lock as KazooLock
    from kazoo import exceptions as kazoo_exceptions


class ZookeeperConnectionTimeout(exception.HeatException):
    message = _("Unable to connect to Zookeeper on: %(hosts)s")


class StackZKLock(object):
    def __init__(self, context, stack_identity):
        self.context = context
        self.stack = db_api.stack_get(context, stack_identity['stack_id'])
        self.engine_id = cfg.CONF.engine_id
        zk_hosts = ",".join(cfg.CONF.zk_hosts)
        self.zk = KazooClient(hosts=zk_hosts)
        try:
            self.zk.start()
        except kazoo_exceptions.TimeoutError as exc:
            logger.exception(exc)
            raise ZookeeperConnectionTimeout(hosts=zk_hosts)
        self.lock_name = "%s_%s" % (self.context.tenant, self.stack.name)
        self.lock = KazooLock(self.zk, self.lock_name)

    def acquire(self):
        """Acquire a lock on the stack"""
        timeout = cfg.CONF.zk_lock_acquire_timeout
        try:
            self.lock.acquire(blocking=True, timeout=timeout)
        except kazoo_exceptions.LockTimeout as exc:
            logger.exception(exc)
            lock = self.zk.get(self.lock_name)[1]
            logger.debug("Stack lock is owned by engine with ZK owner id %s"
                         % lock.ephemeralOwner)
            raise exception.ActionInProgress(stack_name=self.stack.name,
                                             action=self.stack.action)

    def release(self):
        """Release a stack lock"""
        self.lock.release()


class StackDBLock(object):
    def __init__(self, context, stack_identity):
        self.context = context
        self.stack = db_api.stack_get(context, stack_identity['stack_id'])
        self.engine_id = cfg.CONF.engine_id

    @staticmethod
    def _lock_staleness(lock):
        """Returns number of seconds since stack was created or updated."""
        if lock.updated_at:
            changed_time = lock.updated_at
        else:
            changed_time = lock.created_at
        changed_epoch = float(changed_time.strftime('%s'))
        current_epoch = time.time()
        return current_epoch - changed_epoch

    def acquire(self):
        """Acquire a lock on the stack"""
        existing_lock = db_api.stack_lock_get(self.context, self.stack.id)
        if existing_lock:
            if self._lock_staleness(existing_lock) > cfg.CONF.db_lock_timeout:
                # Lock expired, so grab the lock
                db_api.stack_lock_force(self.context, self.stack.id,
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
        db_api.stack_lock_release(self.context, self.stack.id, self.engine_id)


if cfg.CONF.distributed_lock_driver == 'zookeeper':
    StackLock = StackZKLock
elif cfg.CONF.distributed_lock_driver == 'database':
    StackLock = StackDBLock
