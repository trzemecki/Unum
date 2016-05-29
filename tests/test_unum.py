import unittest
import math
import numpy
from fractions import Fraction

import unum
from unum.units import *


class UnumTest(unittest.TestCase):
    def test_Addition_UnitToItself_ReturnDoubleUnitNumber(self):
        result = mg + mg

        self.assertEqual(2 * mg, result)

    def test_Addition_UnitsNotMath_Throws(self):
        with self.assertRaises(unum.IncompatibleUnitsError):
            result = mg + ms

    def test_MathFunction_UnitlessArgument_ReturnUnitlessNumber(self):
        self.assertAlmostEqual(math.log10(1000 * m / m), 3.0, places=3)

    def test_MathFunction_NotUnitlessArgument_Throws(self):
        with self.assertRaises(unum.ShouldBeUnitlessError):
            math.cos(2 * mA)

    def test_NewUnit_NameConflict_Throws(self):
        unum.unit("myunit", 0, "my_new_unit")

        with self.assertRaises(unum.NameConflictError):
            unum.unit("myunit", 0, "my_new_unit")

    def test_AsNumber_Kg_to_g_Return1000(self):
        result = kg.asNumber(g)
        self.assertEqual(1000, result)

    def test_AsNumber_ToNotBasicUnit_Throws(self):
        with self.assertRaises(unum.NonBasicUnitError):
            kg.asNumber(2 * g)

    def test_Equals_SI_J_and_J_ReturnTrue(self):
        self.assertTrue(N * m == J)

    def test_Equals_SI_W_and_W_ReturnTrue(self):
        self.assertTrue(N * m / s == W)

    def test_AsUnit_NoneSIUnitToW_ReturnWTimesRatio(self):
        result = (N * km / s).asUnit(W)

        self.assertEqual(result, 1000 * W)

    def test_AsUnit_UnitNotMatch_Throws(self):
        with self.assertRaises(unum.IncompatibleUnitsError):
            S.asUnit(h)
            
    def test_AsUnit_HoursToSeconds_Return3600s(self):
        result = h.asUnit(s)

        self.assertEqual(result, 3600 * s)

    def test_Addition_Fractions_ReturnFractionWithUnit(self):
        x = Fraction(1, 2) * km
        y = Fraction("1/3") * km

        result = x + y

        self.assertEqual(result, Fraction(5, 6) * km)

    def test_Exponentiation_FractionSquared_ReturnValueWithSquaredUnit(self):
        fraction = Fraction(5, 6) * km

        result = fraction ** 2

        self.assertEqual(result, Fraction(25, 36) * km ** 2)

    def test_Multiplying_UnitByFraction_ReturnFractionWithUnit(self):
        result = km * Fraction(1, 2)

        self.assertEqual(result, Fraction(1, 2) * km)

    def test_Multiplying_NumpyArrayByUnit_ReturnNumpyArrayWithNumbersWithUnit(self):
        result = numpy.array([2, 3, 4]) * ns

        self.assertIsInstance(result, numpy.ndarray)
        self.assertIsInstance(result[0], unum.Unum)

    def test_Multiplying_UnitByNumpyArray_ReturnUnumWithNumpyArrayValue(self):
        result = ns * numpy.array([2, 3, 4])

        self.assertIsInstance(result, unum.Unum)
        self.assertIsInstance(result.asNumber(), numpy.ndarray)

    def test_Uarray_Always_ReturnUnumWithNumpyArrayValue(self):
        result = unum.uarray([2, 3, 4])

        self.assertIsInstance(result, unum.Unum)
        self.assertIsInstance(result.asNumber(), numpy.ndarray)

    def test_Init_GivenUnitsIsDefined_ReturnNewUnumNumberWithGivenUnits(self):
        value = unum.Unum(2, {'m': 1, 's': -2})

        self.assertEqual(2 * m / s ** 2, value)

    def test_Positive_Always_ReturnEqualUnum(self):
        value = 2 * m

        result = +value

        self.assertEqual(result, value)


class FormattingTest(unittest.TestCase):
    def test_Str_ByDefault_UseDots(self):
        value = 5.4 * m

        result = str(value)

        self.assertEqual("5.4 [m]", result)

    def test_Str_NoUnit_DisplayEmptyBrackets(self):
        value = 5.4 * m / m

        result = str(value)

        self.assertEqual("5.4 []", result)

    def test_Str_TwoMultipliedUnis_JoinUnitsByDots(self):
        value = 5.4 * N * m

        result = str(value)

        self.assertEqual("5.4 [N.m]", result)

    def test_Str_DividedByUnit_JoinBySlash(self):
        value = 5.4 * m / s

        result = str(value)

        self.assertEqual("5.4 [m/s]", result)

    def test_Str_MultipliedAndDividedUnit_FirstMultiplication(self):
        value = 4.5 * N / s * m

        result = str(value)

        self.assertEqual("4.5 [N.m/s]", result)

    def test_Str_Powering_AddExponentAfterUnit(self):
        value = 4.5 * m ** 3

        result = str(value)

        self.assertEqual("4.5 [m3]", result)

    def test_Str_ChangeUnitFormat_DisplayUnitUsingNewFormat(self):
        value = 4.5 * m ** 3

        unum.Unum.formatter.UNIT_FORMAT = "{%s}"

        result = str(value)

        self.assertEqual("4.5 {m3}", result)

    def test_Str_ChangeUnitIndent_DisplayUnitWithNewIndent(self):
        value = 4.5 * m ** 3

        unum.Unum.formatter.UNIT_INDENT = "  "

        result = str(value)

        self.assertEqual("4.5  [m3]", result)

    def test_Str_Display2DigitsAfterPoint_ReturnFormattedNumber(self):
        value = 4.545682 * m ** 3

        unum.Unum.formatter.VALUE_FORMAT = "%.2f"

        result = str(value)

        self.assertEqual("4.55 [m3]", result)

    # def test_Str_NotNormalize_(self):
    #     value = 4.545682 * m / m
    #
    #     unum.Unum.AUTO_NORM = False
    #
    #     result = str(value)
    #
    #     self.assertEqual("4.55 [m3]", result)



    def tearDown(self):
        unum.Unum.formatter = unum.Formatter()





