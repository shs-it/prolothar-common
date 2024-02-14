# -*- coding: utf-8 -*-

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