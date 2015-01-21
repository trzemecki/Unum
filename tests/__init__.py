# TODO: write simple regression test suite.
# Main purpose is to be able to setup.py test on various Python installations.

import unum
import math
from unum.units import *
import nose
from nose.tools import *

# Test core arithmetic
def test_addition():
    print (mg)
    print (mg + mg)
    print (2*mg)
    assert mg + mg == 2*mg
    assert_raises(unum.IncompatibleUnitsError, lambda: mg+ms)

def test_unitless():
    assert_almost_equal(math.log10(1000*m/m), 3.0)
    assert_raises(unum.ShouldBeUnitlessError, lambda: math.cos(2*mA)) 

def test_name_conflict():
    MY_UNIT = unum.Unum.unit("myunit", 0, "my_new_unit") #@UnusedVariable
    assert_raises(unum.NameConflictError, unum.Unum.unit,
                  "myunit", 0, "my_new_unit")

def test_nonbasic():
    assert kg.asNumber(g) == 1000
    assert_raises(unum.NonBasicUnitError, lambda: kg.asNumber(2*g))

def test_unit_conversion():
    assert N*m == J
    assert N*m/s == W
    assert (N*km/s).asUnit(W) == 1000*W

def test_fractions():
    try: from fractions import Fraction
    except ImportError: raise nose.SkipTest
    x = Fraction(1, 2) * km
    y = Fraction("1/3") * km
    assert x+y == (Fraction(5, 6) * km)
    assert (x+y)**2 == (Fraction(25, 36)*km**2)
    assert x == (km * Fraction(1,2))

def test_numpy():
    try: from numpy import array, ndarray
    except ImportError: raise nose.SkipTest
    
    # Left multiply: array of Unum
    arr = array([2,3,4]) * ns
    assert isinstance(arr, ndarray)
    assert isinstance(arr[0], unum.Unum)
    
    # Right multiply: Unum containing array
    arr = ns * array([2,3,4])
    assert isinstance(arr, unum.Unum)
    assert isinstance(arr.asNumber(), ndarray)
    
    # Helper function: like right multiply
    arr = unum.uarray([2,3,4])
    assert isinstance(arr, unum.Unum)
    assert isinstance(arr.asNumber(), ndarray)
   
def test_case_sensitive():
    # Test fix for issue #2 with seconds/Siemens confusion
    assert_raises(unum.IncompatibleUnitsError, lambda: S.asUnit(h))
    assert h.asUnit(s) == 3600 * s
