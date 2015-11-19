
Glossary
========

API server
   HTTP REST API service for heat.

CFN
   An abbreviated form of "AWS CloudFormation".

Constraint
   Defines valid input *parameters* for a *template*.

Dependency
   When a *resource* must wait for another resource to finish creation
   before being created itself. Heat adds an implicit dependency when
   a resource references another resource or one of its *attributes*.
   An explicit dependency can also be created by the user in the
   template definition.

Environment
   Used to affect the run-time behavior of the template. Provides a
   way to override the default resource implementation and parameters
   passed to Heat. See `Environments
   <template_guide/environment.rst#environments>`_.

Heat Orchestration Template
   A particular *template* format that is native to Heat. Heat
   Orchestration Templates are expressed in YAML and are not
   backwards-compatible with CloudFormation templates.

HOT
   An acronym for "*Heat Orchestration Template*".

Input parameters
   See *Parameters*.

Metadata
   May refer to *Resource Metadata*, *Nova Instance metadata*, or the
   *Metadata service*.

Metadata service
   A Compute service that enables virtual machine instances to
   retrieve instance-specific data. See Metadata service (OpenStack
   Cloud Admin Guide).

Multi-region
   A feature of Heat that supports deployment to multiple regions.

Nested resource
   A *resource* instantiated as part of a *nested stack*.

Nested stack
   A *template* referenced by URL inside of another template. Used to
   reduce redundant resource definitions and group complex
   architectures into logical groups.

Nova Instance metadata
   User-provided *key:value* pairs associated with a Compute Instance.
   See Instance specific data (OpenStack Operations Guide).

OpenStack
   Open source software for building private and public clouds.

Orchestrate
   Arrange or direct the elements of a situation to produce a desired
   effect.

Outputs
   A top-level block in a *template* that defines what data will be
   returned by a stack after instantiation.

Parameters
   A top-level block in a *template* that defines what data can be
   passed to customise a template when it is used to create or update
   a *stack*.

Provider resource
   A *resource* implemented by a *provider template*. The parent
   resource's properties become the *nested stack's* parameters. See
   What are "Providers"? (OpenStack Wiki).

Provider template
   Allows user-definable *resource providers* to be specified via
   *nested stacks*. The nested stack's *outputs* become the parent
   stack's *attributes*.

Resource
   An element of OpenStack infrastructure instantiated from a
   particular *resource provider*. See also *Nested resource*.

Resource attribute
   Data that can be obtained from a *resource*, e.g. a server's public
   IP or name. Usually passed to another resource's *properties* or
   added to the stack's *outputs*.

Resource group
   A *resource provider* that creates one or more identically
   configured *resources* or *nested resources*.

Resource Metadata
   A *resource property* that contains CFN-style template metadata.
   See AWS::CloudFormation::Init (AWS CloudFormation User Guide)

Resource plugin
   Python code that understands how to instantiate and manage a
   *resource*. See Heat Resource Plugins (OpenStack wiki).

Resource property
   Data utilized for the instantiation of a *resource*. Can be defined
   statically in a *template* or passed in as *input parameters*.

Resource provider
   The implementation of a particular resource type. May be a
   *Resource plugin* or a *Provider template*.

Stack
   A collection of instantiated *resources* that are defined in a
   single *template*.

Stack resource
   A *resource provider* that allows the management of a *nested
   stack* as a *resource* in a parent stack.

Template
   An orchestration document that details everything needed to carry
   out an *orchestration*.

Template resource
   See *Provider resource*.

User data
   A *resource property* that contains a user-provided data blob. User
   data gets passed to cloud-init to automatically configure instances
   at boot time. See also User data (OpenStack End User Guide).

Wait condition
   A *resource provider* that provides a way to communicate data or
   events from servers back to the orchestration engine. Most commonly
   used to pause the creation of the *stack* while the server is being
   configured.
