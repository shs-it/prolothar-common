# -*- coding: utf-8 -*-

from typing import Union, Tuple, List, Sequence
from random import Random

from prolothar_common.models.dataset.transformer.dataset_transformer import DatasetTransformer

from prolothar_common.models.dataset import Dataset

class TargetSequenceAddNoise(DatasetTransformer):
    """
    adds random events to TargetSequenceInstances with a certain probability
    """

    def __init__(
            self, noise_alphabet: Sequence[str], noise_probability: float,
            random_seed: Union[int, None] = None):
        self.__noise_probability = noise_probability
        self.__random_generator = Random(random_seed)
        self.__noise_alphabet = noise_alphabet

    def inplace_transform(self, dataset: Dataset) -> Dataset:
        for instance in dataset:
            instance.set_target_sequence(self.__apply_noise(instance.get_target_sequence()))

    def __apply_noise(self, sequence: Tuple[str]) -> List[str]:
        noisy_sequence = []
        self.__append_noise_or_not(noisy_sequence)
        for event in sequence:
            noisy_sequence.append(event)
            self.__append_noise_or_not(noisy_sequence)
        return noisy_sequence

    def __append_noise_or_not(self, noisy_sequence: List[str]):
        if self.__random_generator.random() < self.__noise_probability:
            noisy_sequence.append(self.__random_generator.choice(self.__noise_alphabet))

