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

from typing import List,Callable

from prolothar_common.parallel.abstract.partitionable.partitionable_list import PartitionableList
from prolothar_common.parallel.abstract.partitionable.partitionable_list import P,E,R

from functools import reduce

class LocalPartitionableList(PartitionableList):
    """partitionable list implementation for a single thread => no partition"""

    def map(self, parameter: P, map_function: Callable[[P,E],R],
            keep_order: bool = True) -> List[R]:
        return [map_function(parameter, element) for element in self._list]

    def map_filter(self, parameter: P, map_function: Callable[[P,E],R],
                   filter_function: Callable[[P,R],bool]) -> List[R]:
        return [mapped_element for mapped_element
                in self.map(parameter, map_function)
                if filter_function(parameter, mapped_element)]

    def map_reduce(self, parameter: P, map_function: Callable[[P,E],R],
                   reduce_function: Callable[[R,R],R]) -> R:
        return reduce(
                reduce_function,
                (map_function(parameter, element) for element in self._list))