# -*- coding: utf-8 -*-

from typing import List,Callable

from functools import reduce

import ray

from prolothar_common.parallel.abstract.partitionable.partitionable_list import PartitionableList
from prolothar_common.parallel.abstract.partitionable.partitionable_list import P,E,R

class RayPartitionableList(PartitionableList):
    """partitionable list implementation for a Ray"""

    def map(
            self, parameter: P, map_function: Callable[[P,E],R],
            keep_order: bool = True) -> List[R]:
        remote_map_function = ray.remote(map_function)
        return ray.get([
            remote_map_function.remote(parameter, element)
            for element in self._list
        ])

    def map_filter(self, parameter: P, map_function: Callable[[P,E],R],
                   filter_function: Callable[[P,R],bool]) -> List[R]:
        remote_map_function = ray.remote(map_function)
        remote_filter_function = ray.remote(filter_function)
        mapped_elements = [
            remote_map_function.remote(parameter, element)
            for element in self._list
        ]
        return ray.get([
            element for element in mapped_elements
            if ray.get(remote_filter_function.remote(parameter, element))
        ])

    def map_reduce(self, parameter: P, map_function: Callable[[P,E],R],
                   reduce_function: Callable[[R,R],R]) -> R:
        mapped_elements = self.map(parameter, map_function)
        return reduce(reduce_function, mapped_elements)