
The `heat.engine.scheduler <../../api/heat.engine.scheduler.rst#module-heat.engine.scheduler>`_ Module
******************************************************************************************************

**class heat.engine.scheduler.DependencyTaskGroup(dependencies,
task=<function <lambda> at 0x7ff2ca30d848>, reverse=False, name=None,
error_wait_time=None, aggregate_exceptions=False)**

   Bases: ``object``

   Task which manages group of subtasks that have ordering
   dependencies.

   **cancel_all(grace_period=None)**

**exception heat.engine.scheduler.ExceptionGroup(exceptions=None)**

   Bases: ``exceptions.Exception``

   Container for multiple exceptions.

   This exception is used by DependencyTaskGroup when the flag
   aggregate_exceptions is set to True and it's re-raised again when
   all tasks are finished.  This way it can be caught later on so that
   the individual exceptions can be acted upon.

**class heat.engine.scheduler.TaskRunner(task, *args, **kwargs)**

   Bases: ``object``

   Wrapper for a resumable task (co-routine).

   **cancel(grace_period=None)**

      Cancel the task and mark it as done.

   **done()**

      Return True if the task is complete.

   **run_to_completion(wait_time=1)**

      Run the task to completion.

      The task will sleep for *wait_time* seconds between steps. To
      avoid sleeping, pass *None* for *wait_time*.

   **start(timeout=None)**

      Initialise the task and run its first step.

      If a timeout is specified, any attempt to step the task after
      that number of seconds has elapsed will result in a Timeout
      being raised inside the task.

   **started()**

      Return True if the task has been started.

   **step()**

      Run another step of the task.

      Return True if the task is complete; False otherwise.

**exception heat.engine.scheduler.TimedCancel(task_runner, timeout)**

   Bases: `heat.engine.scheduler.Timeout
   <../../api/heat.engine.scheduler.rst#heat.engine.scheduler.Timeout>`_

   **trigger(generator)**

      Trigger the timeout on a given generator.

**exception heat.engine.scheduler.Timeout(task_runner, timeout)**

   Bases: ``exceptions.BaseException``

   Raised when task has exceeded its allotted (wallclock) running
   time.

   This allows the task to perform any necessary cleanup, as well as
   use a different exception to notify the controlling task if
   appropriate. If the task suppresses the exception altogether, it
   will be cancelled but the controlling task will not be notified of
   the timeout.

   **expired()**

   **trigger(generator)**

      Trigger the timeout on a given generator.

**heat.engine.scheduler.task_description(task)**

   Return a human-readable string description of a task.

   The description is used to identify the task when logging its
   status.

**heat.engine.scheduler.wrappertask(task)**

   Decorator for a task that needs to drive a subtask.

   This is essentially a replacement for the Python 3-only "yield
   from" keyword (PEP 380), using the "yield" keyword that is
   supported in Python 2. For example:

   ::

      @wrappertask
      def parent_task(self):
          self.setup()

          yield self.child_task()

          self.cleanup()
