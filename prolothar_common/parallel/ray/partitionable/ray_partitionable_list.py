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