
The ``heat.objects.resource`` Module
====================================

Resource object.

**class heat.objects.resource.Resource(context=None, **kwargs)**

   Bases: ``oslo_versionedobjects.base.VersionedObject``,
   ``oslo_versionedobjects.base.VersionedObjectDictCompat``,
   ``oslo_versionedobjects.base.ComparableVersionedObject``

   ``classmethod create(context, values)``

   ``classmethod delete(context, resource_id)``

   ``static encrypt_properties_data(data)``

   ``classmethod exchange_stacks(context, resource_id1,
   resource_id2)``

   ``fields = {'rsrc_metadata': No ... fault'>,nullable=True)}``

   ``classmethod get_all(context)``

   ``classmethod get_all_by_stack(context, stack_id, key_id=False)``

   ``classmethod get_by_name_and_stack(context, resource_name,
   stack_id)``

   ``classmethod get_by_physical_resource_id(context,
   physical_resource_id)``

   ``classmethod get_obj(context, resource_id)``

   **refresh(attrs=None)**

   **select_and_update(values, expected_engine_id=None,
   atomic_key=0)**

   **update_and_save(values)**
