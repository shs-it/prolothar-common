# -*- coding: utf-8 -*-

import unittest
import prolothar_common.math_utils as math_utils


class TestMathUtils(unittest.TestCase):

    def test_prime_factors(self):
        self.assertListEqual([2,2,2,3],
                             math_utils.prime_factors(24))

        self.assertListEqual([3,7,97],
                             math_utils.prime_factors(2037))


if __name__ == '__main__':
    unittest.main()