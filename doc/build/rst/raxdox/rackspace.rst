
Rackspace Resource Types
========================


Rackspace::AutoScale::Group
---------------------------

Note: UNSUPPORTED - This resource is not supported, use at your own risk.

Represents a scaling group.


Required Properties
^^^^^^^^^^^^^^^^^^^


groupConfiguration
""""""""""""""""""

Group configuration.

Map value expected.

Can be updated without replacement.

*Map properties:*


cooldown
~~~~~~~~

Number of seconds after capacity changes during which further capacity
changes are disabled.

Number value expected.

Can be updated without replacement.


maxEntities
~~~~~~~~~~~

Maximum number of entities in this scaling group.

Integer value expected.

Can be updated without replacement.


metadata
~~~~~~~~

Arbitrary key/value metadata to associate with this group.

Map value expected.

Can be updated without replacement.


minEntities
~~~~~~~~~~~

Minimum number of entities in this scaling group.

Integer value expected.

Can be updated without replacement.


name
~~~~

Name of the scaling group.

String value expected.

Can be updated without replacement.


launchConfiguration
"""""""""""""""""""

Launch configuration.

Map value expected.

Can be updated without replacement.

*Map properties:*


args
~~~~

Type-specific server launching arguments.

Map value expected.

Can be updated without replacement.

*Map properties:*


loadBalancers
+++++++++++++

List of load balancers to hook the server up to. If not specified, no
load balancing will be configured.

List value expected.

Can be updated without replacement.

*List contents:*


*
`

Map value expected.

Can be updated without replacement.

*Map properties:*


loadBalancerId
<<<<<<<<<<<<<<

ID of the load balancer.

String value expected.

Can be updated without replacement.


port
<<<<

Server port to connect the load balancer to.

Integer value expected.

Can be updated without replacement.


server
++++++

Server creation arguments, as accepted by the Cloud Servers server
creation API.

Map value expected.

Can be updated without replacement.

*Map properties:*


config_drive
````````````

Enable config drive on the instance.

Boolean value expected.

Can be updated without replacement.


diskConfig
``````````

Configuration specifying the partition layout. AUTO to create a
partition utilizing the entire disk, and MANUAL to create a partition
matching the source image.

String value expected.

Can be updated without replacement.

Allowed values: AUTO, MANUAL


flavorRef
`````````

Flavor ID.

String value expected.

Can be updated without replacement.


imageRef
````````

Image ID.

String value expected.

Can be updated without replacement.


key_name
````````

Name of a previously created SSH keypair to allow key-based
authentication to the server.

String value expected.

Can be updated without replacement.


metadata
````````

Metadata key and value pairs.

Map value expected.

Can be updated without replacement.


name
````

Server name.

String value expected.

Can be updated without replacement.


networks
````````

Networks to attach to. If unspecified, the instance will be attached
to the public Internet and private ServiceNet networks.

List value expected.

Can be updated without replacement.

*List contents:*


*
<

Map value expected.

Can be updated without replacement.

*Map properties:*


uuid
>>>>

UUID of network to attach to.

String value expected.

Can be updated without replacement.


personality
```````````

File path and contents.

Map value expected.

Can be updated without replacement.


user_data
`````````

User data for bootstrapping the instance.

String value expected.

Can be updated without replacement.


type
~~~~

Launch configuration method. Only launch_server is currently
supported.

String value expected.

Can be updated without replacement.

Allowed values: launch_server


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
       type: Rackspace::AutoScale::Group
       properties:
         groupConfiguration: {"maxEntities": Integer, "cooldown": Number, "name": String, "minEntities": Integer, "metadata": {...}}
         launchConfiguration: {"args": {"loadBalancers": [{"port": Integer, "loadBalancerId": String}, {"port": Integer, "loadBalancerId": String}, ...], "server": {"networks": [{"uuid": String}, {"uuid": String}, ...], "diskConfig": String, "name": String, "imageRef": String, "key_name": String, "flavorRef": String, "personality": {...}, "config_drive": Boolean, "user_data": String, "metadata": {...}}}, "type": String}


Rackspace::AutoScale::ScalingPolicy
-----------------------------------

