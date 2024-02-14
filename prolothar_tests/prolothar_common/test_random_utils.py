# -*- coding: utf-8 -*-

import unittest
from collections import defaultdict
from prolothar_common.random_utils import BufferingChoice

class TestRandomUtils(unittest.TestCase):

    def test_buffering_choice(self):
        try:
            BufferingChoice([0, 1, 2], [0.1, 0.9])
            self.fail('ValueError expected')
        except ValueError:
            pass
        options = [0,1,2]
        probabilities = [0.1, 0.2, 0.7]
        buffering_choice = BufferingChoice(options, probabilities, seed=42)
        counter = defaultdict(int)
        for _ in range(1000):
            counter[buffering_choice.next_sample()] += 1
        self.assertAlmostEqual(counter[0], 100, delta=15)
        self.assertAlmostEqual(counter[1], 200, delta=15)
        self.assertAlmostEqual(counter[2], 700, delta=15)

if __name__ == '__main__':
    unittest.main()