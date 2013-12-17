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

===================
Scaling Out Engines
===================

Heat 
In an architecture where a large number of stacks  need to be
handled, the API services can be overloaded. In those scenarios, in order to
increase the system performance, it can be helpful to run multiple APIs and use
a load balancing mechanism.

This guide details how to scale out the ReST and CFN APIs, also known as the
*heat-api* and *heat-api-cfn* services, respectively.


Background
==========



Assumptions
===========

This guide, using a devstack installation of Openstack, assumes that:

    1. You have configured devstack from `Single Machine Installation Guide
       <http://devstack.org/guides/single-machine.html>`_;
    2. You have set up Heat on devstack, as defined at `Heat and Devstack
       <http://docs.openstack.org/developer/heat/getting_started/
       on_devstack.html>`_;
    3. You have installed `HAProxy <http://haproxy.1wt.eu>`_ on the devstack
       server.


Architecture
============

The following diagram shows a scaled out Heat architecture with
multiple engines:

           |- [ REST-API ] -|
           |-     ...      -|
           |- [ REST-API ] -|               |- [ ENGINE ] -|
 [ ... ] --                  -- < AMQP > -- |-     ...    -|
           |- [ API-CFN ]  -|               |- [ ENGINE ] -|
           |-     ...      -|
           |- [ API-CFN ]  -|



A request sent from the CLI looks like:

    1. CLI contacts the proxy;
    2. The HAProxy server, acting as a load balancer, redirects the call to an
       API instance;
    3. The API server sends messages to RabbitMQ, and the engine server picks up
       messages from the RabbitMQ queue.


Deploying Multiple Engines
==========================

Each engine should be configured to subscribe to the same 
::

    [DEFAULT]
    rabbit_password = {RABBIT_PASS}
    rabbit_host = {RABBIT_HOST}


Senarios
========

