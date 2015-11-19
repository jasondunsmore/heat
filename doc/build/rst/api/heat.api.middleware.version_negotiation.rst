
The ``heat.api.middleware.version_negotiation`` Module
======================================================

Inspects the requested URI for a version string and/or Accept headers.

Also attempts to negotiate an API controller to return.

**class
heat.api.middleware.version_negotiation.VersionNegotiationFilter(version_controller,
app, conf, **local_conf)**

   Bases: ``heat.common.wsgi.Middleware``

   **process_request(req)**

      Process Accept header or simply return correct API controller.

      If there is a version identifier in the URI, return the correct
      API controller, otherwise, if we find an Accept: header, process
      it
