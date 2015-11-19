
Supported Resources
===================

The following resources are supported in Rackspace Cloud
Orchestration. These sections will provide deatils on their use,
properties and their constraints, as well as available attributes.

* `OpenStack Resource Types <openstack.rst>`_
  * `OS::Cinder::Volume <openstack.rst#OS::Cinder::Volume>`_
  * `OS::Cinder::VolumeAttachment
    <openstack.rst#OS::Cinder::VolumeAttachment>`_
  * `OS::Heat::CloudConfig <openstack.rst#OS::Heat::CloudConfig>`_
  * `OS::Heat::MultipartMime <openstack.rst#OS::Heat::MultipartMime>`_
  * `OS::Heat::None <openstack.rst#OS::Heat::None>`_
  * `OS::Heat::RandomString <openstack.rst#OS::Heat::RandomString>`_
  * `OS::Heat::ResourceGroup <openstack.rst#OS::Heat::ResourceGroup>`_
  * `OS::Heat::SoftwareConfig
    <openstack.rst#OS::Heat::SoftwareConfig>`_
  * `OS::Heat::SoftwareDeployment
    <openstack.rst#OS::Heat::SoftwareDeployment>`_
  * `OS::Heat::SoftwareDeploymentGroup
    <openstack.rst#OS::Heat::SoftwareDeploymentGroup>`_
  * `OS::Heat::SoftwareDeployments
    <openstack.rst#OS::Heat::SoftwareDeployments>`_
  * `OS::Heat::Stack <openstack.rst#OS::Heat::Stack>`_
  * `OS::Heat::SwiftSignal <openstack.rst#OS::Heat::SwiftSignal>`_
  * `OS::Heat::SwiftSignalHandle
    <openstack.rst#OS::Heat::SwiftSignalHandle>`_
  * `OS::Heat::TestResource <openstack.rst#OS::Heat::TestResource>`_
  * `OS::Neutron::Net <openstack.rst#OS::Neutron::Net>`_
  * `OS::Neutron::Port <openstack.rst#OS::Neutron::Port>`_
  * `OS::Neutron::SecurityGroup
    <openstack.rst#OS::Neutron::SecurityGroup>`_
  * `OS::Neutron::Subnet <openstack.rst#OS::Neutron::Subnet>`_
  * `OS::Nova::KeyPair <openstack.rst#OS::Nova::KeyPair>`_
  * `OS::Nova::Server <openstack.rst#OS::Nova::Server>`_
  * `OS::Swift::Container <openstack.rst#OS::Swift::Container>`_
  * `OS::Trove::Instance <openstack.rst#OS::Trove::Instance>`_
  * `OS::Zaqar::Queue <openstack.rst#OS::Zaqar::Queue>`_
* `Rackspace Resource Types <rackspace.rst>`_
  * `Rackspace::AutoScale::Group
    <rackspace.rst#Rackspace::AutoScale::Group>`_
  * `Rackspace::AutoScale::ScalingPolicy
    <rackspace.rst#Rackspace::AutoScale::ScalingPolicy>`_
  * `Rackspace::AutoScale::WebHook
    <rackspace.rst#Rackspace::AutoScale::WebHook>`_
  * `Rackspace::Cloud::DNS <rackspace.rst#Rackspace::Cloud::DNS>`_
  * `Rackspace::Cloud::LoadBalancer
    <rackspace.rst#Rackspace::Cloud::LoadBalancer>`_
* `Docker Resource Types <docker.rst>`_
  * `DockerInc::Docker::Container
    <docker.rst#DockerInc::Docker::Container>`_

HOT Functions
=============

In addition to resources, several intrinsic functions are available
that allow you to reference other resources in your templates,
transform input, and other useful utilities to pass data between
resources.

* `Intrinsic Functions <functions.rst>`_
  * `get_attr <functions.rst#get-attr>`_
  * `get_file <functions.rst#get-file>`_
  * `get_param <functions.rst#get-param>`_
  * `get_resource <functions.rst#get-resource>`_
  * `list_join <functions.rst#list-join>`_
  * `resource_facade <functions.rst#resource-facade>`_
  * `str_replace <functions.rst#str-replace>`_