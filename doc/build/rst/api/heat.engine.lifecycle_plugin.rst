
The ``heat.engine.lifecycle_plugin`` Module
===========================================

**class heat.engine.lifecycle_plugin.LifecyclePlugin**

   Bases: ``object``

   Base class for pre-op and post-op work on a stack.

   Implementations should extend this class and override the methods.

   **do_post_op(cnxt, stack, current_stack=None, action=None,
   is_stack_failure=False)**

      Method to be run by heat after stack operations, including
      failures.

      On failure to execute all the registered pre_ops, this method
      will be called if and only if the corresponding pre_op was
      successfully called. On failures of the actual stack operation,
      this method will be called if all the pre operations were
      successfully called.

   **do_pre_op(cnxt, stack, current_stack=None, action=None)**

      Method to be run by heat before stack operations.

   **get_ordinal()**

      Get the sort order for pre and post operation execution.

      The values returned by get_ordinal are used to create a partial
      order for pre and post operation method invocations. The default
      ordinal value of 100 may be overridden. If class1inst.ordinal()
      < class2inst.ordinal(), then the method on class1inst will be
      executed before the method on class2inst. If
      class1inst.ordinal() > class2inst.ordinal(), then the method on
      class1inst will be executed after the method on class2inst. If
      class1inst.ordinal() == class2inst.ordinal(), then the order of
      method invocation is indeterminate.
