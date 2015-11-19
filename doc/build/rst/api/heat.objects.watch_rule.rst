
The ``heat.objects.watch_rule`` Module
======================================

WatchRule object.

**class heat.objects.watch_rule.WatchRule(context=None, **kwargs)**

   Bases: ``oslo_versionedobjects.base.VersionedObject``,
   ``oslo_versionedobjects.base.VersionedObjectDictCompat``

   ``classmethod create(context, values)``

   ``classmethod delete(context, watch_id)``

   ``fields = {'updated_at': DateT ... ault'>,nullable=False)}``

   ``classmethod get_all(context)``

   ``classmethod get_all_by_stack(context, stack_id)``

   ``classmethod get_by_id(context, rule_id)``

   ``classmethod get_by_name(context, watch_rule_name)``

   ``classmethod update_by_id(context, watch_id, values)``
