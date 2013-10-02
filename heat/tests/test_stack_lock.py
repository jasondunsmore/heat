
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

from heat.common import exception
from heat.db import api as db_api
from heat.engine import stack_lock
from heat.openstack.common.rpc import proxy
from heat.openstack.common.rpc.common import Timeout
from heat.tests.common import HeatTestCase
from heat.tests import utils


class StackLockTest(HeatTestCase):
    def setUp(self):
        super(StackLockTest, self).setUp()
        utils.setup_dummy_db()
        self.context = utils.dummy_context()
        self.stack = self.m.CreateMockAnything()
        self.stack.id = "aae01f2d-52ae-47ac-8a0d-3fde3d220fea"
        self.stack.name = "test_stack"
        self.stack.action = "CREATE"

    def test_successful_acquire_new_lock(self):
        self.m.StubOutWithMock(db_api, "stack_lock_create")
        db_api.stack_lock_create(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(1)

        self.m.ReplayAll()

        slock = stack_lock.StackLock(self.context, self.stack)
        slock.acquire()
        self.m.VerifyAll()

    def test_successful_acquire_existing_lock_engine_dead(self):
        existing_lock = self.m.CreateMockAnything()
        self.m.StubOutWithMock(db_api, "stack_lock_get")
        db_api.stack_lock_get(mox.IgnoreArg()).AndReturn(existing_lock)

        topic = self.stack.id
        self.m.StubOutWithMock(proxy.RpcProxy, "call")
        rpc = proxy.RpcProxy(topic, "1.0")
        rpc.call(self.context, rpc.make_msg("listening"), timeout=2,
                 topic=mox.IgnoreArg()).AndRaise(Timeout)

        self.m.StubOutWithMock(db_api, "stack_lock_steal")
        db_api.stack_lock_steal(mox.IgnoreArg(), mox.IgnoreArg()).\
            AndReturn(1)

        self.m.ReplayAll()

        slock = stack_lock.StackLock(self.context, self.stack)
        slock.acquire()
        self.m.VerifyAll()

    def test_failed_acquire_existing_lock_engine_dead(self):
        existing_lock = self.m.CreateMockAnything()
        self.m.StubOutWithMock(db_api, "stack_lock_get")
        db_api.stack_lock_get(mox.IgnoreArg()).AndReturn(existing_lock)

        topic = self.stack.id
        self.m.StubOutWithMock(proxy.RpcProxy, "call")
        rpc = proxy.RpcProxy(topic, "1.0")
        rpc.call(self.context, rpc.make_msg("listening"), timeout=2,
                 topic=mox.IgnoreArg()).AndRaise(Timeout)

        self.m.StubOutWithMock(db_api, "stack_lock_steal")
        db_api.stack_lock_steal(mox.IgnoreArg(), mox.IgnoreArg()).\
            AndReturn(0)

        self.m.ReplayAll()

        slock = stack_lock.StackLock(self.context, self.stack)
        exc = self.assertRaises(exception.Error, slock.acquire)
        self.assertIn("failed to steal the lock", str(exc))
        self.m.VerifyAll()

    def test_failed_acquire_existing_lock_engine_alive(self):
        existing_lock = self.m.CreateMockAnything()
        self.m.StubOutWithMock(db_api, "stack_lock_get")
        db_api.stack_lock_get(mox.IgnoreArg()).AndReturn(existing_lock)

        topic = self.stack.id
        self.m.StubOutWithMock(proxy.RpcProxy, "call")
        rpc = proxy.RpcProxy(topic, "1.0")
        rpc.call(self.context, rpc.make_msg("listening"), timeout=2,
                 topic=mox.IgnoreArg()).AndReturn(True)

        self.m.ReplayAll()

        slock = stack_lock.StackLock(self.context, self.stack)
        self.assertRaises(exception.ActionInProgress, slock.acquire)
        self.m.VerifyAll()

    def test_failed_acquire_existing_lock_current_engine(self):
        existing_lock = self.m.CreateMockAnything()
        existing_lock.engine_id = stack_lock.engine_id
        self.m.StubOutWithMock(db_api, "stack_lock_get")
        db_api.stack_lock_get(mox.IgnoreArg()).AndReturn(existing_lock)

        self.m.ReplayAll()

        slock = stack_lock.StackLock(self.context, self.stack)
        self.assertRaises(exception.ActionInProgress, slock.acquire)
        self.m.VerifyAll()
