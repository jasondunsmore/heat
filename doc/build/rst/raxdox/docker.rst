
Docker Resource Types
*********************


DockerInc::Docker::Container
============================

Note: UNSUPPORTED - This resource is not supported, use at your own risk.


Optional Properties
-------------------


cap_add
~~~~~~~

Note: Available since 2015.1 (Kilo)

Be used to add kernel capabilities (only supported for API version >=
1.2.0).

List value expected.

Updates cause replacement.

Defaults to "[]".

*List contents:*

..


   *
   "

   The security features provided by Linux kernels.

   String value expected.

   Updates cause replacement.

   Allowed values: SETPCAP, SYS_MODULE, SYS_RAWIO, SYS_PACCT,
   SYS_ADMIN, SYS_NICE, SYS_RESOURCE, SYS_TIME, SYS_TTY_CONFIG, MKNOD,
   AUDIT_WRITE, AUDIT_CONTROL, MAC_OVERRIDE, MAC_ADMIN, NET_ADMIN,
   SYSLOG, CHOWN, NET_RAW, DAC_OVERRIDE, FOWNER, DAC_READ_SEARCH,
   FSETID, KILL, SETGID, SETUID, LINUX_IMMUTABLE, NET_BIND_SERVICE,
   NET_BROADCAST, IPC_LOCK, IPC_OWNER, SYS_CHROOT, SYS_PTRACE,
   SYS_BOOT, LEASE, SETFCAP, WAKE_ALARM, BLOCK_SUSPEND, ALL


cap_drop
~~~~~~~~

Note: Available since 2015.1 (Kilo)

Be used to drop kernel capabilities (only supported for API version >=
1.2.0).

List value expected.

Updates cause replacement.

Defaults to "[]".

*List contents:*

..


   *
   "

   The security features provided by Linux kernels.

   String value expected.

   Updates cause replacement.

   Allowed values: SETPCAP, SYS_MODULE, SYS_RAWIO, SYS_PACCT,
   SYS_ADMIN, SYS_NICE, SYS_RESOURCE, SYS_TIME, SYS_TTY_CONFIG, MKNOD,
   AUDIT_WRITE, AUDIT_CONTROL, MAC_OVERRIDE, MAC_ADMIN, NET_ADMIN,
   SYSLOG, CHOWN, NET_RAW, DAC_OVERRIDE, FOWNER, DAC_READ_SEARCH,
   FSETID, KILL, SETGID, SETUID, LINUX_IMMUTABLE, NET_BIND_SERVICE,
   NET_BROADCAST, IPC_LOCK, IPC_OWNER, SYS_CHROOT, SYS_PTRACE,
   SYS_BOOT, LEASE, SETFCAP, WAKE_ALARM, BLOCK_SUSPEND, ALL


cmd
~~~

Command to run after spawning the container.

List value expected.

Updates cause replacement.

Defaults to "[]".


cpu_set
~~~~~~~

Note: Available since 5.0.0 (Liberty)

The CPUs in which to allow execution (only supported for API version
>= 1.12).

String value expected.

Updates cause replacement.


cpu_shares
~~~~~~~~~~

Note: Available since 5.0.0 (Liberty)

Relative weight which determines the allocation of the CPU processing
power(only supported for API version >= 1.8).

Integer value expected.

Updates cause replacement.

Defaults to "0".


devices
~~~~~~~

Note: Available since 5.0.0 (Liberty)

Device mappings (only supported for API version >= 1.14).

List value expected.

Updates cause replacement.

Defaults to "[]".

*List contents:*

..


   *
   "

   Map value expected.

   Updates cause replacement.

   *Map properties:*

   ..


      path_in_container
      +++++++++++++++++

      The device path of the container mappings to the host.

      String value expected.

      Updates cause replacement.

      The length must be no greater than 255.

      Value must match pattern: ^/dev/[/_\-a-zA-Z0-9]+$

   ..


      path_on_host
      ++++++++++++

      The device path on the host.

      String value expected.

      Updates cause replacement.

      The length must be no greater than 255.

      Value must match pattern: ^/dev/[/_\-a-zA-Z0-9]+$

   ..


      permissions
      +++++++++++

      The permissions of the container to read/write/create the
      devices.

      String value expected.

      Updates cause replacement.

      Defaults to "rwm".

      Allowed values: r, w, m, rw, rm, wm, rwm


