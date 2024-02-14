# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.dataset import ClassificationDataset
from prolothar_common.models.dataset.instance import ClassificationInstance

class TestClassificationDataset(unittest.TestCase):

    def test_export_to_arff(self):
        dataset = ClassificationDataset(['color'],['size'])
        dataset.add_instance(ClassificationInstance(
            1, {'color': 'red', 'size': 100}, 'A'))
        dataset.add_instance(ClassificationInstance(
            2, {'color': 'blue', 'size': 42}, 'B'))

        arff = dataset.export_to_arff(relation_name='TestDataset')
        self.assertTrue(arff)

        with open('prolothar_tests/resources/datasets/dataset_with_class.arff', 'r') as f:
            expected_arff = f.read()

        self.assertEqual(expected_arff, arff)

    def test_copy_and_eq(self):
        dataset = ClassificationDataset(['color'],['size'])
        dataset.add_instance(ClassificationInstance(
            1, {'color': 'red', 'size': 100}, 'A'))
        dataset.add_instance(ClassificationInstance(
            2, {'color': 'blue', 'size': 42}, 'A'))

        copy = dataset.copy()
        self.assertEqual(copy, dataset)

        copy.add_instance(ClassificationInstance(
            3, {'color': 'blue', 'size': 43}, 'B'))
        self.assertNotEqual(copy, dataset)
        self.assertEqual(copy, copy)
        self.assertEqual(dataset, dataset)

if __name__ == '__main__':
    unittest.main()