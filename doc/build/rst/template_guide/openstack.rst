
OpenStack Resource Types
========================


OS::Cinder::Volume
------------------


Optional Properties
^^^^^^^^^^^^^^^^^^^


availability_zone
"""""""""""""""""

The availability zone in which the volume will be created.

String value expected.

Updates cause replacement.


backup_id
"""""""""

If specified, the backup to create the volume from.

String value expected.

Can be updated without replacement.

Value must be of type cinder.backup


description
"""""""""""

A description of the volume.

String value expected.

Can be updated without replacement.


image
"""""

If specified, the name or ID of the image to create the volume from.

String value expected.

Updates cause replacement.

Value must be of type glance.image


metadata
""""""""

Key/value pairs to associate with the volume.

Map value expected.

Can be updated without replacement.


name
""""

A name used to distinguish the volume.

String value expected.

Can be updated without replacement.


read_only
"""""""""

Note: Available since 5.0.0 (Liberty)

Enables or disables read-only access mode of volume.

Boolean value expected.

Can be updated without replacement.


scheduler_hints
"""""""""""""""

Note: Available since 2015.1 (Kilo)

Arbitrary key-value pairs specified by the client to help the Cinder
scheduler creating a volume.

Map value expected.

Updates cause replacement.


size
""""

The size of the volume in GB. On update only increase in size is
supported.

Integer value expected.

Can be updated without replacement.

The value must be at least 1.


snapshot_id
"""""""""""

If specified, the snapshot to create the volume from.

String value expected.

Updates cause replacement.

Value must be of type cinder.snapshot


source_volid
""""""""""""

If specified, the volume to use as source.

String value expected.

Updates cause replacement.

Value must be of type cinder.volume


volume_type
"""""""""""

If specified, the type of volume to use, mapping to a specific
backend.

String value expected.

Can be updated without replacement.

Value must be of type cinder.vtype


Attributes
^^^^^^^^^^


attachments
"""""""""""

The list of attachments of the volume.


availability_zone
"""""""""""""""""

The availability zone in which the volume is located.


bootable
""""""""

Boolean indicating if the volume can be booted or not.


created_at
""""""""""

The timestamp indicating volume creation.


display_description
"""""""""""""""""""

Description of the volume.


display_name
""""""""""""

Name of the volume.


encrypted
"""""""""

Boolean indicating if the volume is encrypted or not.


metadata
""""""""

Key/value pairs associated with the volume.


metadata_values
"""""""""""""""

Key/value pairs associated with the volume in raw dict form.


show
""""

Detailed information about resource.


size
""""

The size of the volume in GB.


snapshot_id
"""""""""""

The snapshot the volume was created from, if any.


source_volid
""""""""""""

The volume used as source, if any.


status
""""""

The current status of the volume.


volume_type
"""""""""""

The type of the volume mapping to a backend, if any.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Cinder::Volume
       properties:
         availability_zone: String
         backup_id: String
         description: String
         image: String
         metadata: {...}
         name: String
         read_only: Boolean
         scheduler_hints: {...}
         size: Integer
         snapshot_id: String
         source_volid: String
         volume_type: String


OS::Cinder::VolumeAttachment
----------------------------


Required Properties
^^^^^^^^^^^^^^^^^^^


instance_uuid
"""""""""""""

The ID of the server to which the volume attaches.

String value expected.

Can be updated without replacement.


volume_id
"""""""""

The ID of the volume to be attached.

String value expected.

Can be updated without replacement.

Value must be of type cinder.volume


Optional Properties
^^^^^^^^^^^^^^^^^^^


mountpoint
""""""""""

The location where the volume is exposed on the instance. This
assignment may not be honored and it is advised that the path
/dev/disk/by-id/virtio-<VolumeId> be used instead.

String value expected.

Can be updated without replacement.


Attributes
^^^^^^^^^^


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Cinder::VolumeAttachment
       properties:
         instance_uuid: String
         mountpoint: String
         volume_id: String


OS::Heat::CloudConfig
---------------------

Note: Available since 2014.1 (Icehouse)

A configuration resource for representing cloud-init cloud-config.

This resource allows cloud-config YAML to be defined and stored by the
config API. Any intrinsic functions called in the config will be
resolved before storing the result.

This resource will generally be referenced by OS::Nova::Server
user_data, or OS::Heat::MultipartMime parts config. Since cloud-config
is boot-only configuration, any changes to the definition will result
in the replacement of all servers which reference it.


Optional Properties
^^^^^^^^^^^^^^^^^^^


cloud_config
""""""""""""

Map representing the cloud-config data structure which will be
formatted as YAML.

Map value expected.

Updates cause replacement.


Attributes
^^^^^^^^^^


config
""""""

The config value of the software config.


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Heat::CloudConfig
       properties:
         cloud_config: {...}


OS::Heat::MultipartMime
-----------------------

Note: Available since 2014.1 (Icehouse)

Assembles a collection of software configurations as a multi-part
mime.

Parts in the message can be populated with inline configuration or
references to other config resources. If the referenced resource is
itself a valid multi-part mime message, that will be broken into parts
and those parts appended to this message.

The resulting multi-part mime message will be stored by the configs
API and can be referenced in properties such as OS::Nova::Server
user_data.

This resource is generally used to build a list of cloud-init
configuration elements including scripts and cloud-config. Since
cloud-init is boot-only configuration, any changes to the definition
will result in the replacement of all servers which reference it.


Optional Properties
^^^^^^^^^^^^^^^^^^^


parts
"""""

Parts belonging to this message.

List value expected.

Updates cause replacement.

Defaults to "[]".

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


config
++++++

Content of part to attach, either inline or by referencing the ID of
another software config resource

String value expected.

Updates cause replacement.


filename
++++++++

Optional filename to associate with part.

String value expected.

Updates cause replacement.


subtype
+++++++

Optional subtype to specify with the type.

String value expected.

Updates cause replacement.


type
++++

Whether the part content is text or multipart.

String value expected.

Updates cause replacement.

Defaults to "text".

Allowed values: text, multipart


Attributes
^^^^^^^^^^


config
""""""

The config value of the software config.


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Heat::MultipartMime
       properties:
         parts: [{"type": String, "subtype": String, "config": String, "filename": String}, {"type": String, "subtype": String, "config": String, "filename": String}, ...]


OS::Heat::None
--------------

Note: Available since 5.0.0 (Liberty)

Enables easily disabling certain resources via the resource_registry.

It does nothing, but can effectively stub out any other resource
because it will accept any properties and return any attribute (as
None). Note this resource always does nothing on update (e.g it is not
replaced even if a change to the stubbed resource properties would
cause replacement).


Attributes
^^^^^^^^^^


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Heat::None


OS::Heat::RandomString
----------------------

Note: Available since 2014.1 (Icehouse)

A resource which generates a random string.

This is useful for configuring passwords and secrets on services.


Optional Properties
^^^^^^^^^^^^^^^^^^^


character_classes
"""""""""""""""""

A list of character class and their constraints to generate the random
string from.

List value expected.

Updates cause replacement.

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


class
+++++

A character class and its corresponding min constraint to generate the
random string from.

String value expected.

Updates cause replacement.

Defaults to "lettersdigits".

Allowed values: lettersdigits, letters, lowercase, uppercase, digits,
hexdigits, octdigits


min
+++

The minimum number of characters from this character class that will
be in the generated string.

Integer value expected.

Updates cause replacement.

Defaults to "1".

The value must be in the range 1 to 512.


character_sequences
"""""""""""""""""""

A list of character sequences and their constraints to generate the
random string from.

List value expected.

Updates cause replacement.

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


min
+++

The minimum number of characters from this sequence that will be in
the generated string.

Integer value expected.

Updates cause replacement.

Defaults to "1".

The value must be in the range 1 to 512.


sequence
++++++++

A character sequence and its corresponding min constraint to generate
the random string from.

String value expected.

Updates cause replacement.


length
""""""

Length of the string to generate.

Integer value expected.

Updates cause replacement.

Defaults to "32".

The value must be in the range 1 to 512.


salt
""""

