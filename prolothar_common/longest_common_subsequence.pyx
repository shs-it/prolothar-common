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

"""
defines functions to compute the longest common subsequence with backtrace
for arbitrary lists.
See https://en.wikipedia.org/wiki/Longest_common_subsequence_problem for details
"""

from typing import List, Tuple, Union

import numpy as np

cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cdef int[:,:] compute_lcs_matrix(x_list: Union[List,str], y_list: Union[List,str]):
    cdef int[:,:] C = np.zeros((len(x_list) + 1, len(y_list) + 1), dtype=np.intc)

    cdef int i
    cdef int j
    for i, x in enumerate(x_list):
        for j, y in enumerate(y_list):
            if x == y:
                C[i+1,j+1] = C[i,j] + 1
            else:
                C[i+1,j+1] = max(C[i+1,j],C[i,j+1])

    return C

def length_of_common_subsequence(x_list: Union[List,str], y_list: Union[List,str]) -> int:
    return compute_lcs_matrix(x_list, y_list)[len(x_list)][len(y_list)]

@cython.boundscheck(False)
@cython.wraparound(False)
def lcs_with_backtrace(x_list: Union[List,str], y_list: Union[List,str]) -> Tuple[int, List[Tuple[int,int]]]:
    """
    returns a 2-D tuple. the first element is the length of the longest common
    subsequence (https://en.wikipedia.org/wiki/Longest_common_subsequence_problem).
    the seconds element is a list of tuples. the first element of each tuple (i,j)
    corresponds to an index in x_list, and the seconds element to an index in y_list,
    such that x_list[i] == y_list[i]
    """
    cdef int[:,:] C = compute_lcs_matrix(x_list, y_list)
    cdef int i = len(x_list)
    cdef int j = len(y_list)
    backtrace: List[Tuple[int, int]] = []
    while i != 0 and j != 0:
        if x_list[i-1] == y_list[j-1]:
            i -= 1
            j -= 1
            backtrace.append((i,j))
        elif C[i-1][j] > C[i][j-1]:
            i -= 1
        else:
            j -= 1
    return C[len(x_list)][len(y_list)], backtrace[::-1]
