# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.dataset import Dataset
from prolothar_common.models.dataset.instance import Instance
from prolothar_common.models.dataset.transformer import MinMaxScaling

class TestMinMaxScaling(unittest.TestCase):

    def test_transform(self):
        dataset = Dataset(['color'],['size'])
        sizes = [1, 1, 32, 22, 35, 21, 5, 2, 3, 6, 54, 32, 21]
        for i, size in enumerate(sizes):
            dataset.add_instance(Instance(i, {
                'size': size, 'color': 'red' if i % 2 == 0 else 'blue'
            }))

        transformed_dataset = MinMaxScaling().transform(dataset)

        expected_dataset = Dataset(['color'],['size'])
        expected_sizes = [(s - 1) / 53 for s in sizes]
        for i, size in enumerate(expected_sizes):
            expected_dataset.add_instance(Instance(i, {
                'size': size, 'color': 'red' if i % 2 == 0 else 'blue'
            }))

        self.assertEqual(expected_dataset, transformed_dataset)

if __name__ == '__main__':
    unittest.main()