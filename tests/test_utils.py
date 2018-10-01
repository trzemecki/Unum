from __future__ import print_function, absolute_import, division, unicode_literals

import unittest

import numpy

import unum.exceptions
import unum.utils
from unum.units import *


class ModuleTest(unittest.TestCase):
    def test_Uarray_Always_ReturnUnumWithNumpyArrayValue(self):
        result = self.uarray([2, 3, 4])

        self.assertIsInstance(result, unum.Unum)
        self.assertIsInstance(result.number(), numpy.ndarray)

    def test_AsUnum_OnlyFloatValueGiven_ReturnUnumWithNoUnit(self):
        value = 12.3

        actual = self.as_unum(value)

        actual.match_units(unum.Unum(1))

    def test_AsUnum_OnlyUnumValueGiven_ReturnGivenUnum(self):
        value = 12.3 * m

        actual = self.as_unum(value)

        self.assertIs(actual, value)

    def test_AsUnum_FloatValueAndUnitGiven_ReturnUnumWithGivenNumberAndUnit(self):
        value = 12.3

        actual = self.as_unum(value, m)

        self.assertEqual(m, actual.unit())

    def test_AsUnum_FloatWithNotBasicUnitGiven_Throws(self):
        value = 12.3

        with self.assertRaises(unum.exceptions.NonBasicUnitError):
            _ = self.as_unum(value, 2 * m)

    def test_AsUnum_UnumWithCompatibleUnit_ReturnUnumWithCastedUnit(self):
        value = 12.3 * m

        actual = self.as_unum(value, cm)

        self.assertEqual(actual, value)
        self.assertAlmostEqual(1230, actual.number(), delta=0.1)

    def test_AsUnum_UnumWithNotCompatibleUnit_Throws(self):
        value = 12.3 * m

        with self.assertRaises(unum.exceptions.IncompatibleUnitsError):
            _ = self.as_unum(value, Pa)

    def test_AsUnit_FloatGiven_ReturnUnitlessUnum(self):
        value = 12.3

        actual = self.as_unit(value)

        self.assertEqual(unitless, actual)

    def test_AsUnit_UnumGiven_ReturnUnumUnit(self):
        value = 12.3 * m

        actual = self.as_unit(value)

        self.assertEqual(m, actual)

    def test_AsNumber_OnlyUnumGiven_ReturnValueForCurrentUnit(self):
        value = 2.3 * m

        actual = self.as_number(value)

        self.assertAlmostEqual(2.3, actual)

    def test_AsNumber_OnlyFloatGiven_ReturnValueEqualToGivenFloat(self):
        value = 2.3

        actual = self.as_number(value)

        self.assertAlmostEqual(2.3, actual)

    def test_AsNumber_UnumWithCurrentUnit_ReturnUnumValue(self):
        value = 2.3 * m

        actual = self.as_number(value, m)

        self.assertAlmostEqual(2.3, actual)

    def test_AsNumber_UnumWithDifferentUnit_ReturnUnumValueWithAfterCastingToOtherUnit(self):
        value = 2.3 * m

        actual = self.as_number(value, cm)

        self.assertAlmostEqual(230., actual)

    def test_AsNumber_FloatWithUnit_ReturnGivenFloat(self):
        value = 2.3

        actual = self.as_number(value, m)

        self.assertAlmostEqual(2.3, actual)

    def test_AsNumber_UnumWithNotCompatibleUnit_Throws(self):
        value = 2.3 * m

        with self.assertRaises(unum.exceptions.IncompatibleUnitsError):
            _ = self.as_number(value, Pa)

    def test_AsNumber_UnumWith2Units_ReturnValueAfterCastingToSecond(self):
        value = 2.3 * m

        actual = self.as_number(value, mm, cm)

        self.assertAlmostEqual(230., actual)

    def test_AsNumber_UnumWith2UnitsWhichFirstIsIncompatible_Throws(self):
        value = 2.3 * m

        with self.assertRaises(unum.exceptions.IncompatibleUnitsError):
            _ = self.as_number(value, Pa, cm)

    def test_AsNumber_UnumWith2UnitWhichSecondIsIncompatible_Throws(self):
        value = 2.3 * m

        with self.assertRaises(unum.exceptions.IncompatibleUnitsError):
            _ = self.as_number(value, mm, Pa)

    def test_AsNumber_UnumWith2IncompatibleUnits_Throws(self):
        value = 2.3 * m

        with self.assertRaises(unum.exceptions.IncompatibleUnitsError):
            _ = self.as_number(value, Pa, MPa)

    def test_AsNumber_FloatWith2CompatibleUnits_ReturnValueMultipliedByConversionCoefficientFromFirstUnitToSecond(self):
        value = 2.3

        actual = self.as_number(value, m, cm)

        self.assertAlmostEqual(230., actual)

    def test_AsNumber_FloatWith2IncompatibleUnits_Thorws(self):
        value = 2.3

        with self.assertRaises(unum.exceptions.IncompatibleUnitsError):
            _ = self.as_number(value, Pa, m)

    def test_AsNumber_PlacesGiven_ReturnRoundedValue(self):
        value = 125.23 * mm

        actual = str(self.as_number(value, m, places=2))

        self.assertEqual('0.13', actual)

    def test_Encode_FloatGiven_ReturnGivenValue(self):
        value = 12.3

        actual = self.encode(value)

        self.assertAlmostEqual(12.3, actual)

    def test_Decode_FloatGiven_ReturnGivenValue(self):
        value = 12.3

        actual = self.decode(value)

        self.assertAlmostEqual(12.3, actual)

    def test_Encode_UnumGiven_ReturnEncodedUnum(self):
        value = 12.3 * m

        actual = self.encode(value)

        self.assertIsNotNone(actual)

    def test_Decode_EncodedUnumGiven_ReturnUnumEqualToValueBeforeEncoding(self):
        value = 123.3 * m
        encoded = self.encode(value)
        value *= 3 * s  # prevent to storing any encoded value info

        actual = self.decode(encoded)

        self.assertAlmostEqual(123.3, actual.number(m))

    uarray = staticmethod(unum.utils.uarray)
    as_unum = staticmethod(unum.utils.as_unum)
    as_unit = staticmethod(unum.utils.as_unit)
    as_number = staticmethod(unum.utils.as_number)
    decode = staticmethod(unum.utils.decode)
    encode = staticmethod(unum.utils.encode)
