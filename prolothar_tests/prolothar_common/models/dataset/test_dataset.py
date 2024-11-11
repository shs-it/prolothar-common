# -*- coding: utf-8 -*-

import unittest

from multiprocessing import Process, Manager, Queue

import pandas as pd
from pandas.testing import assert_frame_equal

from prolothar_common.models.dataset import Dataset
from prolothar_common.models.dataset.instance import Instance

def count_color(dataset: Dataset, color: str, queue: Queue):
    count = 0
    for instance in dataset:
        if instance['color'] == color:
            count += 1
    queue.put((color, count))

class TestDataset(unittest.TestCase):

    def test_create_manually_unknown_feature_in_instance(self):
        dataset = Dataset([], [])
        try:
            dataset.add_instance(
                    Instance(1, {'unknown': 42}))
            self.fail('should have thrown ValueError')
        except ValueError:
            pass

    def test_create_manually_missing_feature_in_instance(self):
        dataset = Dataset(['known', 'unknown'], [])
        try:
            dataset.add_instance(
                    Instance(1, {'known': 42}))
            self.fail('should have thrown ValueError')
        except ValueError:
            pass

    def test_create_manually_add_instance_with_same_id(self):
        dataset = Dataset(['a'], [])
        try:
            dataset.add_instance(
                    Instance(1, {'a': 42}))
            dataset.add_instance(
                    Instance(1, {'a': 42}))
            self.fail('should have thrown ValueError')
        except ValueError:
            pass

    def test_create_manually(self):
        dataset = Dataset(['color'],['size'])
        dataset.add_instance(
                    Instance(1, {'color': 'red', 'size': 100}))
        dataset.add_instance(
                    Instance(2, {'color': 'blue', 'size': 100}))
        self.assertEqual(2, len(dataset))
        self.assertCountEqual(
                {'red', 'blue'},
                dataset.get_attribute_by_name('color').get_unique_values())
        self.assertCountEqual(
                {100},
                dataset.get_attribute_by_name('size').get_unique_values())

    def test_to_dataframe(self):
        dataset = Dataset(['color'],['size'])
        for i in range(5):
            features = {'color': 'red' if i == 0 else 'blue', 'size': i * 10}
            dataset.add_instance(Instance(i, features))
        actual_df = dataset.to_dataframe()
        expected_df = pd.DataFrame(
            [
                ['red', 0],
                ['blue', 10],
                ['blue', 20],
                ['blue', 30],
                ['blue', 40],
            ], columns=['color', 'size'], index=list(range(5)))
        assert_frame_equal(actual_df, expected_df)
        self.assertEqual(dataset, Dataset.create_from_pandas(expected_df, ['color'], ['size']))

    def test_create_from_arff(self):
        dataset = Dataset(['color'],['size'])
        for i in range(5):
            features = {'color': 'red' if i == 0 else 'blue', 'size': i * 10}
            dataset.add_instance(Instance(i, features))

        reloaded_dataset = Dataset.create_from_arff(dataset.export_to_arff())

        self.assertEqual(dataset, reloaded_dataset)

    def test_group_by_categorical_attribute(self):
        dataset = Dataset(['color'],['size'])
        dataset.add_instance(
                    Instance(1, {'color': 'red', 'size': 100}))
        dataset.add_instance(
                    Instance(2, {'color': 'blue', 'size': 100}))

        grouped_datasets = dataset.group_by_categorical_attribute('color')
        self.assertEqual(2, len(grouped_datasets))
        self.assertCountEqual(['red', 'blue'], grouped_datasets.keys())

if __name__ == '__main__':
    unittest.main()