Value which can be set or changed on stack update to trigger the
resource for replacement with a new random string . The salt value
itself is ignored by the random generator.

String value expected.

Updates cause replacement.


Attributes
^^^^^^^^^^


show
""""

Detailed information about resource.


value
"""""

The random string generated by this resource. This value is also
available by referencing the resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Heat::RandomString
       properties:
         character_classes: [{"class": String, "min": Integer}, {"class": String, "min": Integer}, ...]
         character_sequences: [{"min": Integer, "sequence": String}, {"min": Integer, "sequence": String}, ...]
         length: Integer
         salt: String


OS::Heat::ResourceGroup
-----------------------

Note: Available since 2014.1 (Icehouse)

Creates one or more identically configured nested resources.

In addition to the *refs* attribute, this resource implements
synthetic attributes that mirror those of the resources in the group.
When getting an attribute from this resource, however, a list of
attribute values for each resource in the group is returned. To get
attribute values for a single resource in the group, synthetic
attributes of the form *resource.{resource index}.{attribute name}*
can be used. The resource ID of a particular resource in the group can
be obtained via the synthetic attribute *resource.{resource index}*.

While each resource in the group will be identically configured, this
resource does allow for some index-based customization of the
properties of the resources in the group. For example:

::

   resources:
     my_indexed_group:
       type: OS::Heat::ResourceGroup
       properties:
         count: 3
         resource_def:
           type: OS::Nova::Server
           properties:
             # create a unique name for each server
             # using its index in the group
             name: my_server_%index%
             image: CentOS 6.5
             flavor: 4GB Performance

would result in a group of three servers having the same image and
flavor, but names of *my_server_0*, *my_server_1*, and *my_server_2*.
The variable used for substitution can be customized by using the
*index_var* property.


Required Properties
^^^^^^^^^^^^^^^^^^^


resource_def
""""""""""""

Resource definition for the resources in the group. The value of this
property is the definition of a resource just as if it had been
declared in the template itself.

Map value expected.

Can be updated without replacement.

*Map properties:*


metadata
~~~~~~~~

Note: Available since 5.0.0 (Liberty)

Supplied metadata for the resources in the group

Map value expected.

Can be updated without replacement.


properties
~~~~~~~~~~

Property values for the resources in the group

Map value expected.

Can be updated without replacement.


type
~~~~

The type of the resources in the group

String value expected.

Can be updated without replacement.


Optional Properties
^^^^^^^^^^^^^^^^^^^


count
"""""

The number of resources to create.

Integer value expected.

Can be updated without replacement.

Defaults to "1".

The value must be at least 0.


index_var
"""""""""

Note: Available since 2014.2 (Juno)

A variable that this resource will use to replace with the current
index of a given resource in the group. Can be used, for example, to
customize the name property of grouped servers in order to
differentiate them when listed with nova client.

String value expected.

Updates cause replacement.

Defaults to "%index%".

The length must be at least 3.


removal_policies
""""""""""""""""

Note: Available since 2015.1 (Kilo)

Policies for removal of resources on update

List value expected.

Can be updated without replacement.

Defaults to "[]".

*List contents:*


*
~

Policy to be processed when doing an update which requires removal of
specific resources.

Map value expected.

Can be updated without replacement.

*Map properties:*


resource_list
+++++++++++++

List of resources to be removed when doing an update which requires
removal of specific resources. The resource may be specified several
ways: (1) The resource name, as in the nested stack, (2) The resource
reference returned from get_resource in a template, as available via
the 'refs' attribute Note this is destructive on update when
specified; even if the count is not being reduced, and once a resource
name is removed, it's name is never reused in subsequent updates

List value expected.

Can be updated without replacement.

Defaults to "[]".


Attributes
^^^^^^^^^^


attributes
""""""""""

Note: Available since 2014.2 (Juno)

A map of resource names to the specified attribute of each individual
resource.  Requires heat_template_version: 2014-10-16.


refs
""""

A list of resource IDs for the resources in the group


show
""""

Detailed information about resource.


update_policy
^^^^^^^^^^^^^


batch_create
""""""""""""

Note: Available since 5.0.0 (Liberty)

Map value expected.

Updates cause replacement.

*Map properties:*


max_batch_size
~~~~~~~~~~~~~~

The maximum number of resources to create at once.

Integer value expected.

Updates cause replacement.

Defaults to "1".

The value must be at least 1.


pause_time
~~~~~~~~~~

The number of seconds to wait between batches.

Number value expected.

Updates cause replacement.

Defaults to "0".

The value must be at least 0.


rolling_update
""""""""""""""

Note: Available since 5.0.0 (Liberty)

Map value expected.

Updates cause replacement.

*Map properties:*


max_batch_size
~~~~~~~~~~~~~~

The maximum number of resources to replace at once.

Integer value expected.

Updates cause replacement.

Defaults to "1".

The value must be at least 1.


min_in_service
~~~~~~~~~~~~~~

The minimum number of resources in service while rolling updates are
being executed.

Integer value expected.

Updates cause replacement.

Defaults to "0".

The value must be at least 0.


pause_time
~~~~~~~~~~

The number of seconds to wait between batches of updates.

Number value expected.

Updates cause replacement.

Defaults to "0".

The value must be at least 0.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Heat::ResourceGroup
       properties:
         count: Integer
         index_var: String
         removal_policies: [{"resource_list": [Value, Value, ...]}, {"resource_list": [Value, Value, ...]}, ...]
         resource_def: {"type": String, "properties": {...}, "metadata": {...}}


OS::Heat::SoftwareConfig
------------------------

Note: Available since 2014.1 (Icehouse)

A resource for describing and storing software configuration.

The software_configs API which backs this resource creates immutable
configs, so any change to the template resource definition will result
in a new config being created, and the old one being deleted.

Configs can be defined in the same template which uses them, or they
can be created in one stack, and passed to another stack via a
parameter.

A config resource can be referenced in other resource properties which
are config-aware. This includes the properties OS::Nova::Server
user_data, OS::Heat::SoftwareDeployment config and
OS::Heat::MultipartMime parts config.

Along with the config script itself, this resource can define schemas
for inputs and outputs which the config script is expected to consume
and produce. Inputs and outputs are optional and will map to concepts
which are specific to the configuration tool being used.


Optional Properties
^^^^^^^^^^^^^^^^^^^


config
""""""

Configuration script or manifest which specifies what actual
configuration is performed.

String value expected.

Updates cause replacement.


