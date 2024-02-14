'''
    This file is part of Prolothar-Common (More Info: https://github.com/shs-it/prolothar-common).

    Prolothar-Common is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Prolothar-Common is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Prolothar-Common. If not, see <https://www.gnu.org/licenses/>.
'''

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
