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

=======================================================
Rackspace Cloud Orchestration Templates Developer Guide
=======================================================

Rackspace Cloud Orchestration is a RESTful API Service that can be used to
create and manage cloud resources (for example: servers + software
installation, databases, load balancers, and so forth) by declaring what you
want deployed using a simple template language, as described in this guide.

Cloud Orchestration is based on the OpenStack open source project named Heat.
Rackspace Cloud Orchestration currently supports the HOT
(Heat Orchestration Template) syntax specification of Heat.

.. toctree::
   : maxdepth: 1
   
   legal
   audience
   additional

Concepts
--------
To use Cloud Orchestration effectively, you should understand several key
concepts:

Template
    A Cloud Orchestration template is a portable file, written in a
    user-readable language, that describes how a set of resources should be
    assembled and what software should be installed in order to produce a
    working deployment. The template specifies what resources should be used,
    what attributes can be set, and other parameters that are critical to the
    successful, repeatable automation of a specific application deployment.

Resource
    A resource is a template artifact that represents some component of your
    desired architecture (a Cloud Server, a group of scaled Cloud Servers, a
    load balancer, some configuration management system, and so forth).

Stack
    A stack is a group of resources (servers, load balancers, databases, and so
    forth) combined to fulfill a useful purpose. Based on a template, Heat
    orchestration engine creates an instantiated set of resources (a stack) to
    run the application framework or component specified (in the template). A
    stack is a running instance of a template. The result of creating a stack
    is a deployment of the application framework or component.

How Cloud Orchestration Works
-----------------------------

* A Cloud Orchestration template describes the infrastructure for a cloud
  application in a YAML or JSON text file that is readable and writable by
  humans, and can be checked into version control, diffed, and so forth.
* Infrastructure resources that can be described include: servers, volumes, and
  so forth.
* Cloud Orchestration also provides an autoscaling service that integrates with
  Rackspace Cloud Auto Scale, so you can include a scaling group as a resource
  in a template.
* Templates can also specify the relationships between resources (for example
  this volume is connected to this server). This enables Cloud Orchestration to
  call out to the Rackspace APIs to create all of your infrastructure in the
  correct order to completely launch your application.
* Cloud Orchestration manages the whole lifecycle of the application. When you
  need to change your infrastructure, simply modify the template and use it to
  update your existing stack. Cloud Orchestration knows how to make the
  necessary changes. It will also delete all of the resources when you are
  finished with the application.
* Cloud Orchestration primarily manages infrastructure, but the templates
  integrate well with software configuration management tools such as Puppet
  and Chef.

Rackspace Cloud Orchestration Services are available to Rackspace Cloud
customers. Interactions with Rackspace Cloud Orchestration occur
programmatically via the Rackspace Cloud Orchestration API as described in the
Cloud Orchestration Developer Guide.

We welcome feedback, comments, and bug reports at our community forum:
https://community.rackspace.com/products/f/25/t/3476.

Templates
---------
The following sections will give you a basic understanding of template
structure as well as slightly more advanced topics around customizing your
stack using environments and template composition.

.. toctree::
   :maxdepth: 1

   hot_spec
   hot_guide
   environment
   composition

Supported Resources
-------------------
The following resources are supported in Rackspace Cloud Orchestration. These
sections will provide deatils on their use, properties and their constraints,
as well as available attributes.

.. toctree::
   :maxdepth: 2

   openstack
   rackspace
   docker
 
HOT Functions
-------------
In addition to resources, several intrinsic functions are available that allow
you to reference other resources in your templates, transform input, and other
useful utilities to pass data between resources.

.. toctree::
   :maxdepth: 2

   functions