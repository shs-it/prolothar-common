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

from typing import List

from abc import ABC, abstractmethod

from prolothar_common.parallel.abstract.partitionable.partitionable_list import PartitionableList

class ComputationEngine(ABC):
    """interface for a computation engine that creates parallelizable
    containers"""

    @abstractmethod
    def create_partitionable_list(self, l: List) -> PartitionableList:
        """create a list that can be processed with a parallel operation"""
        pass
