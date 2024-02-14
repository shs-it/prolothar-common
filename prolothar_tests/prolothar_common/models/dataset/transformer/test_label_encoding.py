# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.dataset import Dataset
from prolothar_common.models.dataset.instance import Instance
from prolothar_common.models.dataset.transformer.label_encoding import LabelEncoding

class TestLabelEncoding(unittest.TestCase):

    def test_transform(self):
        dataset = Dataset(['color'],[])
        colors = ['red', 'blue', 'yellow', 'red']
        for i, color in enumerate(colors):
            dataset.add_instance(Instance(i, {'color': color}))

        transformed_dataset = LabelEncoding().transform(dataset)

        expected_dataset = Dataset(['color'], [])
        expected_dataset.add_instance(Instance(0, {'color': 1}))
        expected_dataset.add_instance(Instance(1, {'color': 0}))
        expected_dataset.add_instance(Instance(2, {'color': 2}))
        expected_dataset.add_instance(Instance(3, {'color': 1}))

        self.assertEqual(expected_dataset, transformed_dataset)

        twice_transformed_dataset = LabelEncoding().transform(transformed_dataset)
        self.assertEqual(expected_dataset, twice_transformed_dataset)
        self.assertEqual(transformed_dataset, twice_transformed_dataset)

    def test_transform_with_boolean_attribute(self):
        dataset = Dataset(['fixed'],[])
        fixed_values = [False, False, True, False]
        for i, fixed in enumerate(fixed_values):
            dataset.add_instance(Instance(i, {'fixed': fixed}))

        transformed_dataset = LabelEncoding().transform(dataset)

        expected_dataset = Dataset(['fixed'], [])
        expected_dataset.add_instance(Instance(0, {'fixed': 0}))
        expected_dataset.add_instance(Instance(1, {'fixed': 0}))
        expected_dataset.add_instance(Instance(2, {'fixed': 1}))
        expected_dataset.add_instance(Instance(3, {'fixed': 0}))

        self.assertEqual(expected_dataset, transformed_dataset)

        twice_transformed_dataset = LabelEncoding().transform(transformed_dataset)
        self.assertEqual(expected_dataset, twice_transformed_dataset)
        self.assertEqual(transformed_dataset, twice_transformed_dataset)

if __name__ == '__main__':
    unittest.main()
