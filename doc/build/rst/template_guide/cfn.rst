
CloudFormation Compatible Resource Types
========================================


AWS::CloudFormation::WaitCondition
----------------------------------

Note: Available since 2014.1 (Icehouse)


Required Properties
^^^^^^^^^^^^^^^^^^^


Handle
""""""

A reference to the wait condition handle used to signal this wait
condition.

String value expected.

Updates cause replacement.


Timeout
"""""""

The number of seconds to wait for the correct number of signals to
arrive.

Integer value expected.

Updates cause replacement.

The value must be in the range 1 to 43200.


Optional Properties
^^^^^^^^^^^^^^^^^^^


Count
"""""

The number of success signals that must be received before the stack
creation process continues.

Integer value expected.

Can be updated without replacement.

Defaults to "1".

The value must be at least 1.


Attributes
^^^^^^^^^^


Data
""""

JSON string containing data associated with wait condition signals
sent to the handle.


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
       type: AWS::CloudFormation::WaitCondition
       properties:
         Count: Integer
         Handle: String
         Timeout: Integer


AWS::CloudFormation::WaitConditionHandle
----------------------------------------

Note: Available since 2014.1 (Icehouse)

AWS WaitConditionHandle resource.

the main point of this class is to : have no dependencies (so the
instance can reference it) generate a unique url (to be returned in
the reference) then the cfn-signal will use this url to post to and
WaitCondition will poll it to see if has been written to.


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
       type: AWS::CloudFormation::WaitConditionHandle


AWS::CloudWatch::Alarm
----------------------


Required Properties
^^^^^^^^^^^^^^^^^^^


ComparisonOperator
""""""""""""""""""

String value expected.

Can be updated without replacement.

Allowed values: GreaterThanOrEqualToThreshold, GreaterThanThreshold,
LessThanThreshold, LessThanOrEqualToThreshold


EvaluationPeriods
"""""""""""""""""

String value expected.

Can be updated without replacement.


MetricName
""""""""""

String value expected.

Can be updated without replacement.


Period
""""""

String value expected.

Can be updated without replacement.


Statistic
"""""""""

String value expected.

Can be updated without replacement.

Allowed values: SampleCount, Average, Sum, Minimum, Maximum


Threshold
"""""""""

String value expected.

Can be updated without replacement.


Optional Properties
^^^^^^^^^^^^^^^^^^^


AlarmActions
""""""""""""

List value expected.

Can be updated without replacement.

Defaults to "".


AlarmDescription
""""""""""""""""

String value expected.

Can be updated without replacement.

Defaults to "An alarm".


Dimensions
""""""""""

List value expected.

Can be updated without replacement.

Defaults to "".


InsufficientDataActions
"""""""""""""""""""""""

List value expected.

Can be updated without replacement.

Defaults to "".


Namespace
"""""""""

String value expected.

Can be updated without replacement.

Defaults to "system/linux".


OKActions
"""""""""

List value expected.

Can be updated without replacement.

Defaults to "".


Units
"""""

String value expected.

Can be updated without replacement.

Defaults to "None".

Allowed values: Seconds, Microseconds, Milliseconds, Bytes, Kilobytes,
Megabytes, Gigabytes, Terabytes, Bits, Kilobits, Megabits, Gigabits,
Terabits, Percent, Count, Bytes/Second, Kilobytes/Second,
Megabytes/Second, Gigabytes/Second, Terabytes/Second, Bits/Second,
Kilobits/Second, Megabits/Second, Gigabits/Second, Terabits/Second,
Count/Second, None


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
       type: AWS::CloudWatch::Alarm
       properties:
         AlarmActions: [Value, Value, ...]
         AlarmDescription: String
         ComparisonOperator: String
         Dimensions: [Value, Value, ...]
         EvaluationPeriods: String
         InsufficientDataActions: [Value, Value, ...]
         MetricName: String
         Namespace: String
         OKActions: [Value, Value, ...]
         Period: String
         Statistic: String
         Threshold: String
         Units: String


AWS::EC2::Instance
------------------

Implementation of AWS::EC2::Instance that will create and manage Nova
compute instances.

*Note* that if Metadata is used for instance configuration,
*heat-cfntools* must be present in the target image.


Required Properties
^^^^^^^^^^^^^^^^^^^


ImageId
"""""""

Glance image ID or name.

String value expected.

Updates cause replacement.

Value must be of type glance.image


InstanceType
""""""""""""

Nova instance type (flavor).

String value expected.

Can be updated without replacement.

Value must be of type nova.flavor


Optional Properties
^^^^^^^^^^^^^^^^^^^


