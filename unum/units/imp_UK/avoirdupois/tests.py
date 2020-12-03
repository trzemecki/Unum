import  unittest
from warnings import warn


class TroyTest(unittest.TestCase):
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
        warn("Test definition not precise enough!")
        self.assertAlmostEqual(27.34, dr.cast_unit(grain).number(), 2)
    def test_dram_SI(self):
        from unum.units.imp_UK import dr
        from unum.units import g

        self.assertAlmostEqual(1.7718451953125, dr.cast_unit(g).number(), 13)

    def test_slug(self):
        from unum.units import g
        from unum.units.imp_UK import slug
        self.assertAlmostEqual(14593.90, slug.cast_unit(g).number(),2)





