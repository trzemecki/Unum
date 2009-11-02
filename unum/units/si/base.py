'''
--------------------------------------------------------------------
file : unum/units/si/base.py
ver  : 04.00
role : define the seven SI base units
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
unit = Unum.unit

M   = unit( 'm'  , 0, 'meter'    )
KG  = unit( 'kg' , 0, 'kilogram' )
S   = unit( 's'  , 0, 'second'   )
A   = unit( 'A'  , 0, 'ampere'   )
K   = unit( 'K'  , 0, 'kelvin'   )
MOL = unit( 'mol', 0, 'mole'     )
CD  = unit( 'cd' , 0, 'candela'  )

# cleaning
del Unum
del unit
