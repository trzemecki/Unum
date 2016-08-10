from ..si.base import *
from ..si.derived import *
from unum import unit


__all__ = [
    'kN', 'MN', 'kNm', 'MNm', 'kNcm', 'kG', 'T', 'GPa'
]

kN = unit('kN', N * 1e3, 'kilonewton')
MN = unit('MN', N * 1e6, 'meganewton')

gravity = 9.81 * m / s ** 2

gf = unit('gf', g * gravity, 'gram force')
kgf = kG = unit('kgf', kg * gravity, 'kilogram force')
tf = unit('tf', kg * 10e3 * gravity, 'tone force')

kPa = unit('kPa', Pa * 1e3, 'kilopascal')
MPa = unit('MPa', Pa * 1e6, 'megapascal')
GPa = unit('GPa', Pa * 1e9, 'gigapascal')

kNm = unit('kNm', kN * m, 'kilonewton meter')
MNm = unit('MNm', MN * m, 'meganewton meter')
kNcm = unit('kNcm', kN * cm, 'kilonewton centimeter')
