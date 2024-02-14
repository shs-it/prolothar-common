# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.dataset import TargetSequenceDataset
from prolothar_common.models.dataset.target_sequence_dataset import TargetSequenceInstance
from prolothar_common.models.dataset.transformer import TargetSequenceSwapNoise

class TestTargetSequenceSwapNoise(unittest.TestCase):

    def setUp(self):
        dataset = TargetSequenceDataset([],[])
        dataset.add_instance(TargetSequenceInstance(0, {}, ['A', 'B', 'C']))
        dataset.add_instance(TargetSequenceInstance(1, {}, ['A', 'B', 'C']))
        dataset.add_instance(TargetSequenceInstance(2, {}, ['A', 'B', 'C']))
        dataset.add_instance(TargetSequenceInstance(3, {}, ['A', 'B', 'C']))
        self.dataset = dataset

    def test_transform_zero_noise(self):
        transformed_dataset = TargetSequenceSwapNoise(0.0).transform(self.dataset)
        self.assertEqual(self.dataset, transformed_dataset)

    def test_transform_noise_only_allow_multiple_swaps(self):
        transformed_dataset = TargetSequenceSwapNoise(
            1.0, allow_multiple_swaps=True).transform(self.dataset)

        expected_dataset = TargetSequenceDataset([],[])
        expected_dataset.add_instance(TargetSequenceInstance(0, {}, ['B', 'C', 'A']))
        expected_dataset.add_instance(TargetSequenceInstance(1, {}, ['B', 'C', 'A']))
        expected_dataset.add_instance(TargetSequenceInstance(2, {}, ['B', 'C', 'A']))
        expected_dataset.add_instance(TargetSequenceInstance(3, {}, ['B', 'C', 'A']))

        self.assertEqual(expected_dataset, transformed_dataset)

    def test_transform_noise_only_prohibit_multiple_swaps(self):
        transformed_dataset = TargetSequenceSwapNoise(
            1.0, allow_multiple_swaps=False).transform(self.dataset)

        expected_dataset = TargetSequenceDataset([],[])
        expected_dataset.add_instance(TargetSequenceInstance(0, {}, ['B', 'A', 'C']))
        expected_dataset.add_instance(TargetSequenceInstance(1, {}, ['B', 'A', 'C']))
        expected_dataset.add_instance(TargetSequenceInstance(2, {}, ['B', 'A', 'C']))
        expected_dataset.add_instance(TargetSequenceInstance(3, {}, ['B', 'A', 'C']))

        self.assertEqual(expected_dataset, transformed_dataset)

if __name__ == '__main__':
    unittest.main()