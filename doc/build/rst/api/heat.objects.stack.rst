
The ``heat.objects.stack`` Module
=================================

Stack object.

**class heat.objects.stack.Stack(context=None, **kwargs)**

   Bases: ``oslo_versionedobjects.base.VersionedObject``,
   ``oslo_versionedobjects.base.VersionedObjectDictCompat``,
   ``oslo_versionedobjects.base.ComparableVersionedObject``

   ``classmethod count_all(context, **kwargs)``

   ``classmethod count_total_resources(context, stack_id)``

   ``classmethod create(context, values)``

   ``classmethod delete(context, stack_id)``

   ``classmethod encrypt_hidden_parameters(tmpl)``

   ``fields = {'status': String(de ... ault'>,nullable=False)}``

   ``classmethod get_all(context, *args, **kwargs)``

   ``classmethod get_all_by_owner_id(context, owner_id)``

   ``classmethod get_by_id(context, stack_id, **kwargs)``

   ``classmethod get_by_name(context, stack_name)``

   ``classmethod get_by_name_and_owner_id(context, stack_name,
   owner_id)``

   ``classmethod get_root_id(context, stack_id)``

   ``classmethod persist_state_and_release_lock(context, stack_id,
   engine_id, values)``

   **refresh()**

   ``classmethod select_and_update(context, stack_id, values,
   exp_trvsl=None)``

      Update the stack by selecting on traversal ID.

      If the stack is found with given traversal, it is updated.

      If there occurs a race while updating, only one will succeed and
      other will get return value of False.

   **update_and_save(values)**

   ``classmethod update_by_id(context, stack_id, values)``

      Update and return (boolean) if it was updated.

      Note: the underlying stack_update filters by current_traversal
      and stack_id.
