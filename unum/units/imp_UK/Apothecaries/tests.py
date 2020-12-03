import unittest

from unum.units import g



class ApothercaryTests(unittest.TestCase):
    """
    https://www.wikiwand.com/en/Troy_weight#Conversions

    """
    def test_ap_dram(self):
        from unum.units.imp_UK.Apothecaries import dr_ap
        self.assertAlmostEqual(3.8879346, dr_ap.cast_unit(g).number(),5)

    def test_ap_dram(self):
        from unum.units.imp_UK.troy import lb_t
        from unum.units.imp_UK.Apothecaries import lb_ap
        self.assertAlmostEqual(1, lb_ap.cast_unit(lb_t).number(),5)

    def test_ap_dram(self):
        from unum.units.imp_UK.Apothecaries import dr_ap
        self.assertAlmostEqual(3.8879346, dr_ap.cast_unit(g).number(),5)