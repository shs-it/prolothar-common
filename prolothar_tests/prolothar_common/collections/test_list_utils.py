# -*- coding: utf-8 -*-

import unittest
import prolothar_common.collections.list_utils as list_utils
from hypothesis import given
from hypothesis.strategies import composite, integers

@composite
def same_len_lists(draw, min_nr_of_lists, max_nr_of_lists, min_nr_of_elements, max_nr_of_elements):
    nr_of_lists = draw(integers(min_value=min_nr_of_lists, max_value=max_nr_of_lists))
    nr_of_elements = draw(integers(min_value=min_nr_of_elements, max_value=max_nr_of_elements))
    a_list = list(range(nr_of_elements))
    return [
        a_list
        for _ in range(nr_of_lists)
    ]

class TestListUtils(unittest.TestCase):

    def test_is_sublist_bm(self):
        self.assertTrue(list_utils.is_sublist_bm([1,2,3,4],
                                              []))

        self.assertTrue(list_utils.is_sublist_bm([1,2,3,4],
                                              [1]))
        self.assertTrue(list_utils.is_sublist_bm([1,2,3,4],
                                              [2]))
        self.assertTrue(list_utils.is_sublist_bm([1,2,3,4],
                                              [3]))
        self.assertTrue(list_utils.is_sublist_bm([1,2,3,4],
                                              [4]))

        self.assertTrue(list_utils.is_sublist_bm([1,2,3,4],
                                              [1,2]))
        self.assertTrue(list_utils.is_sublist_bm([1,2,3,4],
                                              [2,3]))
        self.assertTrue(list_utils.is_sublist_bm([1,2,3,4],
                                              [3,4]))

        self.assertTrue(list_utils.is_sublist_bm([1,2,3,4],
                                              [1,2,3]))
        self.assertTrue(list_utils.is_sublist_bm([1,2,3,4],
                                              [2,3,4]))

        self.assertTrue(list_utils.is_sublist_bm([1,2,3,4],
                                              [1,2,3,4]))

        self.assertFalse(list_utils.is_sublist_bm([1,2,3,4],
                                               [1,3,4]))

        self.assertFalse(list_utils.is_sublist_bm([1,2,3,4],
                                               [1,2,5]))

        self.assertFalse(list_utils.is_sublist_bm([1,2,3,4],
                                               [4,3]))

    def test_search_sublist_all_occurences(self):
        self.assertListEqual([], list_utils.search_sublist_all_occurences(
                [1,2,3,4], [5]))
        self.assertListEqual([0,1,2,3,4], list_utils.search_sublist_all_occurences(
                [1,2,3,4], []))
        self.assertListEqual([0,1], list_utils.search_sublist_all_occurences(
                [1,1,1,4], [1,1]))
        self.assertListEqual([0,3], list_utils.search_sublist_all_occurences(
                [1,2,3,1,2], [1,2]))
        self.assertListEqual([1,3], list_utils.search_sublist_all_occurences(
                [1,2,3,2], [2]))

    def test_view_of_n_partitions(self):
        self.assertListEqual(
            [[1,2,3],[4,5,6],[7,8]],
            list_utils.view_of_n_partitions([1,2,3,4,5,6,7,8], 3)
        )
        self.assertListEqual(
            [[1,2,3],[4,5],[6,7],[8,9]],
            list_utils.view_of_n_partitions([1,2,3,4,5,6,7,8,9], 4)
        )
        self.assertListEqual(
            [[1],[2],[3]],
            list_utils.view_of_n_partitions([1,2,3], 4)
        )
        self.assertListEqual(
            [[1,2,3],[4,5,6],[7,8,9]],
            list_utils.view_of_n_partitions([1,2,3,4,5,6,7,8,9], 3)
        )
        self.assertListEqual(
            [[1,2,3,4,5,6,7,8,9]],
            list_utils.view_of_n_partitions([1,2,3,4,5,6,7,8,9], 1)
        )

    def test_enumerate_reversed(self):
        expected = [(2, 'c'), (1, 'b'), (0, 'a')]
        j = 0
        for i,v in list_utils.enumerate_reversed(['a','b','c']):
            self.assertEqual(expected[j], (i,v))
            j += 1

    def test_deep_flatten(self):
        self.assertListEqual([], list_utils.deep_flatten([]))
        self.assertListEqual([], list_utils.deep_flatten([[]]))
        self.assertListEqual([], list_utils.deep_flatten([[[]]]))
        self.assertListEqual([1,2,3], list_utils.deep_flatten([1,2,3]))
        self.assertListEqual(
            [1,2,3,4,5], list_utils.deep_flatten([1, [2], [[3], 4], 5]))

    def test_iterate_self_product(self):
        self.assertListEqual([], list(list_utils.iterate_self_product([])))
        self.assertListEqual(
            [], list(list_utils.iterate_self_product([], skip_diagonal=True)))

        self.assertListEqual([(1,1)], list(list_utils.iterate_self_product([1])))
        self.assertListEqual(
            [], list(list_utils.iterate_self_product([1], skip_diagonal=True)))

        self.assertListEqual(
            [(1,1), (1,2), (2,1), (2,2)],
            list(list_utils.iterate_self_product([1,2])))
        self.assertListEqual(
            [(1,2), (2,1)],
            list(list_utils.iterate_self_product([1,2], skip_diagonal=True)))

    def test_longest_common_sublist(self):
        length, indices = list_utils.longest_common_sublists([], [])
        self.assertEqual(0, length)
        self.assertCountEqual([], indices)

        length, indices = list_utils.longest_common_sublists([0, 3, 5], [7, 6])
        self.assertEqual(0, length)
        self.assertCountEqual([], indices)

        length, indices = list_utils.longest_common_sublists(list('abcdef'), list('zzzcdez'))
        self.assertEqual(3, length)
        self.assertCountEqual([(2,3)], indices)

        length, indices = list_utils.longest_common_sublists(list('ABAB'), list('BABA'))
        self.assertEqual(3, length)
        self.assertCountEqual([(0,1),(1,0)], indices)

        length, indices = list_utils.longest_common_sublists(list('BBCCDD'), list('BBDDCC'))
        self.assertEqual(2, length)
        self.assertCountEqual([(0,0), (2,4), (4,2)], indices)

    @given(same_len_lists(0,3,0,10))
    def test_shuffle_together(self, list_of_lists):
        shuffled_list_of_lists = list_utils.shuffle_together(*list_of_lists)
        i = 0
        while True:
            try:
                all_elements_at_i = [l[i] for l in shuffled_list_of_lists]
                if all_elements_at_i:
                    self.assertEqual(1, len(set(all_elements_at_i)))
                else:
                    break
                i += 1
            except IndexError:
                break

if __name__ == '__main__':
    unittest.main()