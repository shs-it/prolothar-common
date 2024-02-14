# -*- coding: utf-8 -*-

import unittest
import os
from time import sleep
from tempfile import TemporaryDirectory
from prolothar_common.testing import non_productive_result_cache
from prolothar_common.experiments.stopwatch import Stopwatch

class TestNonProductiveResultCache(unittest.TestCase):

    def test_without_cache_key(self):
        with TemporaryDirectory() as tempdir:
            cache_dir = os.path.join(tempdir, 'cache')
            @non_productive_result_cache(cache_dir)
            def dummy_method(i: int, j: int):
                sleep(1)
                return i + 42 - j
            stopwatch = Stopwatch()
            stopwatch.start()
            self.assertEqual(42, dummy_method(0, 0))
            self.assertAlmostEqual(1, stopwatch.get_elapsed_time().total_seconds(), delta=0.1)
            #second call should be faster due to caching
            stopwatch.start()
            self.assertEqual(42, dummy_method(0, 0))
            self.assertLess(stopwatch.get_elapsed_time().total_seconds(), 0.2)
            self.assertTrue(os.path.exists(os.path.join(cache_dir, 'dummy_method')))

    def test_with_cache_key(self):
        with TemporaryDirectory() as tempdir:
            cache_dir = os.path.join(tempdir, 'cache')
            @non_productive_result_cache(cache_dir, key=lambda i,j: f'{i}-{j}')
            def dummy_method(i: int, j: int):
                sleep(1)
                return i + 42 - j
            stopwatch = Stopwatch()
            stopwatch.start()
            self.assertEqual(42, dummy_method(0, 0))
            self.assertAlmostEqual(1, stopwatch.get_elapsed_time().total_seconds(), delta=0.1)
            stopwatch.start()
            self.assertEqual(42, dummy_method(1, 1))
            self.assertAlmostEqual(1, stopwatch.get_elapsed_time().total_seconds(), delta=0.1)
            #second call should be faster due to caching
            stopwatch.start()
            self.assertEqual(42, dummy_method(0, 0))
            self.assertLess(stopwatch.get_elapsed_time().total_seconds(), 0.2)
            stopwatch.start()
            self.assertEqual(42, dummy_method(1, 1))
            self.assertLess(stopwatch.get_elapsed_time().total_seconds(), 0.2)

if __name__ == '__main__':
    unittest.main()