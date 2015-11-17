
The ``heat.engine.rsrc_defn`` Module
************************************

**class heat.engine.rsrc_defn.ResourceDefinition(name, resource_type,
properties=None, metadata=None, depends=None, deletion_policy=None,
update_policy=None, description=None)**

   Bases: ``heat.engine.rsrc_defn.ResourceDefinitionCore``,
   ``_abcoll.Mapping``

   A resource definition that also acts like a cfn template snippet.

   This class exists only for backwards compatibility with existing
   resource plugins and unit tests; it is deprecated and then could be
   replaced with ResourceDefinitionCore as soon as M release.
