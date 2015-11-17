
Rackspace Resource Types
************************


Rackspace::AutoScale::Group
===========================

Note: UNSUPPORTED - This resource is not supported, use at your own risk.

Represents a scaling group.


Required Properties
-------------------


groupConfiguration
~~~~~~~~~~~~~~~~~~

Group configuration.

Map value expected.

Can be updated without replacement.

*Map properties:*

..


   cooldown
   """"""""

   Number of seconds after capacity changes during which further
   capacity changes are disabled.

   Number value expected.

   Can be updated without replacement.

..


   maxEntities
   """""""""""

   Maximum number of entities in this scaling group.

   Integer value expected.

   Can be updated without replacement.

..


   metadata
   """"""""

   Arbitrary key/value metadata to associate with this group.

   Map value expected.

   Can be updated without replacement.

..


   minEntities
   """""""""""

   Minimum number of entities in this scaling group.

   Integer value expected.

   Can be updated without replacement.

..


   name
   """"

   Name of the scaling group.

   String value expected.

   Can be updated without replacement.


launchConfiguration
~~~~~~~~~~~~~~~~~~~

Launch configuration.

Map value expected.

Can be updated without replacement.

*Map properties:*

..


   args
   """"

   Type-specific server launching arguments.

   Map value expected.

   Can be updated without replacement.

   *Map properties:*

   ..


      loadBalancers
      +++++++++++++

      List of load balancers to hook the server up to. If not
      specified, no load balancing will be configured.

      List value expected.

      Can be updated without replacement.

      *List contents:*

      ..


         *
         `

         Map value expected.

         Can be updated without replacement.

         *Map properties:*

         ..


            loadBalancerId
            **************

            ID of the load balancer.

            String value expected.

            Can be updated without replacement.

         ..


            port
            ****

            Server port to connect the load balancer to.

            Integer value expected.

            Can be updated without replacement.

   ..


      server
      ++++++

      Server creation arguments, as accepted by the Cloud Servers
      server creation API.

      Map value expected.

      Can be updated without replacement.

      *Map properties:*

      ..


         config_drive
         ````````````

         Enable config drive on the instance.

         Boolean value expected.

         Can be updated without replacement.

      ..


         diskConfig
         ``````````

         Configuration specifying the partition layout. AUTO to create
         a partition utilizing the entire disk, and MANUAL to create a
         partition matching the source image.

         String value expected.

         Can be updated without replacement.

         Allowed values: AUTO, MANUAL

      ..


         flavorRef
         `````````

         Flavor ID.

         String value expected.

         Can be updated without replacement.

      ..


         imageRef
         ````````

         Image ID.

         String value expected.

         Can be updated without replacement.

      ..


         key_name
         ````````

         Name of a previously created SSH keypair to allow key-based
         authentication to the server.

         String value expected.

         Can be updated without replacement.

      ..


         metadata
         ````````

         Metadata key and value pairs.

         Map value expected.

         Can be updated without replacement.

      ..


         name
         ````

         Server name.

         String value expected.

         Can be updated without replacement.

      ..


         networks
         ````````

         Networks to attach to. If unspecified, the instance will be
         attached to the public Internet and private ServiceNet
         networks.

         List value expected.

         Can be updated without replacement.

         *List contents:*

         ..


            *
            *

            Map value expected.

            Can be updated without replacement.

            *Map properties:*

            ..


               uuid
               ====

               UUID of network to attach to.

               String value expected.

               Can be updated without replacement.

      ..


         personality
         ```````````

         File path and contents.

         Map value expected.

         Can be updated without replacement.

      ..


         user_data
         `````````

         User data for bootstrapping the instance.

         String value expected.

         Can be updated without replacement.

