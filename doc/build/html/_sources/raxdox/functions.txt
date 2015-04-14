..
      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

.. _rax_hot_functions:

===================
Intrinsic Functions
===================
HOT provides a set of intrinsic functions that can be used inside HOT templates
to perform specific tasks, such as getting the value of a resource attribute at
runtime. A definition of all intrinsic functions available in HOT is given
below.


get_attr
--------
The *get_attr* function allows referencing an attribute of a resource. At
runtime, it will be resolved to the value of an attribute of a resource instance
created from the respective resource definition of the template.
The syntax of the get_attr function is as follows:

::

  get_attr:
    - <resource name>
    - <attribute name>
    - <key/index 1> (optional)
    - <key/index 2> (optional)
    - ...

resource name
    This parameter specifies the resource for which the attributes shall be
    resolved. This resource must be defined within the *resources* section of
    the template (see also :ref:`rax_hot_spec_resources`).
attribute name
    The attribute name is required as it specifies the attribute
    to be resolved. If the attribute returns a complex data structure
    such as a list or a map, then subsequent keys or indexes can be specified
    which navigate the data structure to return the desired value.

Some examples of how to use the get_attr function are shown below:

::

  resources:
    my_instance:
      type: OS::Nova::Server
      # ...

  outputs:
    instance_ip:
      description: IP address of the deployed compute instance
      value: { get_attr: [my_instance, first_address] }
    instance_private_ip:
      description: Private IP address of the deployed compute instance
      value: { get_attr: [my_instance, networks, private, 0] }

In this example, if the networks attribute contained the following data:

::

   {"public": ["2001:0db8:0000:0000:0000:ff00:0042:8329", "1.2.3.4"],
    "private": ["10.0.0.1"]}

then the value of the get_attr function would resolve to "10.0.0.1".


get_file
------------
The *get_file* function allows string content to be substituted into the
template. It is generally used as a file inclusion mechanism for files
containing non-heat scripts or configuration files.
The syntax of the get_file function is as follows:

::

  get_file: <content key>

The *content key* will be used to look up the files dictionary that is
provided in the REST API call. The *heat* client command from
python-heatclient is *get_file* aware and will populate the *files* with
the actual content of fetched paths and URLs. The *heat* client command
supports relative paths and will transform these to absolute URLs which
will be used as the *content key* in the files dictionary.

Note: The argument to *get_file* should be a static path or URL and not
rely on intrinsic functions like *get_param*. In general, the *heat* client
does not process intrinsic functions (they are only processed by the heat
server).

The example below demonstrates *get_file* usage with both relative and
absolute URLs.

::

  resources:
    my_instance:
      type: OS::Nova::Server
      properties:
        # general properties ...
        user_data:
          get_file: my_instance_user_data.sh
    my_other_instance:
      type: OS::Nova::Server
      properties:
        # general properties ...
        user_data:
          get_file: http://example.com/my_other_instance_user_data.sh

If this template was launched from a local file this would result in
a *files* dictionary containing entries with keys
*file:///path/to/my_instance_user_data.sh* and
*http://example.com/my_other_instance_user_data.sh*.

.. _rax_hot_functions_get_param:

get_param
---------
The *get_param* function allows for referencing an input parameter of a template
from anywhere within a template. At runtime, it will be resolved to the value
provided for this input parameter. The syntax of the *get_param* function is as
follows:

::

  get_param:
    - <parameter name>
    - <key/index 1> (optional)
    - <key/index 2> (optional)
    - ...

parameter name
    The parameter name is required as it specifies the parameter
    to be resolved. If the parameter returns a complex data structure
    such as a list or a map, then subsequent keys or indexes can be specified
    which navigate the data structure to return the desired value.

A sample use of this function in context of a resource definition
is shown below.

::

  parameters:
    instance_type:
      type: string
      label: Instance Type
      description: Instance type to be used.
    server_data:
      type: json

  resources:
    my_instance:
      type: OS::Nova::Server
      properties:
        flavor: { get_param: instance_type}
        metadata: { get_param: [ server_data, metadata ] }
        key_name: { get_param: [ server_data, keys, 0 ] }


In this example, if the instance_type/server_data parameters contained
the following data:

::

   {"instance_type": "m1.tiny",
   {"server_data": {"metadata": {"foo": "bar"},
                    "keys": ["a_key","other_key"]}}}

then the value of the property 'flavor' would resolve to "m1.tiny", 'metadata'
would resolve to {"foo": "bar"} and 'key_name' would resolve to "a_key".

get_resource
------------
The *get_resource* function allows for referencing another resource within the
same template. At runtime, it will be resolved to reference ID of the resource,
which is resource type specific. For example, a reference to a floating IP
resource will return the respective IP address at runtime.
The syntax of the get_resource function is as follows:

::

  get_resource: <resource ID>

The *resource ID* of the referenced resources as used in the current template is
given as single parameter to the get_resource function.


list_join
---------
The *list_join* function joins a list of strings with the given delimiter. This
function is introduced in the Juno release, usable in HOT versions later than
`2013-05-23`.  The syntax of the list_join function is as follows:

::

  list_join:
  - <delimiter>
  - <list to join>

A sample use of this function with a simple list is shown below.

::

  list_join: [', ', ['one', 'two', 'and three']]

This would resolve to "one, two, and three".


resource_facade
---------------
The *resource_facade* function allows a provider template to retrieve data
about its resource facade in the parent template. A provider template is used
to provide a custom definition of a resource - the facade - in the form of a
Heat template. The resource's properties are passed to the provider template as
its parameters, but other resource data can be included using this function.)

The syntax of the *resource_facade* function is as follows::

  resource_facade: <data type>

The *data type* can be `metadata`, `deletion_policy` or `update_policy`.


str_replace
-----------
The *str_replace* function allows for dynamically constructing strings by
providing a template string with placeholders and a list of mappings to assign
values to those placeholders at runtime. The placeholders are replaced with
mapping values wherever a mapping key exactly matches a placeholder.
The syntax of the str_replace function is as follows:

::

  str_replace:
    template: <template string>
    params: <parameter mappings>

template
    The *template* argument defines the template string that contains
    placeholders which will be substituted at runtime.
params
    The *params* argument provides parameter mappings in the form of a
    dictionary, which will be used for placeholder substitution in the template
    string at runtime. Within parameter mappings one can make use of other
    functions (e.g. get_attr to use resource attribute values) for template
    substitution.

The example below shows a simple use of the str_replace function in the outputs
section of a template to build a URL for logging into a deployed application.

::

  resources:
    my_instance:
      type: OS::Nova::Server
      # general metadata and properties ...

  outputs:
    Login_URL:
      description: The URL to log into the deployed application
      value:
        str_replace:
          template: http://host/MyApplication
          params:
            host: { get_attr: [ my_instance, first_address ] }

The str_replace function can also be used for constructing bigger chunks of text
like scripts for initializing compute instances as shown in the example below:

::

  parameters:
    DBRootPassword:
      type: string
      label: Database Password
      description: Root password for MySQL
      hidden: true

  resources:
    my_instance:
      type: OS::Nova::Server
      properties:
        # general properties ...
        user_data:
          str_replace:
            template: |
              #!/bin/bash
              echo "Hello world"
              echo "Setting MySQL root password"
              mysqladmin -u root password $db_rootpassword
              # do more things ...
            params:
              $db_rootpassword: { get_param: DBRootPassword }

In the example above, one can imagine that MySQL is being configured on a
compute instance and the root password is going to be set based on a user
provided parameter. The script for doing this is provided as userdata to the
compute instance, leveraging the str_replace function.