group
"""""

Namespace to group this software config by when delivered to a server.
This may imply what configuration tool is going to perform the
configuration.

String value expected.

Updates cause replacement.

Defaults to "Heat::Ungrouped".


inputs
""""""

Schema representing the inputs that this software config is expecting.

List value expected.

Updates cause replacement.

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


default
+++++++

Default value for the input if none is specified.

String value expected.

Updates cause replacement.


description
+++++++++++

Description of the input.

String value expected.

Updates cause replacement.


name
++++

Name of the input.

String value expected.

Updates cause replacement.


type
++++

Type of the value of the input.

String value expected.

Updates cause replacement.

Defaults to "String".

Allowed values: String, Number, CommaDelimitedList, Json, Boolean


options
"""""""

Map containing options specific to the configuration management tool
used by this resource.

Map value expected.

Updates cause replacement.


outputs
"""""""

Schema representing the outputs that this software config will
produce.

List value expected.

Updates cause replacement.

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


description
+++++++++++

Description of the output.

String value expected.

Updates cause replacement.


error_output
++++++++++++

Denotes that the deployment is in an error state if this output has a
value.

Boolean value expected.

Updates cause replacement.

Defaults to "False".


name
++++

Name of the output.

String value expected.

Updates cause replacement.


type
++++

Type of the value of the output.

String value expected.

Updates cause replacement.

Defaults to "String".

Allowed values: String, Number, CommaDelimitedList, Json, Boolean


Attributes
^^^^^^^^^^


config
""""""

The config value of the software config.


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Heat::SoftwareConfig
       properties:
         config: String
         group: String
         inputs: [{"default": String, "type": String, "name": String, "description": String}, {"default": String, "type": String, "name": String, "description": String}, ...]
         options: {...}
         outputs: [{"type": String, "name": String, "error_output": Boolean, "description": String}, {"type": String, "name": String, "error_output": Boolean, "description": String}, ...]


OS::Heat::SoftwareDeployment
----------------------------

Note: Available since 2014.1 (Icehouse)

This resource associates a server with some configuration.

The configuration is to be deployed to that server.

A deployment allows input values to be specified which map to the
inputs schema defined in the config resource. These input values are
interpreted by the configuration tool in a tool-specific manner.

Whenever this resource goes to an IN_PROGRESS state, it creates an
ephemeral config that includes the inputs values plus a number of
extra inputs which have names prefixed with >>deploy_<<. The extra
inputs relate to the current state of the stack, along with the
information and credentials required to signal back the deployment
results.

Unless signal_transport=NO_SIGNAL, this resource will remain in an
IN_PROGRESS state until the server signals it with the output values
for that deployment. Those output values are then available as
resource attributes, along with the default attributes deploy_stdout,
deploy_stderr and deploy_status_code.

Specifying actions other than the default CREATE and UPDATE will
result in the deployment being triggered in those actions. For example
this would allow cleanup configuration to be performed during actions
SUSPEND and DELETE. A config could be designed to only work with some
specific actions, or a config can read the value of the deploy_action
input to allow conditional logic to perform different configuration
for different actions.


Required Properties
^^^^^^^^^^^^^^^^^^^


server
""""""

ID of resource to apply configuration to. Normally this should be a
Nova server ID.

String value expected.

Updates cause replacement.


Optional Properties
^^^^^^^^^^^^^^^^^^^


actions
"""""""

Which lifecycle actions of the deployment resource will result in this
deployment being triggered.

List value expected.

Can be updated without replacement.

Defaults to "['CREATE', 'UPDATE']".

Allowed values: CREATE, UPDATE, DELETE, SUSPEND, RESUME


config
""""""

ID of software configuration resource to execute when applying to the
server.

String value expected.

Can be updated without replacement.


input_values
""""""""""""

Input values to apply to the software configuration on this server.

Map value expected.

Can be updated without replacement.


name
""""

Name of the derived config associated with this deployment. This is
used to apply a sort order to the list of configurations currently
deployed to a server.

String value expected.

Updates cause replacement.


signal_transport
""""""""""""""""

How the server should signal to heat with the deployment output
values. CFN_SIGNAL will allow an HTTP POST to a CFN keypair signed
URL. TEMP_URL_SIGNAL will create a Swift TempURL to be signaled via
HTTP PUT. HEAT_SIGNAL will allow calls to the Heat API resource-signal
using the provided keystone credentials. ZAQAR_SIGNAL will create a
dedicated zaqar queue to be signaled using the provided keystone
credentials. NO_SIGNAL will result in the resource going to the
COMPLETE state without waiting for any signal.

String value expected.

Updates cause replacement.

Defaults to "CFN_SIGNAL".

Allowed values: CFN_SIGNAL, TEMP_URL_SIGNAL, HEAT_SIGNAL, NO_SIGNAL,
ZAQAR_SIGNAL


Attributes
^^^^^^^^^^


deploy_status_code
""""""""""""""""""

Returned status code from the configuration execution


deploy_stderr
"""""""""""""

Captured stderr from the configuration execution.


deploy_stdout
"""""""""""""

Captured stdout from the configuration execution.


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Heat::SoftwareDeployment
       properties:
         actions: [Value, Value, ...]
         config: String
         input_values: {...}
         name: String
         server: String
         signal_transport: String


OS::Heat::SoftwareDeploymentGroup
---------------------------------

Note: Available since 5.0.0 (Liberty)

This resource associates a group of servers with some configuration.

The configuration is to be deployed to all servers in the group.

The properties work in a similar way to OS::Heat::SoftwareDeployment,
and in addition to the attributes documented, you may pass any
attribute supported by OS::Heat::SoftwareDeployment, including those
exposing arbitrary outputs, and return a map of deployment names to
the specified attribute.


Optional Properties
^^^^^^^^^^^^^^^^^^^


actions
"""""""

Which lifecycle actions of the deployment resource will result in this
deployment being triggered.

List value expected.

Can be updated without replacement.

Defaults to "['CREATE', 'UPDATE']".

Allowed values: CREATE, UPDATE, DELETE, SUSPEND, RESUME


config
""""""

ID of software configuration resource to execute when applying to the
server.

String value expected.

Can be updated without replacement.


input_values
""""""""""""

Input values to apply to the software configuration on this server.

Map value expected.

Can be updated without replacement.


name
""""

Name of the derived config associated with this deployment. This is
used to apply a sort order to the list of configurations currently
deployed to a server.

String value expected.

Updates cause replacement.


servers
"""""""

A map of Nova names and IDs to apply configuration to.

Map value expected.

Can be updated without replacement.


signal_transport
""""""""""""""""

How the server should signal to heat with the deployment output
values. CFN_SIGNAL will allow an HTTP POST to a CFN keypair signed
URL. TEMP_URL_SIGNAL will create a Swift TempURL to be signaled via
HTTP PUT. HEAT_SIGNAL will allow calls to the Heat API resource-signal
using the provided keystone credentials. ZAQAR_SIGNAL will create a
dedicated zaqar queue to be signaled using the provided keystone
credentials. NO_SIGNAL will result in the resource going to the
COMPLETE state without waiting for any signal.

String value expected.

Updates cause replacement.

Defaults to "CFN_SIGNAL".

Allowed values: CFN_SIGNAL, TEMP_URL_SIGNAL, HEAT_SIGNAL, NO_SIGNAL,
ZAQAR_SIGNAL


Attributes
^^^^^^^^^^


deploy_status_codes
"""""""""""""""""""

A map of Nova names and returned status code from the configuration
execution


deploy_stderrs
""""""""""""""

A map of Nova names and captured stderrs from the configuration
execution to each server.


deploy_stdouts
""""""""""""""

A map of Nova names and captured stdouts from the configuration
execution to each server.


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Heat::SoftwareDeploymentGroup
       properties:
         actions: [Value, Value, ...]
         config: String
         input_values: {...}
         name: String
         servers: {...}
         signal_transport: String


OS::Heat::SoftwareDeployments
-----------------------------

Note: DEPRECATED since 2014.2 (Juno) - The resource
  OS::Heat::SoftwareDeployments is deprecated and usage is
  discouraged. Please use resource OS::Heat::SoftwareDeploymentGroup
  instead.


Optional Properties
^^^^^^^^^^^^^^^^^^^


actions
"""""""

Which lifecycle actions of the deployment resource will result in this
deployment being triggered.

List value expected.

Can be updated without replacement.

Defaults to "['CREATE', 'UPDATE']".

Allowed values: CREATE, UPDATE, DELETE, SUSPEND, RESUME


config
""""""

ID of software configuration resource to execute when applying to the
server.

String value expected.

Can be updated without replacement.


input_values
""""""""""""

Input values to apply to the software configuration on this server.

Map value expected.

Can be updated without replacement.


name
""""

Name of the derived config associated with this deployment. This is
used to apply a sort order to the list of configurations currently
deployed to a server.

String value expected.

Updates cause replacement.


servers
"""""""

A map of Nova names and IDs to apply configuration to.

Map value expected.

Can be updated without replacement.


