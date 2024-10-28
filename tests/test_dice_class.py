import unittest
import DiceyDiagnostics.dice_class as dice
from DiceyDiagnostics.dice_class import WeirdDice


class DiceClassTest(unittest.TestCase):
    def test_dice_init_basic(self):

        test_dice = WeirdDice(d=4,bias_highest=0.00, extra_dimension=False)

        # in a balanced d4 each side should have prob of 0.25
        d4_4_prob = WeirdDice.face_props[4]

        self.assertEqual(d4_4_prob, 0.25)  # add assertion here

    def test_dice_init_bias(self):
        test_dice = WeirdDice(d=4, bias_highest=1.0, extra_dimension=False)
        # in this test there is a known highest bias and
        #


if __name__ == '__main__':
    unittest.main()
