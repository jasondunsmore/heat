
Heat Stack Lifecycle Scheduler Hints
************************************

This is a mechanism whereby when heat processes a stack Server or
Volume resource, the stack id, root stack id, stack resource uuid,
stack resource name and the path in the stack can be passed to nova
and cinder by heat as scheduler hints, to the configured schedulers
for nova and cinder.


Enabling the scheduler hints
============================

By default, passing the lifecycle scheduler hints is disabled. To
enable it, set stack_scheduler_hints to True in heat.conf.


The hints
=========

When heat processes a stack, and the feature is enabled, the stack id,
root stack id, stack resource uuid, stack resource name, and the path
in the stack (as a list of tuple, (stackresourcename, stackname)) will
be passed to nova and cinder by heat as scheduler hints, to the
configured schedulers for nova and cinder.


Purpose
=======

A heat provider may have a need for custom code to examine stack
requests prior to performing the operations to create or update a
stack. After the custom code completes, the provider may want to
provide hints to the nova or cinder schedulers with stack related
identifiers, for processing by any custom scheduler plug-ins
configured for nova or cinder.
