cdef class Instance:
    cdef instance_id
    cdef features

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