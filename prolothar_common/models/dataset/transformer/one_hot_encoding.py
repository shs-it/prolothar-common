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

from typing import Set, Dict

from prolothar_common.models.dataset.transformer.dataset_transformer import DatasetTransformer

from prolothar_common.models.dataset import Dataset
from prolothar_common.models.dataset.attributes import Attribute

class OneHotEncoding(DatasetTransformer):
    """
    one hot encodes categorical attributes
    """

    def __init__(self, possible_attribute_values: Dict[str, Set] = None,
                 attribute_value_join_character: str = ' '):
        """
        configures this one hot encoder

        Parameters
        ----------
        possible_attribute_values : Dict[str, Set], optional
            can be used to predefine the possible values. otherwise all values
            in the dataset to transform will be used, by default None
        attribute_value_join_character : str, optional
            a one hot encoded attribute will have the name
            "attribute_name + attribute_value_join_character + value",
            by default ' '
        """
        self.__possible_attribute_values = possible_attribute_values
        self.__attribute_value_join_character = attribute_value_join_character

    def inplace_transform(self, dataset: Dataset) -> Dataset:
        for attribute in list(dataset.get_attributes()):
            if attribute.is_categorical():
                self.__transform_attribute(attribute, dataset)

    def __transform_attribute(self, attribute: Attribute, dataset: Dataset):
        if self.__possible_attribute_values is not None:
            possible_values = sorted(self.__possible_attribute_values[attribute.get_name()])
        else:
            possible_values = sorted(attribute.get_unique_values())

        #do not transform already 0-1 encoded attributes
        if len(possible_values) == 2 and possible_values[0] == 0 and possible_values[1] == 1:
            return

        for value in possible_values:
            transformed_values = []
            for instance in dataset:
                if instance[attribute.get_name()] == value:
                    transformed_values.append(1)
                else:
                    transformed_values.append(0)
            dataset.add_categorical_attribute(
                attribute.get_name() + self.__attribute_value_join_character +
                str(value), transformed_values)
        dataset.remove_attribute(attribute.get_name())