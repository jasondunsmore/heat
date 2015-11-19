
The ``heat.scaling.scalingutil`` Module
=======================================

**heat.scaling.scalingutil.calculate_new_capacity(current, adjustment,
adjustment_type, min_adjustment_step, minimum, maximum)**

   Calculates new capacity from the given adjustments.

   Given the current capacity, calculates the new capacity which
   results from applying the given adjustment of the given
   adjustment-type.  The new capacity will be kept within the maximum
   and minimum bounds.
