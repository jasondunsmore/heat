
The ``heat.engine.hot.template`` Module
***************************************

**class heat.engine.hot.template.HOTemplate20130523(template,
template_id=None, files=None, env=None)**

   Bases: `heat.engine.template.Template
   <heat.engine.template.rst#heat.engine.template.Template>`_

   A Heat Orchestration Template format stack template.

   ``DESCRIPTION = 'description'``

   ``MAPPINGS = '__undefined__'``

   ``OUTPUTS = 'outputs'``

   ``PARAMETERS = 'parameters'``

   ``PARAMETER_GROUPS = 'parameter_groups'``

   ``RESOURCES = 'resources'``

   ``SECTIONS = ('heat_template_vers ... puts', '__undefined__')``

   ``SECTIONS_NO_DIRECT_ACCESS = set(['heat_template_version',
   'parameters'])``

   ``VERSION = 'heat_template_version'``

   **add_resource(definition, name=None)**

   ``deletion_policies = {'Retain': 'Retain', 'Snapshot': 'Snapshot',
   'Delete': 'Delete'}``

   ``functions = {'Fn::ResourceFacade ... unctions.ResourceRef'>}``

   **get_section_name(section)**

   **param_schemata(param_defaults=None)**

   **parameters(stack_identifier, user_params, param_defaults=None)**

   **resource_definitions(stack)**

   ``static rsrc_defn_from_snippet(name, data)``

   **validate_resource_definitions(stack)**

**class heat.engine.hot.template.HOTemplate20141016(template,
template_id=None, files=None, env=None)**

   Bases: ``heat.engine.hot.template.HOTemplate20130523``

   ``functions = {'Fn::ResourceFacade ... unctions.ResourceRef'>}``

**class heat.engine.hot.template.HOTemplate20150430(template,
template_id=None, files=None, env=None)**

   Bases: ``heat.engine.hot.template.HOTemplate20141016``

   ``functions = {'Fn::ResourceFacade ... unctions.ResourceRef'>}``

**class heat.engine.hot.template.HOTemplate20151015(template,
template_id=None, files=None, env=None)**

   Bases: ``heat.engine.hot.template.HOTemplate20150430``

   ``functions = {'Fn::ResourceFacade ... unctions.ResourceRef'>}``

**class heat.engine.hot.template.HOTemplate20160408(template,
template_id=None, files=None, env=None)**

   Bases: ``heat.engine.hot.template.HOTemplate20151015``

   ``functions = {'Fn::ResourceFacade ... unctions.ResourceRef'>}``
