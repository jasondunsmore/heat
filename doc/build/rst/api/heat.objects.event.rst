
The ``heat.objects.event`` Module
*********************************

Event object.

**class heat.objects.event.Event(context=None, **kwargs)**

   Bases: ``oslo_versionedobjects.base.VersionedObject``,
   ``oslo_versionedobjects.base.VersionedObjectDictCompat``

   ``classmethod count_all_by_stack(context, stack_id)``

   ``classmethod create(context, values)``

   ``fields = {'resource_name': St ... fault'>,nullable=True)}``

   ``classmethod get_all(context)``

   ``classmethod get_all_by_stack(context, stack_id, **kwargs)``

   ``classmethod get_all_by_tenant(context, **kwargs)``

   ``classmethod get_by_id(context, event_id)``
