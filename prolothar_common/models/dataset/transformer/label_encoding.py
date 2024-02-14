# -*- coding: utf-8 -*-

from typing import Set, Dict

from prolothar_common.models.dataset.transformer.dataset_transformer import DatasetTransformer

from prolothar_common.models.dataset import Dataset
from prolothar_common.models.dataset.attributes import Attribute

class LabelEncoding(DatasetTransformer):
    """
    label encodes categorical attributes (maps categories to an index from 0..K)
    """

    def __init__(self, possible_attribute_values: Dict[str, Set] = None):
        """
        configures this label encoder

        Parameters
        ----------
        possible_attribute_values : Dict[str, Set], optional
            can be used to predefine the possible values. otherwise all values
            in the dataset to transform will be used, by default None
        """
        self.__possible_attribute_values = possible_attribute_values

    def inplace_transform(self, dataset: Dataset) -> Dataset:
        for attribute in list(dataset.get_attributes()):
            if attribute.is_categorical():
                self.__transform_attribute(attribute, dataset)

    def __transform_attribute(self, attribute: Attribute, dataset: Dataset):
        if self.__possible_attribute_values is not None:
            possible_values = sorted(self.__possible_attribute_values[attribute.get_name()])
        else:
            possible_values = sorted(attribute.get_unique_values())

        #do not transform already label encoded attributes
        if possible_values and possible_values == list(range(len(possible_values))) \
        and not isinstance(possible_values[0], bool):
            return

        value_map = {value: i for i,value in enumerate(possible_values)}

        encoded_values = []
        for instance in dataset:
            encoded_values.append(value_map[instance[attribute.get_name()]])

        dataset.remove_attribute(attribute.get_name())
        dataset.add_categorical_attribute(attribute.get_name(), encoded_values)
