# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.dataset import Dataset
from prolothar_common.models.dataset.instance import Instance
from prolothar_common.models.dataset.transformer.trainable_q_based_discretization import TrainableQuantileBasedDiscretization

class TestTraininableQuantileBasedDiscretization(unittest.TestCase):

    def test_transform(self):
        dataset = Dataset([],['size'])
        sizes = [1, 1, 32, 22, 35, 21, 5, 2, 3, 6, 54, 32, 21]
        for i, size in enumerate(sizes):
            dataset.add_instance(Instance(i, {'size': size}))

        transformer = TrainableQuantileBasedDiscretization.train(dataset, 3)
        transformed_dataset = transformer.transform(dataset)

        expected_dataset = Dataset(['size'],[])
        expected_sizes = [
            '(0.999, 5.0]', '(0.999, 5.0]', '(22.0, 54.0]', '(5.0, 22.0]',
            '(22.0, 54.0]', '(5.0, 22.0]', 
            '(0.999, 5.0]', 
            '(0.999, 5.0]',
            '(0.999, 5.0]', '(5.0, 22.0]', '(22.0, 54.0]', '(22.0, 54.0]',
            '(5.0, 22.0]']
        for i, size in enumerate(expected_sizes):
            expected_dataset.add_instance(Instance(i, {'size': size}))
        self.assertEqual(expected_dataset, transformed_dataset)

if __name__ == '__main__':
    unittest.main()