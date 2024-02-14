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