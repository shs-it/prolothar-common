# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.dataset import TargetSequenceDataset
from prolothar_common.models.dataset.target_sequence_dataset import TargetSequenceInstance
from prolothar_common.models.dataset.transformer.target_sequence_remove_noise import TargetSequenceRemoveNoise

class TestTargetSequenceRemoveNoise(unittest.TestCase):

    def setUp(self):
        dataset = TargetSequenceDataset([],[])
        dataset.add_instance(TargetSequenceInstance(0, {}, ['A', 'B', 'C']))
        dataset.add_instance(TargetSequenceInstance(1, {}, ['A', 'B', 'C']))
        dataset.add_instance(TargetSequenceInstance(2, {}, ['A', 'B', 'C']))
        dataset.add_instance(TargetSequenceInstance(3, {}, ['A', 'B', 'C']))
        self.dataset = dataset

    def test_transform_zero_noise(self):
        transformed_dataset = TargetSequenceRemoveNoise(0.0).transform(self.dataset)
        self.assertEqual(self.dataset, transformed_dataset)

    def test_transform_noise_only(self):
        transformed_dataset = TargetSequenceRemoveNoise(1.0).transform(self.dataset)
        for instance in transformed_dataset:
            self.assertEqual(0, len(instance.get_target_sequence()))

if __name__ == '__main__':
    unittest.main()