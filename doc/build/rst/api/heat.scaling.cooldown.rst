
The ``heat.scaling.cooldown`` Module
************************************

**class heat.scaling.cooldown.CooldownMixin**

   Bases: ``object``

   Utility class to encapsulate Cooldown related logic.

   This class is shared between AutoScalingGroup and ScalingPolicy.
   This logic includes both cooldown timestamp comparing and scaling
   in progress checking.
