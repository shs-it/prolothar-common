cpdef enum EditOperationType:
    DELETE = 0
    INSERT = 1
    SUBSTITUTE = 2

cdef class EditOperation:
    cdef public int i
    cdef public int j
    cdef public EditOperationType operation_type

cdef int[:,:] compute_cost_matrix(
        s1, s2, int insertion_cost = ?, int deletion_cost = ?,
        int substitution_cost = ?)

cpdef list backtrace(s1, s2, int[:,:] cost_matrix)