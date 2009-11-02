"""Provide base and derived SI defines."""
from unum import Unum
unit = Unum.defineUnit

# Base SI units.
M   = unit('m'  , 0, 'meter'   )
KG  = unit('kg' , 0, 'kilogram')
S   = unit('s'  , 0, 'second'  )
A   = unit('A'  , 0, 'ampere'  )
K   = unit('K'  , 0, 'kelvin'  )
MOL = unit('mol', 0, 'mole'    )
CD  = unit('cd' , 0, 'candela' )

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