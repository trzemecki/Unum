"""Provide base and derived SI Unum.units."""
from unum import Unum

# Base SI units.
M   = Unum.unit('m'  , 0, 'meter'   )
KG  = Unum.unit('kg' , 0, 'kilogram')
S   = Unum.unit('s'  , 0, 'second'  )
A   = Unum.unit('A'  , 0, 'ampere'  )
K   = Unum.unit('K'  , 0, 'kelvin'  )
MOL = Unum.unit('mol', 0, 'mole'    )
CD  = Unum.unit('cd' , 0, 'candela' )

# Derived SI units.
RAD     = Unum.unit('rad'  , M / M         , 'radian'        )
SR      = Unum.unit('sr'   , M**2 / M**2   , 'steradian'     )
HZ      = Unum.unit('Hz'   , 1 / S         , 'hertz'         )
N       = Unum.unit('N'    , M*KG / S**2   , 'newton'        )
PA      = Unum.unit('Pa'   , N / M**2      , 'pascal'        )
J       = Unum.unit('J'    , N*M           , 'joule'         )
W       = Unum.unit('W'    , J / S         , 'watt'          )
C       = Unum.unit('C'    , S * A         , 'coulomb'       )
V       = Unum.unit('V'    , W / A         , 'volt'          )
F       = Unum.unit('F'    , C / V         , 'farad'         )
OHM     = Unum.unit('ohm'  , V / A         , 'ohm'           )
SIEMENS = Unum.unit('S'    , A / V         , 'siemens'       )
WB      = Unum.unit('Wb'   , V * S         , 'weber'         )
T       = Unum.unit('T'    , WB / M**2     , 'tesla'         )
HENRY   = Unum.unit('H'    , WB / A        , 'henry'         )
LM      = Unum.unit('lm'   , CD * SR       , 'lumen'         )
LX      = Unum.unit('lx'   , LM / M**2     , 'lux'           )
BQ      = Unum.unit('Bq'   , 1 / S         , 'becquerel'     )
GY      = Unum.unit('Gy'   , J / KG        , 'gray'          )
SV      = Unum.unit('Sv'   , J / KG        , 'sievert'       )
KAT     = Unum.unit('kat'  , MOL / S       , 'katal'         )

# WARNING: Conversion between degrees Celsius is problematic since
# for relative temperatures 1 deg C = 1 K but this is not true
# for absolute temperatures. In Unum we use relative temperatures.
CELSIUS = Unum.unit('deg C', K             , 'degree Celsius')