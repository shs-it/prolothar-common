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

from typing import List, Hashable, FrozenSet, Tuple

def set_abstraction(prefix: List[Hashable]) -> FrozenSet:
    return frozenset(prefix)

def list_abstraction(prefix: List[Hashable]) -> Tuple:
    return tuple(prefix)

def last_abstraction(prefix: List[Hashable]) -> Hashable:
    try:
        return prefix[-1]
    except IndexError:
        return None

def last_n_abstraction(n: int):
    def state_representation(prefix: List[Hashable]):
        return tuple(prefix[-n:])
    return state_representation
