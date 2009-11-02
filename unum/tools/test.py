'''
--------------------------------------------------------------------
file : unum/test/test.py
ver  : 04.00
role : execute test cases for Unum 
--------------------------------------------------------------------

Copyright (C) 2000-2004 Pierre Denis

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
--------------------------------------------------------------------
'''

# if TRACE is True, all the test cases are displayed
# otherwise, only the failing test cases are displayed         
TRACE = False

_testList = (           \
    ( "from unum.units import *"                , "" ),
    ( "from extraunits import *"                , "" ),
    ( "M"                                       , "1.0 [m]" ),
    ( "50 * M"                                  , "50.0 [m]" ),
    ( "25 * S"                                  , "25.0 [s]" ),
    ( "3 * M/S"                                 , "3.0 [m/s]" ),
    ( "1 / (3 * M/S)"                           , "0.333333333333 [s/m]" ),
    ( "25 * M**2"                               , "25.0 [m2]" ),
    ( "(3 * M) * (4 * M)"                       , "12.0 [m2]" ),
    ( "10 * KG*M/S**2"                          , "10.0 [kg.m/s2]" ),
    ( "M / M"                                   , "1.0 []" ),
    ( "(2 * M/S) * (3 * S/M)"                   , "6.0 []" ),
    ( "distance = 50 * M"                       , "" ),
    ( "distance"                                , "50.0 [m]" ),
    ( "volume = distance ** 3"                  , "" ),
    ( "volume"                                  , "125000.0 [m3]" ),
    ( "duration = 25 * S"                       , "" ),
    ( "duration"                                , "25.0 [s]" ),
    ( "speed = distance / duration"             , "" ),
    ( "speed"                                   , "2.0 [m/s]" ),    
    ( "mass = 1.5 * KG"                         , "" ),
    ( "kinetic_energy = (mass * speed**2) / 2"  , "" ),
    ( "kinetic_energy"                          , "3.0 [kg.m2/s2]" ),
    ( "distance + 20*M"                         , "70.0 [m]" ),
    ( "distance**2 + 20 * M**2"                 , "2520.0 [m2]" ),
    ( "speed - 6 * M/S"                         , "-4.0 [m/s]" ),
    ( "distance += 100 * M"                     , "" ),
    ( "distance"                                , "150.0 [m]" ),
    ( "speed *= 2"                              , "" ),
    ( "speed"                                   , "4.0 [m/s]" ),
    ( "distance >= speed * 20 * S"              , "True" ),    
    ( "distance**2 == 20 * M**2"                , "False" ),
    ( "a = 20*M"                                , "" ),
    ( "a += 10*M"                               , "" ),
    ( "a"                                       , "30.0 [m]" ),
    ( "a += 5*CM"                               , "" ),
    ( "a"                                       , "3005.0 [cm]" ),
    ( "a += 2*KM"                               , "" ),
    ( "a"                                       , "203005.0 [cm]" ),
    ( "a = a.as(M)"                             , "" ),
    ( "a"                                       , "2030.05 [m]" ),
    ( "a /= H"                                  , "" ),
    ( "a"                                       , "2030.05 [m/h]" ),
    ( "a *= S"                                  , "" ),
    ( "a"                                       , "0.563902777778 [m]" ),
    ( "a /= KM"                                 , "" ),
    ( "a"                                       , "0.000563902777778 []" ),
    ( "a *= M/S"                                , "" ),
    ( "a"                                       , "0.000563902777778 [m/s]" ),
    ( "a**-1"                                   , "1773.35533608 [s/m]" ),
    ( "a"                                       , "0.000563902777778 [m/s]" ),
    ( "a += KM"                                 , "unum.DimensionError: [m/s] incompatible with [km]" ),
    ( "a += KM/H"                               , "" ),
    ( "a"                                       , "1.00203005 [km/h]" ),
    ( "a /= KM/H"                               , "" ),
    ( "a"                                       , "1.00203005 []" ),    
    ( "distance + 3 * KG"                       , "unum.DimensionError: [m] incompatible with [kg]" ),
    ( "distance**2 - 20*M"                      , "unum.DimensionError: [m2] incompatible with [m]" ),
    ( "distance + 125"                          , "unum.DimensionError: [m] incompatible with []" ),    
    ( "distance + speed"                        , "unum.DimensionError: [m] incompatible with [m/s]" ),
    ( "distance < speed"                        , "unum.DimensionError: [m] incompatible with [m/s]" ),
    ( "speed += 20"                             , "unum.DimensionError: [m/s] incompatible with []" ),     
    ( "duration == 15 * KG"                     , "unum.DimensionError: [s] incompatible with [kg]" ),
    ( "M ** KG"                                 , "unum.DimensionError: unit [kg] unexpected" ),
    ( "M ** (M/S)"                              , "unum.DimensionError: unit [m/s] unexpected" ),
    ( "M ** (duration/S)"                       , "1.0 [m25.0]" ),
    ( "2 ** (duration /S)"                      , "33554432.0 []" ),
    ( "M ** (M/CM)"                             , "1.0 [m100.0]" ),
    ( "M ** (CM/M)"                             , "1.0 [m0.01]" ),        
    ( "20 * KM + 500 * M"                       , "20.5 [km]" ),
    ( "M / CM"                                  , "100.0 []" ),
    ( "4 * M**2 + 25 * CM**2"                   , "40025.0 [cm2]" ),
    ( "M**2 / CM**2"                            , "10000.0 []" ),
    ( "150 * KM/H + 200 * M/S"                  , "870.0 [km/h]" ),
    ( "3*H + 20*MIN + 15*S"                     , "3.3375 [h]" ),
    ( "1 * KG == 1000 * G"                      , "True" ),
    ( "20 * S >= 3 * H + 15 * MIN"              , "False" ),
    ( "(15 * KM).as(M)"                         , "15000.0 [m]" ),
    ( "(20 * KM + 500 * M).as(CM)"              , "2050000.0 [cm]" ),
    ( "(4 * M**2).as(CM**2)"                    , "40000.0 [cm2]" ),
    ( "(80 * KM/H).as(MILE/H)"                  , "49.709818932 [mile/h]" ),
    ( "(3*H + 20*MIN + 15*S).as(S)"             , "12015.0 [s]" ),
    ( "energy = 3 * KG*(M/S)**2"                , "" ),
    ( "energy"                                  , "3.0 [kg.m2/s2]" ),
    ( "energy.as(J)"                            , "3.0 [J]" ),
    ( "energy.as(KCAL)"                         , "0.000716674629718 [kcal]" ),
    ( "energy.as(KW * H)"                       , "8.33333333333e-007 [h.kW]" ),
    ( "energy"                                  , "3.0 [kg.m2/s2]" ),    
    ( "energy = energy.as(CAL)"                 , "" ),
    ( "energy"                                  , "0.716674629718 [cal]" ),
    ( "M.as(KG)"                                , "unum.DimensionError: [m] incompatible with [kg]" ),
    ( "energy.as(KW)"                           , "unum.DimensionError: [cal] incompatible with [kW]" ),
    ( "apple_mass = 3.14159 * KG"               , "" ),
    ( "c = 300000 * KM/S"                       , "" ),
    ( "apple_energy = c * apple_mass**2"        , "" ),
    ( "apple_energy"                            , "2960876.31843 [kg2.km/s]" ),
    ( "apple_energy.as(KCAL)"                   , "unum.DimensionError: [kg2.km/s] incompatible with [kcal]" ),
    ( "apple_energy = apple_mass * c**2"        , "" ),
    ( "apple_energy.as(KCAL)"                   , "6.75449354993e+013 [kcal]" ),
    ( "apple_energy.as(CAL)"                    , "6.75449354993e+016 [cal]" ),
    ( "apple_energy.as(KJ)"                     , "2.827431e+014 [kJ]" ),
    ( "apple_energy.as(J)"                      , "2.827431e+017 [J]" ),
    ( "apple_energy.as(N*M)"                    , "2.827431e+017 [N.m]" ),
    ( "1e15*G*CM/H**2 + 100*N"                  , "871.604938272 [N]" ),
    ( "5*PA - N/CM**2"                          , "-9995.0 [Pa]" ),
    ( "20*KM+300*M+45*CM"                       , "20.30045 [km]" ),
    ( "(20*KM+300*M+45*CM)/(2*H+30*MIN)"        , "8.12018 [km/h]" ),
    ( "(30*KM*M*CM).as(L)"                      , "300000.0 [L]" ),
    ( "L.as(KM*M*CM)"                           , "0.0001 [cm.km.m]" ),
    ( "KWH.as(J)"                               , "3600000.0 [J]" ),
    ( "KWH.as(KJ)"                              , "3600.0 [kJ]" ),
    ( "KWH + 0*J"                               , "1.0 [kWh]" ),
    ( "KWH + 0*KJ"                              , "1.0 [kWh]" ),    
    ( "length = 1j * M"                         , "" ),
    ( "length"                                  , "1j [m]" ),    
    ( "length**2"                               , "(-1+0j) [m2]" ),
    ( "M / CM"                                  , "100.0 []" ),
    ( "PA * M**2"                               , "1.0 [N]" ),
    ( "PA * CM**2"                              , "0.0001 [N]" ),
    ( "from math import log10,sin,cos,pi"       , "" ),
    ( "log10(M/CM)"                             , "2.0" ),
    ( "f = 440*HZ"                              , "" ),
    ( "sin(f)"                                  , "unum.DimensionError: unit [Hz] unexpected" ),
    ( "dt = 0.1 * S"                            , "" ),
    ( "sin(f*dt*2*pi)"                          , "-3.9198245344e-014" ),
    ( "(2*pi*RAD).as(ARCDEG)"                   , "360.0 [deg]"),
    ( "RAD"                                     , "1.0 [rad]" ),
    ( "ARCDEG"                                  , "1.0 [deg]" ),
    ( "pi*RAD == 180*ARCDEG"                    , "True" ),
    ( "180*ARCDEG"                              , "180.0 [deg]" ),
    ( "(180*ARCDEG).as(RAD)"                    , "3.14159265359 [rad]" ),        
    ( "180*ARCDEG + 0"                          , "3.14159265359 []" ),    
    ( "cos(180*ARCDEG)"                         , "-1.0"),
    ( "cos(pi*RAD)"                             , "-1.0"),
    ( "log10(RAD)"                              , "0.0" ),
    ( "log10(ARCDEG)"                           , "-1.75812263241" ),
    ( "log10(NP)"                               , "0.0" ),
    ( "L/KM"                                    , "1e-006 [m2]" ),
    ( "i = 20 * A"                              , "" ),    
    ( "r = 100 * OHM"                           , "" ),
    ( "i"                                       , "20.0 [A]" ),    
    ( "r"                                       , "100.0 [ohm]" ),
    ( "u = r*i"                                 , "" ),    
    ( "u"                                       , "2000.0 [V]" ),    
    ( "(20*M).asNumber()"                       , "20.0" ),
    ( "(20*M).asNumber(M)"                      , "20.0" ),
    ( "(20*M/S).asNumber(M)"                    , "unum.DimensionError: [m/s] incompatible with [m]" ),
    ( "(20*M/S).asNumber(KM/H)"                 , "72.0" ),
    ( "(M/CM).asNumber()"                       , "100.0" ),        
    ( "(M/CM).asNumber(1)"                      , "100.0" ),
    ( "20*L/(100*KM)"                           , "2e-007 [m2]" ),
    ( "(20*L/(100*KM)).fix()"                   , "0.2 [L/km]" ),
    ( "CYCLE = Unum.unit('cycle',2*pi*RAD)"     , "" ),
    ( "w = (CYCLE/D).fix()"                     , "" ),
    ( "w"                                       , "1.0 [cycle/d]" ),    
    ( "w.as(RAD/S)"                             , "7.27220521664e-005 [rad/s]" ),     
    ( "w.as(ARCDEG/D)"                          , "360.0 [deg/d]" ),
    ( "w.as(ARCDEG/H)"                          , "15.0 [deg/h]" ),    
    ( "r = 6000*KM"                             , "" ),
    ( "w*r"                                     , "37699.1118431 [km/d]" ),
    ( "(w*r).as(KM/H)"                          , "1570.79632679 [km/h]" ),
    ( "(w*r*cos(60*ARCDEG)).as(KM/H)"           , "785.398163397 [km/h]" ),
    ( "EURO = Unum.unit('Euro')"                , ""),
    ( "USD = Unum.unit('$', 1.2545*EURO)"       , ""),
    ( "tariff = 2.5 * USD/KWH"                  , "" ),
    ( "tariff"                                  , "2.5 [$/kWh]" ),
    ( "duration = 2*H + 20*MIN"                 , "" ),
    ( "duration"                                , "2.33333333333 [h]" ),
    ( "power = 60*W"                            , "" ),
    ( "price = power * duration * tariff"       , "" ),
    ( "price"                                   , "0.35 [$]" ),
    ( "price.as(EURO)"                          , "0.439075 [Euro]" ),
    ( "tariff.as(USD/(KG*M**2/S**2))"           , "6.94444444444e-007 [$.s2/kg.m2]" ),
    ( "Unum.AUTO_NORM = False"                  , "" ),
    ( "M / CM"                                  , "1.0 [m/cm]" ),
    ( "PA * M**2"                               , "1.0 [Pa.m2]" ),
    ( "PA * CM**2"                              , "1.0 [Pa.cm2]" ),
    ( "(PA * M**2).normalize()"                 , "1.0 [N]" ),
    ( "(M / CM).normalize()"                    , "100.0 []" ),
    ( "force = PA * M**2"                       , "" ),
    ( "force"                                   , "1.0 [Pa.m2]" ),
    ( "force.normalize()"                       , "1.0 [N]" ),
    ( "force"                                   , "1.0 [N]" ),
    ( "CM.converted()"                          , "0.01 [m]" ),
    ( "N.converted()"                           , "1.0 [kg.m/s2]" ),
    ( "W.converted()"                           , "1.0 [J/s]" ),
    ( "(J/S).converted()"                       , "unum.UnumError: 1.0 [J/s] has no conversion" ),
    ( "M.converted()"                           , "unum.UnumError: 1.0 [m] has no conversion" ),
    ( "(CM**2).converted()"                     , "0.0001 [m2]" ),
    ( "(PA**2).converted()"                     , "1.0 [N2/m4]" ),
    ( "(1/N).converted()"                       , "1.0 [s2/kg.m]" ),
    ( "(1/N**2).converted()"                    , "1.0 [s4/kg2.m2]" ),
    ( "Unum.AUTO_NORM = True"                   , "" ),
    ( "Unum.UNIT_SEP = ' '"                     , "" ),
    ( "Unum.UNIT_DIV_SEP = None"                , "" ),
    ( "Unum.UNIT_FORMAT = '%s'"                 , "" ),
    ( "Unum.UNIT_HIDE_EMPTY = 1"                , "" ),
    ( "M"                                       , "1.0 m" ),
    ( "25 * KG*M/S**2"                          , "25.0 kg m s-2" ),
    ( "CAL / J"                                 , "4.186 " ),
    ( "Unum.UNIT_SEP = '.'"                     , "" ),
    ( "Unum.UNIT_DIV_SEP = '/'"                 , "" ),
    ( "Unum.UNIT_FORMAT = '[%s]'"               , "" ),
    ( "Unum.UNIT_HIDE_EMPTY = 0"                , "" ),    
    ( "STUFF = Unum.unit('stuff') #0"              , "" ),
    ( "KSTUFF = Unum.unit('kilostuff' , 1000.0 * STUFF)"       , "" ),
    ( "MSTUFF = Unum.unit('millistuff' ,  0.001 * STUFF)"      , "" ),
    ( "SPS = Unum.unit('sps' , STUFF / S)"      , "" ),
    ( "20 * STUFF"                              , "20.0 [stuff]" ),
    ( "500 * MSTUFF"                            , "500.0 [millistuff]" ),
    ( "(500 * MSTUFF).as(STUFF)"                , "0.5 [stuff]" ),
    ( "2 * KSTUFF + 3 * STUFF + 4 * MSTUFF"     , "2.003004 [kilostuff]" ),
    ( "3 * STUFF + 20 * S"                      , "unum.DimensionError: [stuff] incompatible with [s]" ),
    ( "5 * SPS * 10*S"                          , "50.0 [stuff]" ),
    ( "(50 * KSTUFF / S).as(SPS)"               , "50000.0 [sps]" ),
    ( "(SPS).as(MSTUFF/S)"                      , "1000.0 [millistuff/s]" ),
    ( "DIST = Unum.unit('1e-25 M',1e-25*M)"     , "" ),
    ( "20 * DIST"                               , "20.0 [1e-25 M]" ),
    ( "CM.as(DIST)"                             , "1e+023 [1e-25 M]" ),
    ( "Unum.reset()"                            , "None" ),
    ( "STUFF = Unum.unit('stuff') #1"              , "" ),
    ( "KSTUFF = 1000.0 * STUFF"                 , "" ),
    ( "MSTUFF = 0.001 * STUFF"                  , "" ),
    ( "S = Unum.unit('s')"                      , "" ),    
    ( "SPS = STUFF / S"                         , "" ),
    ( "25 * KSTUFF"                             , "25000.0 [stuff]" ),
    ( "(125 * STUFF).as(KSTUFF)"                , "unum.UnumError: 1000.0 [stuff] not a basic unit" ),
    ( "Unum.reset()"                            , "None" ),
    ( "STUFF = Unum.unit('stuff') #2"           , "" ),
    ( "KSTUFF = Unum.unit('kilostuff')"         , "" ),
    ( "MSTUFF = Unum.unit('millistuff')"        , "" ),    
    ( "SPS = Unum.unit('sps')"                  , "" ),
    ( "20 * KSTUFF + 15 * STUFF"                , "unum.DimensionError: [kilostuff] incompatible with [stuff]" ),
    ( "(20*KSTUFF).as(STUFF)"                   , "unum.DimensionError: [kilostuff] incompatible with [stuff]" ),
    ( "KSTUFF2STUFF = 1000.0 * STUFF / KSTUFF"  , "" ),
    ( "STUFF2KSTUFF = 1 / KSTUFF2STUFF"         , "" ),
    ( "20 * KSTUFF * KSTUFF2STUFF + 15 * STUFF" , "20015.0 [stuff]" ),
    ( "20 * KSTUFF + 15 * STUFF * STUFF2KSTUFF" , "20.015 [kilostuff]" ),    
    )