AvailabilityZone
""""""""""""""""

Availability zone to launch the instance in.

String value expected.

Updates cause replacement.


BlockDeviceMappings
"""""""""""""""""""

Block device mappings to attach to instance.

List value expected.

Updates cause replacement.

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


DeviceName
++++++++++

A device name where the volume will be attached in the system at
/dev/device_name.e.g. vdb

String value expected.

Updates cause replacement.


Ebs
+++

The ebs volume to attach to the instance.

Map value expected.

Updates cause replacement.

*Map properties:*


DeleteOnTermination
```````````````````

Indicate whether the volume should be deleted when the instance is
terminated.

Boolean value expected.

Updates cause replacement.

Defaults to "True".


Iops
````

Note: Not implemented.


SnapshotId
``````````

The ID of the snapshot to create a volume from.

String value expected.

Updates cause replacement.

Value must be of type cinder.snapshot


VolumeSize
``````````

The size of the volume, in GB. Must be equal or greater than the size
of the snapshot. It is safe to leave this blank and have the Compute
service infer the size.

String value expected.

Updates cause replacement.


VolumeType
``````````

Note: Not implemented.


NoDevice
++++++++

Note: Not implemented.


VirtualName
+++++++++++

Note: Not implemented.


DisableApiTermination
"""""""""""""""""""""

Note: Not implemented.


KernelId
""""""""

Note: Not implemented.


KeyName
"""""""

Optional Nova keypair name.

String value expected.

Updates cause replacement.

Value must be of type nova.keypair


Monitoring
""""""""""

Note: Not implemented.


NetworkInterfaces
"""""""""""""""""

Network interfaces to associate with instance.

List value expected.

Can be updated without replacement.


NovaSchedulerHints
""""""""""""""""""

Scheduler hints to pass to Nova (Heat extension).

List value expected.

Updates cause replacement.

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


Key
+++

String value expected.

Updates cause replacement.


Value
+++++

String value expected.

Updates cause replacement.


PlacementGroupName
""""""""""""""""""

Note: Not implemented.


PrivateIpAddress
""""""""""""""""

Note: Not implemented.


RamDiskId
"""""""""

Note: Not implemented.


SecurityGroupIds
""""""""""""""""

Security group IDs to assign.

List value expected.

Updates cause replacement.


SecurityGroups
""""""""""""""

Security group names to assign.

List value expected.

Updates cause replacement.


SourceDestCheck
"""""""""""""""

Note: Not implemented.


SubnetId
""""""""

Subnet ID to launch instance in.

String value expected.

Can be updated without replacement.


Tags
""""

Tags to attach to instance.

List value expected.

Can be updated without replacement.

*List contents:*


*
~

Map value expected.

Can be updated without replacement.

*Map properties:*


Key
+++

String value expected.

Can be updated without replacement.


Value
+++++

String value expected.

Can be updated without replacement.


Tenancy
"""""""

Note: Not implemented.


UserData
""""""""

User data to pass to instance.

String value expected.

Updates cause replacement.


Volumes
"""""""

Volumes to attach to instance.

List value expected.

Updates cause replacement.

Defaults to "[]".

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


Device
++++++

The device where the volume is exposed on the instance. This
assignment may not be honored and it is advised that the path
/dev/disk/by-id/virtio-<VolumeId> be used instead.

String value expected.

Updates cause replacement.


VolumeId
++++++++

The ID of the volume to be attached.

String value expected.

Updates cause replacement.

Value must be of type cinder.volume


Attributes
^^^^^^^^^^


AvailabilityZone
""""""""""""""""

The Availability Zone where the specified instance is launched.


PrivateDnsName
""""""""""""""

Private DNS name of the specified instance.


PrivateIp
"""""""""

Private IP address of the specified instance.


PublicDnsName
"""""""""""""

Public DNS name of the specified instance.


PublicIp
""""""""

Public IP address of the specified instance.


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
       type: AWS::EC2::Instance
       properties:
         AvailabilityZone: String
         BlockDeviceMappings: [{"DeviceName": String, "Ebs": {"DeleteOnTermination": Boolean, "VolumeSize": String, "SnapshotId": String}}, {"DeviceName": String, "Ebs": {"DeleteOnTermination": Boolean, "VolumeSize": String, "SnapshotId": String}}, ...]
         ImageId: String
         InstanceType: String
         KeyName: String
         NetworkInterfaces: [Value, Value, ...]
         NovaSchedulerHints: [{"Value": String, "Key": String}, {"Value": String, "Key": String}, ...]
         SecurityGroupIds: [Value, Value, ...]
         SecurityGroups: [Value, Value, ...]
         SubnetId: String
         Tags: [{"Value": String, "Key": String}, {"Value": String, "Key": String}, ...]
         UserData: String
         Volumes: [{"Device": String, "VolumeId": String}, {"Device": String, "VolumeId": String}, ...]


AWS::ElasticLoadBalancing::LoadBalancer
---------------------------------------

Implements a HAProxy-bearing instance as a nested stack.

The template for the nested stack can be redefined with
``loadbalancer_template`` option in ``heat.conf``.

Generally the image used for the instance must have the following
packages installed or available for installation at runtime:

::

   - heat-cfntools and its dependencies like python-psutil
   - cronie
   - socat
   - haproxy

Current default builtin template uses Fedora 21 x86_64 base cloud
image (https://getfedora.org/cloud/download/) and apart from
installing packages goes through some hoops around SELinux due to
pecularities of heat-cfntools.


Required Properties
^^^^^^^^^^^^^^^^^^^


AvailabilityZones
"""""""""""""""""