dns
~~~

Set custom dns servers.

List value expected.

Updates cause replacement.


docker_endpoint
~~~~~~~~~~~~~~~

Docker daemon endpoint (by default the local docker daemon will be
used).

String value expected.

Updates cause replacement.


env
~~~

Set environment variables.

List value expected.

Updates cause replacement.


hostname
~~~~~~~~

Hostname of the container.

String value expected.

Updates cause replacement.

Defaults to "".


image
~~~~~

Image name.

String value expected.

Updates cause replacement.


links
~~~~~

Links to other containers.

Map value expected.

Updates cause replacement.


memory
~~~~~~

Memory limit (Bytes).

Integer value expected.

Updates cause replacement.

Defaults to "0".


name
~~~~

Name of the container.

String value expected.

Updates cause replacement.


open_stdin
~~~~~~~~~~

Open stdin.

Boolean value expected.

Updates cause replacement.

Defaults to "False".


port_bindings
~~~~~~~~~~~~~

TCP/UDP ports bindings.

Map value expected.

Updates cause replacement.


port_specs
~~~~~~~~~~

TCP/UDP ports mapping.

List value expected.

Updates cause replacement.


privileged
~~~~~~~~~~

Enable extended privileges.

Boolean value expected.

Updates cause replacement.

Defaults to "False".


read_only
~~~~~~~~~

Note: Available since 2015.1 (Kilo)

If true, mount the container's root filesystem as read only (only
supported for API version >= 1.17).

Boolean value expected.

Updates cause replacement.

Defaults to "False".


restart_policy
~~~~~~~~~~~~~~

Note: Available since 2015.1 (Kilo)

Restart policies (only supported for API version >= 1.2.0).

Map value expected.

Updates cause replacement.

Defaults to "{}".

*Map properties:*

..


   MaximumRetryCount
   """""""""""""""""

   A maximum restart count for the on-failure policy.

   Integer value expected.

   Updates cause replacement.

   Defaults to "0".

..


   Name
   """"

   The behavior to apply when the container exits.

   String value expected.

   Updates cause replacement.

   Defaults to "no".

   Allowed values: no, on-failure, always


stdin_once
~~~~~~~~~~

If true, close stdin after the 1 attached client disconnects.

Boolean value expected.

Updates cause replacement.

Defaults to "False".


tty
~~~

Allocate a pseudo-tty.

Boolean value expected.

Updates cause replacement.

Defaults to "False".


user
~~~~

Username or UID.

String value expected.

Updates cause replacement.

Defaults to "".


volumes
~~~~~~~

Create a bind mount.

Map value expected.

Updates cause replacement.

Defaults to "{}".


volumes_from
~~~~~~~~~~~~

Mount all specified volumes.

List value expected.

Updates cause replacement.

Defaults to "".


Attributes
----------


info
~~~~

Container info.


logs
~~~~

Container logs.


logs_head
~~~~~~~~~

Container first logs line.


logs_tail
~~~~~~~~~

Container last logs line.


network_gateway
~~~~~~~~~~~~~~~

Container ip gateway.


network_info
~~~~~~~~~~~~

Container network info.


network_ip
~~~~~~~~~~

Container ip address.


network_tcp_ports
~~~~~~~~~~~~~~~~~

Container TCP ports.


network_udp_ports
~~~~~~~~~~~~~~~~~

Container UDP ports.


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
       type: DockerInc::Docker::Container
       properties:
         cap_add: [String, String, ...]
         cap_drop: [String, String, ...]
         cmd: [Value, Value, ...]
         cpu_set: String
         cpu_shares: Integer
         devices: [{"path_on_host": String, "path_in_container": String, "permissions": String}, {"path_on_host": String, "path_in_container": String, "permissions": String}, ...]
         dns: [Value, Value, ...]
         docker_endpoint: String
         env: [Value, Value, ...]
         hostname: String
         image: String
         links: {...}
         memory: Integer
         name: String
         open_stdin: Boolean
         port_bindings: {...}
         port_specs: [Value, Value, ...]
         privileged: Boolean
         read_only: Boolean
         restart_policy: {"MaximumRetryCount": Integer, "Name": String}
         stdin_once: Boolean
         tty: Boolean
         user: String
         volumes: {...}
         volumes_from: [Value, Value, ...]
