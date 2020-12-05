import unittest
from warnings import warn

from unum import UnumError
from unum.units import g, cm, kg


class TestPrecisionWarning(UnumError, Warning):
    def __init__(self, msg=None):
        if msg is None:
            # Set some default useful error message
            msg = "Test is not precise enough"
        super(TestPrecisionWarning, self).__init__(msg)


class UKTests(unittest.TestCase):
    """
    https://www.wikiwand.com/en/Troy_weight#Conversions

    """

    def test_pound_force(self):
        from unum.units.imp_UK import lbf
        from unum.units import N
        self.assertAlmostEqual(4.44822, lbf.cast_unit(N).number(), 5)


class ApothecaryTests(unittest.TestCase):
    """
    https://www.wikiwand.com/en/Troy_weight#Conversions

    """

    def test_ap_dram(self):
        from unum.units.imp_UK.Apothecaries import dr_ap
        self.assertAlmostEqual(3.8879346, dr_ap.cast_unit(g).number(), 5)

    def test_ap_lb(self):
        from unum.units.imp_UK.troy import lb_t
        from unum.units.imp_UK.Apothecaries import lb_ap
        self.assertAlmostEqual(1, lb_ap.cast_unit(lb_t).number(), 5)

    def test_ap_minim(self):
        from unum.units.others import L
        from unum.units.imp_UK.Apothecaries import min_ap
        self.assertAlmostEqual(0.0000591938802083, min_ap.cast_unit(L).number(), 5)

    def test_ap_fl_dram(self):
        from unum.units.imp_UK.Apothecaries import fl_dr_ap
        self.assertAlmostEqual(3.5516328125, fl_dr_ap.cast_unit(cm ** 3).number(), 5)

    def test_ap_dram_SI(self):
        from unum.units.imp_UK.Apothecaries import dr_ap
        self.assertAlmostEqual(0.00388793458, dr_ap.cast_unit(kg).number(), 5)

    def test_drachm(self):
        from unum.units.imp_UK.Apothecaries import gr_ap
        from unum.units.imp_UK.Apothecaries import drachm
        self.assertAlmostEqual(60, drachm.cast_unit(gr_ap).number())


class AvoirdupoisTests(unittest.TestCase):
    """
    https://www.wikiwand.com/en/Troy_weight#Conversions

    """

    def test_pound(self):
        from unum.units.imp_UK import lb
        from unum.units import g
        self.assertEqual(453.59237, lb.cast_unit(g).number())

    def test_grain(self):
        from unum.units import mg
        from unum.units.imp_UK.avoirdupois import grain
        self.assertEqual(64.79891, grain.cast_unit(mg).number())

    def test_dram(self):
        from unum.units.imp_UK.avoirdupois import grain
        from unum.units.imp_UK import dr
        # warn("Test definition not precise enough!") #fixed through addition of SI test
        self.assertAlmostEqual(27.34, dr.cast_unit(grain).number(), 2)

    def test_dram_SI(self):
        from unum.units.imp_UK import dr
        from unum.units import g
        self.assertAlmostEqual(1.7718451953125, dr.cast_unit(g).number(), 13)

    def test_slug(self):
        from unum.units import g
        from unum.units.imp_UK import slug
        warn(TestPrecisionWarning())
        self.assertAlmostEqual(14593.90, slug.cast_unit(g).number(), 2)


class MetricTest(unittest.TestCase):
    """
    https://www.wikiwand.com/en/Troy_weight#Conversions

    """

    def test_pound(self):
        from unum.units.imp_UK.metric import lb_m
        from unum.units import g
        self.assertEqual(500, lb_m.cast_unit(g).number())


class TroyTest(unittest.TestCase):
    """
    https://www.wikiwand.com/en/Troy_weight#Conversions

    """

    def test_pound(self):
        from unum.units.imp_UK.troy import lb_t
        from unum.units import g
        self.assertEqual(373.2417216, lb_t.cast_unit(g).number())

    def test_ounce(self):
        from unum.units.imp_UK.troy import oz_t
        from unum.units import g
        self.assertAlmostEqual(31.1034768, oz_t.cast_unit(g).number(), 7)  # float causes inacuracies

    # def test_ounce_dec(self):
    #     self.assertEqual(dec("31.1034768"), as_unum(dec(1), oz_t).cast_unit(g).number())  # float causes inacuracies
    #
    # def test_ounce_dec2(self):
    #     self.assertEqual(dec("31.1034768"), oz_t.cast_unit(g).number())  # float causes inacuracies
    def test_pennyweight(self):
        from unum.units.imp_UK.troy import pwt
        from unum.units import g
        self.assertEqual(1.55517384, pwt.cast_unit(g).number())

    def test_grain(self):
        from unum.units.imp_UK.troy import gr_t
        from unum.units import g
        self.assertEqual(0.06479891, gr_t.cast_unit(g).number())


class MintTests(unittest.TestCase):
    def test_mite(self):
        warn(TestPrecisionWarning())

    def test_blank(self):
        warn(TestPrecisionWarning())

    def test_droit(self):
        warn(TestPrecisionWarning())

    def test_perit(self):
        warn(TestPrecisionWarning())
