
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

cfg.CONF.import_opt('engine_life_check_timeout', 'heat.common.config')

from heat.common import exception
from heat.db import api as db_api

from heat.openstack.common import log as logging
from heat.openstack.common import uuidutils
from heat.openstack.common.db import exception as db_exception
from heat.openstack.common.rpc import proxy
from heat.openstack.common.rpc.common import Timeout

logger = logging.getLogger(__name__)
engine_id = uuidutils.generate_uuid()


class StackLock(object):
    def __init__(self, context, stack):
        self.context = context
        self.stack = stack
        self.listener = None

    def _engine_alive(self, engine_id):
        topic = engine_id
        rpc = proxy.RpcProxy(topic, "1.0")
        msg = rpc.make_msg("listening")
        try:
            return rpc.call(self.context, msg, topic=topic,
                            timeout=cfg.CONF.engine_life_check_timeout)
        except Timeout:
            return False

    def acquire(self):
        """Acquire a lock on the stack."""
        try:
            existing_lock = db_api.stack_lock_create(self.stack.id, engine_id)
            logger.debug("Engine %s acquired lock on stack %s (%s)"
                         % (engine_id, self.stack.id, self.stack.action))

        except db_exception.DBDuplicateEntry:
            if existing_lock.engine_id == engine_id or \
               self._engine_alive(existing_lock.engine_id):
                logger.debug("Stack lock is owned by engine %s"
                             % existing_lock.engine_id)
                raise exception.ActionInProgress(stack_name=self.stack.name,
                                                 action=self.stack.action)
            else:
                logger.info("Stale lock detected.  Engine %s will attempt "
                            "to steal the lock" % engine_id)

                rows_affected = db_api.stack_lock_steal(
                    self.stack.id, existing_lock.engine_id, engine_id)

                if rows_affected == 0:  # old_engine_id didn't match
                    raise exception.ActionInProgress(
                        stack_name=self.stack.name, action=self.stack.action)

                logger.info("Engine %s successfully stole the lock"
                            % engine_id)

    def release(self):
        """Release a stack lock."""
        rows_affected = db_api.stack_lock_release(self.stack.id)
        if rows_affected == 0:
            logger.debug("Lock was already released on stack %s (%s)"
                         % (self.stack.id, self.stack.action))
        else:
            logger.debug("Engine %s released lock on stack %s (%s)"
                         % (engine_id, self.stack.id, self.stack.action))

    def _gt_callback_release(self, gt, *args, **kwargs):
        """Callback function that will be passed to GreenThread.link()."""
        # If gt.wait() isn't called here and a lock exists, then the
        # pending _gt_callback_release() from the previous acquire()
        # will be executed immediately upon the next call to
        # acquire().  This leads to a pre-mature release of the lock.
        gt.wait()
        self.release()
