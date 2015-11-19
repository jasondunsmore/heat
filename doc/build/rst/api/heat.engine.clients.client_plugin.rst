
The ``heat.engine.clients.client_plugin`` Module
================================================

**class heat.engine.clients.client_plugin.ClientPlugin(context)**

   Bases: ``object``

   ``auth_token``

   **client()**

   ``clients``

   ``context``

   **does_endpoint_exist(service_type, service_name)**

   ``exceptions_module = None``

   ``ignore_conflict_and_not_found``

      Raises the exception unless it is a conflict or not-found.

   ``ignore_not_found``

      Raises the exception unless it is a not-found.

   **is_client_exception(ex)**

      Returns True if the current exception comes from the client.

   **is_conflict(ex)**

      Returns True if the exception is a conflict.

   **is_not_found(ex)**

      Returns True if the exception is a not-found.

   **is_over_limit(ex)**

      Returns True if the exception is an over-limit.

   ``service_types = []``

   **url_for(**kwargs)**

**class
heat.engine.clients.client_plugin.ExceptionFilter(should_ignore_ex)**

   Bases: ``object``

   A context manager that prevents some exceptions from being raised.

   For backwards compatibility, these objects can also be called with
   the exception value as an argument - any non-matching exception
   will be re-raised from this call. We attempt but cannot guarantee
   to keep the same traceback; the context manager method is preferred
   for this reason except in cases where the ignored exception affects
   control flow.

   Use this class as a decorator for a function that returns whether a
   given exception should be ignored. e.g.

   >>> @ExceptionFilter
   >>> def ignore_assertions(ex):
   ...     return isinstance(ex, AssertionError)

   and then use it as a context manager:

   >>> with ignore_assertions:
   ...     assert False

   or call it:

   >>> try:
   ...     assert False
   ... except Exception as ex:
   ...     ignore_assertions(ex)
