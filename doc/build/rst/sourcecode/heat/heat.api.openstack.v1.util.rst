
The `heat.api.openstack.v1.util <../../api/heat.api.openstack.v1.util.rst#module-heat.api.openstack.v1.util>`_ Module
*********************************************************************************************************************

**heat.api.openstack.v1.util.get_allowed_params(params, whitelist)**

   Extract from ``params`` all entries listed in ``whitelist``.

   The returning dict will contain an entry for a key if, and only if,
   there's an entry in ``whitelist`` for that key and at least one
   entry in ``params``. If ``params`` contains multiple entries for
   the same key, it will yield an array of values: ``{key: [v1,
   v2,...]}``

   :Parameters:
      * **params** -- a NestedMultiDict from webob.Request.params

      * **whitelist** -- an array of strings to whitelist

   :Returns:
      a dict with {key: value} pairs

**heat.api.openstack.v1.util.identified_stack(handler)**

   Decorator that passes a stack identifier instead of path
   components.

   This is a handler method decorator.

**heat.api.openstack.v1.util.make_link(req, identity,
relationship='self')**

   Return a link structure for the supplied identity dictionary.

**heat.api.openstack.v1.util.make_url(req, identity)**

   Return the URL for the supplied identity dictionary.

**heat.api.openstack.v1.util.policy_enforce(handler)**

   Decorator that enforces policies.

   Checks the path matches the request context and enforce policy
   defined in policy.json.

   This is a handler method decorator.
