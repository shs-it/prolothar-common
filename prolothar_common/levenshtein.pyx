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

from typing import Tuple, List
import numpy as np

cimport cython

cdef int MAX_COST = 100000

cdef class EditOperation:
    def __init__(self, int i, int j, EditOperationType operation_type):
        self.i = i
        self.j = j
        self.operation_type = operation_type

    def __eq__(self, other: 'EditOperation') -> bool:
        return (self.i, self.j, self.operation_type) == (
            other.i, other.j, other.operation_type)

    def __hash__(self) -> int:
        return hash((self.i, self.j, self.operation_type))

    def __repr__(self) -> int:
        return 'EditOperation(%d,%d,%s)' % (self.i, self.j, self.operation_type)

@cython.boundscheck(False)
def levenshtein_with_backtrace(
        s1, s2, int insertion_cost = 1, int deletion_cost = 1,
        int substitution_cost = 1) -> Tuple[int[:,:], List[EditOperation]]:
    """implementation of levenshtein with backtrace. only use this method if
    you really need the backtracing. otherwise use a faster implementation of
    strsimpy

    based on https://gist.github.com/curzona/9435822
    """
    cdef int[:,:] cost_matrix = compute_cost_matrix(
        s1, s2, insertion_cost=insertion_cost, deletion_cost=deletion_cost,
        substitution_cost=substitution_cost)
    cdef list edit_operations = backtrace(s1, s2, cost_matrix)
    return cost_matrix[-1][-1], edit_operations

@cython.boundscheck(False)
@cython.wraparound(False)
cdef int[:,:] compute_cost_matrix(
        s1, s2, int insertion_cost = 1, int deletion_cost = 1,
        int substitution_cost = 1):
    """computes the cost matrix of the levenshtein algorithm"""
    cdef int length_s1 = len(s1)
    cdef int length_s2 = len(s2)
    cdef int[:,:] cost_matrix = np.zeros((length_s1 + 1, length_s2 + 1), dtype=np.intc)

    cdef int i = 0
    cdef int j = 0

    while i <= length_s1:
        cost_matrix[i][0] = i
        i += 1
    while j <= length_s2:
        cost_matrix[0][j] = j
        j += 1

    cdef int insertions, deletions, substitutions

    i = 1
    j = 1
    while i <= length_s1:
        while j <= length_s2:
            insertions = cost_matrix[i][j - 1] + insertion_cost
            deletions = cost_matrix[i - 1][j] + deletion_cost
            substitutions = cost_matrix[i-1][j-1] + (substitution_cost if s1[i-1] != s2[j-1] else 0)
            cost_matrix[i][j] = min(insertions, deletions, substitutions)
            j += 1
        i += 1
        j = 1

    return cost_matrix

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef list backtrace(s1, s2, int[:,:] cost_matrix):
    """
    backtracing of the levenshtein algorithm.
    returns a list of EditOperation
    """
    cdef int i = len(s1)
    cdef int j =  len(s2)

    cdef list edits = []

    cdef int min_cost

    while i != 0 or j != 0:
        min_cost = MAX_COST

        if i != 0 and j != 0:
            min_cost = min(min_cost, cost_matrix[i-1][j-1])
        if i != 0:
            min_cost = min(min_cost, cost_matrix[i-1][j])
        if j != 0:
            min_cost = min(min_cost, cost_matrix[i][j-1])

        if min_cost == cost_matrix[i][j]:
            i, j = i-1, j-1
        elif i != 0 and j != 0 and min_cost == cost_matrix[i-1][j-1]:
            i, j = i-1, j-1
            edits.append(EditOperation(i, j, EditOperationType.SUBSTITUTE))
        elif i != 0 and min_cost == cost_matrix[i-1][j]:
            i = i-1
            edits.append(EditOperation(i, j, EditOperationType.DELETE))
        elif j != 0 and min_cost == cost_matrix[i][j-1]:
            j = j-1
            edits.append(EditOperation(i, j, EditOperationType.INSERT))

        edits.reverse()

    return edits