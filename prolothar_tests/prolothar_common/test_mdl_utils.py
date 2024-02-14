# -*- coding: utf-8 -*-


import unittest
import prolothar_common.mdl_utils as mdl_utils
from math import log2

class TestMdlUtils(unittest.TestCase):

    def test_L_N(self):
        self.assertAlmostEqual(1.514, mdl_utils.L_N(1), delta=0.001)
        self.assertAlmostEqual(2.514, mdl_utils.L_N(2), delta=0.001)
        with self.assertRaises(ValueError):
            mdl_utils.L_N(0)

    def test_log2binom(self):
        self.assertEqual(0.0, mdl_utils.log2binom(5, 0))
        self.assertAlmostEqual(log2(20),
                               mdl_utils.log2binom(20, 1),
                               delta=0.01)
        self.assertAlmostEqual(184.62,
                               mdl_utils.log2binom(5000, 20),
                               delta=0.01)
        self.assertAlmostEqual(2540.876,
                               mdl_utils.log2binom(500000, 200),
                               delta=0.001)

    def test_log2multinom(self):
        self.assertAlmostEqual(0.0,
                               mdl_utils.log2multinom(5000, [5000]),
                               delta=0.01)
        self.assertAlmostEqual(51.2900803082,
                               mdl_utils.log2multinom(32, (10,10,10,2)),
                               delta=0.01)

    def test_L_U(self):
        self.assertAlmostEqual(0,
                               mdl_utils.L_U(0, 0))
        self.assertAlmostEqual(184.62,
                               mdl_utils.L_U(5001, 21),
                               delta=0.01)
        self.assertAlmostEqual(2540.876,
                               mdl_utils.L_U(500001, 201),
                               delta=0.001)

    def test_prequential_coding_length_only_one_symbol(self):
        self.assertEqual(0, mdl_utils.prequential_coding_length({'A': 50}))

    def test_prequential_coding_length_epsilon_one_half(self):
        counts = {
            'A': 0,
            'B': 0,
            'C': 0
        }
        length = 0.0
        for symbol in ['A','B','B','B','C','C','C','C','C','C','C','C'] * 10:
            length -= log2((counts[symbol] + 0.5) / (sum(counts.values()) + 1.5))
            counts[symbol] += 1

        length2 = 0
        nominator = 1
        denominator = 1
        for symbol,count in counts.items():
            for j in range(count):
                nominator *= (0.5 + j)
        for j in range(sum(counts.values())):
            denominator *= (0.5 * len(counts) + j)
        length2 -= log2(nominator / denominator)

        self.assertAlmostEqual(
                length, mdl_utils.prequential_coding_length(counts), delta=0.001)
        self.assertAlmostEqual(
                length2, mdl_utils.prequential_coding_length(counts), delta=0.001)

    def test_prequential_coding_length_epsilon_one(self):
        counts = {
            'A': 0,
            'B': 0,
            'C': 0
        }
        length = 0.0
        for symbol in ['A','B','B','B','C','C','C','C','C','C','C','C'] * 10:
            length -= log2((counts[symbol] + 1) / (sum(counts.values()) + 3))
            counts[symbol] += 1

        length2 = 0
        nominator = 1
        denominator = 1
        for symbol,count in counts.items():
            for j in range(count):
                nominator *= (1 + j)
        for j in range(sum(counts.values())):
            denominator *= (1 * len(counts) + j)
        length2 -= log2(nominator / denominator)

        self.assertAlmostEqual(
                length, mdl_utils.prequential_coding_length(counts, epsilon=1),
                delta=0.001)

    def test_sum_log_i_from_1_to_n(self):
        with self.assertRaises(ValueError):
            mdl_utils.sum_log_i_from_1_to_n(0)
        with self.assertRaises(ValueError):
            mdl_utils.sum_log_i_from_1_to_n(-1)
        self.assertAlmostEqual(0, mdl_utils.sum_log_i_from_1_to_n(1), places=2)
        self.assertAlmostEqual(25.25, mdl_utils.sum_log_i_from_1_to_n(11), places=2)
        self.assertAlmostEqual(65.47, mdl_utils.sum_log_i_from_1_to_n(21), places=2)

    def test_L_R(self):
        self.assertAlmostEqual(log2(3), mdl_utils.L_R(0))
        self.assertEqual(mdl_utils.L_R(1), mdl_utils.L_R(-1))
        self.assertGreater(mdl_utils.L_R(1), mdl_utils.L_R(0))
        self.assertGreater(mdl_utils.L_R(-1), mdl_utils.L_R(0))
        self.assertGreater(mdl_utils.L_R(1.1), mdl_utils.L_R(1))
        self.assertGreater(mdl_utils.L_R(1.2), mdl_utils.L_R(1.1))
        self.assertGreater(mdl_utils.L_R(-1.2), mdl_utils.L_R(1.1))
        self.assertTrue(mdl_utils.L_R(8.612639221334548e-16) > 0)

if __name__ == '__main__':
    unittest.main()