..


   type
   """"

   Launch configuration method. Only launch_server is currently
   supported.

   String value expected.

   Can be updated without replacement.

   Allowed values: launch_server


Attributes
----------


show
~~~~

Detailed information about resource.


HOT Syntax
----------

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
===================================

Note: UNSUPPORTED - This resource is not supported, use at your own risk.

Represents a Rackspace Auto Scale scaling policy.


Required Properties
-------------------


group
~~~~~

Scaling group ID that this policy belongs to.

String value expected.

Updates cause replacement.


name
~~~~

Name of this scaling policy.

String value expected.

Can be updated without replacement.


type
~~~~

Type of this scaling policy. Specifies how the policy is executed.

String value expected.

Can be updated without replacement.

Allowed values: webhook, schedule, cloud_monitoring


Optional Properties
-------------------


args
~~~~

Type-specific arguments for the policy.

Map value expected.

Can be updated without replacement.


change
~~~~~~

Amount to add to or remove from current number of instances.
Incompatible with changePercent and desiredCapacity.

Integer value expected.

Can be updated without replacement.


changePercent
~~~~~~~~~~~~~

Percentage-based change to add or remove from current number of
instances. Incompatible with change and desiredCapacity.

Number value expected.

Can be updated without replacement.


cooldown
~~~~~~~~

Number of seconds after a policy execution during which further
executions are disabled.

Number value expected.

Can be updated without replacement.


desiredCapacity
~~~~~~~~~~~~~~~

Absolute number to set the number of instances to. Incompatible with
change and changePercent.

Integer value expected.

Can be updated without replacement.


Attributes
----------


show
~~~~

Detailed information about resource.


HOT Syntax
----------

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
=============================

Note: UNSUPPORTED - This resource is not supported, use at your own risk.

Represents a Rackspace AutoScale webhook.

Exposes the URLs of the webhook as attributes.


Required Properties
-------------------


name
~~~~

The name of this webhook.

String value expected.

Can be updated without replacement.


policy
~~~~~~

The policy that this webhook should apply to, in
{group_id}:{policy_id} format. Generally a Ref to a Policy resource.

String value expected.

Updates cause replacement.


Optional Properties
-------------------


metadata
~~~~~~~~

Arbitrary key/value metadata for this webhook.

Map value expected.

Can be updated without replacement.


Attributes
----------


capabilityUrl
~~~~~~~~~~~~~

The url for executing the webhook (doesn't require auth).


executeUrl
~~~~~~~~~~

The url for executing the webhook (requires auth).


show
~~~~

Detailed information about resource.


HOT Syntax
----------

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


Rackspace::Cloud::AssociateSharedIP
===================================

Note: Available since 2015.1 (Kilo)

Resource to associate shared IP with servers.


Required Properties
-------------------


servers
~~~~~~~

List of servers to associate a shared IP.

List value expected.

Updates cause replacement.

*List contents:*

..


   *
   "

   Servers ID.

   String value expected.

   Updates cause replacement.


Optional Properties
-------------------


shared_ip
~~~~~~~~~

ID of the shared IP.

String value expected.

Updates cause replacement.


Attributes
----------


associations
~~~~~~~~~~~~

IP associations.


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::Cloud::AssociateSharedIP
       properties:
         servers: [String, String, ...]
         shared_ip: String


Rackspace::Cloud::BackupConfig
==============================

Note: Available since 2015.1 (Kilo)

Rackspace cloud backup configuration resource.


Required Properties
-------------------


BackupConfigurationName
~~~~~~~~~~~~~~~~~~~~~~~

Cloud backup configuration name.

String value expected.

Updates cause replacement.


DayOfWeekId
~~~~~~~~~~~

Indicates the day of the week. Valid values are 0 through 6, with 0
representing Sunday and 6 representing Saturday. null is also a valid
value when the Frequency value is "Manually" ,"Hourly", or "Daily".

String value expected.

Can be updated without replacement.


HourInterval
~~~~~~~~~~~~

Indicates the hour. Valid values are 1 through 23, as well as null
when the Frequency value is "Manually" ,"Daily", or "Weekly".

String value expected.

Can be updated without replacement.


Inclusions
~~~~~~~~~~

Indicates the list of files and folders to back up.

List value expected.

Can be updated without replacement.

*List contents:*

..


   *
   "

   Map value expected.

   Can be updated without replacement.

   *Map properties:*

   ..


      FileItemType
      ++++++++++++

      File item type.

      String value expected.

      Can be updated without replacement.

      Allowed values: Folder, File

   ..


      FilePath
      ++++++++

      File  or folder path.

      String value expected.

      Can be updated without replacement.


NotifyFailure
~~~~~~~~~~~~~

Indicates if emails are sent after a failed backup. Valid values are
true or false.

Boolean value expected.

Can be updated without replacement.


NotifyRecipients
~~~~~~~~~~~~~~~~

Indicates the email address to notify in case of backup success or
failure.

String value expected.

Can be updated without replacement.


StartTimeAmPm
~~~~~~~~~~~~~

Indicates AM or PM. Valid values are "AM" or "PM", as well as null
when the Frequency value is "Manually" or "Hourly".

String value expected.

Can be updated without replacement.

Allowed values: AM, PM,


StartTimeHour
~~~~~~~~~~~~~

Indicates the hour when the backup runs. Valid values are 1 through
12, as well as null when the Frequency value is "Manually" or
"Hourly".

String value expected.

Can be updated without replacement.


StartTimeMinute
~~~~~~~~~~~~~~~

Indicates the minute when the backup runs. Valid values are 0 through
59, as well as null when the Frequency value is "Manually" or
"Hourly".

String value expected.

Can be updated without replacement.


TimeZoneId
~~~~~~~~~~

Specifies the time zone where the backup runs, for example "Eastern
Standard Time".

String value expected.

Can be updated without replacement.

Defaults to "Eastern Standard Time".


host_ip_address
~~~~~~~~~~~~~~~

Cloud server ip address.

String value expected.

Updates cause replacement.


Optional Properties
-------------------


Enabled
~~~~~~~

Indicates backup configuration is enabled or not.

Boolean value expected.

Can be updated without replacement.

Defaults to "True".


Exclusions
~~~~~~~~~~

Indicates the list of files and folders not to back up.

List value expected.

Can be updated without replacement.

*List contents:*

..


   *
   "

   Map value expected.

   Can be updated without replacement.

   *Map properties:*

   ..


      FileItemType
      ++++++++++++

      File item type.

      String value expected.

      Can be updated without replacement.

      Allowed values: Folder, File

   ..


      FilePath
      ++++++++

      File or folder path.

      String value expected.

      Can be updated without replacement.


Frequency
~~~~~~~~~

Frequency of backup schedule. Valid values are Manually, Hourly,
Daily, and Weekly.

String value expected.

Can be updated without replacement.

Defaults to "Daily".

Allowed values: Manually, Hourly, Daily, Weekly


IsActive
~~~~~~~~

Indicates backup configuration is active.

Boolean value expected.

Can be updated without replacement.

Defaults to "True".


NotifySuccess
~~~~~~~~~~~~~

Indicates if emails are sent after a successful backup. Valid values
are true or false.

Boolean value expected.

Can be updated without replacement.

Defaults to "False".


VersionRetention
~~~~~~~~~~~~~~~~

Indicates how many days backup revisions are maintained. Valid values
are 0, 30 , and 60. 0 means indefinite.

Integer value expected.

Can be updated without replacement.

Defaults to "60".

Allowed values: 0, 30, 60


Attributes
----------


backup_agent_id
~~~~~~~~~~~~~~~

Backup agent ID.


backup_config_details
~~~~~~~~~~~~~~~~~~~~~

Backup config details.


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::Cloud::BackupConfig
       properties:
         BackupConfigurationName: String
         DayOfWeekId: String
         Enabled: Boolean
         Exclusions: [{"FileItemType": String, "FilePath": String}, {"FileItemType": String, "FilePath": String}, ...]
         Frequency: String
         HourInterval: String
         Inclusions: [{"FileItemType": String, "FilePath": String}, {"FileItemType": String, "FilePath": String}, ...]
         IsActive: Boolean
         NotifyFailure: Boolean
         NotifyRecipients: String
         NotifySuccess: Boolean
         StartTimeAmPm: String
         StartTimeHour: String
         StartTimeMinute: String
         TimeZoneId: String
         VersionRetention: Integer
         host_ip_address: String


Rackspace::Cloud::BigData
=========================

Note: Available since 2015.8

Represents a Cloud Big Data resource.


Required Properties
-------------------


clusterLogin
~~~~~~~~~~~~

Cluster SSH login.

String value expected.

Updates cause replacement.

Cluster SSH login is to long. The length must be no greater than 50.


clusterName
~~~~~~~~~~~

Rackspace Cloud Big Data Cluster Name.

String value expected.

Updates cause replacement.

Cluster name is to long. The length must be no greater than 50.


flavor
~~~~~~

Rackspace Cloud Big Data Flavor ID to be used for cluster slavenodes.

String value expected.

Updates cause replacement.

Value must be of type cbd.flavor


publicKey
~~~~~~~~~

Cluster public key used to SSH into cluster nodes.

String value expected.

Updates cause replacement.

Public key is to long. The length must be no greater than 1000.


publicKeyName
~~~~~~~~~~~~~

Cluster public key name. This key name will be used along with the
publicKey by the Cloud Big Data system to install SSH keys on to CBD
clusters for user access. If the key name already exists, it will not
be overwritten and the existing key will be used instead.

String value expected.

Updates cause replacement.

Public key name is to long. The length must be no greater than 50.


stackId
~~~~~~~

Rackspace Cloud Big Data Stack ID.

String value expected.

Updates cause replacement.

Value must be of type cbd.stack


Optional Properties
-------------------


numSlaveNodes
~~~~~~~~~~~~~

How many slave nodes to create in the cluster.

Integer value expected.

Updates cause replacement.

Defaults to "3".

Number of slave nodes must be 1-10. The value must be in the range 1
to 10.


Attributes
----------


cbdVersion
~~~~~~~~~~

Rackspace Cloud Big Data version


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::Cloud::BigData
       properties:
         clusterLogin: String
         clusterName: String
         flavor: String
         numSlaveNodes: Integer
         publicKey: String
         publicKeyName: String
         stackId: String


Rackspace::Cloud::ChefSolo
==========================


Required Properties
-------------------


host
~~~~

The host to run chef-solo on.

String value expected.

Updates cause replacement.


private_key
~~~~~~~~~~~

The ssh key to connect to the host with.

String value expected.

Updates cause replacement.


username
~~~~~~~~

The username to connect to the host with.

String value expected.

Updates cause replacement.

Defaults to "root".


Optional Properties
-------------------


Berksfile.lock
~~~~~~~~~~~~~~

The Berksfile.lock to use with berkshelf to specify cookbook versions
for the chef run.

String value expected.

Updates cause replacement.


chef_version
~~~~~~~~~~~~

The version of chef to install on the host.

String value expected.

Updates cause replacement.


clients
~~~~~~~

Clients to be written to the kitchen for the chef run.

Map value expected.

Updates cause replacement.


data_bags
~~~~~~~~~

Data_bags to write to the kitchen during the chef run.

Map value expected.

Updates cause replacement.


environments
~~~~~~~~~~~~

Environments to be written to the kitchen for the chef run.

Map value expected.

Updates cause replacement.


kitchen
~~~~~~~

A git url to the kitchen to clone. This can be used in place of a
Berks or Chef file to install cookbooks on the host.

String value expected.

Updates cause replacement.


node
~~~~

The node file for the chef run. May have a run_list, attributes, etc.

Map value expected.

Updates cause replacement.


roles
~~~~~

Roles to be written to the kitchen for the chef run.

Map value expected.

Updates cause replacement.


users
~~~~~

Users to be written to the kitchen for the chef run.

Map value expected.

Updates cause replacement.


Berksfile
~~~~~~~~~

Note: DEPRECATED - Use property kitchen.

The Berksfile to use with berkshelf to download cookbooks on the host
for the chef run.

String value expected.

Updates cause replacement.


Cheffile
~~~~~~~~

Note: DEPRECATED - Use property kitchen.

The Cheffile to use with librarian-chef to download cookbooks on the
host for the chef run.

String value expected.

Updates cause replacement.


Attributes
----------


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::Cloud::ChefSolo
       properties:
         Berksfile.lock: String
         chef_version: String
         clients: {...}
         data_bags: {...}
         environments: {...}
         host: String
         kitchen: String
         node: {...}
         private_key: String
         roles: {...}
         username: String
         users: {...}


Rackspace::Cloud::CloudFilesCDN
===============================

This resource enables the Rackspace CDN extensions for Swift
(Rackspace Cloud Files) on a given container (OS::Swift::Container).

A CDN-enabled container is a public container that is served by the
Akamai content delivery network. The files in a CDN-enabled container
are publicly accessible and do not require an authentication token for
read access. However, uploading content into a CDN-enabled container
is a secure operation and does require a valid authentication token.
(Private containers are not CDN-enabled and the files in a private
container are not publicly accessible.)

The resource ref for this resource will be the CDN access URI for the
specified container. Other URI's (streaming, etc) are accessed via the
resource attributes.


Required Properties
-------------------


container
~~~~~~~~~

Target container to enable CDN for.

String value expected.

Updates cause replacement.


Optional Properties
-------------------


ttl
~~~

Specifies the Time To Live (TTL) in seconds for an object to be cached
in the CDN.

Integer value expected.

Updates cause replacement.

Defaults to "259200".

The value must be in the range 900 to 31536000.


Attributes
----------


cdn_uri
~~~~~~~

The URI for downloading the object over HTTP. This URI can be combined
with any object name within the container to form the publicly
accessible URI for that object for distribution over a CDN system.


ios_uri
~~~~~~~

The URI for video streaming that uses HTTP Live Streaming from Apple.


show
~~~~

Detailed information about resource.


ssl_uri
~~~~~~~

The URI for downloading the object over HTTPS, using SSL.


streaming_uri
~~~~~~~~~~~~~

The URI for video streaming that uses HTTP Dynamic Streaming from
Adobe.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::Cloud::CloudFilesCDN
       properties:
         container: String
         ttl: Integer


Rackspace::Cloud::DNS
=====================

Note: UNSUPPORTED - This resource is not supported, use at your own risk.

Represents a DNS resource.


Required Properties
-------------------


emailAddress
~~~~~~~~~~~~

Email address to use for contacting the domain administrator.

String value expected.

Can be updated without replacement.


name
~~~~

Specifies the name for the domain or subdomain. Must be a valid domain
name.

String value expected.

Updates cause replacement.

The length must be at least 3.


Optional Properties
-------------------


comment
~~~~~~~

Optional free form text comment

String value expected.

Can be updated without replacement.

The length must be no greater than 160.


records
~~~~~~~

Domain records

List value expected.

Can be updated without replacement.

*List contents:*

..


   *
   "

   Map value expected.

   Can be updated without replacement.

   *Map properties:*

   ..


      comment
      +++++++

      Optional free form text comment

      String value expected.

      Can be updated without replacement.

      The length must be no greater than 160.

   ..


      data
      ++++

      Type specific record data

      String value expected.

      Can be updated without replacement.

   ..


      name
      ++++

      Specifies the name for the domain or subdomain. Must be a valid
      domain name.

      String value expected.

      Can be updated without replacement.

      The length must be at least 3.

   ..


      priority
      ++++++++

      Required for MX and SRV records, but forbidden for other record
      types. If specified, must be an integer from 0 to 65535.

      Integer value expected.

      Can be updated without replacement.

      The value must be in the range 0 to 65535.

   ..


      ttl
      +++

      How long other servers should cache recorddata.

      Integer value expected.

      Can be updated without replacement.

      Defaults to "3600".

      The value must be at least 300.

   ..


      type
      ++++

      Specifies the record type.

      String value expected.

      Can be updated without replacement.

      Allowed values: A, AAAA, NS, MX, CNAME, TXT, SRV


ttl
~~~

How long other servers should cache recorddata.

Integer value expected.

Can be updated without replacement.

Defaults to "3600".

The value must be at least 300.


Attributes
----------


show
~~~~

Detailed information about resource.


HOT Syntax
----------

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
==============================

Note: UNSUPPORTED - This resource is not supported, use at your own risk.

Represents a Rackspace Cloud Loadbalancer.


Required Properties
-------------------


nodes
~~~~~

List value expected.

Can be updated without replacement.

*List contents:*

..


   *
   "

   Map value expected.

   Can be updated without replacement.

   *Map properties:*

   ..


      addresses
      +++++++++

      IP addresses for the load balancer node. Must have at least one
      address.

      List value expected.

      Can be updated without replacement.

      *List contents:*

      ..


         *
         `

         String value expected.

         Can be updated without replacement.

   ..


      condition
      +++++++++

      String value expected.

      Can be updated without replacement.

      Defaults to "ENABLED".

      Allowed values: ENABLED, DISABLED, DRAINING

   ..


      port
      ++++

      Integer value expected.

      Can be updated without replacement.

   ..


      type
      ++++

      String value expected.

      Can be updated without replacement.

      Allowed values: PRIMARY, SECONDARY

   ..


      weight
      ++++++

      Number value expected.

      Can be updated without replacement.

      The value must be in the range 1 to 100.


port
~~~~

Integer value expected.

Can be updated without replacement.


protocol
~~~~~~~~

String value expected.

Can be updated without replacement.

Allowed values: DNS_TCP, DNS_UDP, FTP, HTTP, HTTPS, IMAPS, IMAPv4,
LDAP, LDAPS, MYSQL, POP3, POP3S, SMTP, TCP, TCP_CLIENT_FIRST, UDP,
UDP_STREAM, SFTP


virtualIps
~~~~~~~~~~

List value expected.

Updates cause replacement.

The length must be at least 1.

*List contents:*

..


   *
   "

   Map value expected.

   Updates cause replacement.

   *Map properties:*

   ..


      id
      ++

      ID of a shared VIP to use instead of creating a new one. This
      property cannot be specified if type or version is specified.

      Number value expected.

      Updates cause replacement.

   ..


      ipVersion
      +++++++++

      IP version of the VIP. This property cannot be specified if 'id'
      is specified. This property must be specified if id is not
      specified.

      String value expected.

      Updates cause replacement.

      Allowed values: IPV6, IPV4

   ..


      type
      ++++

      The type of VIP (public or internal). This property cannot be
      specified if 'id' is specified. This property must be specified
      if id is not specified.

      String value expected.

      Updates cause replacement.

      Allowed values: SERVICENET, PUBLIC


Optional Properties
-------------------


accessList
~~~~~~~~~~

List value expected.

Updates cause replacement.

*List contents:*

..


   *
   "

   Map value expected.

   Updates cause replacement.

   *Map properties:*

   ..


      address
      +++++++

      String value expected.

      Updates cause replacement.

   ..


      type
      ++++

      String value expected.

      Updates cause replacement.

      Allowed values: ALLOW, DENY


algorithm
~~~~~~~~~

String value expected.

Can be updated without replacement.

Allowed values: LEAST_CONNECTIONS, RANDOM, ROUND_ROBIN,
WEIGHTED_LEAST_CONNECTIONS, WEIGHTED_ROUND_ROBIN


connectionLogging
~~~~~~~~~~~~~~~~~

Boolean value expected.

Can be updated without replacement.


connectionThrottle
~~~~~~~~~~~~~~~~~~

Map value expected.

Can be updated without replacement.

*Map properties:*

..


   maxConnectionRate
   """""""""""""""""

   Number value expected.

   Can be updated without replacement.

   The value must be in the range 0 to 100000.

