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

cdef class Instance:
    cdef instance_id
    cdef dict features

    cpdef Instance copy(self)
    cpdef remove_feature(self, str attribute)

cdef class ClassificationInstance(Instance):
    cdef str class_label

    cpdef ClassificationInstance copy(self)
    cpdef str get_class(self)

cdef class MultiLabelInstance(Instance):
    cdef set labels

    cpdef set get_labels(self)
    cpdef MultiLabelInstance copy(self)

cdef class MultisetInstance(Instance):
    cdef multiset

    cpdef MultisetInstance copy(self)

cdef class TargetSequenceInstance(Instance):
    cdef tuple target_sequence
    cdef frozenset set_of_symbols

    cpdef tuple get_target_sequence(self)
    cpdef bint contains_symbol(self, str symbol)
    cpdef frozenset get_symbols(self)
    cpdef TargetSequenceInstance copy(self)