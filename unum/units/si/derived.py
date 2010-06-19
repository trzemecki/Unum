"""Define the SI derived units.

Source: http://physics.nist.gov/cuu/Units/units.html
"""

from unum import Unum
from unum.units.si.base import *
unit = Unum.unit

rad        = RAD     = unit( 'rad'   , M / M          , 'radian'         )
sr         = SR      = unit( 'sr'    , M**2 / M**2    , 'steradian'      )
Hz         = HZ      = unit( 'Hz'    , 1 / s          , 'hertz'          )
N          = N       = unit( 'N'     , M*KG / s**2    , 'newton'         )
Pa         = PA      = unit( 'Pa'    , N / M**2       , 'pascal'         )
J          = J       = unit( 'J'     , N*M            , 'joule'          )
W          = W       = unit( 'W'     , J / s          , 'watt'           )
C          = C       = unit( 'C'     , s * A          , 'coulomb'        )
V          = V       = unit( 'V'     , W / A          , 'volt'           )
F          = F       = unit( 'F'     , C / V          , 'farad'          )
ohm        = OHM     = unit( 'ohm'   , V / A          , 'ohm'            )
S          = SIEMENS = unit( 'S'     , A / V          , 'siemens'        )
Wb         = WB      = unit( 'Wb'    , V * s          , 'weber'          )
T          = T       = unit( 'T'     , WB / M**2      , 'tesla'          )
H          = HENRY   = unit( 'H'     , WB / A         , 'henry'          )
# warning : conversion assumes relative temperatures
celsius    = CELSIUS = unit( 'deg C' , K              , 'degree Celsius' )  
lm         = LM      = unit( 'lm'    , CD * SR        , 'lumen'          )
lx         = LX      = unit( 'lx'    , LM / M**2      , 'lux'            )
Bq         = BQ      = unit( 'Bq'    , 1 / s          , 'becquerel'      )
Gy         = GY      = unit( 'Gy'    , J / KG         , 'gray'           )
Sv         = SV      = unit( 'Sv'    , J / KG         , 'sievert'        )
kat        = KAT     = unit( 'kat'   , MOL / s        , 'katal'          )

# cleaning
del Unum
del unit
