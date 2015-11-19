
Welcome to the Heat documentation!
==================================

Heat is a service to orchestrate composite cloud applications using a
declarative template format through an OpenStack-native REST API.


Heat's purpose and vision
-------------------------

* Heat provides a template based orchestration for describing a cloud
  application by executing appropriate `OpenStack
  <glossary.rst#term-openstack>`_ API calls to generate running cloud
  applications.

* A Heat template describes the infrastructure for a cloud application
  in text files which are readable and writable by humans, and can be
  managed by version control tools.

* Templates specify the relationships between resources (e.g. this
  volume is connected to this server). This enables Heat to call out
  to the OpenStack APIs to create all of your infrastructure in the
  correct order to completely launch your application.

* The software integrates other components of OpenStack. The templates
  allow creation of most OpenStack resource types (such as instances,
  floating ips, volumes, security groups, users, etc), as well as some
  more advanced functionality such as instance high availability,
  instance autoscaling, and nested stacks.

* Heat primarily manages infrastructure, but the templates integrate
  well with software configuration management tools such as Puppet and
  Ansible.

* Operators can customise the capabilities of Heat by installing
  plugins.

This documentation offers information aimed at end-users, operators
and developers of Heat.


Using Heat
----------

* `Creating your first stack <getting_started/create_a_stack.rst>`_
* `Template Guide <template_guide/index.rst>`_
* `Example HOT Templates <templates/index.rst>`_
* `Example CFN Templates <templates/index.rst#example-cfn-templates>`_
* `Glossary <glossary.rst>`_

Operating Heat
--------------

* `Installing OpenStack and Heat on RHEL/Fedora/CentOS
  <getting_started/on_fedora.rst>`_
* `Installing Heat on Ubuntu <getting_started/on_ubuntu.rst>`_
* `Scaling a Deployment <scale_deployment.rst>`_
* `Man pages for services and utilities <man/index.rst>`_

Developing Heat
---------------

* `Heat and DevStack <getting_started/on_devstack.rst>`_
* `Heat architecture <architecture.rst>`_
* `Heat Resource Plug-in Development Guide <pluginguide.rst>`_
* `Heat Stack Lifecycle Scheduler Hints <schedulerhints.rst>`_
* `Guru Meditation Reports <gmr.rst>`_
* `Heat Support Status usage Guide <supportstatus.rst>`_

API Documentation
-----------------

* Heat REST API Reference (OpenStack API Complete Reference -
  Orchestration)


Code Documentation
------------------

* `The heat.api.aws.ec2token Module <api/heat.api.aws.ec2token.rst>`_
* `The heat.api.aws.exception Module
  <api/heat.api.aws.exception.rst>`_
* `The heat.api.aws.utils Module <api/heat.api.aws.utils.rst>`_
* `The heat.api.cfn.v1.signal Module
  <api/heat.api.cfn.v1.signal.rst>`_
* `The heat.api.cfn.v1.stacks Module
  <api/heat.api.cfn.v1.stacks.rst>`_
* `The heat.api.cfn.versions Module <api/heat.api.cfn.versions.rst>`_
* `The heat.api.cloudwatch.watch Module
  <api/heat.api.cloudwatch.watch.rst>`_
* `The heat.api.middleware.fault Module
  <api/heat.api.middleware.fault.rst>`_
* `The heat.api.middleware.ssl Module
  <api/heat.api.middleware.ssl.rst>`_
* `The heat.api.middleware.version_negotiation Module
  <api/heat.api.middleware.version_negotiation.rst>`_
* `The heat.api.openstack.v1.actions Module
  <api/heat.api.openstack.v1.actions.rst>`_
* `The heat.api.openstack.v1.build_info Module
  <api/heat.api.openstack.v1.build_info.rst>`_
* `The heat.api.openstack.v1.events Module
  <api/heat.api.openstack.v1.events.rst>`_
* `The heat.api.openstack.v1.resources Module
  <api/heat.api.openstack.v1.resources.rst>`_
* `The heat.api.openstack.v1.services Module
  <api/heat.api.openstack.v1.services.rst>`_
* `The heat.api.openstack.v1.software_configs Module
  <api/heat.api.openstack.v1.software_configs.rst>`_
* `The heat.api.openstack.v1.software_deployments Module
  <api/heat.api.openstack.v1.software_deployments.rst>`_
* `The heat.api.openstack.v1.stacks Module
  <api/heat.api.openstack.v1.stacks.rst>`_
