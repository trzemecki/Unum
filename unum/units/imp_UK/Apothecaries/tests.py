import unittest

from unum.units import g, cm, kg


class ApothercaryTests(unittest.TestCase):
    """
    https://www.wikiwand.com/en/Troy_weight#Conversions

    """
    def test_ap_dram(self):
        from unum.units.imp_UK.Apothecaries import dr_ap
        self.assertAlmostEqual(3.8879346, dr_ap.cast_unit(g).number(),5)

    def test_ap_lb(self):
        from unum.units.imp_UK.troy import lb_t
        from unum.units.imp_UK.Apothecaries import lb_ap
        self.assertAlmostEqual(1, lb_ap.cast_unit(lb_t).number(),5)

    def test_ap_minim(self):
        from unum.units.others import l
        from unum.units.imp_UK.Apothecaries import min_ap
        self.assertAlmostEqual(0.0000591938802083, min_ap.cast_unit(l).number(),5)

    def test_ap_fl_dram(self):
        from unum.units.imp_UK.Apothecaries import fl_dr_ap
        self.assertAlmostEqual(3.5516328125, fl_dr_ap.cast_unit(cm**3).number(),5)

    def test_ap_dram_SI(self):

        from unum.units.imp_UK.Apothecaries import dr_ap
        self.assertAlmostEqual(0.00388793458, dr_ap.cast_unit(kg).number(),5)

    def test_drachm(self):
        from unum.units.imp_UK.Apothecaries import gr_ap
        from unum.units.imp_UK.Apothecaries import drachm
        self.assertAlmostEqual(60, drachm.cast_unit(gr_ap).number())