signal_transport
""""""""""""""""

How the server should signal to heat with the deployment output
values. CFN_SIGNAL will allow an HTTP POST to a CFN keypair signed
URL. TEMP_URL_SIGNAL will create a Swift TempURL to be signaled via
HTTP PUT. HEAT_SIGNAL will allow calls to the Heat API resource-signal
using the provided keystone credentials. ZAQAR_SIGNAL will create a
dedicated zaqar queue to be signaled using the provided keystone
credentials. NO_SIGNAL will result in the resource going to the
COMPLETE state without waiting for any signal.

String value expected.

Updates cause replacement.

Defaults to "CFN_SIGNAL".

Allowed values: CFN_SIGNAL, TEMP_URL_SIGNAL, HEAT_SIGNAL, NO_SIGNAL,
ZAQAR_SIGNAL


Attributes
^^^^^^^^^^


deploy_status_codes
"""""""""""""""""""

A map of Nova names and returned status code from the configuration
execution


deploy_stderrs
""""""""""""""

A map of Nova names and captured stderrs from the configuration
execution to each server.


deploy_stdouts
""""""""""""""

A map of Nova names and captured stdouts from the configuration
execution to each server.


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Heat::SoftwareDeployments
       properties:
         actions: [Value, Value, ...]
         config: String
         input_values: {...}
         name: String
         servers: {...}
         signal_transport: String


OS::Heat::Stack
---------------

A Resource representing a stack.

Stack can be created using specified context.


Required Properties
^^^^^^^^^^^^^^^^^^^


template
""""""""

Template that specifies the stack to be created as a resource.

String value expected.

Can be updated without replacement.


Optional Properties
^^^^^^^^^^^^^^^^^^^


context
"""""""

Context for this stack.

Map value expected.

Updates cause replacement.

*Map properties:*


region_name
~~~~~~~~~~~

Region name in which this stack will be created.

String value expected.

Updates cause replacement.


parameters
""""""""""

Set of parameters passed to this stack.

Map value expected.

Can be updated without replacement.

Defaults to "{}".


timeout
"""""""

Number of minutes to wait for this stack creation.

Integer value expected.

Can be updated without replacement.


Attributes
^^^^^^^^^^


outputs
"""""""

A dict of key-value pairs output from the stack.


show
""""

Detailed information about resource.


stack_name
""""""""""

Name of the stack.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Heat::Stack
       properties:
         context: {"region_name": String}
         parameters: {...}
         template: String
         timeout: Integer


OS::Heat::SwiftSignal
---------------------

Note: Available since 2014.2 (Juno)


Required Properties
^^^^^^^^^^^^^^^^^^^


handle
""""""

URL of TempURL where resource will signal completion and optionally
upload data.

String value expected.

Updates cause replacement.


timeout
"""""""

The maximum number of seconds to wait for the resource to signal
completion.  Once the timeout is reached, creation of the signal
resource will fail.

Number value expected.

Updates cause replacement.

The value must be in the range 1 to 43200.


Optional Properties
^^^^^^^^^^^^^^^^^^^


count
"""""

The number of success signals that must be received before the stack
creation process continues.

Integer value expected.

Updates cause replacement.

Defaults to "1".

The value must be in the range 1 to 1000.


Attributes
^^^^^^^^^^


data
""""

JSON data that was uploaded via the SwiftSignalHandle.


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Heat::SwiftSignal
       properties:
         count: Integer
         handle: String
         timeout: Number


OS::Heat::SwiftSignalHandle
---------------------------

Note: Available since 2014.2 (Juno)


Attributes
^^^^^^^^^^


curl_cli
""""""""

Convenience attribute, provides curl CLI command prefix, which can be
used for signalling handle completion or failure.  You can signal
success by adding --data-binary '{"status": "SUCCESS"}' , or signal
failure by adding --data-binary '{"status": "FAILURE"}'


endpoint
""""""""

Endpoint/url which can be used for signalling handle


show
""""

Detailed information about resource.


token
"""""

Tokens are not needed for Swift TempURLs.  This attribute is being
kept for compatibility with the OS::Heat::WaitConditionHandle resource


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Heat::SwiftSignalHandle


OS::Heat::TestResource
----------------------

Note: Available since 5.0.0 (Liberty)

A resource which stores the string value that was provided.

This resource is to be used only for testing. It has control knobs
such as 'update_replace', 'fail', 'wait_secs'.


Optional Properties
^^^^^^^^^^^^^^^^^^^


action_wait_secs
""""""""""""""""

Options for simulating waiting.

Map value expected.

Can be updated without replacement.

*Map properties:*


create
~~~~~~

Seconds to wait after a create. Defaults to the global wait_secs

Number value expected.

Can be updated without replacement.


delete
~~~~~~

Seconds to wait after a delete. Defaults to the global wait_secs

Number value expected.

Can be updated without replacement.


update
~~~~~~

Seconds to wait after an update. Defaults to the global wait_secs

Number value expected.

Can be updated without replacement.


client_name
"""""""""""

Client to poll.

String value expected.

Can be updated without replacement.

Defaults to "".


entity_name
"""""""""""

Client entity to poll.

String value expected.

Can be updated without replacement.

Defaults to "".


fail
""""

Value which can be set to fail the resource operation to test failure
scenarios.

Boolean value expected.

Can be updated without replacement.

Defaults to "False".


update_replace
""""""""""""""

Value which can be set to trigger update replace for the particular
resource

Boolean value expected.

Can be updated without replacement.

Defaults to "False".


value
"""""

The input string to be stored.

String value expected.

Can be updated without replacement.

Defaults to "test_string".


wait_secs
"""""""""

Seconds to wait after an action (-1 is infinite)

Number value expected.

Can be updated without replacement.

Defaults to "0".


Attributes
^^^^^^^^^^


output
""""""

The string that was stored. This value is also available by
referencing the resource.


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Heat::TestResource
       properties:
         action_wait_secs: {"create": Number, "update": Number, "delete": Number}
         client_name: String
         entity_name: String
         fail: Boolean
         update_replace: Boolean
         value: String
         wait_secs: Number


OS::Neutron::Net
----------------


Optional Properties
^^^^^^^^^^^^^^^^^^^


admin_state_up
""""""""""""""

A boolean value specifying the administrative status of the network.

Boolean value expected.

Can be updated without replacement.

Defaults to "True".


dhcp_agent_ids
""""""""""""""

The IDs of the DHCP agent to schedule the network. Note that the
default policy setting in Neutron restricts usage of this property to
administrative users only.

List value expected.

Can be updated without replacement.


name
""""

A string specifying a symbolic name for the network, which is not
required to be unique.

String value expected.

Can be updated without replacement.


port_security_enabled
"""""""""""""""""""""

Note: Available since 5.0.0 (Liberty)

Flag to enable/disable port security on the network. It provides the
default value for the attribute of the ports created on this network

Boolean value expected.

Can be updated without replacement.


shared
""""""

Whether this network should be shared across all tenants. Note that
the default policy setting restricts usage of this attribute to
administrative users only.

Boolean value expected.

Can be updated without replacement.

Defaults to "False".


tenant_id
"""""""""

The ID of the tenant which will own the network. Only administrative
users can set the tenant identifier; this cannot be changed using
authorization policies.

String value expected.

Updates cause replacement.


value_specs
"""""""""""

Extra parameters to include in the "network" object in the creation
request. Parameters are often specific to installed hardware or
extensions.

Map value expected.

Can be updated without replacement.

Defaults to "{}".


Attributes
^^^^^^^^^^


admin_state_up
""""""""""""""

The administrative status of the network.


mtu
"""

Note: Available since 5.0.0 (Liberty)

The maximum transmission unit size(in bytes) for the network.


name
""""

The name of the network.


port_security_enabled
"""""""""""""""""""""

Note: Available since 5.0.0 (Liberty)

Port security enabled of the network.


show
""""

