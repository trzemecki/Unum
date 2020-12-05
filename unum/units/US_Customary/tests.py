import unittest
from warnings import warn

from unum.units.imp_UK.tests import TestPrecisionWarning


class UKTests(unittest.TestCase):
    """
    https://www.wikiwand.com/en/Troy_weight#Conversions

    """

    def test_pound_force(self):
        from unum.units.US_Customary import ton
        warn(TestPrecisionWarning())
        from unum.units import kg
        self.assertAlmostEqual(907.185, ton.cast_unit(kg).number(), 3)

    def test_blank(self):
        warn(TestPrecisionWarning())
