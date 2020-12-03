import  unittest



class TroyTest(unittest.TestCase):
    """
    https://www.wikiwand.com/en/Troy_weight#Conversions

    """
    def test_pound(self):
        from unum.units.imp_UK.metric import lb_m
        from unum.units import g
        self.assertEqual(500, lb_m.cast_unit(g).number())