'''
--------------------------------------------------------------------
file : unum/test/extraunits.py
ver  : 04.00
role : define an extra set of units
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
from unum.units import *
unit = Unum.unit

CM       = unit( 'cm'       ,   .01 * M   , 'centimeter'       )
MM       = unit( 'mm'       ,  .001 * M   , 'millimeter'       )
KM       = unit( 'km'       , 1000. * M   , 'kilometer'        ) 
CC       = unit( 'cc'       , CM**3       , 'cubic centimeter' )
MS       = unit( 'ms'       ,  .001 * S   ,	'millisecond'      )
G        = unit( 'g'        , .001 * KG   ,	'gram'             )
KJ       = unit( 'kJ'       , 1000. * J   , 'kiloJoule'        )
CAL      = unit( 'cal'      , 4.186 * J   , 'calorie'          )
KCAL     = unit( 'kcal'     , 1000. * CAL , 'kilocalorie'      )
KW       = unit( 'kW'       , 1000. * W   , 'kiloWatt'         )
WH       = unit( 'Wh'       , W*H         , 'Watt-hour'        )
KWH      = unit( 'kWh'      , 1000. * WH  , 'kilowatt-hour'    )
CV       = unit( 'CV'       , 745.7 * W   , 'Cheval-Vapeur'    )

# cleaning
del Unum
del unit