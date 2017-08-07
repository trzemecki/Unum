from ..si.base import *
from ..si.derived import *
from unum import new_unit


__all__ = [
    'kN', 'MN', 'kNm', 'MNm', 'kNcm', 'kG', 'T', 'kPa', 'MPa', 'GPa'
]

kN = new_unit('kN', N * 1e3, 'kilonewton')
MN = new_unit('MN', N * 1e6, 'meganewton')

gravity = 9.81 * m / s ** 2

gf = new_unit('gf', g * gravity, 'gram force')
kgf = kG = new_unit('kgf', kg * gravity, 'kilogram force')
tf = new_unit('tf', kg * 10e3 * gravity, 'tone force')

kPa = new_unit('kPa', Pa * 1e3, 'kilopascal')
MPa = new_unit('MPa', Pa * 1e6, 'megapascal')
GPa = new_unit('GPa', Pa * 1e9, 'gigapascal')

kNm = new_unit('kNm', kN * m, 'kilonewton meter')
MNm = new_unit('MNm', MN * m, 'meganewton meter')
kNcm = new_unit('kNcm', kN * cm, 'kilonewton centimeter')
