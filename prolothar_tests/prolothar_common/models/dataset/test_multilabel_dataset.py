# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.dataset import MultiLabelDataset
from prolothar_common.models.dataset.instance import MultiLabelInstance

class TestMultilabelDataset(unittest.TestCase):

    def test_export_to_arff(self):
        dataset = MultiLabelDataset(['color'],['size'])
        dataset.add_instance(MultiLabelInstance(
            1, {'color': 'red', 'size': 100}, set(['A'])))
        dataset.add_instance(MultiLabelInstance(
            2, {'color': 'blue', 'size': 42}, set(['B','C'])))

        arff = dataset.export_to_arff(relation_name='TestDataset')
        self.assertTrue(arff)

        with open('prolothar_tests/resources/datasets/dataset_with_multilabel.arff', 'r') as f:
            expected_arff = f.read()

        self.assertEqual(expected_arff, arff)

    def test_create_from_arff(self):
        expected_dataset = MultiLabelDataset(['color'],['size'])
        expected_dataset.add_instance(MultiLabelInstance(
            1, {'color': 'red', 'size': 100}, set(['A'])))
        expected_dataset.add_instance(MultiLabelInstance(
            2, {'color': 'blue', 'size': 42}, set(['B','C'])))

        with open('prolothar_tests/resources/datasets/dataset_with_multilabel.arff', 'r') as f:
            arff = f.read()

        actual_dataset = MultiLabelDataset.create_from_arff(arff, ['A', 'B', 'C'])

        self.assertEqual(expected_dataset, actual_dataset)

    def test_create_from_sparse_arff(self):
        with open('prolothar_tests/resources/datasets/20ng.arff', 'r') as f:
            arff = f.read()

        set_of_labels = set([
            'comp.os_ms_windows_misc', 'religion.rmisc', 'rec.sport.baseball',
            'sci.space', 'comp.sys.mac_hardware', 'sci.med', 'politics.pmisc',
            'rec.autos', 'misc_forsale', 'politics.mideast', 'rec.motorcycles',
            'politics.guns', 'rec.sport.hockey', 'comp.sys.ibm_pc_hardware',
            'comp.graphics', 'sci.crypt', 'sci.electronics', 'religion.christian',
            'religion.atheism', 'comp.windows_x',
        ])
        dataset = MultiLabelDataset.create_from_arff(arff, set_of_labels)

        self.assertEqual(set_of_labels, dataset.get_set_of_labels())

    def test_copy_and_eq(self):
        dataset = MultiLabelDataset(['color'],['size'])
        dataset.add_instance(MultiLabelInstance(
            1, {'color': 'red', 'size': 100}, set(['A'])))
        dataset.add_instance(MultiLabelInstance(
            2, {'color': 'blue', 'size': 42}, set(['B','C'])))

        copy = dataset.copy()
        self.assertEqual(copy, dataset)

        copy.add_instance(MultiLabelInstance(
            3, {'color': 'blue', 'size': 43}, set(['B'])))
        self.assertNotEqual(copy, dataset)
        self.assertEqual(copy, copy)
        self.assertEqual(dataset, dataset)

if __name__ == '__main__':
    unittest.main()
