from __future__ import unicode_literals, absolute_import

import math
import unittest
from fractions import Fraction

import numpy

import unum
from unum.units import *
from unum.utils import as_unum


class UnumTest(unittest.TestCase):
    def test_Addition_UnitToItself_ReturnDoubleUnitNumber(self):
        result = mg + mg

        self.assertEqual(2 * mg, result)

    def test_Addition_UnitsNotMath_Throws(self):
        with self.assertRaises(unum.IncompatibleUnitsError):
            _ = mg + ms

    def test_MathFunction_UnitlessArgument_ReturnUnitlessNumber(self):
        self.assertAlmostEqual(math.log10(1000 * m / m), 3.0, places=3)

    def test_MathFunction_NotUnitlessArgument_Throws(self):
        with self.assertRaises(unum.ShouldBeUnitlessError):
            math.cos(2 * mA)

    def test_NewUnit_NameConflict_Throws(self):
        unum.new_unit("a_unit", 0, "my_new_unit")

        with self.assertRaises(unum.NameConflictError):
            unum.new_unit("a_unit", 0, "my_new_unit")

    def test_Number_Kg_to_g_Return1000(self):
        result = kg.number(g)

        self.assertEqual(1000, result)

    def test_Number_ToNotBasicUnit_Throws(self):
        with self.assertRaises(unum.NonBasicUnitError):
            kg.number(2 * g)

    def test_Equals_SI_J_and_J_ReturnTrue(self):
        self.assertEqual(J, N * m)

    def test_Equals_SI_W_and_W_ReturnTrue(self):
        self.assertEqual(W, N * m / s)

    def test_AsUnit_NoneSIUnitToW_ReturnWTimesRatio(self):
        result = (N * km / s).cast_unit(W)

        self.assertEqual(1000 * W, result)

    def test_CastUnit_UnitNotMatch_Throws(self):
        with self.assertRaises(unum.IncompatibleUnitsError):
            S.cast_unit(h)

    def test_CastUnit_HoursToSeconds_Return3600s(self):
        result = h.cast_unit(s)

        self.assertEqual(3600 * s, result)

    def test_Addition_Fractions_ReturnFractionWithUnit(self):
        x = Fraction(1, 2) * km
        y = Fraction("1/3") * km

        result = x + y

        self.assertEqual(Fraction(5, 6) * km, result)

    def test_Exponentiation_FractionSquared_ReturnValueWithSquaredUnit(self):
        fraction = Fraction(5, 6) * km

        result = fraction ** 2

        self.assertEqual(Fraction(25, 36) * km ** 2, result)

    def test_Multiplying_UnitByFraction_ReturnFractionWithUnit(self):
        result = km * Fraction(1, 2)

        self.assertEqual(Fraction(1, 2) * km, result)

    def test_Multiplying_NumpyArrayByUnit_ReturnNumpyArrayWithNumbersWithUnit(self):
        result = numpy.array([2, 3, 4]) * ns

        self.assertIsInstance(result, numpy.ndarray)
        self.assertIsInstance(result[0], unum.Unum)

    def test_Multiplying_UnitByNumpyArray_ReturnUnumWithNumpyArrayValue(self):
        result = as_unum(ns * numpy.array([2, 3, 4]))

        self.assertIsInstance(result, unum.Unum)
        self.assertIsInstance(result.number(), numpy.ndarray)

    def test_Init_GivenUnitsIsDefined_ReturnNewUnumNumberWithGivenUnits(self):
        value = unum.Unum(2, {'m': 1, 's': -2})

        self.assertEqual(2 * m / s ** 2, value)

    def test_Positive_Always_ReturnEqualUnum(self):
        value = 2 * m

        self.assertEqual(value, (+value))

    def test_CastUnit_m_to_cm_ReturnUnumWithCMUnit(self):
        value = as_unum(5 * m)

        result = value.cast_unit(cm)

        self.assertEqual("500.0 [cm]", str(result))

    def test_CastUnit_NotBasicUnit_Throws(self):
        value = as_unum(5 * m)

        with self.assertRaises(unum.NonBasicUnitError):
            value.cast_unit(2 * cm)

    def test_SimplifyUnit_J_over_m_ReturnValueInN(self):
        value = as_unum(10 * J / m)

        value.simplify_unit()

        self.assertEqual(N, value.unit())

    def test_SimplifyUnit_J_over_m2kg_Return_1_over_s2(self):
        value = as_unum(10 * J / kg / m ** 2)

        value.simplify_unit()

        self.assertEqual(1 / (s ** 2), value.unit())

    def test_SimplifyUnit_SameUnitWithDifferentPrefix_ReturnUnitless(self):
        value = as_unum(10 * kg / g)

        value.simplify_unit()

        self.assertEqual(unitless, value.unit())

    def test_SimplifyUnit_NamedDimensionlessUnitForDisplay_ReturnWithUnit(self):
        value = as_unum(10 * rad)

        value.simplify_unit(forDisplay=True)

        self.assertEqual(rad, value.unit())

    def test_SimplifyUnit_J_over_cm_ReturnN(self):
        value = as_unum(14 * J / cm)

        value.simplify_unit()

        self.assertEqual(N, value.unit())

    def test_SimplifyUnit_SamePrimaryUnit_ReturnUnitless(self):
        value = as_unum(5 * Hz * s)

        value.simplify_unit()

        self.assertEqual(unitless, value.unit())

    def test_Equal_DifferentUnits_ReturnFalse(self):
        a = 5 * m
        b = 4 * K

        assert not a == b

    def test_Equal_WithNone_ReturnFalse(self):
        value = 5 * m

        assert not value == None

    def test_NotEqual_DifferentUnits_ReturnTrue(self):
        a = 5 * K
        b = 4 * m

        assert a != b

    def test_NotEqual_WithNone_ReturnTrue(self):
        a = 5 * K
        b = None

        assert a != b

    def test_Bool_ZeroValue_ReturnFalse(self):
        a = 0. * K

        assert not a

    def test_Bool_NonZeroValue_ReturnTrue(self):
        a = 5 * K

        assert a

    @classmethod
    def setUpClass(cls):
        unum.Unum.set_format(superscript=False, mul_separator='.')

    @classmethod
    def tearDownClass(cls):
        unum.Unum.reset_format()


