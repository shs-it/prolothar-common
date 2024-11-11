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

from statistics import quantiles

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
        if len(dataset.get_attribute_by_name(attribute_name).get_unique_values()) > self.__nr_of_bins:
            cut_points = quantiles(values, n=self.__nr_of_bins, method='inclusive')
            min_value = min(values)
            max_value = max(values)
            transformed_values = [
                self.__get_label_for_value(value, cut_points, min_value, max_value)
                for value in values
            ]
        else:
            transformed_values = [str(value) for value in values]
        dataset.remove_attribute(attribute_name)
        dataset.add_categorical_attribute(attribute_name, transformed_values)

    def __get_label_for_value(self, value: float, cut_points: list[float], min_value: float, max_value: float) -> str:
        if value <= cut_points[0]:
            return f'[{min_value}, {cut_points[0]}]'
        for a,b in zip(cut_points, cut_points[1:]):
            if a < value <= b:
                return f'({a}, {b}]'
        else:
            return f'({cut_points[-1]}, {max_value}]'