..


   maxConnections
   """"""""""""""

   Integer value expected.

   Can be updated without replacement.

   The value must be in the range 1 to 100000.

..


   minConnections
   """"""""""""""

   Integer value expected.

   Can be updated without replacement.

   The value must be in the range 1 to 1000.

..


   rateInterval
   """"""""""""

   Number value expected.

   Can be updated without replacement.

   The value must be in the range 1 to 3600.


contentCaching
~~~~~~~~~~~~~~

String value expected.

Can be updated without replacement.

Allowed values: ENABLED, DISABLED


errorPage
~~~~~~~~~

String value expected.

Can be updated without replacement.


halfClosed
~~~~~~~~~~

Boolean value expected.

Can be updated without replacement.


healthMonitor
~~~~~~~~~~~~~

Map value expected.

Can be updated without replacement.

*Map properties:*

..


   attemptsBeforeDeactivation
   """"""""""""""""""""""""""

   Number value expected.

   Can be updated without replacement.

   The value must be in the range 1 to 10.

..


   bodyRegex
   """""""""

   String value expected.

   Can be updated without replacement.

..


   delay
   """""

   Number value expected.

   Can be updated without replacement.

   The value must be in the range 1 to 3600.

..


   hostHeader
   """"""""""

   String value expected.

   Can be updated without replacement.

..


   path
   """"

   String value expected.

   Can be updated without replacement.

