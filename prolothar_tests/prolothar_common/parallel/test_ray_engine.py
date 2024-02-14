# -*- coding: utf-8 -*-

import unittest

from prolothar_tests.prolothar_common.parallel.test_engine import TestEngine

from prolothar_common.parallel.abstract.computation_engine import ComputationEngine
from prolothar_common.parallel.ray.ray import RayComputationEngine

class TestRayEngine(TestEngine, unittest.TestCase):
    def create_engine(self) -> ComputationEngine:
        return RayComputationEngine()

if __name__ == '__main__':
    unittest.main()