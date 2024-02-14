# -*- coding: utf-8 -*-

import unittest
from prolothar_common.levenshtein import levenshtein_with_backtrace
from prolothar_common.levenshtein import EditOperation, EditOperationType


class TestLevenshtein(unittest.TestCase):

    def test_levenshtein_with_backtrace_empty_strings(self):
        distance, edits = levenshtein_with_backtrace('', '')
        self.assertEqual(0, distance)
        self.assertCountEqual([], edits)

    def test_levenshtein_with_backtrace_equal_strings(self):
        distance, edits = levenshtein_with_backtrace('abc', 'abc')
        self.assertEqual(0, distance)
        self.assertCountEqual([], edits)

    def test_levenshtein_with_backtrace_only_inserts(self):
        distance, edits = levenshtein_with_backtrace('', 'abc')
        self.assertEqual(3, distance)
        self.assertCountEqual([
            EditOperation(0, 0, EditOperationType.INSERT),
            EditOperation(0, 1, EditOperationType.INSERT),
            EditOperation(0, 2, EditOperationType.INSERT)
        ], edits)

    def test_levenshtein_with_backtrace_only_deletes(self):
        distance, edits = levenshtein_with_backtrace('abc', '')
        self.assertEqual(3, distance)
        self.assertCountEqual([
            EditOperation(0, 0, EditOperationType.DELETE),
            EditOperation(1, 0, EditOperationType.DELETE),
            EditOperation(2, 0, EditOperationType.DELETE)
        ], edits)

    def test_levenshtein_with_backtrace_only_substitutes(self):
        distance, edits = levenshtein_with_backtrace('abc', 'def')
        self.assertEqual(3, distance)
        self.assertCountEqual([
            EditOperation(0, 0, EditOperationType.SUBSTITUTE),
            EditOperation(1, 1, EditOperationType.SUBSTITUTE),
            EditOperation(2, 2, EditOperationType.SUBSTITUTE)
        ], edits)

    def test_levenshtein_with_backtrace(self):
        distance, _ = levenshtein_with_backtrace('abc', 'ca')
        self.assertEqual(3, distance)

    def test_levenshtein_with_backtrace_double_cost_for_substitute(self):
        distance, edits = levenshtein_with_backtrace(['B', 'E'], ['A', 'B'])
        self.assertEqual(2, distance)
        self.assertCountEqual([
            EditOperation(0, 0, EditOperationType.SUBSTITUTE),
            EditOperation(1, 1, EditOperationType.SUBSTITUTE),
        ], edits)

        distance, edits = levenshtein_with_backtrace(
            ['B', 'E'], ['A', 'B'], substitution_cost = 2)
        self.assertEqual(2, distance)
        self.assertCountEqual([
            EditOperation(0, 0, EditOperationType.INSERT),
            EditOperation(1, 2, EditOperationType.DELETE),
        ], edits)

if __name__ == '__main__':
    unittest.main()