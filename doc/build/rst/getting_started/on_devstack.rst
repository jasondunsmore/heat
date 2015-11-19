
Heat and DevStack
=================

Heat is fully integrated into DevStack. This is a convenient way to
try out or develop heat alongside the current development state of all
the other OpenStack projects. Heat on DevStack works on both Ubuntu
and Fedora.

These instructions assume you already have a working DevStack
installation which can launch basic instances.


Configure DevStack to enable Heat
---------------------------------

Heat is configured by default on devstack for Icehouse and Juno
releases. Newer versions of OpenStack require enabling heat services
in devstack *local.conf*.

Add the following to *[[local|localrc]]* section of *local.conf*:

::

   [[local|localrc]]

   #Enable heat services
   enable_service h-eng h-api h-api-cfn h-api-cw

It would also be useful to automatically download and register a VM
image that Heat can launch. To do that add the following to your
devstack *localrc*:

::

   IMAGE_URLS+=",http://download.fedoraproject.org/pub/fedora/linux/releases/21/Cloud/Images/x86_64/Fedora-Cloud-Base-20141203-21.x86_64.qcow2"

URLs for any cloud image may be specified, but fedora images from F20
contain the heat-cfntools package which is required for some heat
functionality.

That is all the configuration that is required. When you run
*./stack.sh* the Heat processes will be launched in *screen* with the
labels prefixed with *h-*.


Configure DevStack to enable Ceilometer (if using Alarms)
---------------------------------------------------------

To use Ceilometer Alarms you need to enable Ceilometer in devstack.
Adding the following lines to your *localrc* file will enable the
ceilometer services:

::

   CEILOMETER_BACKEND=mongodb
   enable_plugin ceilometer https://git.openstack.org/openstack/ceilometer


Configure DevStack to enable OSprofiler
---------------------------------------

Add the profiler notifier to your Ceilometer to your config:

::

   CEILOMETER_NOTIFICATION_TOPICS=notifications,profiler

Enable the profiler in /etc/heat/heat.conf:

::

   $ echo -e "[profiler]\nprofiler_enabled = True\ntrace_sqlalchemy = True\n" >> /etc/heat/heat.conf

Change the default hmac_key in /etc/heat/api-paste.ini:

::

   $ sed -i "s/hmac_keys =.*/hmac_keys = SECRET_KEY/" /etc/heat/api-paste.ini

Run any command with --profile SECRET_KEY:

::

   $ heat --profile SECRET_KEY stack-list
   # it will print <Trace ID>

Get pretty HTML with traces:

::

   $ osprofiler trace show --html <Profile ID>

Note that osprofiler should be run with the admin user name & tenant.


Create a stack
--------------

Now that you have a working Heat environment you can go to `Creating
your first stack <create_a_stack.rst#create-a-stack>`_.
