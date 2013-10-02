
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

import datetime
import mox
import sqlalchemy
import time

from kazoo import exceptions as kazoo_exceptions
from kazoo.client import KazooClient
from kazoo.recipe.lock import Lock as KazooLock

from oslo.config import cfg

# Ensure the kazoo libraries are loaded in stack_lock.py
cfg.CONF.import_opt('distributed_lock_driver', 'heat.common.config')
cfg.CONF.set_override('distributed_lock_driver', 'zookeeper')

from heat.common import exception
from heat.common import identifier
from heat.db import api as db_api
from heat.engine import stack_lock
from heat.tests.common import HeatTestCase
from heat.tests import utils


class StackZKLockTest(HeatTestCase):
    def setUp(self):
        super(StackZKLockTest, self).setUp()
        utils.setup_dummy_db()
        cfg.CONF.set_override('distributed_lock_driver', 'zookeeper')
        self.context = utils.dummy_context()
        self.context.tenant = "1234"
        self.stack = self.m.CreateMockAnything()
        self.stack.name = "test_stack"
        self.stack.action = "CREATE"
        self.zk = KazooClient(hosts="1.2.3.4")
        self.m.StubOutWithMock(KazooClient, "start")
        self.zk.start().AndReturn(None)

    def test_successful_acquire(self):
        self.m.StubOutWithMock(KazooClient, "get")
        self.zk.get(mox.IgnoreArg()).AndRaise(kazoo_exceptions.NoNodeError())
        self.m.StubOutWithMock(KazooLock, "acquire")
        lock = KazooLock(self.zk, "%s_%s" % (self.context.tenant,
                                             self.stack.name))
        lock.acquire(blocking=True, timeout=mox.IgnoreArg()).AndReturn(True)
        self.m.ReplayAll()
        slock = stack_lock.StackZKLock(self.context, self.stack)
        slock.acquire()
        self.m.VerifyAll()

    def test_failed_acquire_current_engine(self):
        existing_lock = self.m.CreateMockAnything()
        existing_lock.numChildren = 1
        existing_lock.ephemeralOwner = 1
        zknodestat = ('', existing_lock)
        self.m.StubOutWithMock(KazooClient, "get")
        self.zk.get(mox.IgnoreArg()).AndReturn(zknodestat)
        self.m.ReplayAll()
        slock = stack_lock.StackZKLock(self.context, self.stack)
        self.assertRaises(exception.ActionInProgress, slock.acquire)
        self.m.VerifyAll()

    def test_failed_acquire_other_engine(self):
        existing_lock = self.m.CreateMockAnything()
        existing_lock.numChildren = 1
        existing_lock.ephemeralOwner = 2
        zknodestat = ('', existing_lock)
        self.m.StubOutWithMock(KazooClient, "get")
        self.zk.get(mox.IgnoreArg()).AndReturn(zknodestat)
        self.m.ReplayAll()
        slock = stack_lock.StackZKLock(self.context, self.stack)
        self.assertRaises(exception.ActionInProgress, slock.acquire)
        self.m.VerifyAll()

    def test_failed_acquire_timeout(self):
        self.m.StubOutWithMock(KazooClient, "get")
        self.zk.get(mox.IgnoreArg()).AndRaise(kazoo_exceptions.NoNodeError())
        self.m.StubOutWithMock(KazooLock, "acquire")
        lock = KazooLock(self.zk, "%s_%s" % (self.context.tenant,
                                             self.stack.name))
        lock.acquire(blocking=True, timeout=mox.IgnoreArg())\
            .AndRaise(kazoo_exceptions.LockTimeout)
        self.m.ReplayAll()
        slock = stack_lock.StackZKLock(self.context, self.stack)
        self.assertRaises(exception.ActionInProgress, slock.acquire)
        self.m.VerifyAll()


