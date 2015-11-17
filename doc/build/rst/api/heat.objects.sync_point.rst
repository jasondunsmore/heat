
The ``heat.objects.sync_point`` Module
**************************************

SyncPoint object.

**class heat.objects.sync_point.SyncPoint(context=None, **kwargs)**

   Bases: ``oslo_versionedobjects.base.VersionedObject``,
   ``oslo_versionedobjects.base.VersionedObjectDictCompat``,
   ``oslo_versionedobjects.base.ComparableVersionedObject``

   ``classmethod create(context, values)``

   ``classmethod delete_all_by_stack_and_traversal(context, stack_id,
   traversal_id)``

   ``fields = {'input_data': NoneT ... fault'>,nullable=True)}``

   ``classmethod get_by_key(context, entity_id, traversal_id,
   is_update)``

   ``classmethod update_input_data(context, entity_id, traversal_id,
   is_update, atomic_key, input_data)``