* `The heat.api.openstack.v1.util Module
  <api/heat.api.openstack.v1.util.rst>`_
* `The heat.api.openstack.v1.views.stacks_view Module
  <api/heat.api.openstack.v1.views.stacks_view.rst>`_
* `The heat.api.openstack.v1.views.views_common Module
  <api/heat.api.openstack.v1.views.views_common.rst>`_
* `The heat.api.openstack.versions Module
  <api/heat.api.openstack.versions.rst>`_
* `The heat.api.versions Module <api/heat.api.versions.rst>`_
* `The heat.engine.api Module <api/heat.engine.api.rst>`_
* `The heat.engine.attributes Module
  <api/heat.engine.attributes.rst>`_
* `The heat.engine.cfn.functions Module
  <api/heat.engine.cfn.functions.rst>`_
* `The heat.engine.cfn.template Module
  <api/heat.engine.cfn.template.rst>`_
* `The heat.engine.clients.client_plugin Module
  <api/heat.engine.clients.client_plugin.rst>`_
* `The heat.engine.clients.os.barbican Module
  <api/heat.engine.clients.os.barbican.rst>`_
* `The heat.engine.clients.os.ceilometer Module
  <api/heat.engine.clients.os.ceilometer.rst>`_
* `The heat.engine.clients.os.cinder Module
  <api/heat.engine.clients.os.cinder.rst>`_
* `The heat.engine.clients.os.designate Module
  <api/heat.engine.clients.os.designate.rst>`_
* `The heat.engine.clients.os.glance Module
  <api/heat.engine.clients.os.glance.rst>`_
* `The heat.engine.clients.os.heat_plugin Module
  <api/heat.engine.clients.os.heat_plugin.rst>`_
* `The heat.engine.clients.os.keystone Module
  <api/heat.engine.clients.os.keystone.rst>`_
* `The heat.engine.clients.os.magnum Module
  <api/heat.engine.clients.os.magnum.rst>`_
* `The heat.engine.clients.os.manila Module
  <api/heat.engine.clients.os.manila.rst>`_
* `The heat.engine.clients.os.mistral Module
  <api/heat.engine.clients.os.mistral.rst>`_
* `The heat.engine.clients.os.monasca Module
  <api/heat.engine.clients.os.monasca.rst>`_
* `The heat.engine.clients.os.neutron.lbaas_constraints Module
  <api/heat.engine.clients.os.neutron.lbaas_constraints.rst>`_
* `The heat.engine.clients.os.neutron.neutron_constraints Module
  <api/heat.engine.clients.os.neutron.neutron_constraints.rst>`_
* `The heat.engine.clients.os.nova Module
  <api/heat.engine.clients.os.nova.rst>`_
* `The heat.engine.clients.os.sahara Module
  <api/heat.engine.clients.os.sahara.rst>`_
* `The heat.engine.clients.os.swift Module
  <api/heat.engine.clients.os.swift.rst>`_
* `The heat.engine.clients.os.trove Module
  <api/heat.engine.clients.os.trove.rst>`_
* `The heat.engine.clients.os.zaqar Module
  <api/heat.engine.clients.os.zaqar.rst>`_
* `The heat.engine.clients.progress Module
  <api/heat.engine.clients.progress.rst>`_
* `The heat.engine.constraint.common_constraints Module
  <api/heat.engine.constraint.common_constraints.rst>`_
* `The heat.engine.constraints Module
  <api/heat.engine.constraints.rst>`_
* `The heat.engine.dependencies Module
  <api/heat.engine.dependencies.rst>`_
* `The heat.engine.environment Module
  <api/heat.engine.environment.rst>`_
* `The heat.engine.event Module <api/heat.engine.event.rst>`_
* `The heat.engine.function Module <api/heat.engine.function.rst>`_
* `The heat.engine.hot.functions Module
  <api/heat.engine.hot.functions.rst>`_
* `The heat.engine.hot.parameters Module
  <api/heat.engine.hot.parameters.rst>`_
* `The heat.engine.hot.template Module
  <api/heat.engine.hot.template.rst>`_
* `The heat.engine.lifecycle_plugin Module
  <api/heat.engine.lifecycle_plugin.rst>`_
* `The heat.engine.notification.autoscaling Module
  <api/heat.engine.notification.autoscaling.rst>`_
* `The heat.engine.notification.stack Module
  <api/heat.engine.notification.stack.rst>`_
* `The heat.engine.parameter_groups Module
  <api/heat.engine.parameter_groups.rst>`_