class StackDBLockTest(HeatTestCase):
    def setUp(self):
        super(StackDBLockTest, self).setUp()
        utils.setup_dummy_db()
        cfg.CONF.set_override('distributed_lock_driver', 'database')
        cfg.CONF.set_override('db_lock_timeout', 10)
        self.context = utils.dummy_context()
        self.stack = self.m.CreateMockAnything()
        self.stack.id = "aae01f2d-52ae-47ac-8a0d-3fde3d220fea"
        self.stack.name = "test_stack"
        self.stack.action = "CREATE"

    def test_successful_acquire_new_lock(self):
        self.m.StubOutWithMock(db_api, "stack_lock_get")
        db_api.stack_lock_get(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(None)
        self.m.StubOutWithMock(db_api, "stack_lock_create")
        db_api.stack_lock_create(mox.IgnoreArg(), mox.IgnoreArg(),
                                 mox.IgnoreArg()).AndReturn(None)
        self.m.ReplayAll()
        slock = stack_lock.StackDBLock(self.context, self.stack)
        slock.acquire()
        self.m.VerifyAll()

    def test_successful_acquire_force_lock_updated(self):
        existing_lock = self.m.CreateMockAnything()
        existing_lock.updated_at = datetime.datetime(2012, 10, 16, 18, 35, 18)
        current_time = datetime.datetime(2012, 10, 16, 18, 35, 29)
        current_timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        self.m.StubOutWithMock(sqlalchemy.func, "current_timestamp")
        sqlalchemy.func.current_timestamp().AndReturn(current_timestamp)
        self.m.StubOutWithMock(db_api, "stack_lock_get")
        db_api.stack_lock_get(mox.IgnoreArg(), mox.IgnoreArg())\
              .AndReturn(existing_lock)
        self.m.StubOutWithMock(db_api, "stack_lock_steal")
        db_api.stack_lock_steal(mox.IgnoreArg(), mox.IgnoreArg(),
                                mox.IgnoreArg()).AndReturn(None)
        self.m.ReplayAll()
        slock = stack_lock.StackDBLock(self.context, self.stack)
        slock.acquire()
        self.m.VerifyAll()

    def test_successful_acquire_force_lock_created(self):
        existing_lock = self.m.CreateMockAnything()
        existing_lock.updated_at = None
        existing_lock.created_at = datetime.datetime(2012, 10, 16, 18, 35, 18)
        current_epoch = float(existing_lock.created_at.strftime('%s'))
        self.m.StubOutWithMock(time, "time")
        time.time().MultipleTimes().AndReturn(current_epoch + 11)
        self.m.StubOutWithMock(db_api, "stack_lock_get")
        db_api.stack_lock_get(mox.IgnoreArg(), mox.IgnoreArg())\
              .AndReturn(existing_lock)
        self.m.StubOutWithMock(db_api, "stack_lock_steal")
        db_api.stack_lock_steal(mox.IgnoreArg(), mox.IgnoreArg(),
                                mox.IgnoreArg()).AndReturn(None)
        self.m.ReplayAll()
        slock = stack_lock.StackDBLock(self.context, self.stack)
        slock.acquire()
        self.m.VerifyAll()

    def test_failed_acquire(self):
        existing_lock = self.m.CreateMockAnything()
        existing_lock.updated_at = datetime.datetime(2012, 10, 16, 18, 35, 18)
        current_epoch = float(existing_lock.updated_at.strftime('%s'))
        self.m.StubOutWithMock(time, "time")
        time.time().MultipleTimes().AndReturn(current_epoch + 9)
        self.m.StubOutWithMock(db_api, "stack_lock_get")
        db_api.stack_lock_get(mox.IgnoreArg(), mox.IgnoreArg())\
              .AndReturn(existing_lock)
        self.m.ReplayAll()
        slock = stack_lock.StackDBLock(self.context, self.stack)
        self.assertRaises(exception.ActionInProgress, slock.acquire)
        self.m.VerifyAll()
