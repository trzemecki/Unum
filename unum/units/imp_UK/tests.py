import unittest




class UKTests(unittest.TestCase):
    """
    https://www.wikiwand.com/en/Troy_weight#Conversions

    """
    def test_pound_force(self):
        from unum.units.imp_UK import lbf
        from unum.units import N
        self.assertAlmostEqual(4.44822, lbf.cast_unit(N).number(),5)