import  unittest



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
        self.assertAlmostEqual(31.1034768, oz_t.cast_unit(g).number(),7) #float causes inacuracies

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