Detailed information about resource.


status
""""""

The status of the network.


subnets
"""""""

Subnets of this network.


tenant_id
"""""""""

The tenant owning this network.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Neutron::Net
       properties:
         admin_state_up: Boolean
         dhcp_agent_ids: [Value, Value, ...]
         name: String
         port_security_enabled: Boolean
         shared: Boolean
         tenant_id: String
         value_specs: {...}


OS::Neutron::Port
-----------------


Optional Properties
^^^^^^^^^^^^^^^^^^^


device_id
"""""""""

Device ID of this port.

String value expected.

Can be updated without replacement.


device_owner
""""""""""""

Name of the network owning the port. The value is typically
network:floatingip or network:router_interface or network:dhcp

String value expected.

Can be updated without replacement.


fixed_ips
"""""""""

Desired IPs for this port.

List value expected.

Can be updated without replacement.

Defaults to "[]".

*List contents:*


*
~

Map value expected.

Can be updated without replacement.

*Map properties:*


ip_address
++++++++++

IP address desired in the subnet for this port.

String value expected.

Can be updated without replacement.

Value must be of type ip_addr


subnet
++++++

Note: Available since 2014.2 (Juno)

Subnet in which to allocate the IP address for this port.

String value expected.

Can be updated without replacement.

Value must be of type neutron.subnet


name
""""

A symbolic name for this port.

String value expected.

Can be updated without replacement.


network
"""""""

Note: Available since 2014.2 (Juno)

Network this port belongs to. If you plan to use current port to
assign Floating IP, you should specify fixed_ips with subnet

String value expected.

Updates cause replacement.

Value must be of type neutron.network


replacement_policy
""""""""""""""""""

Policy on how to respond to a stack-update for this resource.
REPLACE_ALWAYS will replace the port regardless of any property
changes. AUTO will update the existing port for any changed
update-allowed property.

String value expected.

Can be updated without replacement.

Defaults to "AUTO".

Allowed values: REPLACE_ALWAYS, AUTO


security_groups
"""""""""""""""

Security group IDs to associate with this port.

List value expected.

Can be updated without replacement.


Attributes
^^^^^^^^^^


admin_state_up
""""""""""""""

The administrative state of this port.


allowed_address_pairs
"""""""""""""""""""""

Additional MAC/IP address pairs allowed to pass through a port.


device_id
"""""""""

Unique identifier for the device.


device_owner
""""""""""""

Name of the network owning the port.


fixed_ips
"""""""""

Fixed IP addresses.


mac_address
"""""""""""

MAC address of the port.


name
""""

Friendly name of the port.


network_id
""""""""""

Unique identifier for the network owning the port.


port_security_enabled
"""""""""""""""""""""

Note: Available since 5.0.0 (Liberty)

Port security enabled of the port.


security_groups
"""""""""""""""

A list of security groups for the port.


show
""""

Detailed information about resource.


status
""""""

The status of the port.


subnets
"""""""

A list of all subnet attributes for the port.


tenant_id
"""""""""

Tenant owning the port.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Neutron::Port
       properties:
         device_id: String
         device_owner: String
         fixed_ips: [{"subnet_id": String, "subnet": String, "ip_address": String}, {"subnet_id": String, "subnet": String, "ip_address": String}, ...]
         name: String
         network: String
         replacement_policy: String
         security_groups: [Value, Value, ...]


OS::Neutron::SecurityGroup
--------------------------

Note: Available since 2014.1 (Icehouse)


Optional Properties
^^^^^^^^^^^^^^^^^^^


description
"""""""""""

Description of the security group.

String value expected.

Can be updated without replacement.


name
""""

A string specifying a symbolic name for the security group, which is
not required to be unique.

String value expected.

Can be updated without replacement.


rules
"""""

List of security group rules.

List value expected.

Can be updated without replacement.

Defaults to "[]".

*List contents:*


*
~

Map value expected.

Can be updated without replacement.

*Map properties:*


direction
+++++++++

The direction in which the security group rule is applied. For a
compute instance, an ingress security group rule matches traffic that
is incoming (ingress) for that instance. An egress rule is applied to
traffic leaving the instance.

String value expected.

Can be updated without replacement.

Defaults to "ingress".

Allowed values: ingress, egress


ethertype
+++++++++

Ethertype of the traffic.

String value expected.

Can be updated without replacement.

Defaults to "IPv4".

Allowed values: IPv4, IPv6


port_range_max
++++++++++++++

The maximum port number in the range that is matched by the security
group rule. The port_range_min attribute constrains the port_range_max
attribute. If the protocol is ICMP, this value must be an ICMP type.

Integer value expected.

Can be updated without replacement.

The value must be in the range 0 to 65535.


port_range_min
++++++++++++++

The minimum port number in the range that is matched by the security
group rule. If the protocol is TCP or UDP, this value must be less
than or equal to the value of the port_range_max attribute. If the
protocol is ICMP, this value must be an ICMP type.

Integer value expected.

Can be updated without replacement.

The value must be in the range 0 to 65535.


protocol
++++++++

The protocol that is matched by the security group rule. Valid values
include tcp, udp, and icmp.

String value expected.

Can be updated without replacement.


remote_group_id
+++++++++++++++

The remote group ID to be associated with this security group rule. If
no value is specified then this rule will use this security group for
the remote_group_id. The remote mode parameter must be set to
"remote_group_id".

String value expected.

Can be updated without replacement.


remote_ip_prefix
++++++++++++++++

The remote IP prefix (CIDR) to be associated with this security group
rule.

String value expected.

Can be updated without replacement.

Value must be of type net_cidr


remote_mode
+++++++++++

Whether to specify a remote group or a remote IP prefix.

String value expected.

Can be updated without replacement.

Defaults to "remote_ip_prefix".

Allowed values: remote_ip_prefix, remote_group_id


Attributes
^^^^^^^^^^


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Neutron::SecurityGroup
       properties:
         description: String
         name: String
         rules: [{"remote_group_id": String, "direction": String, "remote_ip_prefix": String, "port_range_min": Integer, "remote_mode": String, "ethertype": String, "port_range_max": Integer, "protocol": String}, {"remote_group_id": String, "direction": String, "remote_ip_prefix": String, "port_range_min": Integer, "remote_mode": String, "ethertype": String, "port_range_max": Integer, "protocol": String}, ...]


OS::Neutron::Subnet
-------------------


Required Properties
^^^^^^^^^^^^^^^^^^^


cidr
""""

The CIDR.

String value expected.

Updates cause replacement.

Value must be of type net_cidr


Optional Properties
^^^^^^^^^^^^^^^^^^^


allocation_pools
""""""""""""""""

The start and end addresses for the allocation pools.

List value expected.

Can be updated without replacement.

*List contents:*


*
~

Map value expected.

Can be updated without replacement.

*Map properties:*


end
+++

String value expected.

Can be updated without replacement.

Value must be of type ip_addr


start
+++++

String value expected.

Can be updated without replacement.

Value must be of type ip_addr


dns_nameservers
"""""""""""""""

A specified set of DNS name servers to be used.

List value expected.

Can be updated without replacement.

Defaults to "[]".


enable_dhcp
"""""""""""

Set to true if DHCP is enabled and false if DHCP is disabled.

Boolean value expected.

Can be updated without replacement.

Defaults to "True".


gateway_ip
""""""""""

The gateway IP address. Set to any of [ null | ~ | "" ] to create the
subnet without a gateway. If omitted, the first IP address within the
subnet is assigned to the gateway.

String value expected.

Can be updated without replacement.


host_routes
"""""""""""

List value expected.

Can be updated without replacement.

*List contents:*


*
~

Map value expected.

Can be updated without replacement.

*Map properties:*


destination
+++++++++++

String value expected.

Can be updated without replacement.

Value must be of type net_cidr


nexthop
+++++++

