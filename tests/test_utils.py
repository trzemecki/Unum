from __future__ import print_function, absolute_import, division, unicode_literals

import unittest

import unum.exceptions
import unum.utils
from unum.units import *


class ModuleTest(unittest.TestCase):
    def test_AsNumber_OnlyUnumGiven_ReturnValueForCurrentUnit(self):
        value = 2.3 * m

        actual = self.as_number(value)

        self.assertAlmostEqual(2.3, actual)

    def test_AsNumber_OnlyFloatGiven_ReturnValueEqualToGivenFloat(self):
        value = 2.3

        actual = self.as_number(value)

        self.assertAlmostEqual(2.3, value)

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

    as_number = staticmethod(unum.utils.as_number)
