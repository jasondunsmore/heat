
The `heat.api.cfn.v1.stacks <../../api/heat.api.cfn.v1.stacks.rst#module-heat.api.cfn.v1.stacks>`_ Module
=========================================================================================================

Stack endpoint for Heat CloudFormation v1 API.

**class heat.api.cfn.v1.stacks.StackController(options)**

   Bases: ``object``

   WSGI controller for stacks resource in Heat CloudFormation v1 API.

   Implements the API actions.

   ``CREATE_OR_UPDATE_ACTION = ('CreateStack', 'UpdateStack')``

   ``CREATE_STACK = 'CreateStack'``

   ``UPDATE_STACK = 'UpdateStack'``

   **cancel_update(req)**

   **create(req)**

   **create_or_update(req, action=None)**

      Implements CreateStack and UpdateStack API actions.

      Create or update stack as defined in template file.

   **default(req, **args)**

   **delete(req)**

      Implements the DeleteStack API action.

      Deletes the specified stack.

   **describe(req)**

      Implements DescribeStacks API action.

      Gets detailed information for a stack (or all stacks).

   **describe_stack_resource(req)**

      Implements the DescribeStackResource API action.

      Return the details of the given resource belonging to the given
      stack.

   **describe_stack_resources(req)**

      Implements the DescribeStackResources API action.

      Return details of resources specified by the parameters.

      *StackName*: returns all resources belonging to the stack.

      *PhysicalResourceId*: returns all resources belonging to the
      stack this resource is associated with.

      Only one of the parameters may be specified.

      Optional parameter:

      *LogicalResourceId*: filter the resources list by the logical
      resource id.

   **estimate_template_cost(req)**

      Implements the EstimateTemplateCost API action.

      Get the estimated monthly cost of a template.

   **events_list(req)**

      Implements the DescribeStackEvents API action.

      Returns events related to a specified stack (or all stacks).

   **get_template(req)**

      Implements the GetTemplate API action.

      Get the template body for an existing stack.

   **list(req)**

      Implements ListStacks API action.

      Lists summary information for all stacks.

   **list_stack_resources(req)**

      Implements the ListStackResources API action.

      Return summary of the resources belonging to the specified
      stack.

   **update(req)**

   **validate_template(req)**

      Implements the ValidateTemplate API action.

      Validates the specified template.

**heat.api.cfn.v1.stacks.create_resource(options)**

   Stacks resource factory method.