String value expected.

Can be updated without replacement.

Value must be of type ip_addr


ip_version
""""""""""

The IP version, which is 4 or 6.

Integer value expected.

Updates cause replacement.

Defaults to "4".

Allowed values: 4, 6


ipv6_address_mode
"""""""""""""""""

Note: Available since 2015.1 (Kilo)

IPv6 address mode. dhcpv6-stateful, dhcpv6-stateless, or slaac.

String value expected.

Updates cause replacement.

Allowed values: dhcpv6-stateful, dhcpv6-stateless, slaac


ipv6_ra_mode
""""""""""""

Note: Available since 2015.1 (Kilo)

IPv6 RA (Router Advertisement) mode. dhcpv6-stateful,
dhcpv6-stateless, or slaac.

String value expected.

Updates cause replacement.

Allowed values: dhcpv6-stateful, dhcpv6-stateless, slaac


name
""""

The name of the subnet.

String value expected.

Can be updated without replacement.


network
"""""""

Note: Available since 2014.2 (Juno)

The ID of the attached network.

String value expected.

Updates cause replacement.

Value must be of type neutron.network


tenant_id
"""""""""

The ID of the tenant who owns the network. Only administrative users
can specify a tenant ID other than their own.

String value expected.

Updates cause replacement.


value_specs
"""""""""""

Extra parameters to include in the creation request.

Map value expected.

Can be updated without replacement.

Defaults to "{}".


Attributes
^^^^^^^^^^


allocation_pools
""""""""""""""""

Ip allocation pools and their ranges.


cidr
""""

CIDR block notation for this subnet.


dns_nameservers
"""""""""""""""

List of dns nameservers.


enable_dhcp
"""""""""""

'true' if DHCP is enabled for this subnet; 'false' otherwise.


gateway_ip
""""""""""

Ip of the subnet's gateway.


host_routes
"""""""""""

Additional routes for this subnet.


ip_version
""""""""""

Ip version for the subnet.


name
""""

Friendly name of the subnet.


network_id
""""""""""

Parent network of the subnet.


show
""""

Detailed information about resource.


tenant_id
"""""""""

Tenant owning the subnet.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Neutron::Subnet
       properties:
         allocation_pools: [{"start": String, "end": String}, {"start": String, "end": String}, ...]
         cidr: String
         dns_nameservers: [Value, Value, ...]
         enable_dhcp: Boolean
         gateway_ip: String
         host_routes: [{"nexthop": String, "destination": String}, {"nexthop": String, "destination": String}, ...]
         ip_version: Integer
         ipv6_address_mode: String
         ipv6_ra_mode: String
         name: String
         network: String
         tenant_id: String
         value_specs: {...}


OS::Nova::KeyPair
-----------------

Note: Available since 2014.1 (Icehouse)

A resource for creating Nova key pairs.

**Note** that if a new key is generated setting *save_private_key* to
*True* results in the system saving the private key which can then be
retrieved via the *private_key* attribute of this resource.

Setting the *public_key* property means that the *private_key*
attribute of this resource will always return an empty string
regardless of the *save_private_key* setting since there will be no
private key data to save.


Required Properties
^^^^^^^^^^^^^^^^^^^


name
""""

The name of the key pair.

String value expected.

Updates cause replacement.

The length must be in the range 1 to 255.


Optional Properties
^^^^^^^^^^^^^^^^^^^


public_key
""""""""""

The optional public key. This allows users to supply the public key
from a pre-existing key pair. If not supplied, a new key pair will be
generated.

String value expected.

Updates cause replacement.


save_private_key
""""""""""""""""

True if the system should remember a generated private key; False
otherwise.

Boolean value expected.

Updates cause replacement.

Defaults to "False".


Attributes
^^^^^^^^^^


private_key
"""""""""""

The private key if it has been saved.


public_key
""""""""""

The public key.


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Nova::KeyPair
       properties:
         name: String
         public_key: String
         save_private_key: Boolean


OS::Nova::Server
----------------

Note: UNSUPPORTED - This resource is not supported, use at your own risk.

Resource for Rackspace Cloud Servers.

This resource overloads existent integrated OS::Nova::Server resource
and is used for Rackspace Cloud Servers.


Required Properties
^^^^^^^^^^^^^^^^^^^


flavor
""""""

The ID or name of the flavor to boot onto.

String value expected.

Can be updated without replacement.

Value must be of type nova.flavor


Optional Properties
^^^^^^^^^^^^^^^^^^^


admin_pass
""""""""""

The administrator password for the server.

String value expected.

Can be updated without replacement.


availability_zone
"""""""""""""""""

Name of the availability zone for server placement.

String value expected.

Updates cause replacement.


block_device_mapping
""""""""""""""""""""

Block device mappings for this server.

List value expected.

Updates cause replacement.

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


delete_on_termination
+++++++++++++++++++++

Indicate whether the volume should be deleted when the server is
terminated.

Boolean value expected.

Updates cause replacement.


device_name
+++++++++++

A device name where the volume will be attached in the system at
/dev/device_name. This value is typically vda.

String value expected.

Updates cause replacement.


snapshot_id
+++++++++++

The ID of the snapshot to create a volume from.

String value expected.

Updates cause replacement.

Value must be of type cinder.snapshot


volume_id
+++++++++

The ID of the volume to boot from. Only one of volume_id or
snapshot_id should be provided.

String value expected.

Updates cause replacement.

Value must be of type cinder.volume


volume_size
+++++++++++

The size of the volume, in GB. It is safe to leave this blank and have
the Compute service infer the size.

Integer value expected.

Updates cause replacement.


block_device_mapping_v2
"""""""""""""""""""""""

Note: Available since 2015.1 (Kilo)

Block device mappings v2 for this server.

List value expected.

Updates cause replacement.

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


boot_index
++++++++++

Integer used for ordering the boot disks.

Integer value expected.

Updates cause replacement.


delete_on_termination
+++++++++++++++++++++

Indicate whether the volume should be deleted when the server is
terminated.

Boolean value expected.

Updates cause replacement.


device_name
+++++++++++

A device name where the volume will be attached in the system at
/dev/device_name. This value is typically vda.

String value expected.

Updates cause replacement.


device_type
+++++++++++

Device type: at the moment we can make distinction only between disk
and cdrom.

String value expected.

Updates cause replacement.

Allowed values: cdrom, disk


disk_bus
++++++++

Bus of the device: hypervisor driver chooses a suitable default if
omitted.

String value expected.

Updates cause replacement.

Allowed values: ide, lame_bus, scsi, usb, virtio


image_id
++++++++

The ID of the image to create a volume from.

String value expected.

Updates cause replacement.

Value must be of type glance.image


snapshot_id
+++++++++++

The ID of the snapshot to create a volume from.

String value expected.

Updates cause replacement.

Value must be of type cinder.snapshot


swap_size
+++++++++

The size of the swap, in MB.

Integer value expected.

Updates cause replacement.


volume_id
+++++++++

The volume_id can be boot or non-boot device to the server.

String value expected.

Updates cause replacement.

Value must be of type cinder.volume


volume_size
+++++++++++

Size of the block device in GB. If it is omitted, hypervisor driver
calculates size.

Integer value expected.

Updates cause replacement.


config_drive
""""""""""""

If True, enable config drive on the server.

Boolean value expected.

Updates cause replacement.


diskConfig
""""""""""

Control how the disk is partitioned when the server is created.

String value expected.

Updates cause replacement.

Allowed values: AUTO, MANUAL


flavor_update_policy
""""""""""""""""""""

Policy on how to apply a flavor update; either by requesting a server
resize or by replacing the entire server.

String value expected.

Can be updated without replacement.

Defaults to "RESIZE".

Allowed values: RESIZE, REPLACE


image
"""""

The ID or name of the image to boot with.

String value expected.

Can be updated without replacement.

Value must be of type glance.image


