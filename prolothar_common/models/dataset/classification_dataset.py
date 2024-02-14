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

from typing import Iterable, Set
from collections import defaultdict

from prolothar_common.models.dataset.dataset import Dataset
from prolothar_common.models.dataset.instance import ClassificationInstance

class ClassificationDataset(Dataset):
    """
    a dataset with a class target
    """

    def __init__(self, categorical_attribute_names: Iterable[str],
                 numerical_attribute_names: Iterable[str]):
        super().__init__(categorical_attribute_names, numerical_attribute_names)
        self.__category_counter = defaultdict(lambda: defaultdict(int))
        self.__category_class_counter = defaultdict(lambda: defaultdict(int))
        self.__class_label_counter = defaultdict(int)

    def remove_attribute(self, attribute_name: str):
        super().remove_attribute(attribute_name)
        if attribute_name in self.__category_counter:
            self.__category_counter.pop(attribute_name)
        if attribute_name in self.__category_class_counter:
            self.__category_class_counter.pop(attribute_name)

    def get_count_for_category(self, attribute_name: str, category) -> int:
        """
        returns how many instance have value "category" for categorical attribute
        "attribute_name"
        """
        return self.__category_counter[attribute_name][category]

    def get_count_for_category_and_class(
            self, attribute_name: str, category, class_label: str) -> int:
        """
        returns how many instance have value "category" for categorical attribute
        "attribute_name" and a given class_label
        """
        return self.__category_class_counter[attribute_name][(category, class_label)]

    def get_class_count(self, class_label: str) -> int:
        """
        returns how many instances have a given class label
        """
        return self.__class_label_counter[class_label]

    def add_instance(self, instance: ClassificationInstance):
        super().add_instance(instance)
        self.__class_label_counter[instance.get_class()] += 1
        for categorical_attribute in self.get_categorical_attribute_names():
            self.__category_counter[categorical_attribute][
                instance[categorical_attribute]] += 1
            self.__category_class_counter[categorical_attribute][(
                instance[categorical_attribute], instance.get_class())] += 1

    def _add_attributes_definition_to_arff(self, arff: str, **kwargs) -> str:
        arff = super()._add_attributes_definition_to_arff(arff)

        arff += '\n@ATTRIBUTE "%s" {%s}' % (kwargs.get('class_attribute_name', 'class'), ','.join(
            '"%s"' % c for c in sorted(self.__class_label_counter.keys())
        ))
        return arff

    def _add_instance_to_arff(self, arff: str, instance: ClassificationInstance, **kwargs) -> str:
        arff = super()._add_instance_to_arff(arff, instance)
        arff += ',"%s"' % instance.get_class()
        return arff

    def get_set_of_classes(self) -> Set[str]:
        return self.__class_label_counter.keys()

    def copy(self) -> 'ClassificationDataset':
        """
        returns a copy of this dataset. for this a new dataset is created
        and a copy of each instance is added to the new dataset
        """
        copy = ClassificationDataset(self.get_categorical_attribute_names(),
                                     self.get_numerical_attribute_names())
        for instance in self:
            copy.add_instance(instance.copy())
        return copy