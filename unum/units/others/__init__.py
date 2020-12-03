"""Define common units that are not SI units.

Source: http://physics.nist.gov/cuu/Units/outside.html
"""
from math import pi
from unum.core import new_unit

from ..si import *

__all = [
    'minutes', 'MIN',
    'h', 'H',
    'd', 'D',
    'deg', 'ARCDEG',
    'arcmin', 'ARCMIN',
    'arcsec', 'ARCSEC',
    'L', 'L',
    't', 'TON',
    'Np', 'NP',
    'dB', 'DECIBEL',
    'eV', 'EV',
    'u', 'U',
    'ua', 'AU',
    'mile', 'MILE',
    'nmile', 'NMILE',
    'knot', 'KNOT',
    'a', 'ARE',
    'ha', 'HA',
    'bar', 'BAR',
    'angstrom', 'ANGSTROM',
    'b', 'B',
    'Ci', 'CI',
    'R', 'R',
    'rem', 'REM',
]

minutes = MIN = new_unit('min', 60 * s, 'minute')
h = H = new_unit('h', 60 * MIN, 'hour')
d = D = new_unit('d', 24 * H, 'day')
deg = ARCDEG = new_unit('deg', pi / 180 * RAD, 'degree (angle)')
arcmin = ARCMIN = new_unit("'", ARCDEG / 60, 'minute (angle)')
arcsec = ARCSEC = new_unit("''", ARCMIN / 60, 'second (angle)')
L = L = new_unit('L', 1E-3 * M ** 3, 'liter')
t = TON = new_unit('t', 1E3 * KG, 'metric ton')
Np = NP = new_unit('Np', 1, 'neper')
dB = DECIBEL = new_unit('dB', 0, 'decibel')
eV = EV = new_unit('eV', 1.60218E-19 * J, 'electronvolt')
u = U = new_unit('u', 1.66054E-27 * KG, 'unified atomic mass unit')
ua = AU = UA = new_unit('ua', 1.49598E11 * M, 'astronomical unit')
mile = MILE = new_unit('mile', 1609.34 * M, 'statute mile')
nmile = NMILE = new_unit('nmi', 1852 * M, 'nautical mile')
knot = KNOT = new_unit('knot', MILE / H, 'knot')
a = ARE = new_unit('a', 1E2 * M ** 2, 'are')
ha = HA = new_unit('ha', 1E4 * M ** 2, 'hectare')
bar = BAR = new_unit('bar', 1E5 * PA, 'bar')
angstrom = ANGSTROM = new_unit('angstrom', 1E-10 * M, 'angstrom')
b = B = new_unit('b', 1E-28 * M ** 2, 'barn')
Ci = CI = new_unit('Ci', 3.7E10 * BQ, 'curie')
R = new_unit('R', 2.58E-4 * C / KG, 'roentgen')
rem = REM = new_unit('rem', 1E-2 * SV, 'rem')
g0 = standard_gravity = new_unit('g0', 9.80665 * m / (s ** 2), 'Standard gravity')

# Note : 'rad' defined as 1E-2 Gy as been left out because it conflits with
# using 'rad' for radians.
