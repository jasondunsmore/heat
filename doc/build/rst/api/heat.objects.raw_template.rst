
The ``heat.objects.raw_template`` Module
========================================

RawTemplate object.

**class heat.objects.raw_template.RawTemplate(context=None,
**kwargs)**

   Bases: ``oslo_versionedobjects.base.VersionedObject``,
   ``oslo_versionedobjects.base.VersionedObjectDictCompat``,
   ``oslo_versionedobjects.base.ComparableVersionedObject``

   ``classmethod create(context, values)``

   ``classmethod delete(context, template_id)``

   ``classmethod encrypt_hidden_parameters(tmpl)``

   ``fields = {'files': NoneType(d ... ault'>,nullable=False)}``

   ``classmethod get_by_id(context, template_id)``

   ``classmethod update_by_id(context, template_id, values)``
