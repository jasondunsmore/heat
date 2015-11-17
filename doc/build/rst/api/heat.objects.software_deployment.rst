
The ``heat.objects.software_deployment`` Module
***********************************************

SoftwareDeployment object.

**class
heat.objects.software_deployment.SoftwareDeployment(context=None,
**kwargs)**

   Bases: ``oslo_versionedobjects.base.VersionedObject``,
   ``oslo_versionedobjects.base.VersionedObjectDictCompat``,
   ``oslo_versionedobjects.base.ComparableVersionedObject``

   ``classmethod create(context, values)``

   ``classmethod delete(context, deployment_id)``

   ``fields = {'status': String(de ... ault'>,nullable=False)}``

   ``classmethod get_all(context, server_id=None)``

   ``classmethod get_by_id(context, deployment_id)``

   ``classmethod update_by_id(context, deployment_id, values)``

      Note this is a bit unusual as it returns the object.

      Other update_by_id methods return a bool (was it updated).
