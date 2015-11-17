
The ``heat.api.middleware.fault`` Module
****************************************

A middleware that turns exceptions into parsable string.

Inspired by Cinder's faultwrapper.

**class heat.api.middleware.fault.Fault(error)**

   Bases: ``object``

**class heat.api.middleware.fault.FaultWrapper(application)**

   Bases: ``heat.common.wsgi.Middleware``

   Replace error body with something the client can parse.

   ``error_map = {'InvalidBreakPointH ... b.exc.HTTPBadRequest'>}``

   **process_request(req)**
