"""Provide base and derived SI defines."""
import sys
from unum import Unum
unit = Unum.unit

# Base SI units.
kg = None
m = M = unit('m'  , 0, 'meter'   )
g = G = unit('g' , 0, 'gram'     )
s = S = unit('s'  , 0, 'second'  )
A = unit('A'  , 0, 'ampere'  )
K = unit('K'  , 0, 'kelvin'  )
mol = MOL = unit('mol', 0, 'mole'    )
cd = CD = unit('cd' , 0, 'candela' )

# TODO: would be nice to have a helper to auto-generate prefixed units.
# Prefixed versions of base SI units.
prefixes = [
    (10**24, 'yotta', 'Y'),
    (10**21, 'zetta', 'Z'),
    (10**18, 'exa', 'E'),
    (10**15, 'peta', 'P'),
    (10**12, 'tera', 'T'),
    (10**9, 'giga', 'G'),
    (10**6, 'mega', 'M'),
    (10**3, 'kilo', 'k'),
    (10**2, 'hecto', 'h'),
    (10**1, 'deka', 'da'),
    
    (10**-24, 'yocto', 'y'),
    (10**-21, 'zepto', 'z'),
    (10**-18, 'atto', 'a'),
    (10**-15, 'femto', 'f'),
    (10**-12, 'pico', 'p'),
    (10**-9, 'nano', 'n'),
    (10**-6, 'micro', 'u'),
    (10**-3, 'milli', 'm'),
    (10**-2, 'centi', 'c'),
    (10**-1, 'deka', 'd'),    
]

this_module = sys.modules[__name__]
for base in ('m', 'g', 's', 'A', 'K', 'mol', 'cd'):
    
    base_unit = getattr(this_module, base)
    for multiplier, name, symbol in prefixes:
        prefixed_unit = unit(symbol+base, multiplier * base_unit, 
                             name+base_unit._unitTable[base][2])
        setattr(this_module, symbol+base, prefixed_unit)
KG = kg                


# Derived SI units.
RAD     = unit('rad'  , M / M         , 'radian'        )
SR      = unit('sr'   , M**2 / M**2   , 'steradian'     )
HZ      = unit('Hz'   , 1 / S         , 'hertz'         )
N       = unit('N'    , M*KG / S**2   , 'newton'        )
PA      = unit('Pa'   , N / M**2      , 'pascal'        )
J       = unit('J'    , N*M           , 'joule'         )
W       = unit('W'    , J / S         , 'watt'          )
C       = unit('C'    , S * A         , 'coulomb'       )
V       = unit('V'    , W / A         , 'volt'          )
F       = unit('F'    , C / V         , 'farad'         )
OHM     = unit('ohm'  , V / A         , 'ohm'           )
SIEMENS = unit('S'    , A / V         , 'siemens'       )
WB      = unit('Wb'   , V * S         , 'weber'         )
T       = unit('T'    , WB / M**2     , 'tesla'         )
HENRY   = unit('H'    , WB / A        , 'henry'         )
LM      = unit('lm'   , CD * SR       , 'lumen'         )
LX      = unit('lx'   , LM / M**2     , 'lux'           )
BQ      = unit('Bq'   , 1 / S         , 'becquerel'     )
GY      = unit('Gy'   , J / KG        , 'gray'          )
SV      = unit('Sv'   , J / KG        , 'sievert'       )
KAT     = unit('kat'  , MOL / S       , 'katal'         )

# WARNING: Conversion between degrees Celsius is problematic since
# for relative temperatures 1 deg C = 1 K but this is not true
# for absolute temperatures. In Unum we use relative temperatures.
CELSIUS = unit('deg C', K             , 'degree Celsius')

del unit