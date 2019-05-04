import unittest
from wip.technical_analysis.momentum import StochasticOscillatorAgent as SO
# from pandas import Series


class TestTechnicalAnalysis(unittest.TestCase):

    def test_set_days(self):
        so = SO()
        with self.assertRaises(ValueError):
            so.set_days(29)
        with self.assertRaises(ValueError):
            so.set_days(-1)
        self.assertEqual(so.set_days(20), 20)

    def test_set_roll_days(self):
        so = SO()
        with self.assertRaises(ValueError):
            so.set_roll_days(1)
        with self.assertRaises(ValueError):
            so.set_roll_days(8)
        self.assertEqual(so.set_roll_days(7), 7)

    def test_k_line(self):
        max_high = 50
        min_low = 40
        closing_price = 42
        SO.k_line(max_high, min_low, closing_price)


    # def test_generate_signals(self):
    #     high = [10, 11, 12, 10, 11, 12, 13, 10, 11, 12, 10, 11, 12, 13, 14, 15, 16, 15, 15, 15]
    #     low = [7, 6, 4, 7, 6, 5, 5, 7, 6, 4, 7, 6, 5, 5, 4, 3, 4, 3, 2, 2]
    #     close = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    #
    #     so = StochasticOscillatorAgent()
    #     self.assertEqual(True, True)


def run_tests():
    unittest.main()


