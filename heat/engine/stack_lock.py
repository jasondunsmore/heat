"""Stack """

import time

from oslo.config import cfg

cfg.CONF.import_opt('distributed_lock_driver', 'heat.common.config')
cfg.CONF.import_opt('engine_id', 'heat.common.config')
cfg.CONF.import_opt('zk_lock_acquire_timeout', 'heat.common.config')

from heat.common import exception

if cfg.CONF.distributed_lock_driver == 'zookeeper':
    from kazoo.client import KazooClient
    from kazoo.recipe.lock import Lock as KazooLock

from heat.db import api as db_api


class StackZKLock(object):
    """"""
    def __init__(self, context, stack_identity):
        self.context = context
        self.stack = db_api.stack_get(context, stack_identity['stack_id'])
        self.engine_id = cfg.CONF.engine_id
        zk = KazooClient(hosts='127.0.0.1:2181')
        zk.start()
        lock_name = "%s_%s_%s" % (self.engine_id, self.context.tenant,
                                  self.stack.name)
        self.lock = KazooLock(zk, lock_name)

    def acquire(self):
        """Acquire a lock on the stack"""
        timeout = cfg.CONF.zk_lock_acquire_timeout
        self.lock.acquire(blocking=True, timeout=timeout)

    def release(self):
        """Release a stack lock"""
        self.lock.release()


class StackDBLock(object):
    """"""
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
            # TODO: Make lock timeout configurable
            if self._lock_staleness(existing_lock) > 300:  # Lock expired
                db_api.stack_lock_force(self.context, self.stack.id,
                                        self.engine_id)
            else:
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
elif cfg.CONF.distributed_lock_driver == 'db':
    StackLock = StackDBLock
