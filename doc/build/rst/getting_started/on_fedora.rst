
Installing OpenStack and Heat on RHEL/Fedora/CentOS
***************************************************

Go to the OpenStack Documentation for the latest version of the
Installation Guide for Red Hat Enterprise Linux, CentOS and Fedora
which includes a chapter on installing the Orchestration module
(Heat).

There are instructions for installing the RDO OpenStack distribution
on Fedora and CentOS.

If installing with packstack, you can install heat by specifying
``--os-heat-install=y`` in your packstack invocation, or setting
``CONFIG_HEAT_INSTALL=y`` in your answers file.

If installing with RDO-Manager Heat will be installed by default.
