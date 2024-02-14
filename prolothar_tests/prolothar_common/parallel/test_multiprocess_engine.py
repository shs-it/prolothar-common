# -*- coding: utf-8 -*-

import unittest

from prolothar_tests.prolothar_common.parallel.test_engine import TestEngine

from prolothar_common.parallel.abstract.computation_engine import ComputationEngine
from prolothar_common.parallel.multiprocess.multiprocess import MultiprocessComputationEngine

class TestMultiprocessEngine(TestEngine, unittest.TestCase):
    def create_engine(self) -> ComputationEngine:
        return MultiprocessComputationEngine(nr_of_workers=8)

if __name__ == '__main__':
    unittest.main()