Note: UNSUPPORTED - This resource is not supported, use at your own risk.

Represents a Rackspace Auto Scale scaling policy.


Required Properties
^^^^^^^^^^^^^^^^^^^


group
"""""

Scaling group ID that this policy belongs to.

String value expected.

Updates cause replacement.


name
""""

Name of this scaling policy.

String value expected.

Can be updated without replacement.


type
""""

Type of this scaling policy. Specifies how the policy is executed.

String value expected.

Can be updated without replacement.

Allowed values: webhook, schedule, cloud_monitoring


Optional Properties
^^^^^^^^^^^^^^^^^^^


args
""""

Type-specific arguments for the policy.

Map value expected.

Can be updated without replacement.


change
""""""

Amount to add to or remove from current number of instances.
Incompatible with changePercent and desiredCapacity.

Integer value expected.

Can be updated without replacement.


changePercent
"""""""""""""

Percentage-based change to add or remove from current number of
instances. Incompatible with change and desiredCapacity.

Number value expected.

Can be updated without replacement.


cooldown
""""""""

Number of seconds after a policy execution during which further
executions are disabled.

Number value expected.

Can be updated without replacement.


desiredCapacity
"""""""""""""""

Absolute number to set the number of instances to. Incompatible with
change and changePercent.

Integer value expected.

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
       type: Rackspace::AutoScale::ScalingPolicy
       properties:
         args: {...}
         change: Integer
         changePercent: Number
         cooldown: Number
         desiredCapacity: Integer
         group: String
         name: String
         type: String


Rackspace::AutoScale::WebHook
-----------------------------

Note: UNSUPPORTED - This resource is not supported, use at your own risk.

Represents a Rackspace AutoScale webhook.

Exposes the URLs of the webhook as attributes.


Required Properties
^^^^^^^^^^^^^^^^^^^


name
""""

The name of this webhook.

String value expected.

Can be updated without replacement.


policy
""""""

The policy that this webhook should apply to, in
{group_id}:{policy_id} format. Generally a Ref to a Policy resource.

String value expected.

Updates cause replacement.


Optional Properties
^^^^^^^^^^^^^^^^^^^


metadata
""""""""

Arbitrary key/value metadata for this webhook.

Map value expected.

Can be updated without replacement.


Attributes
^^^^^^^^^^


capabilityUrl
"""""""""""""

