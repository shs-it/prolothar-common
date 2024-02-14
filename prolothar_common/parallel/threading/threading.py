# -*- coding: utf-8 -*-

from typing import List

from prolothar_common.parallel.abstract.computation_engine import ComputationEngine
from prolothar_common.parallel.threading.partitionable.threading_partitionable_list import ThreadingPartitionableList

import psutil

class ThreadingComputationEngine(ComputationEngine):
    """computation engine that distributes computations across the local CPU
    using the threading library"""

    def __init__(self, nr_of_workers: int = max(2,psutil.cpu_count())):
        """creates a new MultithreadComputationEngine

        Args:
            nr_of_workers:
                default is max(2, the number of available cores).
                = the number of workers (cores) to use for computations.
                must be greater 0
        """
        if nr_of_workers <= 0:
            raise ValueError('nr_of_workers must not be <= 0')
        self.__nr_of_workers = nr_of_workers

    def create_partitionable_list(self, l: List) -> ThreadingPartitionableList:
        return ThreadingPartitionableList(l, self.__nr_of_workers)
