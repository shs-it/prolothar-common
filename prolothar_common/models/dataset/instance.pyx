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

cdef class Instance:
    """Instance of a dataset"""
    def __init__(self, instance_id: Hashable, features: Dict[str, Any]):
        self.instance_id = instance_id
        self.features = features

    cpdef Instance copy(self):
        """returns a copy of this instance"""
        return Instance(self.instance_id, dict(self.features))

    def get_id(self):
        return self.instance_id

    def get_feature_names(self) -> Iterable[str]:
        return self.features.keys()

    def get_features_dict(self) -> Dict[str, Any]:
        return self.features

    cpdef remove_feature(self, str attribute):
        """
        removes a feature from this instance
        """
        self.features.pop(attribute)

    def __getitem__(self, feature_name: str) -> Any:
        return self.features[feature_name]

    def __setitem__(self, feature_name: str, value: Any) -> Any:
        self.features[feature_name] = value

    def __hash__(self) -> int:
        return hash(self.instance_id)

    def __eq__(self, other) -> bool:
        return self.get_id() == other.get_id()

    def __repr__(self) -> str:
        return 'ID: %r\n%r\n' % (self.instance_id, self.features)


cdef class ClassificationInstance(Instance):
    def __init__(self, instance_id: Hashable, features: Dict[str, Any],
                 class_label: str):
        super().__init__(instance_id, features)
        self.class_label = class_label

    cpdef str get_class(self):
        return self.class_label

    cpdef ClassificationInstance copy(self):
        """returns a copy of this instance"""
        return ClassificationInstance(self.instance_id, dict(self.features), self.class_label)

cdef class MultiLabelInstance(Instance):
    def __init__(self, instance_id: Hashable, features: Dict[str, Any],
                 labels: Set[str]):
        super().__init__(instance_id, features)
        self.labels = labels

    cpdef set get_labels(self):
        return self.labels

    cpdef MultiLabelInstance copy(self):
        """returns a copy of this instance"""
        return MultiLabelInstance(self.instance_id, dict(self.features), self.labels)

cdef class MultisetInstance(Instance):
    def __init__(self, instance_id: Hashable, features: Dict[str, Any],
                 multiset: Counter):
        super().__init__(instance_id, features)
        self.multiset = multiset

    def get_multiset(self) -> Counter:
        return self.multiset

    cpdef MultisetInstance copy(self):
        """returns a copy of this instance"""
        return MultisetInstance(self.instance_id, dict(self.features), Counter(self.multiset))

cdef class TargetSequenceInstance(Instance):
    def __init__(self, instance_id: Hashable, features: Dict[str, Any],
                 target_sequence: Union[List[str], Tuple[str]]):
        super().__init__(instance_id, features)
        self.set_target_sequence(target_sequence)

    cpdef tuple get_target_sequence(self):
        return self.target_sequence

    def set_target_sequence(self, target_sequence: Union[List[str], Tuple[str]]):
        if not isinstance(target_sequence, tuple):
            self.target_sequence = tuple(target_sequence)
        else:
            self.target_sequence = target_sequence
        self.set_of_symbols = frozenset(target_sequence)

    def __repr__(self) -> str:
        return 'ID: %r\n%r\n%r\n' % (self.instance_id, self.features,
                                   self.target_sequence)

    cpdef bint contains_symbol(self, str symbol):
        """
        return True iff target_sequence contains the given symbol
        """
        return symbol in self.set_of_symbols

    cpdef frozenset get_symbols(self):
        """
        returns the set of symbols in the target sequence of this instance
        """
        return self.set_of_symbols

    cpdef TargetSequenceInstance copy(self):
        """returns a copy of this instance"""
        return TargetSequenceInstance(
            self.instance_id, dict(self.features), tuple(self.target_sequence))