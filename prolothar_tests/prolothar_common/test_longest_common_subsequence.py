# -*- coding: utf-8 -*-

import unittest
from hypothesis import given, example
import hypothesis.strategies as st

from prolothar_common.longest_common_subsequence import lcs_with_backtrace

class TestLongestCommonSubsequence(unittest.TestCase):

    def test_lcs_with_backtrace_empty_strings(self):
        lcs, backtrace = lcs_with_backtrace('', '')
        self.assertEqual(0, lcs)
        self.assertListEqual([], backtrace)

    def test_lcs_with_backtrace_wikipedia_example(self):
        x = ['this', 'is', 'some', 'text', 'that', 'will', 'be', 'changed']
        y = ['this', 'is', 'the', 'changed', 'text']
        lcs, backtrace = lcs_with_backtrace(x, y)
        self.assertEqual(3, lcs)
        self.assertListEqual([(0,0), (1,1), (7,3)], backtrace)

    @given(
        x=st.text(min_size = 0, max_size = 100),
        y=st.text(min_size = 0, max_size = 100)
    )
    @example(
        x = ['this', 'is', 'some', 'text', 'that', 'will', 'be', 'changed'],
        y = ['this', 'is', 'the', 'changed', 'text']
    )
    def test_lcs_with_backtrace(self, x, y):
        lcs, backtrace = lcs_with_backtrace(x, y)
        self.assertEqual(lcs, len(backtrace))
        for i,j in backtrace:
            self.assertEqual(x[i], y[j])

if __name__ == '__main__':
    unittest.main()