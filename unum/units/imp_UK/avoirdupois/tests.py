import  unittest




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
    def test_slug(self):
        from unum.units import g
        from unum.units.imp_UK import slug
        self.assertAlmostEqual(14593.90, slug.cast_unit(g).number(),2)





