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

from typing import Dict

import pandas as pd

from prolothar_common.models.dataset.transformer.dataset_transformer import DatasetTransformer

from prolothar_common.models.dataset import Dataset

class TrainableQuantileBasedDiscretization(DatasetTransformer):
    """
    discretizes numerical attributes into equal-sized buckets.
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.qcut.html
    The buckets must be learned before the transformation which enables
    a re-use of this transformer
    """

    def __init__(self, attribute_bins_dict: Dict[str, pd.IntervalIndex]):
        self.__attribute_bins_dict = attribute_bins_dict

    def inplace_transform(self, dataset: Dataset) -> Dataset:
        for attribute in list(dataset.get_attributes()):
            if attribute.is_numerical():
                self.__transform_attribute(attribute.get_name(), dataset)

    def __transform_attribute(self, attribute_name: str, dataset: Dataset):
        bins = self.__attribute_bins_dict[attribute_name]
        bin_labels = [str(b) for b in bins]
        transformed_values = []
        for instance in dataset:
            try:
                transformed_values.append(bin_labels[bins.contains(
                    instance[attribute_name]).tolist().index(True)])
            except ValueError:
                #the observed value is larger than the largest value in the
                #training set => put it into the last bin
                transformed_values.append(bin_labels[-1])
        dataset.remove_attribute(attribute_name)
        dataset.add_categorical_attribute(attribute_name, transformed_values)

    @staticmethod
    def train(dataset: Dataset, nr_of_bins: int):
        attribute_bins_dict = {}
        for attribute in (a for a in dataset.get_attributes() if a.is_numerical()):
            values = [instance[attribute.get_name()] for instance in dataset]
            bins = pd.qcut(values, nr_of_bins, duplicates='drop').categories
            attribute_bins_dict[attribute.get_name()] = bins
        return TrainableQuantileBasedDiscretization(attribute_bins_dict)

