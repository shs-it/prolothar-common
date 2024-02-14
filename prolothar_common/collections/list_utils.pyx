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

from typing import List, Tuple
from random import Random
import numpy as np

cimport cython

def search_sublist_all_occurences(l, sublist):
    """
    returns a list of start indices of all occurences of sublist in list l.
    this list is empty iff sublist is no sublist of list
    """
    occurences = []
    char_table = make_boyer_moore_char_table(sublist)
    offset_table = make_boyer_moore_offset_table(sublist)

    index = 0
    subindex = search_sublist_bm(l, sublist, char_table=char_table,
                                 offset_table=offset_table)

    while subindex >= 0 and index <= len(l):
        index = index + subindex
        occurences.append(index)
        index = index + 1
        subindex = search_sublist_bm(l[index:], sublist,
                                     char_table=char_table,
                                     offset_table=offset_table)

    return occurences

def is_sublist_bm(l, sublist, char_table=None, offset_table=None):
    """
    Uses the Boyer Moore Search Algorithm to check if sublist is a sublist of
    list. For performance reasons it is possible to precompute char_table
    and offset_table with "make_boyer_moore_char_table" and
    "make_boyer_moore_offset_table" if one repeats the search for the same
    sublist but different list.
    """
    return search_sublist_bm(l, sublist,
                             char_table=char_table,
                             offset_table=offset_table) >= 0

def search_sublist_bm(l, sublist, char_table=None, offset_table=None):
    """
    http://www.martinbroadhurst.com/boyer-moore-search-of-a-list-for-a-sub-list-in-python.html
    """
    if len(sublist) == 0:
        return 0
    if char_table is None:
        char_table = make_boyer_moore_char_table(sublist)
    if offset_table is None:
        offset_table = make_boyer_moore_offset_table(sublist)
    i = len(sublist) - 1

    while i < len(l):
        j = len(sublist) - 1
        while sublist[j] == l[i]:
            if j == 0:
                return i
            i -= 1
            j -= 1
        i += max(offset_table[len(sublist) - 1 - j], char_table.get(l[i], 1));
    return -1

def make_boyer_moore_char_table(needle):
    """
    Boyer Moore Search:
    Makes the jump table based on the mismatched character information.
    """
    table = {}
    for i in range(len(needle) - 1):
        table[needle[i]] = len(needle) - 1 - i
    return table

def make_boyer_moore_offset_table(needle):
    """
    Boyer Moore Search:
    Makes the jump table based on the scan offset in which mismatch occurs.
    """
    table = []
    last_prefix_position = len(needle)
    for i in reversed(range(len(needle))):
        if is_prefix(needle, i + 1):
            last_prefix_position = i + 1
        table.append(last_prefix_position - i + len(needle) - 1)
    for i in range(len(needle) - 1):
        slen = suffix_length(needle, i)
        table[slen] = len(needle) - 1 - i + slen
    return table

def is_prefix(needle, p):
    """
    Is needle[p:end] a prefix of needle?
    """
    j = 0
    for i in range(p, len(needle)):
        if needle[i] != needle[j]:
            return 0
        j += 1
    return 1

def suffix_length(needle, p):
    """
    Returns the maximum length of the substring ending at p that is a suffix.
    """
    length = 0;
    j = len(needle) - 1
    for i in reversed(range(p + 1)):
        if needle[i] == needle[j]:
            length += 1
        else:
            break
        j -= 1
    return length

def view_of_n_partitions(l, n: int):
    """http://wordaligned.org/articles/slicing-a-list-evenly-with-python"""
    L = len(l)
    n = max(min(n, L), 0)
    s, r = divmod(L, n)
    t = s + 1
    return ([l[p:p+t] for p in range(0, r*t, t)] +
            [l[p:p+s] for p in range(r*t, L, s)])

def enumerate_reversed(l):
    for index, value in enumerate(reversed(l)):
        index = len(l)-1 - index
        yield index, value

def deep_flatten(xs):
    """
    flattens a potentially deep nested list, i.e. the elements of sublists
    (and sublists of sublists and so on) will be collected into one list,
    e.g. [[1,2],3] => [1,2,3]
    https://medium.com/swlh/top-useful-python-snippets-that-save-time-38958f256822
    """
    flat_list = []
    if isinstance(xs, list):
        [flat_list.extend(deep_flatten(x)) for x in xs]
    else:
        flat_list.append(xs)
    return flat_list

def iterate_self_product(l: List, skip_diagonal: bool = False) -> List[Tuple]:
    """
    a generator that enables iteration of the self product of a given list.

    iterate_self_product([1,2,3])
    => (1,1) (1,2) (1,3) (2,1) (2,2) (2,3) (3,1) (3,2) (3,3)

    iterate_self_product([1,2,3], skip_diagonal=True)
    => (1,2) (1,3) (2,1) (2,3) (3,1) (3,2)

    Parameters
    ----------
    l : List
        the given list
    skip_diagonal : bool, optional
        if True, the diagonal elements of the self proudct are skipped,
        by default False

    Returns
    -------
    a list of tuples
    """
    for i, element_i in enumerate(l):
        for j, element_j in enumerate(l):
            if not skip_diagonal or i != j:
                yield (element_i, element_j)

@cython.boundscheck(False)
@cython.wraparound(False)
def longest_common_sublists(list list_a not None, list list_b not None) -> tuple[int, list[tuple]]:
    """
    computes the longest common sublist (longest common substring) between two
    lists.
    See https://en.wikipedia.org/wiki/Longest_common_substring_problem

    Returns
    -------
    a 2-tuple consisting of the length of longest common list and a list with
    a 2-tuple for each common sublists (there can be more than one longest).
    each of these 2-tuples consists of the start index in list_a and the start index
    in list_b.
    """
    cdef int length_a = len(list_a)
    cdef int length_b = len(list_b)
    cdef int[:,:] matrix = np.zeros((length_a, length_b), dtype=np.intc)

    cdef int i = 0
    cdef int j = 0
    cdef int length = 0
    cdef list indices = []

    for i in range(length_a):
        for j in range(length_b):
            if list_a[i] == list_b[j]:
                if i == 0 or j == 0:
                    matrix[i,j] = 1
                else:
                    matrix[i,j] = matrix[i-1,j-1] + 1
                if matrix[i,j] > length:
                    length = matrix[i,j]
                    indices = [(i,j)]
                elif matrix[i,j] == length:
                    indices.append((i,j))

    return length, [(i-length+1,j-length+1) for i,j in indices]

def shuffle_together(*list_of_lists, random: Random|None = None):
    #https://stackoverflow.com/questions/23289547/shuffle-two-list-at-once-with-same-order
    temp = list(zip(*list_of_lists))
    if random is not None:
        random.shuffle(temp)
    else:
        Random().shuffle(temp)
    return [
        list(x) for x in zip(*temp)
    ]

