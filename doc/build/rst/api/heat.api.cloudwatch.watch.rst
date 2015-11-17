
The ``heat.api.cloudwatch.watch`` Module
****************************************

Endpoint for heat AWS-compatible CloudWatch API.

**class heat.api.cloudwatch.watch.WatchController(options)**

   Bases: ``object``

   WSGI controller for CloudWatch resource in heat API.

   Implements the API actions.

   **delete_alarms(req)**

      Implements DeleteAlarms API action.

   **describe_alarm_history(req)**

      Implements DescribeAlarmHistory API action.

   **describe_alarms(req)**

      Implements DescribeAlarms API action.

   **describe_alarms_for_metric(req)**

      Implements DescribeAlarmsForMetric API action.

   **disable_alarm_actions(req)**

      Implements DisableAlarmActions API action.

   **enable_alarm_actions(req)**

      Implements EnableAlarmActions API action.

   **get_metric_statistics(req)**

      Implements GetMetricStatistics API action.

   **list_metrics(req)**

      Implements ListMetrics API action.

      Lists metric datapoints associated with a particular alarm, or
      all alarms if none specified.

   **put_metric_alarm(req)**

      Implements PutMetricAlarm API action.

   **put_metric_data(req)**

      Implements PutMetricData API action.

   **set_alarm_state(req)**

      Implements SetAlarmState API action.

**heat.api.cloudwatch.watch.create_resource(options)**

   Watch resource factory method.
