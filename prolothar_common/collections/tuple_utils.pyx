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

from cpython.list cimport PyList_GET_ITEM, PyList_GET_SIZE

cpdef list all_splits_of_size_k(tuple t, int k):
    if k < 1:
        raise ValueError(f'k must not be < 1 but was {k}')
    cdef list current_left = []
    cdef list current_middle = []
    cdef list current_right = []
    cdef list next_left, next_middle, next_right
    cdef int i, j
    cdef tuple left_i, middle_i, right_i
    for i in range(len(t) - k + 1):
        current_left.append(t[:i])
        current_middle.append((t[i],))
        current_right.append(t[i+1:])
    while k > 1:
        next_left = []
        next_middle = []
        next_right = []
        for i in range(PyList_GET_SIZE(current_left)):
            left_i = <tuple>PyList_GET_ITEM(current_left,i )
            middle_i = <tuple>PyList_GET_ITEM(current_middle, i)
            right_i = <tuple>PyList_GET_ITEM(current_right, i)
            for j in range(len(right_i)):
                next_left.append(left_i + right_i[:j])
                next_middle.append(middle_i + (right_i[j],))
                next_right.append(right_i[j+1:])
        k -= 1
        current_left = next_left
        current_middle = next_middle
        current_right = next_right
    cdef list result_list = []
    for i in range(PyList_GET_SIZE(current_left)):
        result_list.append((
            <tuple>PyList_GET_ITEM(current_middle, i),
            <tuple>PyList_GET_ITEM(current_left, i) + <tuple>PyList_GET_ITEM(current_right, i),
        ))
    return result_list
