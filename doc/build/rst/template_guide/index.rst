.. _template-guide:


Template Guide
==============

* `Heat Orchestration Template (HOT) Guide <hot_guide.rst>`_
  * `Status <hot_guide.rst#status>`_
  * `Writing a hello world HOT template
    <hot_guide.rst#writing-a-hello-world-hot-template>`_
* `Writing a hello world HOT template <hello_world.rst>`_
  * `A most basic template <hello_world.rst#a-most-basic-template>`_
  * `Input parameters <hello_world.rst#input-parameters>`_
  * `Template outputs <hello_world.rst#template-outputs>`_
* `Heat Orchestration Template (HOT) specification <hot_spec.rst>`_
  * `Status <hot_spec.rst#status>`_
  * `Template structure <hot_spec.rst#template-structure>`_
  * `Heat template version <hot_spec.rst#heat-template-version>`_
  * `Parameter groups section
    <hot_spec.rst#parameter-groups-section>`_
  * `Parameters section <hot_spec.rst#parameters-section>`_
  * `Resources section <hot_spec.rst#resources-section>`_
  * `Outputs section <hot_spec.rst#outputs-section>`_
  * `Intrinsic functions <hot_spec.rst#intrinsic-functions>`_
* `Instances <basic_resources.rst>`_
  * `Manage instances <basic_resources.rst#manage-instances>`_
  * `Manage networks <basic_resources.rst#manage-networks>`_
  * `Manage volumes <basic_resources.rst#manage-volumes>`_
* `Software configuration <software_deployment.rst>`_
  * `Image building <software_deployment.rst#image-building>`_
  * `User-data boot scripts and cloud-init
    <software_deployment.rst#user-data-boot-scripts-and-cloud-init>`_
  * `Software deployment resources
    <software_deployment.rst#software-deployment-resources>`_
* `Environments <environment.rst>`_
  * `Environment file format
    <environment.rst#environment-file-format>`_
  * `Global and effective environments
    <environment.rst#global-and-effective-environments>`_
  * `Usage examples <environment.rst#usage-examples>`_
* `Template composition <composition.rst>`_
  * `Use the template filename as type
    <composition.rst#use-the-template-filename-as-type>`_
  * `Define a new resource type
    <composition.rst#define-a-new-resource-type>`_
  * `Get access to nested attributes
    <composition.rst#get-access-to-nested-attributes>`_
  * `Making your template resource more "transparent"
    <composition.rst#making-your-template-resource-more-transparent>`_
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
* `CloudFormation Compatible Resource Types <cfn.rst>`_
  * `AWS::CloudFormation::WaitCondition
    <cfn.rst#AWS::CloudFormation::WaitCondition>`_
  * `AWS::CloudFormation::WaitConditionHandle
    <cfn.rst#AWS::CloudFormation::WaitConditionHandle>`_
  * `AWS::CloudWatch::Alarm <cfn.rst#AWS::CloudWatch::Alarm>`_
  * `AWS::EC2::Instance <cfn.rst#AWS::EC2::Instance>`_
  * `AWS::ElasticLoadBalancing::LoadBalancer
    <cfn.rst#AWS::ElasticLoadBalancing::LoadBalancer>`_
  * `AWS::RDS::DBInstance <cfn.rst#AWS::RDS::DBInstance>`_
* `Unsupported Heat Resource Types <unsupported.rst>`_
  * `AWS::CloudFormation::WaitCondition
    <unsupported.rst#AWS::CloudFormation::WaitCondition>`_
  * `AWS::CloudFormation::WaitConditionHandle
    <unsupported.rst#AWS::CloudFormation::WaitConditionHandle>`_
  * `AWS::CloudWatch::Alarm <unsupported.rst#AWS::CloudWatch::Alarm>`_
  * `AWS::EC2::Instance <unsupported.rst#AWS::EC2::Instance>`_
  * `AWS::ElasticLoadBalancing::LoadBalancer
    <unsupported.rst#AWS::ElasticLoadBalancing::LoadBalancer>`_
  * `AWS::RDS::DBInstance <unsupported.rst#AWS::RDS::DBInstance>`_
  * `DockerInc::Docker::Container
    <unsupported.rst#DockerInc::Docker::Container>`_
  * `OS::Cinder::Volume <unsupported.rst#OS::Cinder::Volume>`_
  * `OS::Cinder::VolumeAttachment
    <unsupported.rst#OS::Cinder::VolumeAttachment>`_
  * `OS::Heat::CloudConfig <unsupported.rst#OS::Heat::CloudConfig>`_
  * `OS::Heat::MultipartMime
    <unsupported.rst#OS::Heat::MultipartMime>`_
  * `OS::Heat::None <unsupported.rst#OS::Heat::None>`_
  * `OS::Heat::RandomString <unsupported.rst#OS::Heat::RandomString>`_
  * `OS::Heat::ResourceGroup
    <unsupported.rst#OS::Heat::ResourceGroup>`_
  * `OS::Heat::SoftwareConfig
    <unsupported.rst#OS::Heat::SoftwareConfig>`_
  * `OS::Heat::SoftwareDeployment
    <unsupported.rst#OS::Heat::SoftwareDeployment>`_
  * `OS::Heat::SoftwareDeploymentGroup
    <unsupported.rst#OS::Heat::SoftwareDeploymentGroup>`_
  * `OS::Heat::SoftwareDeployments
    <unsupported.rst#OS::Heat::SoftwareDeployments>`_
  * `OS::Heat::Stack <unsupported.rst#OS::Heat::Stack>`_
  * `OS::Heat::SwiftSignal <unsupported.rst#OS::Heat::SwiftSignal>`_
  * `OS::Heat::SwiftSignalHandle
    <unsupported.rst#OS::Heat::SwiftSignalHandle>`_
  * `OS::Heat::TestResource <unsupported.rst#OS::Heat::TestResource>`_
  * `OS::Neutron::Net <unsupported.rst#OS::Neutron::Net>`_
  * `OS::Neutron::Port <unsupported.rst#OS::Neutron::Port>`_
  * `OS::Neutron::SecurityGroup
    <unsupported.rst#OS::Neutron::SecurityGroup>`_
  * `OS::Neutron::Subnet <unsupported.rst#OS::Neutron::Subnet>`_
  * `OS::Nova::KeyPair <unsupported.rst#OS::Nova::KeyPair>`_
  * `OS::Nova::Server <unsupported.rst#OS::Nova::Server>`_
  * `OS::Swift::Container <unsupported.rst#OS::Swift::Container>`_
  * `OS::Trove::Instance <unsupported.rst#OS::Trove::Instance>`_
  * `OS::Zaqar::Queue <unsupported.rst#OS::Zaqar::Queue>`_
  * `Rackspace::AutoScale::Group
    <unsupported.rst#Rackspace::AutoScale::Group>`_
  * `Rackspace::AutoScale::ScalingPolicy
    <unsupported.rst#Rackspace::AutoScale::ScalingPolicy>`_
  * `Rackspace::AutoScale::WebHook
    <unsupported.rst#Rackspace::AutoScale::WebHook>`_
  * `Rackspace::Cloud::DNS <unsupported.rst#Rackspace::Cloud::DNS>`_
  * `Rackspace::Cloud::LoadBalancer
    <unsupported.rst#Rackspace::Cloud::LoadBalancer>`_
