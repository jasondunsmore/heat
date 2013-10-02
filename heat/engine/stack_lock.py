
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

from heat.common import exception
from heat.db import api as db_api

from heat.openstack.common import log as logging
from heat.openstack.common import uuidutils
from heat.openstack.common.rpc import proxy
from heat.openstack.common.rpc.common import Timeout

logger = logging.getLogger(__name__)
engine_id = uuidutils.generate_uuid()


class StackLock(object):

    def __init__(self, context, stack):
        self.context = context
        self.stack = stack
        self.listener = None
        # TODO(jason): Make this an option in config.py
        self.rpc_timeout = 5

    def engine_alive(self, engine_id):
        topic = engine_id
        rpc = proxy.RpcProxy(topic, "1.0")
        try:
            listening = rpc.call(self.context, rpc.make_msg("listening"),
                                 topic=topic, timeout=self.rpc_timeout)
        except Timeout:
            return False

        if listening is True:
            return True
        else:
            raise exception.Error("Call to EngineListener.listening() did not "
                                  "return True.  Return value was: \"%s\""
                                  % listening)

    def acquire(self):
        """Acquire a lock on the stack."""
        existing_lock = db_api.stack_lock_get(self.context, self.stack.id)
        if existing_lock is not None:
            if self.engine_alive(existing_lock.engine_id):
                logger.debug("Stack lock is owned by engine %s"
                             % existing_lock.engine_id)
                raise exception.ActionInProgress(stack_name=self.stack.name,
                                                 action=self.stack.action)
            else:
                db_api.stack_lock_steal(self.context, self.stack.id, engine_id)
                logger.info("Stale lock detected.  Engine %s stole the lock"
                            % engine_id)

        else:
            db_api.stack_lock_create(self.context, self.stack.id, engine_id)
            logger.debug("Acquired lock for engine: %s, stack: %s, action: %s"
                         % (engine_id, self.stack.id, self.stack.action))

    def release(self):
        """Release a stack lock."""
        db_api.stack_lock_release(self.context, self.stack.id)
        logger.debug("Released lock for engine: %s, stack: %s, action: %s"
                     % (engine_id, self.stack.id, self.stack.action))

    def _gt_callback_release(self, gt, *args, **kwargs):
        """Callback function that will be passed to GreenThread.link()."""
        # If gt.wait() isn't called here and a lock exists, then the
        # pending _gt_callback_release() from the previous acquire()
        # will be executed immediately upon the next call to
        # acquire().  This leads to a pre-mature release of the lock.
        gt.wait()
        self.release()
