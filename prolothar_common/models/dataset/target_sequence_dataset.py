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

from typing import Set, Tuple, List, Iterable

from collections import Counter

from prolothar_common.models.dataset.dataset import Dataset
from prolothar_common.models.dataset.instance import TargetSequenceInstance

class TargetSequenceDataset(Dataset):
    """
    a dataset with a sequence target
    """

    def __init__(self, categorical_attribute_names: Iterable[str],
                 numerical_attribute_names: Iterable[str]):
        super().__init__(categorical_attribute_names, numerical_attribute_names)
        self.__set_of_sequence_symbols = set()

    def add_instance(self, instance: TargetSequenceInstance):
        super().add_instance(instance)
        self.__set_of_sequence_symbols.update(instance.get_target_sequence())

    def compute_set_of_unique_sequences(self) -> Set[Tuple[str]]:
        """returns the set of unique target sequences in this dataset"""
        unique_sequences = set()
        for instance in self:
            unique_sequences.add(instance.get_target_sequence())
        return unique_sequences

    def get_set_of_sequence_symbols(self) -> Set[str]:
        return self.__set_of_sequence_symbols

    def _add_attributes_definition_to_arff(self, arff: str, **kwargs) -> str:
        arff = super()._add_attributes_definition_to_arff(arff)

        arff += '\n@ATTRIBUTE "%s" {%s}' % (kwargs.get('sequence_attribute_name', 'sequence'), ','.join(
            '"[%s]"' % kwargs.get('sequence_element_separator', ';').join(sequence)
            for sequence in sorted(
                self.compute_set_of_unique_sequences())
        ))
        return arff

    def _add_instance_to_arff(self, arff: str, instance: TargetSequenceInstance, **kwargs) -> str:
        arff = super()._add_instance_to_arff(arff, instance)
        arff += ',"[%s]"' % kwargs.get('sequence_element_separator', ';').join(
            instance.get_target_sequence())
        return arff

    @staticmethod
    def create_from_arff(arff: str, sequence_attribute: str) -> 'TargetSequenceDataset':
        """
        creates a TargetSequenceDataset from the given ARFF string
        """
        raw_dataset = Dataset.create_from_arff(arff)
        dataset = TargetSequenceDataset(
            raw_dataset.get_categorical_attribute_names(),
            raw_dataset.get_numerical_attribute_names()
        )
        dataset.remove_attribute(sequence_attribute)
        for raw_instance in raw_dataset:
            features = dict(raw_instance.get_features_dict())
            dataset.add_instance(TargetSequenceInstance(
                raw_instance.get_id(),
                features,
                tuple(features.pop(sequence_attribute).strip('"[]').split(','))
            ))
        return dataset

    def get_sequences_ordered_by_frequency(self) -> List[Tuple[str]]:
        """
        orders the target sequences by frequencies. sequences that appear
        equally frequent are ordered by the sum of the frequencies of their events.
        the sequence with the lowest frequency is the first element in the result
        list.

        Returns
        -------
        List[Tuple[str]]
            the target sequences ordered by their frequency. every unique
            sequence is returned only once.
        """
        sequence_frequencies = Counter()
        event_frequencies = Counter()
        for instance in self:
            sequence_frequencies[instance.get_target_sequence()] += 1
            for event in instance.get_target_sequence():
                event_frequencies[event] += 1

        for sequence, frequency in sequence_frequencies.items():
            sequence_frequencies[sequence] = (frequency, sum(
                event_frequencies[e] for e in sequence
            ))

        frequency_ordered_sequences = [
            s[0] for s in sorted(
                sequence_frequencies.items(), key=lambda x: x[1],
            )
        ]

        return frequency_ordered_sequences

    def copy(self) -> 'TargetSequenceDataset':
        """
        returns a copy of this dataset. for this a new dataset is created
        and a copy of each instance is added to the new dataset
        """
        copy = TargetSequenceDataset(self.get_categorical_attribute_names(),
                                     self.get_numerical_attribute_names())
        for instance in self:
            copy.add_instance(instance.copy())
        return copy
