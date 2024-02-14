# -*- coding: utf-8 -*-
import unittest
from hypothesis import given, example
from hypothesis.strategies import floats
from hypothesis.strategies import lists
import numpy as np
from statistics import mean
from statistics import stdev

from prolothar_common.experiments.statistics import Statistics

class TestResultCollector(unittest.TestCase):

    @given(lists(
        floats(
            allow_nan=False, allow_infinity=False,
            min_value=-1_000_000, max_value=1_000_000
        ),
        min_size=0, max_size=10_000_000
    ))
    @example([])
    def test_statistics(self, list_of_numbers):
        statistics = Statistics(list_of_numbers)
        if len(list_of_numbers) > 0:
            self.assertAlmostEqual(mean(list_of_numbers), statistics.mean())
            self.assertAlmostEqual(min(list_of_numbers), statistics.minimum())
            self.assertAlmostEqual(max(list_of_numbers), statistics.maximum())
            if len(list_of_numbers) > 1:
                self.assertAlmostEqual(stdev(list_of_numbers), statistics.stddev())
            else:
                self.assertTrue(np.isnan(statistics.stddev()))
        else:
            self.assertEqual(0, statistics.mean())
            self.assertTrue(np.isnan(statistics.stddev()))
            self.assertTrue(np.isnan(statistics.minimum()))
            self.assertTrue(np.isnan(statistics.maximum()))

    @given(
        lists(
            floats(
                allow_nan=False, allow_infinity=False,
                min_value=-1_000_000, max_value=1_000_000
            ),
            min_size=0, max_size=5_000_000
        ),
        lists(
            floats(
                allow_nan=False, allow_infinity=False,
                min_value=-1_000_000, max_value=1_000_000
            ),
            min_size=0, max_size=5_000_000
        ),
    )
    def test_merge_statistics(self, list_1, list_2):
        expected_complete_statistics = Statistics(list_1 + list_2)
        actual_complete_statistics = Statistics()
        actual_complete_statistics.merge(Statistics(list_1))
        actual_complete_statistics.merge(Statistics(list_2))
        if not list_1 and not list_2:
            self.assertEqual(0, actual_complete_statistics.mean())
            self.assertTrue(np.isnan(actual_complete_statistics.stddev()))
            self.assertTrue(np.isnan(actual_complete_statistics.minimum()))
            self.assertTrue(np.isnan(actual_complete_statistics.maximum()))
        else:
            self.assertAlmostEqual(expected_complete_statistics.minimum(), actual_complete_statistics.minimum())
            self.assertAlmostEqual(expected_complete_statistics.maximum(), actual_complete_statistics.maximum())
            self.assertAlmostEqual(expected_complete_statistics.mean(), actual_complete_statistics.mean())
        if len(list_1) + len(list_2) > 1:
            self.assertAlmostEqual(expected_complete_statistics.stddev(), actual_complete_statistics.stddev())

if __name__ == '__main__':
    unittest.main()