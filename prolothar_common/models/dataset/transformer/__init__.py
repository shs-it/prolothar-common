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

from prolothar_common.models.dataset.transformer.one_hot_encoding import OneHotEncoding
from prolothar_common.models.dataset.transformer.quantile_based_discretization import QuantileBasedDiscretization
from prolothar_common.models.dataset.transformer.min_max_scaling import MinMaxScaling
from prolothar_common.models.dataset.transformer.trainable_q_based_discretization import TrainableQuantileBasedDiscretization
from prolothar_common.models.dataset.transformer.remove_attrs_with_one_value import RemoveAttributesWithOneUniqueValue
from prolothar_common.models.dataset.transformer.select_attributes import SelectAttributes
from prolothar_common.models.dataset.transformer.target_sequence_remove_noise import TargetSequenceRemoveNoise
from prolothar_common.models.dataset.transformer.target_sequence_add_noise import TargetSequenceAddNoise
from prolothar_common.models.dataset.transformer.target_sequence_swap_noise import TargetSequenceSwapNoise