image_update_policy
"""""""""""""""""""

Policy on how to apply an image-id update; either by requesting a
server rebuild or by replacing the entire server

String value expected.

Can be updated without replacement.

Defaults to "REBUILD".

Allowed values: REBUILD, REPLACE, REBUILD_PRESERVE_EPHEMERAL


key_name
""""""""

Name of keypair to inject into the server.

String value expected.

Updates cause replacement.

Value must be of type nova.keypair


metadata
""""""""

Arbitrary key/value metadata to store for this server. Both keys and
values must be 255 characters or less.  Non-string values will be
serialized to JSON (and the serialized string must be 255 characters
or less).

Map value expected.

Can be updated without replacement.


name
""""

Server name.

String value expected.

Can be updated without replacement.


networks
""""""""

An ordered list of nics to be added to this server, with information
about connected networks, fixed ips, port etc.

List value expected.

Can be updated without replacement.

*List contents:*


*
~

Map value expected.

Can be updated without replacement.

*Map properties:*


fixed_ip
++++++++

Fixed IP address to specify for the port created on the requested
network.

String value expected.

Can be updated without replacement.

Value must be of type ip_addr


network
+++++++

Name or ID of network to create a port on.

String value expected.

Can be updated without replacement.

Value must be of type neutron.network


port
++++

ID of an existing port to associate with this server.

String value expected.

Can be updated without replacement.

Value must be of type neutron.port


port_extra_properties
+++++++++++++++++++++

Note: Available since 6.0.0 (Mitaka)

Dict, which has expand properties for port. Used only if port property
is not specified for creating port.

Map value expected.

Can be updated without replacement.

*Map properties:*


admin_state_up
``````````````

The administrative state of this port.

Boolean value expected.

Can be updated without replacement.

Defaults to "True".


allowed_address_pairs
`````````````````````

Additional MAC/IP address pairs allowed to pass through the port.

List value expected.

Can be updated without replacement.

*List contents:*


*
<

Map value expected.

Can be updated without replacement.

*Map properties:*


ip_address
>>>>>>>>>>

IP address to allow through this port.

String value expected.

Can be updated without replacement.

Value must be of type net_cidr


mac_address
>>>>>>>>>>>

MAC address to allow through this port.

String value expected.

Can be updated without replacement.

Value must be of type mac_addr


binding:vnic_type
`````````````````

Note: Available since 2015.1 (Kilo)

The vnic type to be bound on the neutron port. To support SR-IOV PCI
passthrough networking, you can request that the neutron port to be
realized as normal (virtual nic), direct (pci passthrough), or macvtap
(virtual interface with a tap-like software interface). Note that this
only works for Neutron deployments that support the bindings
extension.

String value expected.

Can be updated without replacement.

Allowed values: normal, direct, macvtap


mac_address
```````````

MAC address to give to this port.

String value expected.

Can be updated without replacement.

Value must be of type mac_addr


port_security_enabled
`````````````````````

Note: Available since 5.0.0 (Liberty)

Flag to enable/disable port security on the port. When disable this
feature(set it to False), there will be no packages filtering, like
security-group and address-pairs.

Boolean value expected.

Can be updated without replacement.


value_specs
```````````

Extra parameters to include in the "port" object in the creation
request.

Map value expected.

Can be updated without replacement.

Defaults to "{}".


subnet
++++++

Note: Available since 5.0.0 (Liberty)

Subnet in which to allocate the IP address for port. Used for creating
port, based on derived properties. If subnet is specified, network
property becomes optional.

String value expected.

Can be updated without replacement.


personality
"""""""""""

A map of files to create/overwrite on the server upon boot. Keys are
file names and values are the file contents.

Map value expected.

Updates cause replacement.

Defaults to "{}".


reservation_id
""""""""""""""

A UUID for the set of servers being requested.

String value expected.

Updates cause replacement.


scheduler_hints
"""""""""""""""

Arbitrary key-value pairs specified by the client to help boot a
server.

Map value expected.

Updates cause replacement.


security_groups
"""""""""""""""

List of security group names or IDs. Cannot be used if neutron ports
are associated with this server; assign security groups to the ports
instead.

List value expected.

Updates cause replacement.

Defaults to "[]".


software_config_transport
"""""""""""""""""""""""""

How the server should receive the metadata required for software
configuration. POLL_SERVER_CFN will allow calls to the cfn API action
DescribeStackResource authenticated with the provided keypair.
POLL_SERVER_HEAT will allow calls to the Heat API resource-show using
the provided keystone credentials. POLL_TEMP_URL will create and
populate a Swift TempURL with metadata for polling. ZAQAR_MESSAGE will
create a dedicated zaqar queue and post the metadata for polling.

String value expected.

Updates cause replacement.

Defaults to "POLL_SERVER_CFN".

Allowed values: POLL_SERVER_CFN, POLL_SERVER_HEAT, POLL_TEMP_URL,
ZAQAR_MESSAGE


user_data
"""""""""

User data script to be executed by cloud-init.

String value expected.

Updates cause replacement.

Defaults to "".


user_data_format
""""""""""""""""

How the user_data should be formatted for the server. For
HEAT_CFNTOOLS, the user_data is bundled as part of the heat-cfntools
cloud-init boot configuration data. For RAW the user_data is passed to
Nova unmodified. For SOFTWARE_CONFIG user_data is bundled as part of
the software config data, and metadata is derived from any associated
SoftwareDeployment resources.

String value expected.

Updates cause replacement.

Defaults to "RAW".

Allowed values: HEAT_CFNTOOLS, RAW, SOFTWARE_CONFIG


Attributes
^^^^^^^^^^


accessIPv4
""""""""""

The manually assigned alternative public IPv4 address of the server.


accessIPv6
""""""""""

The manually assigned alternative public IPv6 address of the server.


addresses
"""""""""

A dict of all network addresses with corresponding port_id. Each
network will have two keys in dict, they are network name and network
id. The port ID may be obtained through the following expression:
"{get_attr: [<server>, addresses, <network name_or_id>, 0, port]}".


console_urls
""""""""""""

Note: Available since 2015.1 (Kilo)

URLs of server's consoles. To get a specific console type, the
requested type can be specified as parameter to the get_attr function,
e.g. get_attr: [ <server>, console_urls, novnc ]. Currently supported
types are novnc, xvpvnc, spice-html5, rdp-html5, serial.


instance_name
"""""""""""""

AWS compatible instance name.


name
""""

Name of the server.


networks
""""""""

A dict of assigned network addresses of the form: {"public": [ip1,
ip2...], "private": [ip3, ip4], "public_uuid": [ip1, ip2...],
"private_uuid": [ip3, ip4]}. Each network will have two keys in dict,
they are network name and network id.


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Nova::Server
       properties:
         admin_pass: String
         availability_zone: String
         block_device_mapping: [{"device_name": String, "volume_size": Integer, "snapshot_id": String, "delete_on_termination": Boolean, "volume_id": String}, {"device_name": String, "volume_size": Integer, "snapshot_id": String, "delete_on_termination": Boolean, "volume_id": String}, ...]
         block_device_mapping_v2: [{"boot_index": Integer, "device_type": String, "volume_size": Integer, "snapshot_id": String, "device_name": String, "disk_bus": String, "image_id": String, "swap_size": Integer, "volume_id": String, "delete_on_termination": Boolean}, {"boot_index": Integer, "device_type": String, "volume_size": Integer, "snapshot_id": String, "device_name": String, "disk_bus": String, "image_id": String, "swap_size": Integer, "volume_id": String, "delete_on_termination": Boolean}, ...]
         config_drive: Boolean
         diskConfig: String
         flavor: String
         flavor_update_policy: String
         image: String
         image_update_policy: String
         key_name: String
         metadata: {...}
         name: String
         networks: [{"subnet": String, "uuid": String, "fixed_ip": String, "port_extra_properties": {"allowed_address_pairs": [{"ip_address": String, "mac_address": String}, {"ip_address": String, "mac_address": String}, ...], "admin_state_up": Boolean, "binding:vnic_type": String, "value_specs": {...}, "mac_address": String, "port_security_enabled": Boolean}, "port": String, "network": String}, {"subnet": String, "uuid": String, "fixed_ip": String, "port_extra_properties": {"allowed_address_pairs": [{"ip_address": String, "mac_address": String}, {"ip_address": String, "mac_address": String}, ...], "admin_state_up": Boolean, "binding:vnic_type": String, "value_specs": {...}, "mac_address": String, "port_security_enabled": Boolean}, "port": String, "network": String}, ...]
         personality: {...}
         reservation_id: String
         scheduler_hints: {...}
         security_groups: [Value, Value, ...]
         software_config_transport: String
         user_data: String
         user_data_format: String


