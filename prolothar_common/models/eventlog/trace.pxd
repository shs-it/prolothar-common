cdef class Trace:
    cdef public list events
    cdef public dict attributes
    cdef __id

    cpdef int get_first_index_of_first_matching_activity(self, set activity_set)
    cpdef int get_last_index_of_first_matching_activity(self, set activity_set)
    cpdef bint contains_activity(self, activity)
    cpdef dict to_dict(self)
    cpdef list to_activity_list(self)