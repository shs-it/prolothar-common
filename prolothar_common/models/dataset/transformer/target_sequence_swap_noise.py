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

class TargetSequenceSwapNoise(DatasetTransformer):
    """
    randomly swaps neighbored events from TargetSequenceInstances with a certain probability
    """

    def __init__(
        self, noise_probability: float, allow_multiple_swaps: bool = False,
        random_seed: Union[int, None] = None):
        """
        configures the amount and type of swap noise

        Parameters
        ----------
        noise_probability : float
            between 0 and 1 (both inclusive)
        allow_multiple_swaps : bool, optional
            if True, then an event can be swapped multiple times to a later position.
            otherwise an event can never change more than one position. by default False
        random_seed : Union[int, None], optional
            [description], by default None
        """
        self.__noise_probability = noise_probability
        self.__random_generator = Random(random_seed)
        self.__allow_multiple_swaps = allow_multiple_swaps

    def inplace_transform(self, dataset: Dataset) -> Dataset:
        for instance in dataset:
            instance.set_target_sequence(self.__apply_noise(instance.get_target_sequence()))

    def __apply_noise(self, sequence: Tuple[str]) -> List[str]:
        noisy_sequence = []
        stack = list(sequence[::-1])
        while len(stack) > 1:
            event = stack.pop()
            if self.__random_generator.random() < self.__noise_probability:
                next_event = stack.pop()
                noisy_sequence.append(next_event)
                if self.__allow_multiple_swaps:
                    stack.append(event)
                else:
                    noisy_sequence.append(event)
            else:
                noisy_sequence.append(event)
        #sequence can be completely empty
        if stack:
            noisy_sequence.append(stack.pop())
        return noisy_sequence