class FormatterTest(unittest.TestCase):
    def test_Format_ByDefault_UseDots(self):
        formatter = self.create()
        value = 5.4 * m

        result = formatter.format(value)

        self.assertEqual("5.4 [m]", result)

    def test_Format_NoUnit_DisplayEmptyBrackets(self):
        formatter = self.create(unitless='[]')
        value = 5.4 * m / m

        result = formatter.format(value)

        self.assertEqual("5.4 []", result)

    def test_Format_TwoMultipliedUnis_JoinUnitsByDots(self):
        formatter = self.create()
        value = 5.4 * N * m

        result = formatter.format(value)

        self.assertEqual("5.4 [N.m]", result)

    def test_Format_DividedByUnit_JoinBySlash(self):
        formatter = self.create()
        value = 5.4 * m / s

        result = formatter.format(value)

        self.assertEqual("5.4 [m/s]", result)

    def test_Format_MultipliedAndDividedUnit_FirstMultiplication(self):
        formatter = self.create()
        value = 4.5 * N / s * m

        result = formatter.format(value)

        self.assertEqual("4.5 [N.m/s]", result)

    def test_Format_Powering_AddExponentAfterUnit(self):
        formatter = self.create()
        value = 4.5 * m ** 3

        result = formatter.format(value)

        self.assertEqual("4.5 [m3]", result)

    def test_Format_ChangeUnitFormat_DisplayUnitUsingNewFormat(self):
        formatter = self.create(unit_format="{%s}")
        value = 4.5 * m ** 3

        result = formatter.format(value)

        self.assertEqual("4.5 {m3}", result)

    def test_Format_ChangeUnitIndent_DisplayUnitWithNewIndent(self):
        formatter = self.create(indent="  ")
        value = 4.5 * m ** 3

        result = formatter.format(value)

        self.assertEqual("4.5  [m3]", result)

    def test_Format_Display2DigitsAfterPoint_ReturnFormattedNumber(self):
        formatter = self.create(value_format="%.2f")
        value = 4.545682 * m ** 3

        result = formatter.format(value)

        self.assertEqual("4.55 [m3]", result)

    def test_Format_NoDivSeparator(self):
        formatter = self.create(div_separator='')
        value = 4.54 * m / s ** 2

        result = formatter.format(value)

        self.assertEqual("4.54 [m.s-2]", result)

    def test_Format_OnyNegativeExponents_ReturnOneOnBegin(self):
        formatter = self.create()
        value = 4.54 / s ** 2

        result = formatter.format(value)

        self.assertEqual("4.54 [1/s2]", result)

    def test_Format_HideEmptyNoUnit_FormatOnlyValue(self):
        formatter = self.create(unitless='')
        value = 4.54 * m / m

        result = formatter.format(value)

        self.assertEqual("4.54", result)

    def test_Format_NoUnitAndNoDivSeparator_FormatOnlyValue(self):
        formatter = self.create(unitless='', div_separator='')
        value = 4.54 * m / m

        result = formatter.format(value)

        self.assertEqual("4.54", result)

    def test_Format_UnitGiven_CastValueToUnitBeforeFormat(self):
        formatter = self.create(unit=cm)
        value = 1.2 * m

        result = formatter.format(value)

        self.assertEqual('120.0 [cm]', result)
        
    def test_Format_UseSuperscript_ReplaceNumbersInUnitsByUnicodeSuperscript(self):
        formatter = self.create(superscript=True)
        value = 1.4 * m ** 2

        result = formatter.format(value)

        self.assertEqual('1.4 [m\u00B2]', result)

    @staticmethod
    def create(**kwargs):
        kwargs.setdefault('superscript', False)
        kwargs.setdefault('mul_separator', '.')
        return unum.Formatter(**kwargs)
