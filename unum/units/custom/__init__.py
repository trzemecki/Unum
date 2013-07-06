"""Sample file for defining new units.

Note that this file will be overwritten when you upgrade to a new version
of Unum, so if you have custom units they should be in their own file.
"""

from unum import Unum
unit = Unum.unit

# << uncomment this import if you want to derive your units from SI >>
# from unum.units.si import *

# << define your units hereafter, e.g.
#    M  = unit(  'm' , 0          , 'meter'     )
#    KM = unit( 'km' , 1000. * M  , 'kilometer' ) >>




# cleaning
del Unum
del unit