The Availability Zones in which to create the load balancer.

List value expected.

Updates cause replacement.


Listeners
"""""""""

One or more listeners for this load balancer.

List value expected.

Updates cause replacement.

*List contents:*


*
~

Map value expected.

Updates cause replacement.

*Map properties:*


InstancePort
++++++++++++

TCP port on which the instance server is listening.

Integer value expected.

Updates cause replacement.


LoadBalancerPort
++++++++++++++++

The external load balancer port number.

Integer value expected.

Updates cause replacement.


PolicyNames
+++++++++++

Note: Not implemented.


Protocol
++++++++

The load balancer transport protocol to use.

String value expected.

Updates cause replacement.

Allowed values: TCP, HTTP


SSLCertificateId
++++++++++++++++

Note: Not implemented.


Optional Properties
^^^^^^^^^^^^^^^^^^^


AppCookieStickinessPolicy
"""""""""""""""""""""""""

Note: Not implemented.


HealthCheck
"""""""""""

An application health check for the instances.

Map value expected.

Updates cause replacement.

*Map properties:*


HealthyThreshold
~~~~~~~~~~~~~~~~

The number of consecutive health probe successes required before
moving the instance to the healthy state.

Integer value expected.

Updates cause replacement.


Interval
~~~~~~~~

The approximate interval, in seconds, between health checks of an
individual instance.

Integer value expected.

Updates cause replacement.


Target
~~~~~~

The port being checked.

String value expected.

Updates cause replacement.


Timeout
~~~~~~~

Health probe timeout, in seconds.

Integer value expected.

Updates cause replacement.


UnhealthyThreshold
~~~~~~~~~~~~~~~~~~

The number of consecutive health probe failures required before moving
the instance to the unhealthy state

Integer value expected.

Updates cause replacement.


Instances
"""""""""

The list of instance IDs load balanced.

List value expected.

Can be updated without replacement.


LBCookieStickinessPolicy
""""""""""""""""""""""""

Note: Not implemented.


SecurityGroups
""""""""""""""

List of Security Groups assigned on current LB.

List value expected.

Can be updated without replacement.


Subnets
"""""""

Note: Not implemented.


Attributes
^^^^^^^^^^


CanonicalHostedZoneName
"""""""""""""""""""""""

The name of the hosted zone that is associated with the LoadBalancer.


CanonicalHostedZoneNameID
"""""""""""""""""""""""""

The ID of the hosted zone name that is associated with the
LoadBalancer.


DNSName
"""""""

The DNS name for the LoadBalancer.


SourceSecurityGroup.GroupName
"""""""""""""""""""""""""""""

The security group that you can use as part of your inbound rules for
your LoadBalancer's back-end instances.


SourceSecurityGroup.OwnerAlias
""""""""""""""""""""""""""""""

Owner of the source security group.


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
       type: AWS::ElasticLoadBalancing::LoadBalancer
       properties:
         AvailabilityZones: [Value, Value, ...]
         HealthCheck: {"HealthyThreshold": Integer, "Interval": Integer, "Target": String, "Timeout": Integer, "UnhealthyThreshold": Integer}
         Instances: [Value, Value, ...]
         Listeners: [{"InstancePort": Integer, "LoadBalancerPort": Integer, "Protocol": String}, {"InstancePort": Integer, "LoadBalancerPort": Integer, "Protocol": String}, ...]
         SecurityGroups: [Value, Value, ...]


AWS::RDS::DBInstance
--------------------


Required Properties
^^^^^^^^^^^^^^^^^^^


AllocatedStorage
""""""""""""""""

String value expected.

Can be updated without replacement.


DBInstanceClass
"""""""""""""""

String value expected.

Can be updated without replacement.


DBName
""""""

String value expected.

Can be updated without replacement.


Engine
""""""

String value expected.

Can be updated without replacement.

Allowed values: MySQL


MasterUserPassword
""""""""""""""""""

String value expected.

Can be updated without replacement.


MasterUsername
""""""""""""""

String value expected.

Can be updated without replacement.


Optional Properties
^^^^^^^^^^^^^^^^^^^


DBSecurityGroups
""""""""""""""""

List value expected.

Can be updated without replacement.

Defaults to "".


KeyName
"""""""

String value expected.

Can be updated without replacement.

Defaults to "".


Port
""""

String value expected.

Can be updated without replacement.

Defaults to "3306".


Attributes
^^^^^^^^^^


Endpoint.Address
""""""""""""""""


Endpoint.Port
"""""""""""""


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
       type: AWS::RDS::DBInstance
       properties:
         AllocatedStorage: String
         DBInstanceClass: String
         DBName: String
         DBSecurityGroups: [Value, Value, ...]
         Engine: String
         KeyName: String
         MasterUserPassword: String
         MasterUsername: String
         Port: String
