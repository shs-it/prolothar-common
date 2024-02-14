cdef class Event:
    cdef public activity_name
    cdef public dict attributes
    cdef public str transition_id

    cpdef dict to_dict(self)
