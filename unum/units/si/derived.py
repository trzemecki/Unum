'''
--------------------------------------------------------------------
file : unum/units/si/derived.py
ver  : 04.00
role : define the SI derived units
       (source : http://physics.nist.gov/cuu/Units/units.html)
--------------------------------------------------------------------

Copyright (C) 2000-2004 Pierre Denis

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
--------------------------------------------------------------------
'''

from unum import Unum
from unum.units.si.base import *
unit = Unum.unit

RAD     = unit( 'rad'   , M / M          , 'radian'         )
SR      = unit( 'sr'    , M**2 / M**2    , 'steradian'      )
HZ      = unit( 'Hz'    , 1 / S          , 'hertz'          )
N       = unit( 'N'     , M*KG / S**2    , 'newton'         )
PA      = unit( 'Pa'    , N / M**2       , 'pascal'         )
J       = unit( 'J'     , N*M            , 'joule'          )
W       = unit( 'W'     , J / S          , 'watt'           )
C       = unit( 'C'     , S * A          , 'coulomb'        )
V       = unit( 'V'     , W / A          , 'volt'           )
F       = unit( 'F'     , C / V          , 'farad'          )
OHM     = unit( 'ohm'   , V / A          , 'ohm'            )
SIEMENS = unit( 'S'     , A / V          , 'siemens'        )
WB      = unit( 'Wb'    , V * S          , 'weber'          )
T       = unit( 'T'     , WB / M**2      , 'tesla'          )
HENRY   = unit( 'H'     , WB / A         , 'henry'          )
CELSIUS = unit( 'deg C' , K              , 'degree Celsius' )  # warning : conversion assumes relative temperatures
LM      = unit( 'lm'    , CD * SR        , 'lumen'          )
LX      = unit( 'lx'    , LM / M**2      , 'lux'            )
BQ      = unit( 'Bq'    , 1 / S          , 'becquerel'      )
GY      = unit( 'Gy'    , J / KG         , 'gray'           )
SV      = unit( 'Sv'    , J / KG         , 'sievert'        )
KAT     = unit( 'kat'   , MOL / S        , 'katal'          )

# cleaning
del Unum
del unit
