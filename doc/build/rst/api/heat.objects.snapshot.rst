
The ``heat.objects.snapshot`` Module
************************************

Snapshot object.

**class heat.objects.snapshot.Snapshot(context=None, **kwargs)**

   Bases: ``oslo_versionedobjects.base.VersionedObject``,
   ``oslo_versionedobjects.base.VersionedObjectDictCompat``,
   ``oslo_versionedobjects.base.ComparableVersionedObject``

   ``classmethod create(context, values)``

   ``classmethod delete(context, snapshot_id)``

   ``fields = {'status': String(de ... fault'>,nullable=True)}``

   ``classmethod get_all(context, stack_id)``

   ``classmethod get_snapshot_by_stack(context, snapshot_id, stack)``

   ``classmethod update(context, snapshot_id, values)``
