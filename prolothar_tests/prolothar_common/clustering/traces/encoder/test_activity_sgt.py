# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.eventlog import EventLog
from prolothar_common.clustering.traces.encoder import ActivitySgt

class TestActivitySgt(unittest.TestCase):

    def setUp(self):
        self.log = EventLog.create_from_simple_activity_log([
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

    def test_encode_log(self):
        sgt_embedded_log = ActivitySgt().encode_log(self.log)
        self.assertEqual((len(self.log), 33), sgt_embedded_log.shape)

if __name__ == '__main__':
    unittest.main()