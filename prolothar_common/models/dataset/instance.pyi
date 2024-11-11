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

from typing import Hashable, Dict, Any, List, Iterable, Tuple, Union, Set
from collections import Counter

class Instance:
    """Instance of a dataset"""
    def __init__(self, instance_id: Hashable, features: Dict[str, Any]): ...

    def copy(self) -> Instance:
        """returns a copy of this instance"""
        ...

    def get_id(self) -> Any: ...

    def get_feature_names(self) -> Iterable[str]: ...

    def get_features_dict(self) -> Dict[str, Any]: ...

    def remove_feature(self, attribute: str): ...

    def __getitem__(self, feature_name: str) -> Any: ...

    def __setitem__(self, feature_name: str, value: Any) -> Any: ...

class ClassificationInstance(Instance):
    def __init__(self, instance_id: Hashable, features: Dict[str, Any],
                 class_label: str): ...

    def get_class(self) -> str: ...

    def copy(self) -> 'ClassificationInstance':
        """returns a copy of this instance"""
        ...

class MultiLabelInstance(Instance):
    def __init__(self, instance_id: Hashable, features: Dict[str, Any],
                 labels: Set[str]): ...

    def get_labels(self) -> Set[str]: ...

    def copy(self) -> 'MultiLabelInstance':
        """returns a copy of this instance"""
        ...

class MultisetInstance(Instance):
    def __init__(self, instance_id: Hashable, features: Dict[str, Any],
                 multiset: Counter): ...

    def get_multiset(self) -> Counter: ...

    def copy(self) -> 'MultisetInstance':
        """returns a copy of this instance"""
        ...

class TargetSequenceInstance(Instance):
    def __init__(self, instance_id: Hashable, features: Dict[str, Any],
                 target_sequence: Union[List[str], Tuple[str]]): ...

    def get_target_sequence(self) -> Tuple[str]: ...

    def set_target_sequence(self, target_sequence: Union[List[str], Tuple[str]]): ...

    def contains_symbol(self, symbol: str) -> bool:
        """
        return True iff target_sequence contains the given symbol
        """
        ...

    def get_symbols(self) -> frozenset:
        """
        returns the set of symbols in the target sequence of this instance
        """
        ...

    def copy(self) -> 'TargetSequenceInstance':
        """returns a copy of this instance"""
        ...