"""Provide additional common units in addition to the SI units."""
from math import pi
from unum import Unum
from unum.units.si import *
unit = Unum.defineUnit

MIN      = unit('min'     , 60 * S           , 'minute'                   )
H        = unit('h'       , 60 * MIN         , 'hour'                     )
D        = unit('d'       , 24 * H           , 'day'                      )
ARCDEG   = unit('deg'     , pi/180 * RAD     , 'degree (angle)'           )
ARCMIN   = unit("'"       , ARCDEG / 60      , 'minute (angle)'           )
ARCSEC   = unit("''"      , ARCMIN / 60      , 'second (angle)'           )
L        = unit('L'       , 1E-3 * M**3      , 'liter'                    )
TON      = unit('t'       , 1E3 * KG         , 'metric ton'               )
NP       = unit('Np'      , 1                , 'neper'                    )
DECIBEL  = unit('dB'      , 0                , 'decibel'                  )
EV       = unit('eV'      , 1.60218E-19 * J  , 'electronvolt'             )
U        = unit('u'       , 1.66054E-27 * KG , 'unified atomic mass unit' )
UA       = unit('ua'      , 1.49598E11 * M   , 'astronomical unit'        )
MILE     = unit('mile'    , 1609.34 * M      , 'statute mile'             )
NMILE    = unit('nmi'     , 1852 * M         , 'nautical mile'            )
KNOT     = unit('knot'    , MILE / H         , 'knot'                     )
ARE      = unit('a'       , 1E2 * M**2       , 'are'                      )
HA       = unit('ha'      , 1E4 * M**2       , 'hectare'                  )
BAR      = unit('bar'     , 1E5 * PA         , 'bar'                      )
ANGSTROM = unit('angstrom', 1E-10 * M        , 'angstrom'                 )
B        = unit('b'       , 1E-28 * M**2     , 'barn'                     )
CI       = unit('Ci'      , 3.7E10 * BQ      , 'curie'                    )
R        = unit('R'       , 2.58E-4 * C / KG , 'roentgen'                 )
REM      = unit('rem'     , 1E-2 * SV        , 'rem'                      )

# Note : 'rad' defined as 1E-2 Gy as been left because of the
#        name collision with 'rad' as an angle.

del pi
del unit
