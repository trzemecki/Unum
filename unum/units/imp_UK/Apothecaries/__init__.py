"""
https://www.britannica.com/topic/Imperial-unit
"""


## Apothecary
from unum import new_unit
from unum.units.imp_UK import pint
from unum.units.imp_UK.troy import lb_t,oz_t, gr_t

##Volume
apothecary_fluidram = apothecary_fluid_drachm = fl_dr_ap=   new_unit("fl drachm ap",     pint/8,             "Fluid Drachm")
fl_s_ap = apothecary_fl_scruple              =              new_unit("fl scruple ap",    fl_dr_ap/3,         "Fluid Scruple")
fl_min_ap = apothecary_minim                   =            new_unit("minim ap",         fl_s_ap/20,      "Minim")


##Mass/Weight
apothecary_pound = lb_ap =                                  new_unit("lb ap",         lb_t,      "Apothecary Pound") # some sources state that apothecary weight measure are a set of subdivisions of the troy system
apothecary_ounce =oz_ap =                                   new_unit("oz ap",         oz_t,      "Apothecary Ounce")
gr_ap = apothecary_grain =                                  new_unit("gr ap",         gr_t,      "Apothecary Grain")
s_ap = apothecary_scruple =                                 new_unit("s ap",         20*gr_ap,      "Apothecary Scruple")
dr_ap = apothecary_dram =                                   new_unit("dr ap",         3*apothecary_scruple,      "Apothecary Dram")