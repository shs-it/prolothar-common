# -*- coding: utf-8 -*-

from typing import List

from prolothar_common.parallel.abstract.computation_engine import ComputationEngine
from prolothar_common.parallel.single_thread.partitionable.local_partitionable_list import LocalPartitionableList

class SingleThreadComputationEngine(ComputationEngine):
    """computation engine that makes all computations in a single thread"""

    def create_partitionable_list(self, l: List) -> LocalPartitionableList:
        return LocalPartitionableList(l)
