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

from prolothar_common.parallel.abstract.computation_engine import ComputationEngine
from prolothar_common.parallel.multiprocess.partitionable.multiprocess_partitionable_list import MultiprocessPartitionableList

import psutil

class MultiprocessComputationEngine(ComputationEngine):
    """computation engine that distributes computations across the local CPU
    using the multiprocess library"""

    def __init__(self, nr_of_workers: int = max(2,psutil.cpu_count()), show_progressbar: bool = False):
        """creates a new MultiprocessComputationEngine

        Args:
            nr_of_workers:
                default is max(2, the number of available cores).
                = the number of workers (cores) to use for computations.
                must be greater 0
            show_progressbar:
                default is False.
                shows progressbars if available. not all functions of
                partitionable list have an implemented progress bar.
        """
        if nr_of_workers <= 0:
            raise ValueError('nr_of_workers must not be <= 0')
        self.__nr_of_workers = nr_of_workers
        self.__show_progressbar = show_progressbar

    def create_partitionable_list(self, l: List) -> MultiprocessPartitionableList:
        return MultiprocessPartitionableList(l, self.__nr_of_workers, show_progressbar=self.__show_progressbar)
