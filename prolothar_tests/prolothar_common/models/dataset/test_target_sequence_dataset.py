# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.dataset import TargetSequenceDataset
from prolothar_common.models.dataset.instance import TargetSequenceInstance

class TestTargetSequenceDataset(unittest.TestCase):

    def test_export_to_arff(self):
        dataset = TargetSequenceDataset(['color'],['size'])
        dataset.add_instance(TargetSequenceInstance(
            1, {'color': 'red', 'size': 100}, []))
        dataset.add_instance(TargetSequenceInstance(
            2, {'color': 'blue', 'size': 42}, ['A', 'B']))

        arff = dataset.export_to_arff(relation_name='TestDataset', sequence_element_separator=',')
        self.assertTrue(arff)

        with open('prolothar_tests/resources/datasets/dataset_with_target_sequences.arff', 'r') as f:
            expected_arff = f.read()

        self.assertEqual(expected_arff, arff)

    def test_create_from_arff(self):
        expected_dataset = TargetSequenceDataset(['color'],['size'])
        expected_dataset.add_instance(TargetSequenceInstance(
            1, {'color': 'red', 'size': 100}, []))
        expected_dataset.add_instance(TargetSequenceInstance(
            2, {'color': 'blue', 'size': 42}, ['A', 'B']))

        with open('prolothar_tests/resources/datasets/dataset_with_target_sequences.arff', 'r') as f:
            dataset = TargetSequenceDataset.create_from_arff(f.read(), 'sequence')

        self.assertEqual(expected_dataset, dataset)

    def test_copy_and_eq(self):
        dataset = TargetSequenceDataset(['color'],['size'])
        dataset.add_instance(TargetSequenceInstance(
            1, {'color': 'red', 'size': 100}, []))
        dataset.add_instance(TargetSequenceInstance(
            2, {'color': 'blue', 'size': 42}, ['A', 'B']))

        copy = dataset.copy()
        self.assertEqual(copy, dataset)

        copy.add_instance(TargetSequenceInstance(
            3, {'color': 'blue', 'size': 43}, ['A', 'B']))
        self.assertNotEqual(copy, dataset)
        self.assertEqual(copy, copy)
        self.assertEqual(dataset, dataset)

    def test_split(self):
        dataset = TargetSequenceDataset(['color'],['size'])
        for i in range(100):
            dataset.add_instance(TargetSequenceInstance(
                i, {'color': 'red', 'size': 100}, []))

        trainset,testset = dataset.split(0.2)
        self.assertEqual(len(trainset), 80)
        self.assertEqual(len(testset), 20)

        trainset,testset = dataset.split(0.222)
        self.assertEqual(len(trainset), 77)
        self.assertEqual(len(testset), 23)

        trainset,testset = dataset.split(0.0001)
        self.assertEqual(len(trainset), 99)
        self.assertEqual(len(testset), 1)

        trainset,testset = dataset.split(0.9999)
        self.assertEqual(len(trainset), 0)
        self.assertEqual(len(testset), 100)

    def test_random_subset(self):
        dataset = TargetSequenceDataset(['color'],['size'])
        for i in range(100):
            dataset.add_instance(TargetSequenceInstance
            (i, {'color': 'red', 'size': 100}, []))

        subset_1 = dataset.random_subset(45, random_seed=42)
        subset_2 = dataset.random_subset(45, random_seed=43)

        self.assertEqual(len(subset_1), 45)
        self.assertEqual(len(subset_2), 45)
        self.assertNotEqual(
            set(instance.get_id() for instance in subset_1),
            set(instance.get_id() for instance in subset_2))

        self.assertEqual(len(dataset.random_subset(0)), 0)
        self.assertEqual(len(dataset.random_subset(100)), 100)

        with self.assertRaises(ValueError):
            dataset.random_subset(-1)
        with self.assertRaises(ValueError):
            dataset.random_subset(101)

        self.assertIsInstance(subset_1, TargetSequenceDataset)
        self.assertIsInstance(subset_2, TargetSequenceDataset)

if __name__ == '__main__':
    unittest.main()