
The ``heat.engine.watchrule`` Module
************************************

**class heat.engine.watchrule.WatchRule(context, watch_name, rule,
stack_id=None, state='NODATA', wid=None, watch_data=None,
last_evaluated=datetime.datetime(2015, 11, 16, 21, 43, 24, 880599))**

   Bases: ``object``

   ``ACTION_MAP = {'ALARM': 'AlarmActi ...  'NORMAL': 'OKActions'}``

   ``ALARM = 'ALARM'``

   ``CEILOMETER_CONTROLLED = 'CEILOMETER_CONTROLLED'``

   ``NODATA = 'NODATA'``

   ``NORMAL = 'NORMAL'``

   ``SUSPENDED = 'SUSPENDED'``

   ``WATCH_STATES = ('ALARM', 'NORMAL', 'NODATA', 'SUSPENDED',
   'CEILOMETER_CONTROLLED')``

   **create_watch_data(data)**

   ``created_at = None``

   **destroy()**

      Delete the watchrule from the database.

   **do_Average()**

   **do_Maximum()**

   **do_Minimum()**

   **do_SampleCount()**

      Count all samples within the specified period.

   **do_Sum()**

   **do_data_cmp(data, threshold)**

   **evaluate()**

   **get_alarm_state()**

   **get_details()**

   ``classmethod load(context, watch_name=None, watch=None)``

      Load the watchrule object.

      The object can be loaded either from the DB by name or from an
      existing DB object.

   **rule_actions(new_state)**

   **run_rule()**

   **set_watch_state(state)**

      Temporarily set the watch state.

      :Returns:
         list of functions to be scheduled in the stack ThreadGroup
         for the specified state.

   **state_set(state)**

      Persistently store the watch state.

   **store()**

      Store the watchrule in the database and return its ID.

      If self.id is set, we update the existing rule.

   ``updated_at = None``

**heat.engine.watchrule.rule_can_use_sample(wr, stats_data)**
