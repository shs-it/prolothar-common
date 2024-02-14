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

from typing import Iterable, Set, List

from prolothar_common.models.dataset.dataset import Dataset
from prolothar_common.models.dataset.instance import MultiLabelInstance

class MultiLabelDataset(Dataset):
    """
    a dataset with a multilabel class target
    """

    def __init__(self, categorical_attribute_names: Iterable[str],
                 numerical_attribute_names: Iterable[str]):
        super().__init__(categorical_attribute_names, numerical_attribute_names)
        self.__set_of_labels = set()

    def add_instance(self, instance: MultiLabelInstance):
        super().add_instance(instance)
        self.__set_of_labels.update(instance.get_labels())

    def _add_attributes_definition_to_arff(self, arff: str, **kwargs) -> str:
        arff = super()._add_attributes_definition_to_arff(arff)

        for label in sorted(self.__set_of_labels):
            arff += '\n@ATTRIBUTE "%s%s" {0,1}' % (kwargs.get('label_prefix', ''), label)
        return arff

    def _add_instance_to_arff(self, arff: str, instance: MultiLabelInstance, **kwargs) -> str:
        arff = super()._add_instance_to_arff(arff, instance) + ","
        for i,label in enumerate(sorted(self.__set_of_labels)):
            arff += '1' if label in instance.get_labels() else '0'
            if i < len(self.__set_of_labels) - 1:
                arff += ','
        return arff

    def get_set_of_labels(self) -> Set[str]:
        """
        returns the set of labels (classes) in this dataset
        """
        return self.__set_of_labels

    def copy(self) -> 'MultiLabelDataset':
        """
        returns a copy of this dataset. for this a new dataset is created
        and a copy of each instance is added to the new dataset
        """
        copy = MultiLabelDataset(self.get_categorical_attribute_names(),
                                 self.get_numerical_attribute_names())
        for instance in self:
            copy.add_instance(instance.copy())
        return copy

    @staticmethod
    def create_from_arff(arff: str, label_attributes: List[str]) -> 'MultiLabelDataset':
        """
        creates a MultiLabelDataset from the given ARFF string
        """
        raw_dataset = Dataset.create_from_arff(arff)

        dataset = MultiLabelDataset(
            list(set(raw_dataset.get_categorical_attribute_names()
                     ).difference(label_attributes)),
            list(set(raw_dataset.get_numerical_attribute_names()
                     ).difference(label_attributes)),
        )

        for raw_instance in raw_dataset:
            dataset.add_instance(MultiLabelInstance(
                raw_instance.get_id(),
                {
                    attribute_name: attribute_value
                    for attribute_name, attribute_value in raw_instance.get_features_dict().items()
                    if attribute_name not in label_attributes
                },
                set(label for label in label_attributes if raw_instance[label] in [1, '1'])
            ))

        return dataset
