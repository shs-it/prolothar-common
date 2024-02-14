# -*- coding: utf-8 -*-

import unittest
import prolothar_common.models.patterns as patterns

class TestPatterns(unittest.TestCase):

    def test_is_tandem_array(self):
        self.assertTrue(patterns.is_tandem_array(
                ['a', 'b', 'a', 'b'], 0, ['a', 'b']),
            msg='(a,b)^2 should be a tandem array')

        self.assertFalse(patterns.is_tandem_array(
                ['a', 'b', 'a', 'b'], 1, ['b', 'a']),
            msg='(b,a)^1 should not be a tandem array')

        try:
            patterns.TandemArray(['a', 'b', 'a', 'b'], 1, ['b', 'a'], 1)
        except ValueError:
            pass

    def test_is_maximal_tandem_array(self):
        self.assertFalse(patterns.TandemArray(
                ['a', 'b', 'a', 'b', 'a', 'b'], 0, ['a', 'b'], 2).is_maximal())

        self.assertFalse(patterns.TandemArray(
                ['a', 'b', 'a', 'b', 'a', 'b'], 2, ['a', 'b'], 2).is_maximal())

        self.assertTrue(patterns.TandemArray(
                ['a', 'b', 'a', 'b', 'a', 'b'], 0, ['a', 'b'], 3).is_maximal())

    def test_has_primitive_tandem_repeat_type(self):
        self.assertTrue(patterns
                .TandemArray(['a', 'b', 'a', 'b', 'a', 'b'], 0, ['a', 'b'], 2)
                .has_primitive_tandem_repeat_type())
        self.assertFalse(patterns
                .TandemArray(['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b'], 0,
                             ['a', 'b', 'a', 'b'], 2)
                .has_primitive_tandem_repeat_type())
        self.assertFalse(patterns
                .TandemArray(['a', 'a', 'a', 'a'], 0,
                             ['a', 'a'], 2)
                .has_primitive_tandem_repeat_type())
        self.assertTrue(patterns
                .TandemArray(['a', 'a', 'a', 'a'], 0,
                             ['a'], 4)
                .has_primitive_tandem_repeat_type())
        self.assertTrue(patterns
                .TandemArray(['a', 'a', 'b', 'a', 'a', 'b'], 0,
                             ['a', 'a', 'b'], 2)
                .has_primitive_tandem_repeat_type())

    def is_maximal_pair(self):
        self.assertTrue(patterns.is_maximal_pair(
                ['a', 'a', 'b', 'c', 'd', 'b', 'b', 'c', 'd', 'a'],
                (2,5), (6,9)))
        self.assertTrue(patterns.is_maximal_pair(
                ['a', 'a', 'b', 'c', 'd', 'b', 'b', 'c', 'd', 'a'],
                (0,1), (1,2)))
        self.assertTrue(patterns.is_maximal_pair(
                ['a', 'a', 'b', 'c', 'd', 'b', 'b', 'c', 'd', 'a'],
                (0,1), (9,10)))
        self.assertTrue(patterns.is_maximal_pair(
                ['a', 'a', 'b', 'c', 'd', 'b', 'b', 'c', 'd', 'a'],
                (1,2), (9,10)))
        self.assertFalse(patterns.is_maximal_pair(
                ['a', 'a', 'b', 'c', 'd', 'b', 'b', 'c', 'd', 'a'],
                (1,2), (2,3)))
        self.assertFalse(patterns.is_maximal_pair(
                ['a', 'a', 'b', 'c', 'd', 'b', 'b', 'c', 'd', 'a'],
                (2,4), (6,8)))
        self.assertFalse(patterns.is_maximal_pair(
                ['a', 'a', 'b', 'c', 'd', 'b', 'b', 'c', 'd', 'a'],
                (3,5), (7,9)))

    def test_find_maximal_repeats(self):
        maximal_repeats = patterns.find_maximal_repeats(['a', 'a', 'b', 'c', 'd', 'b', 'b', 'c', 'd', 'a'])
        self.assertListEqual(
                [['a'], ['b'], ['b', 'c', 'd'], ['c', 'd'], ['d']],
                maximal_repeats)

    def test_find_super_maximal_repeats(self):
        super_maximal_repeats = patterns.find_super_maximal_repeats(
                ['a', 'a', 'b', 'c', 'd', 'b', 'b', 'c', 'd', 'a'])
        self.assertListEqual(
                [['a'], ['b', 'c', 'd']],
                super_maximal_repeats)

    def test_find_near_super_maximal_repeats(self):
        near_super_maximal_repeats = patterns.find_near_super_maximal_repeats(
                ['b', 'b', 'b', 'c', 'd', 'b', 'b', 'b', 'c', 'c', 'a', 'a'])
        self.assertCountEqual(
                [['c'], ['b', 'b', 'b', 'c'], ['a']],
                near_super_maximal_repeats)

    def test_find_primitive_tandem_repeats(self):
        self.assertCountEqual(
            [[0],[1,2,3]],
            patterns.find_primitive_tandem_repeats([0,0,4,0,0,1,2,3,1,2,3]))
        self.assertCountEqual(
            [[0],[0,0,1],[1,2,3]],
            patterns.find_primitive_tandem_repeats([0,0,1,0,0,1,2,3,1,2,3]))
        self.assertCountEqual(
            [[0],[4,5],[5,4]],
            patterns.find_primitive_tandem_repeats([0,0,1,2,3,4,5,4,5,4,5,6]))

    def test_create_tandem_arrays_from_repeat_types(self):
        primitive_tandem_repeats = [['a', 'b'], ['c']]
        sequence = ['a', 'b', 'a', 'b', 'c', 'a', 'b', 'c', 'c', 'c', 'a', 'b']
        expected_tandem_arrays = [
            (0, ['a', 'b'], 2),
            (4, ['c'], 1),
            (5, ['a', 'b'], 1),
            (7, ['c'], 3),
            (10, ['a', 'b'], 1)
        ]
        actual_tandem_arrays = patterns.create_tandem_arrays_from_repeat_types(
                        primitive_tandem_repeats, sequence)
        self.assertListEqual(expected_tandem_arrays, actual_tandem_arrays)

if __name__ == '__main__':
    unittest.main()