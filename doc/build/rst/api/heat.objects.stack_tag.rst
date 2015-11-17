
The ``heat.objects.stack_tag`` Module
*************************************

StackTag object.

**class heat.objects.stack_tag.StackTag(context=None, **kwargs)**

   Bases: ``oslo_versionedobjects.base.VersionedObject``,
   ``oslo_versionedobjects.base.VersionedObjectDictCompat``,
   ``oslo_versionedobjects.base.ComparableVersionedObject``

   ``fields = {'stack_id': String( ... fault'>,nullable=True)}``

   ``classmethod get_obj(context, tag)``

**class heat.objects.stack_tag.StackTagList(*args, **kwargs)**

   Bases: ``oslo_versionedobjects.base.VersionedObject``,
   ``oslo_versionedobjects.base.ObjectListBase``

   ``classmethod delete(context, stack_id)``

   ``fields = {'objects': List(def ... ault'>,nullable=False)}``

   ``classmethod get(context, stack_id)``

   ``classmethod set(context, stack_id, tags)``
