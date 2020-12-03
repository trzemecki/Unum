"""Define the SI derived units.

Source: http://physics.nist.gov/cuu/Units/units.html
"""

from .base import *
from unum.core import new_unit

__all__ = [
    "rad",  "RAD",
    "sr",  "SR",
    "Hz",  "HZ",
    "N",
    "Pa",  "PA",
    "J",
    "W",
    "C",
    "V",
    "F",
    "ohm",  "OHM",
    "S",  "SIEMENS",
    "Wb",  "WB",
    "T",
    "H",  "HENRY",
    "celsius",  "CELSIUS",
    "lm",  "LM",
    "lx",  "LX",
    "Bq",  "BQ",
    "Gy",  "GY",
    "Sv",  "SV",
    "kat",  "KAT",
]

rad = RAD = new_unit('rad', M / M, 'radian')
sr = SR = new_unit('sr', M ** 2 / M ** 2, 'steradian')
Hz = HZ = new_unit('Hz', 1 / s, 'hertz')
N = new_unit('N', M * KG / s ** 2, 'newton')
Pa = PA = new_unit('Pa', N / M ** 2, 'pascal')
J = new_unit('J', N * M, 'joule')
W = new_unit('W', J / s, 'watt')
C = new_unit('C', s * A, 'coulomb')
V = new_unit('V', W / A, 'volt')
F = new_unit('F', C / V, 'farad')
ohm = OHM = new_unit('ohm', V / A, 'ohm')
S = SIEMENS = new_unit('S', A / V, 'siemens')
Wb = WB = new_unit('Wb', V * s, 'weber')
T = new_unit('T', WB / M ** 2, 'tesla')
H = HENRY = new_unit('H', WB / A, 'henry')
# warning : conversion assumes relative temperatures
celsius = CELSIUS = new_unit('deg C', K, 'degree Celsius')
lm = LM = new_unit('lm', CD * SR, 'lumen')
lx = LX = new_unit('lx', LM / M ** 2, 'lux')
Bq = BQ = new_unit('Bq', 1 / s, 'becquerel')
Gy = GY = new_unit('Gy', J / KG, 'gray')
Sv = SV = new_unit('Sv', J / KG, 'sievert')
kat = KAT = new_unit('kat', MOL / s, 'katal')


