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

from typing import Generator
from random import Random

def search_sublist_all_occurences(l: list, sublist: list) -> list[int]:
    """
    returns a list of start indices of all occurences of sublist in list.
    this list is empty iff sublist is no sublist of list
    """
    ...

def is_sublist_bm(list: list, sublist: list, char_table=None, offset_table=None) -> bool:
    """
    Uses the Boyer Moore Search Algorithm to check if sublist is a sublist of
    list. For performance reasons it is possible to precompute char_table
    and offset_table with "make_boyer_moore_char_table" and
    "make_boyer_moore_offset_table" if one repeats the search for the same
    sublist but different list.
    """
    ...

def shuffle_together(*list_of_lists, random: Random|None = None) -> list:
    """
    shuffles all given lists such that all lists keep their relative order

    Parameters
    ----------
    random : Random | None, optional
        random number generator that is used to shuffle the lists, by default None

    Returns
    -------
    list
        a list of all shuffled lists
    """
    ...

def iterate_self_product(l: list, skip_diagonal: bool = False) -> Generator[tuple, None, None]:
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
    a generator of tuples
    """
    ...

def deep_flatten(xs: list) -> list:
    """
    flattens a potentially deep nested list, i.e. the elements of sublists
    (and sublists of sublists and so on) will be collected into one list,
    e.g. [[1,2],3] => [1,2,3]
    https://medium.com/swlh/top-useful-python-snippets-that-save-time-38958f256822
    """