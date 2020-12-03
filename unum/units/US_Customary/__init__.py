"""
US Customary units.
Author: L Selter, 2020
Maintainer: L Selter
https://github.com/Tirpitz93

Much of these units are based off: https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/English_Length_Units_Graph.svg/348px-English_Length_Units_Graph.svg.png
and its parent page: https://www.wikiwand.com/en/Imperial_units
as well as: https://www.britannica.com/topic/Imperial-unit
"""


from unum import new_unit
from unum.units import cm
from unum.units.imp_UK import short_ton as ton_s_UK
from unum.units.imp_UK import short_hundredweight as hundred_weight_s_UK
fl_dr_US = us_fluid_dram = new_unit("fl dr (US)", 3.6966911953125 * cm**3, "Fluid Dram (US)")
ton = ton_s_UK
hundredweight = hundred_weight_s_UK
