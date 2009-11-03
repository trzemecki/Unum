"""Provide additional common units in addition to the SI units."""
from math import pi
from unum import Unum
from unum.units.si import *
unit = Unum.unit

min = MIN = unit('min', 60 * S, 'minute')
h = H = unit('h', 60 * MIN, 'hour')
d = D = unit('d', 24 * H, 'day')
deg = arcdeg = ARCDEG = unit('deg', pi/180 * RAD, 'degree (angle)')
arcmin = ARCMIN = unit("'", ARCDEG / 60, 'minute (angle)')
arcsec = ARCSEC = unit("''", ARCMIN / 60, 'second (angle)')
liter = L = unit('L', 1E-3 * M**3, 'liter')
t = ton = TON = unit('t', 1E3 * KG, 'metric ton')
Np = NP = unit('Np', 1, 'neper')
dB = decibel = DECIBEL = unit('dB', 0, 'decibel')
eV = EV = unit('eV', 1.60218E-19 * J, 'electronvolt')
u = U = unit('u', 1.66054E-27 * KG, 'unified atomic mass unit')
# While ua is recommended, AU is common in English-speaking countries.
AU = au = UA = ua = unit('ua', 1.49598E11 * M, 'astronomical unit')
mile = MILE = unit('mile', 1609.34 * M, 'statute mile')
nmi = nmile = NMILE = unit('nmi', 1852 * M, 'nautical mile')
knot = KNOT = unit('knot', MILE / H, 'knot')
a = ARE = unit('a', 1E2 * M**2, 'are')
ha = HA = unit('ha', 1E4 * M**2, 'hectare')
bar = BAR = unit('bar', 1E5 * PA, 'bar')
angstrom = ANGSTROM = unit('angstrom', 1E-10 * M, 'angstrom')
b = B = unit('b', 1E-28 * M**2, 'barn')
Ci = CI = unit('Ci', 3.7E10 * BQ, 'curie')
R = unit('R', 2.58E-4 * C / KG, 'roentgen')
rem = REM = unit('rem', 1E-2 * SV, 'rem')

# Note : 'rad' defined as 1E-2 Gy as been left because of the
#        name collision with 'rad' as an angle.

del pi
del unit