The url for executing the webhook (doesn't require auth).


executeUrl
""""""""""

The url for executing the webhook (requires auth).


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
       type: Rackspace::AutoScale::WebHook
       properties:
         metadata: {...}
         name: String
         policy: String


Rackspace::Cloud::DNS
---------------------

Note: UNSUPPORTED - This resource is not supported, use at your own risk.

Represents a DNS resource.


Required Properties
^^^^^^^^^^^^^^^^^^^


emailAddress
""""""""""""

Email address to use for contacting the domain administrator.

String value expected.

Can be updated without replacement.


name
""""

Specifies the name for the domain or subdomain. Must be a valid domain
name.

String value expected.

Updates cause replacement.

The length must be at least 3.


Optional Properties
^^^^^^^^^^^^^^^^^^^


comment
"""""""

Optional free form text comment

String value expected.

Can be updated without replacement.

The length must be no greater than 160.


records
"""""""

Domain records

List value expected.

Can be updated without replacement.

*List contents:*


*
~

Map value expected.

Can be updated without replacement.

*Map properties:*


comment
+++++++

Optional free form text comment

String value expected.

Can be updated without replacement.

The length must be no greater than 160.


data
++++

Type specific record data

String value expected.

Can be updated without replacement.


name
++++

Specifies the name for the domain or subdomain. Must be a valid domain
name.

String value expected.

Can be updated without replacement.

The length must be at least 3.


priority
++++++++

Required for MX and SRV records, but forbidden for other record types.
If specified, must be an integer from 0 to 65535.

Integer value expected.

Can be updated without replacement.

The value must be in the range 0 to 65535.


ttl
+++

How long other servers should cache recorddata.

Integer value expected.

Can be updated without replacement.

Defaults to "3600".

The value must be at least 300.


type
++++

Specifies the record type.

String value expected.

Can be updated without replacement.

Allowed values: A, AAAA, NS, MX, CNAME, TXT, SRV


ttl
"""

How long other servers should cache recorddata.

Integer value expected.

Can be updated without replacement.

Defaults to "3600".

The value must be at least 300.


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
       type: Rackspace::Cloud::DNS
       properties:
         comment: String
         emailAddress: String
         name: String
         records: [{"comment": String, "name": String, "data": String, "priority": Integer, "ttl": Integer, "type": String}, {"comment": String, "name": String, "data": String, "priority": Integer, "ttl": Integer, "type": String}, ...]
         ttl: Integer


Rackspace::Cloud::LoadBalancer
------------------------------

Note: UNSUPPORTED - This resource is not supported, use at your own risk.

Represents a Rackspace Cloud Loadbalancer.


Required Properties
^^^^^^^^^^^^^^^^^^^


nodes
"""""

List value expected.

Can be updated without replacement.

*List contents:*


*
~

Map value expected.

Can be updated without replacement.

*Map properties:*


addresses
+++++++++

IP addresses for the load balancer node. Must have at least one
address.

List value expected.

Can be updated without replacement.

*List contents:*


*
`

String value expected.

Can be updated without replacement.


condition
+++++++++

String value expected.

Can be updated without replacement.

Defaults to "ENABLED".

Allowed values: ENABLED, DISABLED, DRAINING


port
++++

Integer value expected.

Can be updated without replacement.


type
++++

String value expected.

Can be updated without replacement.

Allowed values: PRIMARY, SECONDARY


weight
++++++

Number value expected.

Can be updated without replacement.

The value must be in the range 1 to 100.


port
""""

Integer value expected.

Can be updated without replacement.


protocol
""""""""

String value expected.

Can be updated without replacement.

Allowed values: DNS_TCP, DNS_UDP, FTP, HTTP, HTTPS, IMAPS, IMAPv4,
LDAP, LDAPS, MYSQL, POP3, POP3S, SMTP, TCP, TCP_CLIENT_FIRST, UDP,
UDP_STREAM, SFTP


virtualIps
""""""""""

List value expected.

Updates cause replacement.

The length must be at least 1.

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


id
++

ID of a shared VIP to use instead of creating a new one. This property
cannot be specified if type or version is specified.

Number value expected.

Updates cause replacement.


ipVersion
+++++++++

IP version of the VIP. This property cannot be specified if 'id' is
specified. This property must be specified if id is not specified.

String value expected.

Updates cause replacement.

Allowed values: IPV6, IPV4


type
++++

The type of VIP (public or internal). This property cannot be
specified if 'id' is specified. This property must be specified if id
is not specified.

String value expected.

Updates cause replacement.

Allowed values: SERVICENET, PUBLIC


Optional Properties
^^^^^^^^^^^^^^^^^^^


accessList
""""""""""

List value expected.

Updates cause replacement.

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


address
+++++++

String value expected.

Updates cause replacement.


type
++++

String value expected.

Updates cause replacement.

Allowed values: ALLOW, DENY


algorithm
"""""""""

String value expected.

Can be updated without replacement.

Allowed values: LEAST_CONNECTIONS, RANDOM, ROUND_ROBIN,
WEIGHTED_LEAST_CONNECTIONS, WEIGHTED_ROUND_ROBIN


connectionLogging
"""""""""""""""""

Boolean value expected.

Can be updated without replacement.


connectionThrottle
""""""""""""""""""

Map value expected.

Can be updated without replacement.

*Map properties:*


maxConnectionRate
~~~~~~~~~~~~~~~~~

Number value expected.

Can be updated without replacement.

The value must be in the range 0 to 100000.


maxConnections
~~~~~~~~~~~~~~

Integer value expected.

Can be updated without replacement.

The value must be in the range 1 to 100000.


minConnections
~~~~~~~~~~~~~~

Integer value expected.

Can be updated without replacement.

The value must be in the range 1 to 1000.


rateInterval
~~~~~~~~~~~~

Number value expected.

Can be updated without replacement.

The value must be in the range 1 to 3600.


contentCaching
""""""""""""""

String value expected.

Can be updated without replacement.

Allowed values: ENABLED, DISABLED


errorPage
"""""""""

String value expected.

Can be updated without replacement.


halfClosed
""""""""""

Boolean value expected.

Can be updated without replacement.


healthMonitor
"""""""""""""

Map value expected.

Can be updated without replacement.

*Map properties:*


attemptsBeforeDeactivation
~~~~~~~~~~~~~~~~~~~~~~~~~~

Number value expected.

Can be updated without replacement.

The value must be in the range 1 to 10.


bodyRegex
~~~~~~~~~

String value expected.

Can be updated without replacement.


delay
~~~~~

Number value expected.

Can be updated without replacement.

The value must be in the range 1 to 3600.


hostHeader
~~~~~~~~~~

String value expected.

Can be updated without replacement.


path
~~~~

String value expected.

Can be updated without replacement.


statusRegex
~~~~~~~~~~~

String value expected.

Can be updated without replacement.


timeout
~~~~~~~

Number value expected.

Can be updated without replacement.

The value must be in the range 1 to 300.


type
~~~~

String value expected.

Can be updated without replacement.

Allowed values: CONNECT, HTTP, HTTPS


httpsRedirect
"""""""""""""

Note: Available since 2015.1 (Kilo)

Enables or disables HTTP to HTTPS redirection for the load balancer.
When enabled, any HTTP request returns status code 301 (Moved
Permanently), and the requester is redirected to the requested URL via
the HTTPS protocol on port 443. Only available for HTTPS protocol
(port=443), or HTTP protocol with a properly configured SSL
termination (secureTrafficOnly=true, securePort=443).

Boolean value expected.

Can be updated without replacement.

Defaults to "False".


metadata
""""""""

Map value expected.

Can be updated without replacement.


name
""""

String value expected.

Can be updated without replacement.


sessionPersistence
""""""""""""""""""

String value expected.

Can be updated without replacement.

Allowed values: HTTP_COOKIE, SOURCE_IP


sslTermination
""""""""""""""

Map value expected.

Can be updated without replacement.

*Map properties:*


certificate
~~~~~~~~~~~

String value expected.

Can be updated without replacement.


intermediateCertificate
~~~~~~~~~~~~~~~~~~~~~~~

String value expected.

Can be updated without replacement.


privatekey
~~~~~~~~~~

String value expected.

Can be updated without replacement.


securePort
~~~~~~~~~~

Integer value expected.

Can be updated without replacement.

Defaults to "443".


secureTrafficOnly
~~~~~~~~~~~~~~~~~

Boolean value expected.

Can be updated without replacement.

Defaults to "False".


timeout
"""""""

Number value expected.

Can be updated without replacement.

The value must be in the range 1 to 120.


Attributes
^^^^^^^^^^


PublicIp
""""""""

Public IP address of the specified instance.


show
""""

Detailed information about resource.


virtualIps
""""""""""

A list of assigned virtual ip addresses


HOT Syntax
^^^^^^^^^^

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::Cloud::LoadBalancer
       properties:
         accessList: [{"type": String, "address": String}, {"type": String, "address": String}, ...]
         algorithm: String
         connectionLogging: Boolean
         connectionThrottle: {"maxConnectionRate": Number, "maxConnections": Integer, "rateInterval": Number, "minConnections": Integer}
         contentCaching: String
         errorPage: String
         halfClosed: Boolean
         healthMonitor: {"attemptsBeforeDeactivation": Number, "delay": Number, "hostHeader": String, "statusRegex": String, "timeout": Number, "bodyRegex": String, "path": String, "type": String}
         httpsRedirect: Boolean
         metadata: {...}
         name: String
         nodes: [{"weight": Number, "type": String, "addresses": [String, String, ...], "condition": String, "port": Integer}, {"weight": Number, "type": String, "addresses": [String, String, ...], "condition": String, "port": Integer}, ...]
         port: Integer
         protocol: String
         sessionPersistence: String
         sslTermination: {"privatekey": String, "securePort": Integer, "secureTrafficOnly": Boolean, "certificate": String, "intermediateCertificate": String}
         timeout: Number
         virtualIps: [{"ipVersion": String, "type": String, "id": Number}, {"ipVersion": String, "type": String, "id": Number}, ...]
