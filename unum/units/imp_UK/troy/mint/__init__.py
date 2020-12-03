"""
https://www.wikiwand.com/en/Troy_weight#Mint_masses
"""
from unum import new_unit
from unum.units.imp_UK.troy import gr_t

mite = new_unit("mite", gr_t/20, "Mint Mite")
droit = new_unit("droit", mite/24, "Mint Droit")
perit = new_unit("perit", droit/20, "Mint Perit")
blank = new_unit("blank", perit/24, "Mint blank")
