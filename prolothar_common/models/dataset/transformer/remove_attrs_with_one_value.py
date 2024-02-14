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

class RemoveAttributesWithOneUniqueValue(DatasetTransformer):
    """
    Removes all attributes from a dataset that has only one unique value
    """

    def inplace_transform(self, dataset: Dataset) -> Dataset:
        for attribute in list(dataset.get_attributes()):
            if attribute.get_nr_of_unique_values() == 1:
                dataset.remove_attribute(attribute.get_name())
