from prolothar_common.models.eventlog.event cimport Event

cdef class ComplexEvent(Event):
    cdef public list children
