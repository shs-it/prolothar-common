# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.eventlog import EventLog
from prolothar_common.clustering.traces.one_hot_activity_clustering import dbscan
from prolothar_common.clustering.traces.one_hot_activity_clustering import optics

class TestOneHotActivityClustering(unittest.TestCase):

    def setUp(self):
        self.log1 = EventLog.create_from_simple_activity_log([
            [0,0,0,1,2,3,4,5,4,5,6],
            [0,0,0,1,2,3,4,5,4,5,6],
            [0,0,1,2,3,4,5,4,5,4,5,6],
            [0,0,0,1,3,2,4,5,4,5,6],
            [0,0,1,3,2,4,5,4,5,6],
            [7,8,9,6],
            [7,8,9,6],
            [7,8,8,8,9,6],
            [7,8,8,8,9,6],
            [7,8,8,9,6],
        ])

    def test_dbscan(self):
        clusters,outliers = dbscan(self.log1)
        self.assertEqual(0, len(outliers))
        self.assertEqual(2, len(clusters))

    def test_optics(self):
        clusters,outliers = optics(self.log1)
        self.assertEqual(0, len(outliers))
        self.assertEqual(2, len(clusters))

if __name__ == '__main__':
    unittest.main()