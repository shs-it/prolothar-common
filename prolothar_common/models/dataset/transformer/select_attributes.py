# -*- coding: utf-8 -*-
from typing import Set

from prolothar_common.models.dataset.transformer.dataset_transformer import DatasetTransformer

from prolothar_common.models.dataset import Dataset

class SelectAttributes(DatasetTransformer):
    """
    Selects a subset of attributes from the dataset
    """

    def __init__(self, attributes: Set[str]):
        self.__attributes = set(attributes)

    def inplace_transform(self, dataset: Dataset) -> Dataset:
        for attribute in list(dataset.get_attributes()):
            if attribute.get_name() not in self.__attributes:
                dataset.remove_attribute(attribute.get_name())