* `The heat.engine.parameters Module
  <api/heat.engine.parameters.rst>`_
* `The heat.engine.plugin_manager Module
  <api/heat.engine.plugin_manager.rst>`_
* `The heat.engine.properties Module
  <api/heat.engine.properties.rst>`_
* `The heat.engine.resource Module <api/heat.engine.resource.rst>`_
* `The heat.engine.rsrc_defn Module <api/heat.engine.rsrc_defn.rst>`_
* `The heat.engine.scheduler Module <api/heat.engine.scheduler.rst>`_
* `The heat.engine.service Module <api/heat.engine.service.rst>`_
* `The heat.engine.service_software_config Module
  <api/heat.engine.service_software_config.rst>`_
* `The heat.engine.service_stack_watch Module
  <api/heat.engine.service_stack_watch.rst>`_
* `The heat.engine.stack Module <api/heat.engine.stack.rst>`_
* `The heat.engine.stack_lock Module
  <api/heat.engine.stack_lock.rst>`_
* `The heat.engine.support Module <api/heat.engine.support.rst>`_
* `The heat.engine.sync_point Module
  <api/heat.engine.sync_point.rst>`_
* `The heat.engine.template Module <api/heat.engine.template.rst>`_
* `The heat.engine.timestamp Module <api/heat.engine.timestamp.rst>`_
* `The heat.engine.update Module <api/heat.engine.update.rst>`_
* `The heat.engine.watchrule Module <api/heat.engine.watchrule.rst>`_
* `The heat.engine.worker Module <api/heat.engine.worker.rst>`_
* `The heat.httpd.heat_api Module <api/heat.httpd.heat_api.rst>`_
* `The heat.httpd.heat_api_cfn Module
  <api/heat.httpd.heat_api_cfn.rst>`_
* `The heat.httpd.heat_api_cloudwatch Module
  <api/heat.httpd.heat_api_cloudwatch.rst>`_
* `The heat.objects.event Module <api/heat.objects.event.rst>`_
* `The heat.objects.fields Module <api/heat.objects.fields.rst>`_
* `The heat.objects.raw_template Module
  <api/heat.objects.raw_template.rst>`_
* `The heat.objects.resource Module <api/heat.objects.resource.rst>`_
* `The heat.objects.resource_data Module
  <api/heat.objects.resource_data.rst>`_
* `The heat.objects.service Module <api/heat.objects.service.rst>`_
* `The heat.objects.snapshot Module <api/heat.objects.snapshot.rst>`_
* `The heat.objects.software_config Module
  <api/heat.objects.software_config.rst>`_
* `The heat.objects.software_deployment Module
  <api/heat.objects.software_deployment.rst>`_
* `The heat.objects.stack Module <api/heat.objects.stack.rst>`_
* `The heat.objects.stack_lock Module
  <api/heat.objects.stack_lock.rst>`_
* `The heat.objects.stack_tag Module
  <api/heat.objects.stack_tag.rst>`_
* `The heat.objects.sync_point Module
  <api/heat.objects.sync_point.rst>`_
* `The heat.objects.user_creds Module
  <api/heat.objects.user_creds.rst>`_
* `The heat.objects.watch_data Module
  <api/heat.objects.watch_data.rst>`_
* `The heat.objects.watch_rule Module
  <api/heat.objects.watch_rule.rst>`_
* `The heat.rpc.api Module <api/heat.rpc.api.rst>`_
* `The heat.rpc.client Module <api/heat.rpc.client.rst>`_
* `The heat.rpc.listener_client Module
  <api/heat.rpc.listener_client.rst>`_
* `The heat.rpc.worker_api Module <api/heat.rpc.worker_api.rst>`_
* `The heat.rpc.worker_client Module
  <api/heat.rpc.worker_client.rst>`_
* `The heat.scaling.cooldown Module <api/heat.scaling.cooldown.rst>`_
* `The heat.scaling.lbutils Module <api/heat.scaling.lbutils.rst>`_
* `The heat.scaling.rolling_update Module
  <api/heat.scaling.rolling_update.rst>`_
* `The heat.scaling.scalingutil Module
  <api/heat.scaling.scalingutil.rst>`_
* `The heat.scaling.template Module <api/heat.scaling.template.rst>`_
* `The heat.version Module <api/heat.version.rst>`_

Indices and tables
------------------

* `Index <genindex.rst>`_

* `Module Index <py-modindex.rst>`_

* `Search Page <search.rst>`_
