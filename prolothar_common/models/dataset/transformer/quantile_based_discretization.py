# -*- coding: utf-8 -*-

import pandas as pd

from prolothar_common.models.dataset.transformer.dataset_transformer import DatasetTransformer

from prolothar_common.models.dataset import Dataset

class QuantileBasedDiscretization(DatasetTransformer):
    """
    discretizes numerical attributes into equal-sized buckets.
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.qcut.html
    """

    def __init__(self, nr_of_bins: int):
        self.__nr_of_bins = nr_of_bins

    def inplace_transform(self, dataset: Dataset) -> Dataset:
        for attribute in list(dataset.get_attributes()):
            if attribute.is_numerical():
                self.__transform_attribute(attribute.get_name(), dataset)

    def __transform_attribute(self, attribute_name: str, dataset: Dataset):
        values = [instance[attribute_name] for instance in dataset]
        if len(dataset.get_attribute_by_name(
                attribute_name).get_unique_values()) > self.__nr_of_bins:
            transformed_values = [
                str(discretized_value) for discretized_value
                in pd.qcut(values, self.__nr_of_bins, duplicates='drop')]
        else:
            transformed_values = [str(value) for value in values]
        dataset.remove_attribute(attribute_name)
        dataset.add_categorical_attribute(attribute_name, transformed_values)
