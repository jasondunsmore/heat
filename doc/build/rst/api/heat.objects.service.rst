
The ``heat.objects.service`` Module
===================================

Service object.

**class heat.objects.service.Service(context=None, **kwargs)**

   Bases: ``oslo_versionedobjects.base.VersionedObject``,
   ``oslo_versionedobjects.base.VersionedObjectDictCompat``,
   ``oslo_versionedobjects.base.ComparableVersionedObject``

   ``classmethod create(context, values)``

   ``classmethod delete(context, service_id, soft_delete=True)``

   ``fields = {'topic': String(def ... fault'>,nullable=True)}``

   ``classmethod get_all(context)``

   ``classmethod get_all_by_args(context, host, binary, hostname)``

   ``classmethod get_by_id(context, service_id)``

   ``classmethod update_by_id(context, service_id, values)``
