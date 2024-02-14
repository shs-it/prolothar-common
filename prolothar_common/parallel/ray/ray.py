# -*- coding: utf-8 -*-

from typing import List

import ray as ray_framework

from prolothar_common.parallel.abstract.computation_engine import ComputationEngine
from prolothar_common.parallel.ray.partitionable.ray_partitionable_list import RayPartitionableList

class RayComputationEngine(ComputationEngine):
    """
    computation engine that uses the Ray framework for distributed computations.
    https://github.com/ray-project/ray
    """

    def __init__(self, **kwargs):
        """
        configures and intializes the ray framework if it is not initialized

        https://docs.ray.io/en/master/package-ref.html
        """
        if not ray_framework.is_initialized():
            ray_framework.init(**kwargs)

    def create_partitionable_list(self, l: List) -> RayPartitionableList:
        return RayPartitionableList(l)
