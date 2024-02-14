# -*- coding: utf-8 -*-

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
