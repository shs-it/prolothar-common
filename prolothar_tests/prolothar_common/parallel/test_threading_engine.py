# -*- coding: utf-8 -*-

import unittest

from prolothar_tests.prolothar_common.parallel.test_engine import TestEngine

from prolothar_common.parallel.abstract.computation_engine import ComputationEngine
from prolothar_common.parallel.threading.threading import ThreadingComputationEngine

class TestMultiprocessEngine(TestEngine, unittest.TestCase):
    def create_engine(self) -> ComputationEngine:
        return ThreadingComputationEngine(nr_of_workers=8)

if __name__ == '__main__':
    unittest.main()