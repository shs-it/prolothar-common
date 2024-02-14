# -*- coding: utf-8 -*-

import unittest

from prolothar_common.clustering.activities.activity_k_medoid import ActivityKMedoid
from prolothar_common.models.eventlog import EventLog

class TestActivityKMedoid(unittest.TestCase):

    def test_cluster_fuzzy(self):
        log = EventLog.create_from_simple_activity_log([
            ['0','1','2','4','5','4','5','1','2','6'],
            ['0','1','2','4','5','4','5','1','2','6'],
            ['0','1','2','4','5','4','5','4','5','1','2','6'],
            ['0','1','2','4','5','4','5','1','7','2','6'],
            ['0','1','2','4','5','1','2','6'],
            ['0','7','8','6']
        ])
        membership_dict, medoids = ActivityKMedoid(
                log, fuzzy=True).cluster_activities(2, random_seed=42)

        self.assertEqual(2, len(medoids))
        self.assertEqual(8, len(membership_dict))

    def test_cluster_nonfuzzy(self):
        log = EventLog.create_from_simple_activity_log([
            ['0','1','2','4','5','4','5','1','2','6'],
            ['0','1','2','4','5','4','5','1','2','6'],
            ['0','1','2','4','5','4','5','4','5','1','2','6'],
            ['0','1','2','4','5','4','5','1','7','2','6'],
            ['0','1','2','4','5','1','2','6'],
            ['0','7','8','6']
        ])
        membership_dict, medoids = ActivityKMedoid(
                log, fuzzy=False).cluster_activities(2, random_seed=42)

        self.assertEqual(2, len(medoids))
        self.assertEqual(8, len(membership_dict))

if __name__ == '__main__':
    unittest.main()