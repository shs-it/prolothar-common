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

from prolothar_common.models.dataset.transformer.dataset_transformer import DatasetTransformer

from prolothar_common.models.dataset import Dataset

class MinMaxScaling(DatasetTransformer):
    """
    scales numerical attributes such that all values are in a given min max range.

    also see https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html
    """

    def __init__(self, scaled_min_value: float = 0.0, scaled_max_value: float = 1.0):
        """
        configures this Min-Max-Scaler

        Parameters
        ----------
        scaled_min_value : float, optional
            target minimum value after scaling, by default 0.0
        scaled_max_value : float, optional
            target maximum value after scaling, by default 1.0
        """
        self.__scaled_min_value = scaled_min_value
        self.__scaled_max_value = scaled_max_value

    def inplace_transform(self, dataset: Dataset) -> Dataset:
        for attribute in list(dataset.get_attributes()):
            if attribute.is_numerical():
                self.__transform_attribute(attribute.get_name(), dataset)

    def __transform_attribute(self, attribute_name: str, dataset: Dataset):
        values = [instance[attribute_name] for instance in dataset]
        min_value = min(values)
        max_value = max(values)
        values = [
            (v - min_value) / (max_value - min_value) *
            (self.__scaled_max_value - self.__scaled_min_value) +
            self.__scaled_min_value for v in values
        ]
        dataset.remove_attribute(attribute_name)
        dataset.add_numerical_attribute(attribute_name, values)
