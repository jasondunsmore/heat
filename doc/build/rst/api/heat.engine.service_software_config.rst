
The ``heat.engine.service_software_config`` Module
==================================================

**class
heat.engine.service_software_config.SoftwareConfigService(threads=1000)**

   Bases: ``oslo_service.service.Service``

   **create_software_config(cnxt, group, name, config, inputs,
   outputs, options)**

   **create_software_deployment(cnxt, server_id, config_id,
   input_values, action, status, status_reason,
   stack_user_project_id)**

   **delete_software_config(cnxt, config_id)**

   **delete_software_deployment(cnxt, deployment_id)**

   **list_software_configs(cnxt, limit=None, marker=None,
   tenant_safe=True)**

   **list_software_deployments(cnxt, server_id)**

   **metadata_software_deployments(cnxt, server_id)**

   **show_software_config(cnxt, config_id)**

   **show_software_deployment(cnxt, deployment_id)**

   **signal_software_deployment(cnxt, deployment_id, details,
   updated_at)**

   **update_software_deployment(cnxt, deployment_id, config_id,
   input_values, output_values, action, status, status_reason,
   updated_at)**
