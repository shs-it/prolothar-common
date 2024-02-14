# -*- coding: utf-8 -*-

import unittest
from dhcollections.tuple_utils import all_splits_of_size_k

class TestTupleUtils(unittest.TestCase):

    def test_all_splits_of_size_k(self):
        self.assertRaises(
            ValueError,
            lambda: all_splits_of_size_k((1,2,3,4,5), 0),
        )

        self.assertEqual(
            all_splits_of_size_k((1,2,3,4,5), 1),
            [
                ((1,), (2,3,4,5)),
                ((2,), (1,3,4,5)),
                ((3,), (1,2,4,5)),
                ((4,), (1,2,3,5)),
                ((5,), (1,2,3,4))
            ]
        )

        self.assertEqual(
            all_splits_of_size_k((1,2,3,4,5), 2),
            [
                ((1, 2), (3, 4, 5)),
                ((1, 3), (2, 4, 5)),
                ((1, 4), (2, 3, 5)),
                ((1, 5), (2, 3, 4)),
                ((2, 3), (1, 4, 5)),
                ((2, 4), (1, 3, 5)),
                ((2, 5), (1, 3, 4)),
                ((3, 4), (1, 2, 5)),
                ((3, 5), (1, 2, 4)),
                ((4, 5), (1, 2, 3))
            ]
        )

        self.assertEqual(
            all_splits_of_size_k((1,2,3,4,5), 3),
            [
                ((1, 2, 3), (4, 5)),
                ((1, 2, 4), (3, 5)),
                ((1, 2, 5), (3, 4)),
                ((1, 3, 4), (2, 5)),
                ((1, 3, 5), (2, 4)),
                ((1, 4, 5), (2, 3)),
                ((2, 3, 4), (1, 5)),
                ((2, 3, 5), (1, 4)),
                ((2, 4, 5), (1, 3)),
                ((3, 4, 5), (1, 2))
            ]
        )

        self.assertEqual(
            all_splits_of_size_k((1,2,3,4,5), 4),
            [
                ((1,2,3,4), (5,)),
                ((1,2,3,5), (4,)),
                ((1,2,4,5), (3,)),
                ((1,3,4,5), (2,)),
                ((2,3,4,5), (1,))
            ]
        )

        self.assertEqual(
            all_splits_of_size_k((1,2,3,4,5), 5),
            [
                ((1,2,3,4,5), tuple())
            ]
        )

        self.assertEqual(
            all_splits_of_size_k((1,2,3,4,5), 6),
            []
        )


if __name__ == '__main__':
    unittest.main()