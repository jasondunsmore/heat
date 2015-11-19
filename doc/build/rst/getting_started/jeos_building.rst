
Building JEOS images for use with Heat
======================================

Heat's full functionality can only be used when launching cloud images
that have the heat-cfntools package installed. This document describes
some options for creating a heat-cfntools enabled image for yourself.


Building an image with diskimage-builder
----------------------------------------

diskimage-builder is a tool for customizing cloud images.
tripleo-image-elements is a collection of diskimage-builder elements
related to the TripleO project. It includes an element for
heat-cfntools which can be used to create heat-enabled images.

Install the tool (preferably in a virtualenv) and fetch the elements:

::

   pip install git+https://git.openstack.org/openstack/diskimage-builder
   git clone https://git.openstack.org/openstack/tripleo-image-elements

To create a heat-cfntools enabled image with the current release of
Fedora x86_64:

::

   export ELEMENTS_PATH=tripleo-image-elements/elements
   disk-image-create vm fedora heat-cfntools -a amd64 -o fedora-heat-cfntools

The image may then be pushed to glance, e.g:

::

   source ~/.openstack/keystonerc
   glance image-create --name fedora-heat-cfntools --is-public true --disk-format qcow2 --container-format bare < fedora-heat-cfntools.qcow2

To create a heat-cfntools enabled image with the current release of
Ubuntu i386:

::

   export ELEMENTS_PATH=tripleo-image-elements/elements
   disk-image-create vm ubuntu heat-cfntools -a i386 -o ubuntu-heat-cfntools

If you are creating your own images you should consider creating
golden images which contain all the packages required for the stacks
that you launch. You can do this by writing your own diskimage-builder
elements and invoking those elements in the call to disk-image-create.

This means that the resulting heat templates only need to modify
configuration files. This will speed stack launch time and reduce the
risk of a transient package download failure causing the stack launch
to fail.

To create an image that contains hooks needed for SoftwareConfig and
SoftwareDeployment, you can follow the steps bellow to build a fedora
based image:

::

   pip install git+https://git.openstack.org/openstack/diskimage-builder
   git clone https://git.openstack.org/openstack/tripleo-image-elements
   git clone https://git.openstack.org/openstack/heat-templates
   export ELEMENTS_PATH=tripleo-image-elements/elements:heat-templates/hot/software-config/elements
   disk-image-create vm \
       fedora selinux-permissive \
       heat-config \
       os-collect-config \
       os-refresh-config \
       os-apply-config \
       heat-config-cfn-init \
       heat-config-puppet \
       heat-config-script \
       -o fedora-software-config.qcow2

The image may then be pushed to glance, e.g:

::

   source ~/.openstack/keystonerc
   glance image-create --name=fedora-software-config --is-public=true --disk-format=qcow2 --container-format=bare < fedora-software-config.qcow2