..


   statusRegex
   """""""""""

   String value expected.

   Can be updated without replacement.

..


   timeout
   """""""

   Number value expected.

   Can be updated without replacement.

   The value must be in the range 1 to 300.

..


   type
   """"

   String value expected.

   Can be updated without replacement.

   Allowed values: CONNECT, HTTP, HTTPS


httpsRedirect
~~~~~~~~~~~~~

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
~~~~~~~~

Map value expected.

Can be updated without replacement.


name
~~~~

String value expected.

Can be updated without replacement.


sessionPersistence
~~~~~~~~~~~~~~~~~~

String value expected.

Can be updated without replacement.

Allowed values: HTTP_COOKIE, SOURCE_IP


sslTermination
~~~~~~~~~~~~~~

Map value expected.

Can be updated without replacement.

*Map properties:*

..


   certificate
   """""""""""

   String value expected.

   Can be updated without replacement.

..


   intermediateCertificate
   """""""""""""""""""""""

   String value expected.

   Can be updated without replacement.

..


   privatekey
   """"""""""

   String value expected.

   Can be updated without replacement.

..


   securePort
   """"""""""

   Integer value expected.

   Can be updated without replacement.

   Defaults to "443".

..


   secureTrafficOnly
   """""""""""""""""

   Boolean value expected.

   Can be updated without replacement.

   Defaults to "False".


timeout
~~~~~~~

Number value expected.

Can be updated without replacement.

The value must be in the range 1 to 120.


Attributes
----------


PublicIp
~~~~~~~~

Public IP address of the specified instance.


show
~~~~

Detailed information about resource.


virtualIps
~~~~~~~~~~

A list of assigned virtual ip addresses


HOT Syntax
----------

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


Rackspace::Cloud::SharedIP
==========================

Note: Available since 2015.1 (Kilo)

Rackspace shared IP resource.


Required Properties
-------------------


ports
~~~~~

Provide list of ports that share an IP.

List value expected.

Updates cause replacement.

*List contents:*

..


   *
   "

   Port ID.

   String value expected.

   Updates cause replacement.


Optional Properties
-------------------


network_id
~~~~~~~~~~

ID of network to create shared_ip.

String value expected.

Updates cause replacement.

Value must be of type neutron.network


Attributes
----------


shared_ip_address
~~~~~~~~~~~~~~~~~

Shared IP address.


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::Cloud::SharedIP
       properties:
         network_id: String
         ports: [String, String, ...]


Rackspace::Cloud::WinServer
===========================

Rackspace cloud Windows server resource.


Required Properties
-------------------


flavor
~~~~~~

The ID or name of the flavor to boot onto.

String value expected.

Can be updated without replacement.

Value must be of type nova.flavor


Optional Properties
-------------------


admin_pass
~~~~~~~~~~

The administrator password for the server.

String value expected.

Can be updated without replacement.


availability_zone
~~~~~~~~~~~~~~~~~

Name of the availability zone for server placement.

String value expected.

Updates cause replacement.


block_device_mapping
~~~~~~~~~~~~~~~~~~~~

Block device mappings for this server.

List value expected.

Updates cause replacement.

*List contents:*

..


   *
   "

   Map value expected.

   Updates cause replacement.

   *Map properties:*

   ..


      delete_on_termination
      +++++++++++++++++++++

      Indicate whether the volume should be deleted when the server is
      terminated.

      Boolean value expected.

      Updates cause replacement.

   ..


      device_name
      +++++++++++

      A device name where the volume will be attached in the system at
      /dev/device_name. This value is typically vda.

      String value expected.

      Updates cause replacement.

   ..


      snapshot_id
      +++++++++++

      The ID of the snapshot to create a volume from.

      String value expected.

      Updates cause replacement.

      Value must be of type cinder.snapshot

   ..


      volume_id
      +++++++++

      The ID of the volume to boot from. Only one of volume_id or
      snapshot_id should be provided.

      String value expected.

      Updates cause replacement.

      Value must be of type cinder.volume

   ..


      volume_size
      +++++++++++

      The size of the volume, in GB. It is safe to leave this blank
      and have the Compute service infer the size.

      Integer value expected.

      Updates cause replacement.


block_device_mapping_v2
~~~~~~~~~~~~~~~~~~~~~~~

Note: Available since 2015.1 (Kilo)

Block device mappings v2 for this server.

List value expected.

Updates cause replacement.

*List contents:*

..


   *
   "

   Map value expected.

   Updates cause replacement.

   *Map properties:*

   ..


      boot_index
      ++++++++++

      Integer used for ordering the boot disks.

      Integer value expected.

      Updates cause replacement.

   ..


      delete_on_termination
      +++++++++++++++++++++

      Indicate whether the volume should be deleted when the server is
      terminated.

      Boolean value expected.

      Updates cause replacement.

   ..


      device_name
      +++++++++++

      A device name where the volume will be attached in the system at
      /dev/device_name. This value is typically vda.

      String value expected.

      Updates cause replacement.

   ..


      device_type
      +++++++++++

      Device type: at the moment we can make distinction only between
      disk and cdrom.

      String value expected.

      Updates cause replacement.

      Allowed values: cdrom, disk

   ..


      disk_bus
      ++++++++

      Bus of the device: hypervisor driver chooses a suitable default
      if omitted.

      String value expected.

      Updates cause replacement.

      Allowed values: ide, lame_bus, scsi, usb, virtio

   ..


      image_id
      ++++++++

      The ID of the image to create a volume from.

      String value expected.

      Updates cause replacement.

      Value must be of type glance.image

   ..


      snapshot_id
      +++++++++++

      The ID of the snapshot to create a volume from.

      String value expected.

      Updates cause replacement.

      Value must be of type cinder.snapshot

   ..


      swap_size
      +++++++++

      The size of the swap, in MB.

      Integer value expected.

      Updates cause replacement.

   ..


      volume_id
      +++++++++

      The volume_id can be boot or non-boot device to the server.

      String value expected.

      Updates cause replacement.

      Value must be of type cinder.volume

   ..


      volume_size
      +++++++++++

      Size of the block device in GB. If it is omitted, hypervisor
      driver calculates size.

      Integer value expected.

      Updates cause replacement.


config_drive
~~~~~~~~~~~~

If True, enable config drive on the server.

Boolean value expected.

Updates cause replacement.


diskConfig
~~~~~~~~~~

Control how the disk is partitioned when the server is created.

String value expected.

Updates cause replacement.

Allowed values: AUTO, MANUAL


flavor_update_policy
~~~~~~~~~~~~~~~~~~~~

Policy on how to apply a flavor update; either by requesting a server
resize or by replacing the entire server.

String value expected.

Can be updated without replacement.

Defaults to "RESIZE".

Allowed values: RESIZE, REPLACE


image
~~~~~

The ID or name of the image to boot with.

String value expected.

Can be updated without replacement.

Value must be of type glance.image


image_update_policy
~~~~~~~~~~~~~~~~~~~

Policy on how to apply an image-id update; either by requesting a
server rebuild or by replacing the entire server

String value expected.

Can be updated without replacement.

Defaults to "REBUILD".

Allowed values: REBUILD, REPLACE, REBUILD_PRESERVE_EPHEMERAL


key_name
~~~~~~~~

Name of keypair to inject into the server.

String value expected.

Updates cause replacement.

Value must be of type nova.keypair


metadata
~~~~~~~~

Arbitrary key/value metadata to store for this server. Both keys and
values must be 255 characters or less.  Non-string values will be
serialized to JSON (and the serialized string must be 255 characters
or less).

Map value expected.

Can be updated without replacement.


name
~~~~

Server name.

String value expected.

Can be updated without replacement.


networks
~~~~~~~~

An ordered list of nics to be added to this server, with information
about connected networks, fixed ips, port etc.

List value expected.

Can be updated without replacement.

*List contents:*

..


   *
   "

   Map value expected.

   Can be updated without replacement.

   *Map properties:*

   ..


      fixed_ip
      ++++++++

      Fixed IP address to specify for the port created on the
      requested network.

      String value expected.

      Can be updated without replacement.

      Value must be of type ip_addr

   ..


      network
      +++++++

      Name or ID of network to create a port on.

      String value expected.

      Can be updated without replacement.

      Value must be of type neutron.network

   ..


      port
      ++++

      ID of an existing port to associate with this server.

      String value expected.

      Can be updated without replacement.

      Value must be of type neutron.port

   ..


      port_extra_properties
      +++++++++++++++++++++

      Note: Available since 6.0.0 (Mitaka)

      Dict, which has expand properties for port. Used only if port
      property is not specified for creating port.

      Map value expected.

      Can be updated without replacement.

      *Map properties:*

      ..


         admin_state_up
         ``````````````

         The administrative state of this port.

         Boolean value expected.

         Can be updated without replacement.

         Defaults to "True".

      ..


         allowed_address_pairs
         `````````````````````

         Additional MAC/IP address pairs allowed to pass through the
         port.

         List value expected.

         Can be updated without replacement.

         *List contents:*

         ..


            *
            *

            Map value expected.

            Can be updated without replacement.

            *Map properties:*

            ..


               ip_address
               ==========

               IP address to allow through this port.

               String value expected.

               Can be updated without replacement.

               Value must be of type net_cidr

            ..


               mac_address
               ===========

               MAC address to allow through this port.

               String value expected.

               Can be updated without replacement.

               Value must be of type mac_addr

      ..


         binding:vnic_type
         `````````````````

         Note: Available since 2015.1 (Kilo)

         The vnic type to be bound on the neutron port. To support
         SR-IOV PCI passthrough networking, you can request that the
         neutron port to be realized as normal (virtual nic), direct
         (pci passthrough), or macvtap (virtual interface with a
         tap-like software interface). Note that this only works for
         Neutron deployments that support the bindings extension.

         String value expected.

         Can be updated without replacement.

         Allowed values: normal, direct, macvtap

      ..


         mac_address
         ```````````

         MAC address to give to this port.

         String value expected.

         Can be updated without replacement.

         Value must be of type mac_addr

      ..


         port_security_enabled
         `````````````````````

         Note: Available since 5.0.0 (Liberty)

         Flag to enable/disable port security on the port. When
         disable this feature(set it to False), there will be no
         packages filtering, like security-group and address-pairs.

         Boolean value expected.

         Can be updated without replacement.

      ..


         value_specs
         ```````````

         Extra parameters to include in the "port" object in the
         creation request.

         Map value expected.

         Can be updated without replacement.

         Defaults to "{}".

   ..


      subnet
      ++++++

      Note: Available since 5.0.0 (Liberty)

      Subnet in which to allocate the IP address for port. Used for
      creating port, based on derived properties. If subnet is
      specified, network property becomes optional.

      String value expected.

      Can be updated without replacement.


personality
~~~~~~~~~~~

A map of files to create/overwrite on the server upon boot. Keys are
file names and values are the file contents.

Map value expected.

Updates cause replacement.

Defaults to "{}".


reservation_id
~~~~~~~~~~~~~~

A UUID for the set of servers being requested.

String value expected.

Updates cause replacement.


save_admin_pass
~~~~~~~~~~~~~~~

True if the system should remember the admin password; False
otherwise.

Boolean value expected.

Updates cause replacement.

Defaults to "False".


scheduler_hints
~~~~~~~~~~~~~~~

Arbitrary key-value pairs specified by the client to help boot a
server.

Map value expected.

Updates cause replacement.


security_groups
~~~~~~~~~~~~~~~

List of security group names or IDs. Cannot be used if neutron ports
are associated with this server; assign security groups to the ports
instead.

List value expected.

Updates cause replacement.

Defaults to "[]".


software_config_transport
~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~

User data script to be executed by cloud-init.

String value expected.

Updates cause replacement.

Defaults to "".


user_data_format
~~~~~~~~~~~~~~~~

How the user_data should be formatted for the server. For
HEAT_CFNTOOLS, the user_data is bundled as part of the heat-cfntools
cloud-init boot configuration data. For RAW the user_data is passed to
Nova unmodified. For SOFTWARE_CONFIG user_data is bundled as part of
the software config data, and metadata is derived from any associated
SoftwareDeployment resources.

String value expected.

Updates cause replacement.

Defaults to "HEAT_CFNTOOLS".

Allowed values: HEAT_CFNTOOLS, RAW, SOFTWARE_CONFIG


Attributes
----------


accessIPv4
~~~~~~~~~~

The manually assigned alternative public IPv4 address of the server.


accessIPv6
~~~~~~~~~~

The manually assigned alternative public IPv6 address of the server.


addresses
~~~~~~~~~

A dict of all network addresses with corresponding port_id. Each
network will have two keys in dict, they are network name and network
id. The port ID may be obtained through the following expression:
"{get_attr: [<server>, addresses, <network name_or_id>, 0, port]}".


admin_pass
~~~~~~~~~~

The administrator password for the server.


console_urls
~~~~~~~~~~~~

Note: Available since 2015.1 (Kilo)

URLs of server's consoles. To get a specific console type, the
requested type can be specified as parameter to the get_attr function,
e.g. get_attr: [ <server>, console_urls, novnc ]. Currently supported
types are novnc, xvpvnc, spice-html5, rdp-html5, serial.


instance_name
~~~~~~~~~~~~~

AWS compatible instance name.


name
~~~~

Name of the server.


networks
~~~~~~~~

A dict of assigned network addresses of the form: {"public": [ip1,
ip2...], "private": [ip3, ip4], "public_uuid": [ip1, ip2...],
"private_uuid": [ip3, ip4]}. Each network will have two keys in dict,
they are network name and network id.


privateIPv4
~~~~~~~~~~~

The private IPv4 address of the server.


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::Cloud::WinServer
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
         save_admin_pass: Boolean
         scheduler_hints: {...}
         security_groups: [Value, Value, ...]
         software_config_transport: String
         user_data: String
         user_data_format: String


Rackspace::CloudMonitoring::AgentToken
======================================

Agent tokens are used to authenticate Monitoring agents to the
Monitoring Service. Multiple agents can share a single token.


Optional Properties
-------------------


label
~~~~~

A friendly label for this resource

String value expected.

Can be updated without replacement.

The length must be in the range 1 to 255.


Attributes
----------


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::CloudMonitoring::AgentToken
       properties:
         label: String


Rackspace::CloudMonitoring::Alarm
=================================

Alarms bind alerting rules, entities, and notification plans into a
logical unit. Alarms are responsible for determining a state (*OK*,
*WARNING* or *CRITICAL*) based on the result of a Check, and executing
a notification plan whenever that state changes. You create alerting
rules by using the alarm DSL. For information about using the alarm
language, refer to the reference documentation.

**Note** Criteria is optional. If you don't provide a criteria, the
state of your alarm depends entirely on the success or failure of the
check. This is a convenient shortcut for setting a simple alarm with a
notification plan. For example, if you set a ping check on a server,
it won't alert unless no pings are returned at all, whereas adding
criteria would enable the alert to trigger if the ping round trip time
went past a certain threshold.


Required Properties
-------------------


check
~~~~~

The check to alert on

String value expected.

Updates cause replacement.


plan
~~~~

The notification plan to execute when the state changes

String value expected.

Updates cause replacement.


Optional Properties
-------------------


criteria
~~~~~~~~

The alarm DSL for describing alerting conditions and their output
states

String value expected.

Can be updated without replacement.


disabled
~~~~~~~~

Disable processing and alerts on this alarm

Boolean value expected.

Can be updated without replacement.

Defaults to "False".


label
~~~~~

A friendly label for this resource

String value expected.

Can be updated without replacement.

The length must be in the range 1 to 255.


metadata
~~~~~~~~

Arbitrary key/value pairs that are passed during the alerting phase.
Both keys and values must be 255 characters or less. Non-string values
will be serialized to JSON (and the serialized string must be 255
characters or less).

Map value expected.

Can be updated without replacement.


Attributes
----------


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::CloudMonitoring::Alarm
       properties:
         check: String
         criteria: String
         disabled: Boolean
         label: String
         metadata: {...}
         plan: String


Rackspace::CloudMonitoring::Check
=================================

A check is one of the foundational building blocks of the monitoring
system. The check determines the parts or pieces of the entity that
you want to monitor, the monitoring frequency, how many monitoring
zones are originating the check, and so on.


Required Properties
-------------------


entity
~~~~~~

The id of the entity for which to create the check. This can either be
the id of a configured monitoring entity, a cloud server or a cloud
database instance.

String value expected.

Updates cause replacement.


type
~~~~

The specific type of resource

String value expected.

Updates cause replacement.

The length must be in the range 1 to 64.


Optional Properties
-------------------


details
~~~~~~~

A hash of type-specific details

Map value expected.

Updates cause replacement.

Defaults to "{}".


disabled
~~~~~~~~

Disables the check

Boolean value expected.

Can be updated without replacement.

Defaults to "False".


label
~~~~~

A friendly label for this resource

String value expected.

Can be updated without replacement.

The length must be in the range 1 to 255.


metadata
~~~~~~~~

Arbitrary key/value pairs that are passed during the alerting phase.
Both keys and values must be 255 characters or less. Non-string values
will be serialized to JSON (and the serialized string must be 255
characters or less).

Map value expected.

Can be updated without replacement.


monitoring_zones_poll
~~~~~~~~~~~~~~~~~~~~~

List of monitoring zones to poll from. Note: This argument is only
required for remote (non-agent) checks

List value expected.

Updates cause replacement.

*List contents:*

..


   *
   "

   String value expected.

   Updates cause replacement.

   Value must be of type monitoring.zone


period
~~~~~~

The period in seconds for a check. The value must be greater than the
minimum period set on your account.

Integer value expected.

Can be updated without replacement.

Defaults to "60".

The value must be in the range 30 to 1800.


target_alias
~~~~~~~~~~~~

A key in the entity's 'ip_addresses' hash used to resolve this check
to an IP address. This parameter is mutually exclusive with
target_hostname.

String value expected.

Updates cause replacement.

The length must be in the range 1 to 64.


target_hostname
~~~~~~~~~~~~~~~

The hostname this check should target. This parameter is mutually
exclusive with target_alias. Value must be a Valid FQDN, IPv4 or IPv6
address

String value expected.

Updates cause replacement.


target_receiver
~~~~~~~~~~~~~~~

Determines how to resolve the check target.

String value expected.

Updates cause replacement.

Defaults to "IPv4".

Allowed values: IPv4, IPv6


timeout
~~~~~~~

The timeout in seconds for a check. This has to be less than the
period.

Integer value expected.

Can be updated without replacement.

Defaults to "30".

The value must be in the range 2 to 1800.


Attributes
----------


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::CloudMonitoring::Check
       properties:
         details: {...}
         disabled: Boolean
         entity: String
         label: String
         metadata: {...}
         monitoring_zones_poll: [String, String, ...]
         period: Integer
         target_alias: String
         target_hostname: String
         target_receiver: String
         timeout: Integer
         type: String


Rackspace::CloudMonitoring::Entity
==================================

An entity is the target of what you are monitoring. For example, you
can create an entity to monitor your website, a particular web
service, or your Rackspace server or server instance. Note that an
entity represents only one item in the monitoring system. For example,
if you wanted to monitor each server in a cluster, you would create an
entity for each of the servers. You would not create a single entity
to represent the entire cluster.

An entity can have multiple checks associated with it. This allows you
to check multiple services on the same host by creating multiple
checks on the same entity, instead of multiple entities each with a
single check.


Optional Properties
-------------------


agent_id
~~~~~~~~

Agent to which this entity is bound

String value expected.

Can be updated without replacement.

Value must match pattern: [-\.\w]+

The length must be in the range 1 to 255.


ip_addresses
~~~~~~~~~~~~

IP addresses that can be referenced by checks on this entity. Keys
must be between 1 and 64 characters long. Values must be valid IPv4 or
IPv6 addresses.

Map value expected.

Updates cause replacement.


label
~~~~~

A friendly label for this resource

String value expected.

Can be updated without replacement.

The length must be in the range 1 to 255.


metadata
~~~~~~~~

Arbitrary key/value pairs that are passed during the alerting phase.
Both keys and values must be 255 characters or less. Non-string values
will be serialized to JSON (and the serialized string must be 255
characters or less).

Map value expected.

Can be updated without replacement.


Attributes
----------


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::CloudMonitoring::Entity
       properties:
         agent_id: String
         ip_addresses: {...}
         label: String
         metadata: {...}


Rackspace::CloudMonitoring::Notification
========================================

A notification is a destination to send an alarm, it can be a variety
of different types, and will evolve over time.

For instance, with a webhook type notification Rackspace Cloud
Monitoring posts JSON formatted data to a user-specified URL on an
alert condition (Check goes from *OK* -> *CRITICAL* and so on).


Required Properties
-------------------


type
~~~~

The specific type of resource

String value expected.

Updates cause replacement.

The length must be in the range 1 to 64.


Optional Properties
-------------------


details
~~~~~~~

A hash of type-specific details

Map value expected.

Updates cause replacement.

Defaults to "{}".


label
~~~~~

A friendly label for this resource

String value expected.

Can be updated without replacement.

The length must be in the range 1 to 255.


Attributes
----------


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::CloudMonitoring::Notification
       properties:
         details: {...}
         label: String
         type: String


Rackspace::CloudMonitoring::NotificationPlan
============================================

A notification plan contains a set of notification actions that
Rackspace Cloud Monitoring executes when triggered by an alarm.
Rackspace Cloud Monitoring currently supports webhook and email
notifications.

Each notification state can contain multiple notification actions. For
example, you can create a notification plan that hits a webhook/email
to notify your operations team if a warning occurs. However, if the
warning escalates to an Error, the notification plan could be
configured to hit a different webhook/email that triggers both email
and SMS messages to the operations team.


Optional Properties
-------------------


critical_state
~~~~~~~~~~~~~~

The notification list to send to when the state is CRITICAL.

List value expected.

Can be updated without replacement.


label
~~~~~

A friendly label for this resource

String value expected.

Can be updated without replacement.

The length must be in the range 1 to 255.


ok_state
~~~~~~~~

The notification list to send to when the state is OK.

List value expected.

Can be updated without replacement.


warning_state
~~~~~~~~~~~~~

The notification list to send to when the state is WARNING.

List value expected.

Can be updated without replacement.


Attributes
----------


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::CloudMonitoring::NotificationPlan
       properties:
         critical_state: [Value, Value, ...]
         label: String
         ok_state: [Value, Value, ...]
         warning_state: [Value, Value, ...]


Rackspace::CloudMonitoring::PlanNotifications
=============================================

Binds notifications to existing notification plans. This is useful for
cases (such as using monitoring with autoscale), when you need a plan
but must create the notifications dynamically later. Note that these
notifications will overwrite any of the same level created as part of
the NotificationPlan resource.


Required Properties
-------------------


plan
~~~~

The notification plan to add notifications to

String value expected.

Updates cause replacement.


Optional Properties
-------------------


critical_state
~~~~~~~~~~~~~~

The notification list to send to when the state is CRITICAL.

List value expected.

Can be updated without replacement.


ok_state
~~~~~~~~

The notification list to send to when the state is OK.

List value expected.

Can be updated without replacement.


warning_state
~~~~~~~~~~~~~

The notification list to send to when the state is WARNING.

List value expected.

Can be updated without replacement.


Attributes
----------


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::CloudMonitoring::PlanNotifications
       properties:
         critical_state: [Value, Value, ...]
         ok_state: [Value, Value, ...]
         plan: String
         warning_state: [Value, Value, ...]


Rackspace::Neutron::SecurityGroupAttachment
===========================================

Note: Available since 5.0.0 (Liberty)


Required Properties
-------------------


port
~~~~

The ID of the port to attach a security group.

String value expected.

Updates cause replacement.

Value must be of type neutron.port


security_group
~~~~~~~~~~~~~~

The ID of the security group to be attached.

String value expected.

Updates cause replacement.


Attributes
----------


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::Neutron::SecurityGroupAttachment
       properties:
         port: String
         security_group: String


Rackspace::RackConnect::PoolNode
================================

A resource for RackConnect LoadBalancerPool node.


Required Properties
-------------------


pool
~~~~

The id of the pool.

String value expected.

Updates cause replacement.

Value must be of type rackconnect.pool


server_id
~~~~~~~~~

The id of the server to be added.

String value expected.

Updates cause replacement.

Value must be of type nova.server


Attributes
----------


show
~~~~

Detailed information about resource.


virtual_ip
~~~~~~~~~~

Rackconnected loadbalancer virtual IP.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::RackConnect::PoolNode
       properties:
         pool: String
         server_id: String


Rackspace::RackConnect::PublicIP
================================

A resource for RackConnect public ips.


Required Properties
-------------------


server_id
~~~~~~~~~

The id of the server to be added.

String value expected.

Updates cause replacement.

Value must be of type nova.server


Attributes
----------


public_ip_v4
~~~~~~~~~~~~

Rackconnected server public IP.


show
~~~~

Detailed information about resource.


HOT Syntax
----------

::

   heat_template_version: 2015-04-30
   ...
   resources:
     ...
     the_resource:
       type: Rackspace::RackConnect::PublicIP
       properties:
         server_id: String
