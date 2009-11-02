"""Provide additional common units in addition to the SI units."""
from math import pi
from unum import Unum
from unum.units.si import *

MIN      = Unum.unit('min'     , 60 * S           , 'minute'                   )
H        = Unum.unit('h'       , 60 * MIN         , 'hour'                     )
D        = Unum.unit('d'       , 24 * H           , 'day'                      )
ARCDEG   = Unum.unit('deg'     , pi/180 * RAD     , 'degree (angle)'           )
ARCMIN   = Unum.unit("'"       , ARCDEG / 60      , 'minute (angle)'           )
ARCSEC   = Unum.unit("''"      , ARCMIN / 60      , 'second (angle)'           )
L        = Unum.unit('L'       , 1E-3 * M**3      , 'liter'                    )
TON      = Unum.unit('t'       , 1E3 * KG         , 'metric ton'               )
NP       = Unum.unit('Np'      , 1                , 'neper'                    )
DECIBEL  = Unum.unit('dB'      , 0                , 'decibel'                  )
EV       = Unum.unit('eV'      , 1.60218E-19 * J  , 'electronvolt'             )
U        = Unum.unit('u'       , 1.66054E-27 * KG , 'unified atomic mass unit' )
UA       = Unum.unit('ua'      , 1.49598E11 * M   , 'astronomical unit'        )
MILE     = Unum.unit('mile'    , 1609.34 * M      , 'statute mile'             )
NMILE    = Unum.unit('nmi'     , 1852 * M         , 'nautical mile'            )
KNOT     = Unum.unit('knot'    , MILE / H         , 'knot'                     )
ARE      = Unum.unit('a'       , 1E2 * M**2       , 'are'                      )
HA       = Unum.unit('ha'      , 1E4 * M**2       , 'hectare'                  )
BAR      = Unum.unit('bar'     , 1E5 * PA         , 'bar'                      )
ANGSTROM = Unum.unit('angstrom', 1E-10 * M        , 'angstrom'                 )
B        = Unum.unit('b'       , 1E-28 * M**2     , 'barn'                     )
CI       = Unum.unit('Ci'      , 3.7E10 * BQ      , 'curie'                    )
R        = Unum.unit('R'       , 2.58E-4 * C / KG , 'roentgen'                 )
REM      = Unum.unit('rem'     , 1E-2 * SV        , 'rem'                      )

# Note : 'rad' defined as 1E-2 Gy as been left because of the
#        name collision with 'rad' as an angle.

del pi
