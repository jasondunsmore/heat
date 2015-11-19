
The `heat.engine.cfn.template <../../api/heat.engine.cfn.template.rst#module-heat.engine.cfn.template>`_ Module
===============================================================================================================

**class heat.engine.cfn.template.CfnTemplate(template,
template_id=None, files=None, env=None)**

   Bases: `heat.engine.template.Template
   <../../api/heat.engine.template.rst#heat.engine.template.Template>`_

   A stack template.

   ``ALTERNATE_VERSION = 'HeatTemplateFormatVersion'``

   ``DESCRIPTION = 'Description'``

   ``MAPPINGS = 'Mappings'``

   ``OUTPUTS = 'Outputs'``

   ``PARAMETERS = 'Parameters'``

   ``RESOURCES = 'Resources'``

   ``SECTIONS = ('AWSTemplateFormatV ... 'Resources', 'Outputs')``

   ``SECTIONS_NO_DIRECT_ACCESS = set(['AWSTemplateFor ... ersion',
   'Parameters'])``

   ``VERSION = 'AWSTemplateFormatVersion'``

   **add_resource(definition, name=None)**

   ``deletion_policies = {'Retain': 'Retain', 'Snapshot': 'Snapshot',
   'Delete': 'Delete'}``

   ``functions = {'Fn::Select': <clas ... cfn.functions.Base64'>}``

   **get_section_name(section)**

   **param_schemata(param_defaults=None)**

   **parameters(stack_identifier, user_params, param_defaults=None)**

   **resource_definitions(stack)**

   **validate_resource_definitions(stack)**

**class heat.engine.cfn.template.HeatTemplate(template,
template_id=None, files=None, env=None)**

   Bases: `heat.engine.cfn.template.CfnTemplate
   <../../api/heat.engine.cfn.template.rst#heat.engine.cfn.template.CfnTemplate>`_

   ``functions = {'Fn::Select': <clas ... .functions.FindInMap'>}``
