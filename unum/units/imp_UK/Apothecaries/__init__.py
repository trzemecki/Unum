# -*- encoding: UTF-8 -*-

"""
https://www.britannica.com/topic/Imperial-unit
"""

# Apothecary
from unum import new_unit
from unum.units.imp_UK import fl_oz
from unum.units.imp_UK.troy import lb_t, oz_t, gr_t

# Volume
apothecary_fluid_drachm = fl_dr_ap = new_unit("fl drachm ap", fl_oz / 8, "Fluid Drachm")
fl_s_ap = apothecary_fl_scruple = new_unit("fl scruple ap", fl_dr_ap / 3, "Fluid Scruple")
min_ap = apothecary_minim = new_unit("minim ap", fl_s_ap / 20, "Minim")

# Mass/Weight

apothecary_pound = lb_ap = new_unit("lb ap", lb_t, "Apothecary Pound")  # some sources state that apothecary weight measure are a set of subdivisions of the troy system
apothecary_ounce = oz_ap = new_unit("oz ap", oz_t, "Apothecary Ounce")
gr_ap = apothecary_grain = new_unit("gr ap", gr_t, "Apothecary Grain")
s_ap = apothecary_scruple = new_unit("s ap", 20 * gr_ap, "Apothecary Scruple")
dr_ap = apothecary_drachm = drachm = new_unit("dr ap", apothecary_ounce / 8, "Apothecary Drachm")
# dram now meant only avoirdupois drams, which were ​1⁄16 of an avoirdupois ounce of 437.5 grains, thus equal to 27.34 grains
# drachm now meant only apothecaries' drachms, which were ​1⁄8 of an apothecaries' ounce of 480 grains, thus equal to 60 grains
