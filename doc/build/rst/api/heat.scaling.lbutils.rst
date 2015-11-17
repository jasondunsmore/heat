
The ``heat.scaling.lbutils`` Module
***********************************

**heat.scaling.lbutils.reload_loadbalancers(group, load_balancers,
exclude=None)**

   Notify the LoadBalancer to reload its config.

   This must be done after activation (instance in ACTIVE state),
   otherwise the instances' IP addresses may not be available.
