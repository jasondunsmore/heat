
The ``heat.engine.stack_lock`` Module
=====================================

**class heat.engine.stack_lock.StackLock(context, stack_id,
engine_id)**

   Bases: ``object``

   **acquire(retry=True)**

      Acquire a lock on the stack.

      :Parameters:
         **retry** (*boolean*) -- When True, retry if lock was
         released while stealing.

   ``static engine_alive(context, engine_id)``

   ``static generate_engine_id()``

   **get_engine_id()**

   **release()**

      Release a stack lock.

   **thread_lock(*args, **kwds)**

      Acquire a lock and release it only if there is an exception.

      The release method still needs to be scheduled to be run at the
      end of the thread using the Thread.link method.

   **try_acquire()**

      Try to acquire a stack lock.

      Don't raise an ActionInProgress exception or try to steal lock.

   **try_thread_lock(*args, **kwds)**

      Similar to thread_lock, but acquire the lock using try_acquire.

      Only release it upon any exception after a successful
      acquisition.