from sys import exc_info

from unum import Unum

_globalDict = globals()
nbSuccesses = 0
nbFailures = 0
print("Starting Unum Automatic Tests ...")
for unumExpression, expectedResult in _testList:
    try: 
       try:
          actualResult = str(eval(unumExpression,_globalDict))
       except (Unum.DimensionError,Unum.UnumError) as err:
          actualResult = "%s: %s" % (err.__class__,err)
    except:
       try:
          exec(unumExpression, _globalDict)
          actualResult = ""
       except (Unum.DimensionError,Unum.UnumError) as err:   
          actualResult = "%s: %s" % (err.__class__,err)
       except:
          actualResult = "%s: %s" % exc_info()[:2]    
    # the following condition allows to cope with Python versions earlier to 2.3
    error = actualResult != expectedResult \
       and not (actualResult == '1' and expectedResult == 'True') \
       and not (actualResult == '0' and expectedResult == 'False')
    if error:
       nbFailures += 1        
    else:    
       nbSuccesses += 1
    if TRACE or error:
       print(">>> %s" % unumExpression)
       if actualResult:
          print(actualResult)
    if error:
       print("#### TEST ERROR")
       print("####   expected : '%s'" % expectedResult)
       print("####   actual   : '%s'" % actualResult)

print("End      Unum Automatic Tests")
print(80 * '-')
print("Number of failing tests    : %4d" % nbFailures)
print("Number of successful tests : %4d" % nbSuccesses)
print("Total number of tests      : %4d" % (nbFailures + nbSuccesses))
print(80 * '-')
