# -*- coding: utf-8 -*-

from typing import Union, Tuple, List
from random import Random

from prolothar_common.models.dataset.transformer.dataset_transformer import DatasetTransformer

from prolothar_common.models.dataset import Dataset

class TargetSequenceRemoveNoise(DatasetTransformer):
    """
    removes random events from TargetSequenceInstances with a certain probability
    """

    def __init__(self, noise_probability: float, random_seed: Union[int, None] = None):
        self.__noise_probability = noise_probability
        self.__random_generator = Random(random_seed)

    def inplace_transform(self, dataset: Dataset) -> Dataset:
        for instance in dataset:
            instance.set_target_sequence(self.__apply_noise(instance.get_target_sequence()))

    def __apply_noise(self, sequence: Tuple[str]) -> List[str]:
        return [
            event for event in sequence
            if self.__random_generator.random() > self.__noise_probability
        ]
