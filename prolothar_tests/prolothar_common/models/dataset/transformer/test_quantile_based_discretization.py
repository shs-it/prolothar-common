# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.dataset import Dataset
from prolothar_common.models.dataset.instance import Instance
from prolothar_common.models.dataset.transformer.quantile_based_discretization import QuantileBasedDiscretization

class TestQuantileBasedDiscretization(unittest.TestCase):

    def test_transform(self):
        dataset = Dataset([],['size'])
        sizes = [1, 1, 32, 22, 35, 21, 5, 2, 3, 6, 54, 32, 21]
        for i, size in enumerate(sizes):
            dataset.add_instance(Instance(i, {'size': size}))

        transformed_dataset = QuantileBasedDiscretization(3).transform(dataset)

        expected_dataset = Dataset(['size'],[])
        expected_sizes = [
            '[1, 5.0]', 
            '[1, 5.0]', 
            '(22.0, 54]',
            '(5.0, 22.0]',
            '(22.0, 54]', 
            '(5.0, 22.0]', 
            '[1, 5.0]', 
            '[1, 5.0]',
            '[1, 5.0]', 
            '(5.0, 22.0]', 
            '(22.0, 54]', 
            '(22.0, 54]',
            '(5.0, 22.0]']
        for i, size in enumerate(expected_sizes):
            expected_dataset.add_instance(Instance(i, {'size': size}))

        self.assertEqual(expected_dataset, transformed_dataset)

    def test_transform_nr_of_unique_values_equals_nr_of_bins(self):
        dataset = Dataset([],['size'])
        sizes = [1, 1, 2, 2, 3, 1, 3]
        for i, size in enumerate(sizes):
            dataset.add_instance(Instance(i, {'size': size}))

        transformed_dataset = QuantileBasedDiscretization(3).transform(dataset)
        expected_dataset = Dataset(['size'],[])
        expected_sizes = [
            '1', '1', '2', '2', '3', '1', '3']
        for i, size in enumerate(expected_sizes):
            expected_dataset.add_instance(Instance(i, {'size': size}))

        self.assertEqual(expected_dataset, transformed_dataset)


if __name__ == '__main__':
    unittest.main()