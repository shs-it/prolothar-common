# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.dataset import Dataset
from prolothar_common.models.dataset.instance import Instance
from prolothar_common.models.dataset.transformer.one_hot_encoding import OneHotEncoding

class TestOneHotEncoding(unittest.TestCase):

    def test_transform(self):
        dataset = Dataset(['color'],[])
        colors = ['red', 'blue', 'yellow']
        for i, color in enumerate(colors):
            dataset.add_instance(Instance(i, {'color': color}))

        transformed_dataset = OneHotEncoding().transform(dataset)

        expected_dataset = Dataset(['color blue', 'color red', 'color yellow'], [])
        expected_dataset.add_instance(
            Instance(0, {'color red': 1, 'color blue': 0, 'color yellow': 0}))
        expected_dataset.add_instance(
            Instance(1, {'color red': 0, 'color blue': 1, 'color yellow': 0}))
        expected_dataset.add_instance(
            Instance(2, {'color red': 0, 'color blue': 0, 'color yellow': 1}))

        self.assertEqual(expected_dataset, transformed_dataset)

        twice_transformed_dataset = OneHotEncoding().transform(transformed_dataset)
        self.assertEqual(expected_dataset, twice_transformed_dataset)
        self.assertEqual(transformed_dataset, twice_transformed_dataset)

if __name__ == '__main__':
    unittest.main()