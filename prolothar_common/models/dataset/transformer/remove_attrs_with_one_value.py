# -*- coding: utf-8 -*-
from prolothar_common.models.dataset.transformer.dataset_transformer import DatasetTransformer

from prolothar_common.models.dataset import Dataset

class RemoveAttributesWithOneUniqueValue(DatasetTransformer):
    """
    Removes all attributes from a dataset that has only one unique value
    """

    def inplace_transform(self, dataset: Dataset) -> Dataset:
        for attribute in list(dataset.get_attributes()):
            if attribute.get_nr_of_unique_values() == 1:
                dataset.remove_attribute(attribute.get_name())
