"""
This is one of those lovely confusing messes we are left with when people try to standardise.
https://www.wikiwand.com/en/Pound_(mass)#Metric_pounds
"""

from unum import new_unit
from unum.units import g

metric_pound = lb_m = new_unit("lb m", 500 * g, "Metric Pound")
