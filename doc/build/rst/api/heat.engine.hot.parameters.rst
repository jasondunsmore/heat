
The ``heat.engine.hot.parameters`` Module
*****************************************

**class heat.engine.hot.parameters.HOTParamSchema(data_type,
description=None, default=None, schema=None, constraints=None,
hidden=False, label=None)**

   Bases: `heat.engine.parameters.Schema
   <heat.engine.parameters.rst#heat.engine.parameters.Schema>`_

   HOT parameter schema.

   ``BOOLEAN = 'boolean'``

   ``CONSTRAINTS = 'constraints'``

   ``DEFAULT = 'default'``

   ``DESCRIPTION = 'description'``

   ``HIDDEN = 'hidden'``

   ``KEYS = ('type', 'descriptio ... ts', 'hidden', 'label')``

   ``LABEL = 'label'``

   ``LIST = 'comma_delimited_list'``

   ``MAP = 'json'``

   ``NUMBER = 'number'``

   ``PARAMETER_KEYS = ('type', 'descriptio ... ts', 'hidden',
   'label')``

   ``SCHEMA = 'schema'``

   ``STRING = 'string'``

   ``TYPE = 'type'``

   ``TYPES = ('string', 'number', 'comma_delimited_list', 'json',
   'boolean')``

   ``classmethod from_dict(param_name, schema_dict)``

      Return a Parameter Schema object from a legacy schema
      dictionary.

      :Parameters:
         **param_name** (*str*) -- name of the parameter owning the
         schema; used for more verbose logging

**class heat.engine.hot.parameters.HOTParameters(stack_identifier,
tmpl, user_params=None, param_defaults=None)**

   Bases: `heat.engine.parameters.Parameters
   <heat.engine.parameters.rst#heat.engine.parameters.Parameters>`_

   ``PARAM_PROJECT_ID = 'OS::project_id'``

   ``PARAM_REGION = 'OS::region'``

   ``PARAM_STACK_ID = 'OS::stack_id'``

   ``PARAM_STACK_NAME = 'OS::stack_name'``

   ``PSEUDO_PARAMETERS = ('OS::stack_id', 'OS::stack_name',
   'OS::region', 'OS::project_id')``

   **set_stack_id(stack_identifier)**

      Set the StackId pseudo parameter value.