OS::Swift::Container
--------------------


Optional Properties
^^^^^^^^^^^^^^^^^^^


PurgeOnDelete
"""""""""""""

Note: Available since 2015.1 (Kilo)

If True, delete any objects in the container when the container is
deleted. Otherwise, deleting a non-empty container will result in an
error.

Boolean value expected.

Updates cause replacement.

Defaults to "False".


X-Account-Meta
""""""""""""""

A map of user-defined meta data to associate with the account. Each
key in the map will set the header X-Account-Meta-{key} with the
corresponding value.

Map value expected.

Updates cause replacement.

Defaults to "{}".


X-Container-Meta
""""""""""""""""

A map of user-defined meta data to associate with the container. Each
key in the map will set the header X-Container-Meta-{key} with the
corresponding value.

Map value expected.

Updates cause replacement.

Defaults to "{}".


X-Container-Read
""""""""""""""""

Specify the ACL permissions on who can read objects in the container.

String value expected.

Updates cause replacement.


X-Container-Write
"""""""""""""""""

Specify the ACL permissions on who can write objects to the container.

String value expected.

Updates cause replacement.


name
""""

Name for the container. If not specified, a unique name will be
generated.

String value expected.

Updates cause replacement.


Attributes
^^^^^^^^^^


BytesUsed
"""""""""

The number of bytes stored in the container.


DomainName
""""""""""

The host from the container URL.


HeadContainer
"""""""""""""

A map containing all headers for the container.


ObjectCount
"""""""""""

The number of objects stored in the container.


RootURL
"""""""

The parent URL of the container.


WebsiteURL
""""""""""

The URL of the container.


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Swift::Container
       properties:
         PurgeOnDelete: Boolean
         X-Account-Meta: {...}
         X-Container-Meta: {...}
         X-Container-Read: String
         X-Container-Write: String
         name: String


OS::Trove::Instance
-------------------

Note: Available since 2014.1 (Icehouse)

OpenStack cloud database instance resource.


Required Properties
^^^^^^^^^^^^^^^^^^^


flavor
""""""

Reference to a flavor for creating DB instance.

String value expected.

Updates cause replacement.

Value must be of type trove.flavor


size
""""

Database volume size in GB.

Integer value expected.

Updates cause replacement.

The value must be in the range 1 to 150.


Optional Properties
^^^^^^^^^^^^^^^^^^^


availability_zone
"""""""""""""""""

Name of the availability zone for DB instance.

String value expected.

Updates cause replacement.


databases
"""""""""

List of databases to be created on DB instance creation.

List value expected.

Updates cause replacement.

Defaults to "[]".

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


character_set
+++++++++++++

Set of symbols and encodings.

String value expected.

Updates cause replacement.

Defaults to "utf8".


collate
+++++++

Set of rules for comparing characters in a character set.

String value expected.

Updates cause replacement.

Defaults to "utf8_general_ci".


name
++++

Specifies database names for creating databases on instance creation.

String value expected.

Updates cause replacement.

The length must be no greater than 64.

Value must match pattern: [a-zA-Z0-9_]+[a-zA-Z0-9_@?#\s]*[a-zA-Z0-9_]+


datastore_type
""""""""""""""

Name of registered datastore type.

String value expected.

Updates cause replacement.

The length must be no greater than 255.


datastore_version
"""""""""""""""""

Name of the registered datastore version. It must exist for provided
datastore type. Defaults to using single active version. If several
active versions exist for provided datastore type, explicit value for
this parameter must be specified.

String value expected.

Updates cause replacement.

The length must be no greater than 255.


name
""""

Name of the DB instance to create.

String value expected.

Updates cause replacement.

The length must be no greater than 255.


networks
""""""""

List of network interfaces to create on instance.

List value expected.

Updates cause replacement.

Defaults to "[]".

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


fixed_ip
++++++++

Fixed IPv4 address for this NIC.

String value expected.

Updates cause replacement.

Value must be of type ip_addr


network
+++++++

Name or UUID of the network to attach this NIC to. Either port or
network must be specified.

String value expected.

Updates cause replacement.

Value must be of type neutron.network


port
++++

Name or UUID of Neutron port to attach this NIC to. Either port or
network must be specified.

String value expected.

Updates cause replacement.

Value must be of type neutron.port


replica_count
"""""""""""""

Note: Available since 5.0.0 (Liberty)

The number of replicas to be created.

Integer value expected.

Updates cause replacement.


replica_of
""""""""""

Note: Available since 5.0.0 (Liberty)

Identifier of the source instance to replicate.

String value expected.

Updates cause replacement.


restore_point
"""""""""""""

DB instance restore point.

String value expected.

Updates cause replacement.


users
"""""

List of users to be created on DB instance creation.

List value expected.

Updates cause replacement.

Defaults to "[]".

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


databases
+++++++++

Names of databases that those users can access on instance creation.

List value expected.

Updates cause replacement.

The length must be at least 1.

*List contents:*


*
`

String value expected.

Updates cause replacement.


host
++++

The host from which a user is allowed to connect to the database.

String value expected.

Updates cause replacement.

Defaults to "%".


name
++++

User name to create a user on instance creation.

String value expected.

Updates cause replacement.

The length must be no greater than 16.

Value must match pattern: [a-zA-Z0-9_]+[a-zA-Z0-9_@?#\s]*[a-zA-Z0-9_]+


password
++++++++

Password for those users on instance creation.

String value expected.

Updates cause replacement.

Value must match pattern: [a-zA-Z0-9_]+[a-zA-Z0-9_@?#\s]*[a-zA-Z0-9_]+


Attributes
^^^^^^^^^^


hostname
""""""""

Hostname of the instance.


href
""""

Api endpoint reference of the instance.


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Trove::Instance
       properties:
         availability_zone: String
         databases: [{"character_set": String, "name": String, "collate": String}, {"character_set": String, "name": String, "collate": String}, ...]
         datastore_type: String
         datastore_version: String
         flavor: String
         name: String
         networks: [{"fixed_ip": String, "network": String, "port": String}, {"fixed_ip": String, "network": String, "port": String}, ...]
         replica_count: Integer
         replica_of: String
         restore_point: String
         size: Integer
         users: [{"host": String, "password": String, "name": String, "databases": [String, String, ...]}, {"host": String, "password": String, "name": String, "databases": [String, String, ...]}, ...]


OS::Zaqar::Queue
----------------

Note: Available since 2014.2 (Juno)


Required Properties
^^^^^^^^^^^^^^^^^^^


name
""""

Name of the queue instance to create.

String value expected.

Updates cause replacement.


Optional Properties
^^^^^^^^^^^^^^^^^^^


metadata
""""""""

Arbitrary key/value metadata to store contextual information about
this queue.

Map value expected.

Can be updated without replacement.


Attributes
^^^^^^^^^^


href
""""

The resource href of the queue.


show
""""

Detailed information about resource.


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: OS::Zaqar::Queue
       properties:
         metadata: {...}
         name: String
