
The ``heat.objects.stack_lock`` Module
======================================

StackLock object.

**class heat.objects.stack_lock.StackLock(context=None, **kwargs)**

   Bases: ``oslo_versionedobjects.base.VersionedObject``,
   ``oslo_versionedobjects.base.VersionedObjectDictCompat``,
   ``oslo_versionedobjects.base.ComparableVersionedObject``

   ``classmethod create(stack_id, engine_id)``

   ``fields = {'stack_id': String( ... fault'>,nullable=True)}``

   ``classmethod get_engine_id(stack_id)``

   ``classmethod release(stack_id, engine_id)``

   ``classmethod steal(stack_id, old_engine_id, new_engine_id)``