* `Contributed Heat Resource Types <contrib.rst>`_
  * `OS::Cinder::Volume <contrib.rst#OS::Cinder::Volume>`_
  * `OS::Cinder::VolumeAttachment
    <contrib.rst#OS::Cinder::VolumeAttachment>`_
  * `OS::Heat::CloudConfig <contrib.rst#OS::Heat::CloudConfig>`_
  * `OS::Heat::MultipartMime <contrib.rst#OS::Heat::MultipartMime>`_
  * `OS::Heat::None <contrib.rst#OS::Heat::None>`_
  * `OS::Heat::RandomString <contrib.rst#OS::Heat::RandomString>`_
  * `OS::Heat::ResourceGroup <contrib.rst#OS::Heat::ResourceGroup>`_
  * `OS::Heat::SoftwareConfig <contrib.rst#OS::Heat::SoftwareConfig>`_
  * `OS::Heat::SoftwareDeployment
    <contrib.rst#OS::Heat::SoftwareDeployment>`_
  * `OS::Heat::SoftwareDeploymentGroup
    <contrib.rst#OS::Heat::SoftwareDeploymentGroup>`_
  * `OS::Heat::SoftwareDeployments
    <contrib.rst#OS::Heat::SoftwareDeployments>`_
  * `OS::Heat::Stack <contrib.rst#OS::Heat::Stack>`_
  * `OS::Heat::SwiftSignal <contrib.rst#OS::Heat::SwiftSignal>`_
  * `OS::Heat::SwiftSignalHandle
    <contrib.rst#OS::Heat::SwiftSignalHandle>`_
  * `OS::Heat::TestResource <contrib.rst#OS::Heat::TestResource>`_
  * `OS::Neutron::Net <contrib.rst#OS::Neutron::Net>`_
  * `OS::Neutron::Port <contrib.rst#OS::Neutron::Port>`_
  * `OS::Neutron::SecurityGroup
    <contrib.rst#OS::Neutron::SecurityGroup>`_
  * `OS::Neutron::Subnet <contrib.rst#OS::Neutron::Subnet>`_
  * `OS::Nova::KeyPair <contrib.rst#OS::Nova::KeyPair>`_
  * `OS::Nova::Server <contrib.rst#OS::Nova::Server>`_
  * `OS::Swift::Container <contrib.rst#OS::Swift::Container>`_
  * `OS::Trove::Instance <contrib.rst#OS::Trove::Instance>`_
  * `OS::Zaqar::Queue <contrib.rst#OS::Zaqar::Queue>`_
  * `Rackspace Cloud Resource Types
    <contrib.rst#rackspace-cloud-resource-types>`_
  * `DockerInc Resource <contrib.rst#dockerinc-resource>`_
* `CloudFormation Compatible Functions <functions.rst>`_
  * `Ref <functions.rst#ref>`_
  * `Fn::Base64 <functions.rst#fn-base64>`_
  * `Fn::FindInMap <functions.rst#fn-findinmap>`_
  * `Fn::GetAtt <functions.rst#fn-getatt>`_
  * `Fn::GetAZs <functions.rst#fn-getazs>`_
  * `Fn::Join <functions.rst#fn-join>`_
  * `Fn::Select <functions.rst#fn-select>`_
  * `Fn::Split <functions.rst#fn-split>`_
  * `Fn::Replace <functions.rst#fn-replace>`_
  * `Fn::ResourceFacade <functions.rst#fn-resourcefacade>`_
  * `Fn::MemberListToMap <functions.rst#fn-memberlisttomap>`_