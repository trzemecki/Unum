from unum import new_unit
from unum.units import g
ounce = oz_t = new_unit("oz t", 31.1034768*g, "Troy ounce")
pound = lb_t = new_unit("lb t", 12*oz_t, "Troy Pound")
pennyweight = pwt = new_unit("pwt", oz_t/20, "Troy Pennyweight")
grain = gr_t = new_unit("gr t", pwt/24, "Troy Grain")

