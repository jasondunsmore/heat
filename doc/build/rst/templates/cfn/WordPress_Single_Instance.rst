
AWS Wordpress Single Instance Template
**************************************

https://git.openstack.org/cgit/openstack/heat-templates/tree/cfn/F18/WordPress_Single_Instance.template


Description
***********

AWS CloudFormation Sample Template WordPress_Single_Instance:
WordPress is web software you can use to create a beautiful website or
blog. This template installs a single-instance WordPress deployment
using a local MySQL database to store the data.


Parameters
**********

*KeyName* ``(required)``
   *type*
      *string*

   *description*
      Name of an existing EC2 KeyPair to enable SSH access to the
      instance

*InstanceType* ``(optional)``
   *type*
      *string*

   *description*
      The EC2 instance type

*DBName* ``(optional)``
   *type*
      *string*

   *description*
      The WordPress database name

*DBUsernameName* ``(optional)``
   *type*
      *string*

   *description*
      The WordPress database admin account username

*DBPassword* ``(optional)``
   *type*
      *string*

   *description*
      The WordPress database admin account password

*DBRootPassword* ``(optional)``
   *type*
      *string*

   *description*
      Root password for MySQL

*LinuxDistribution* ``(optional)``
   *type*
      *string*

   *description*
      Linux distribution of choice
