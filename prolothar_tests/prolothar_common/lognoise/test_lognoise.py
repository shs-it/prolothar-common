# -*- coding: utf-8 -*-

import unittest

from prolothar_common.lognoise.remove_events import RemoveEvents
from prolothar_common.lognoise.swap_events import SwapEvents
from prolothar_common.lognoise.add_activity import AddActivity
from prolothar_common.lognoise.combined_noise import CombinedNoise

from prolothar_common.models.eventlog import EventLog

class TestRemoveEvents(unittest.TestCase):

    def setUp(self):
        self.event_log = EventLog.create_from_simple_activity_log([
            [0,0,0,1,2,3,4,5,4,5,6],
            [0,0,0,1,2,3,4,5,4,5,6],
            [0,0,1,2,3,4,5,4,5,4,5,6],
            [0,0,0,1,3,2,4,5,4,5,6],
            [0,0,1,3,2,4,5,4,5,6],
            [0,7,8,6]
        ])

    def test_remove_events(self):
        for unallowed_probability in [-0.1, 1.0, 1.1]:
            try:
                RemoveEvents(unallowed_probability)
                self.fail(msg='probability %r should lead to ValueError' %
                          unallowed_probability)
            except ValueError:
                pass

        original_log = self.event_log.copy()
        RemoveEvents(0).apply(self.event_log)
        self.assertEqual(original_log, self.event_log)

        RemoveEvents(0.5, random_seed=42).apply(self.event_log)
        self.assertEqual(
                original_log.count_nr_of_events() // 2,
                self.event_log.count_nr_of_events())

    def test_swap_events(self):
        for unallowed_probability in [-0.1, 1.0, 1.1]:
            try:
                SwapEvents(unallowed_probability)
                self.fail(msg='probability %r should lead to ValueError' %
                          unallowed_probability)
            except ValueError:
                pass

        original_log = self.event_log.copy()
        SwapEvents(0).apply(self.event_log)
        self.assertEqual(original_log, self.event_log)

        SwapEvents(0.5, random_seed=42).apply(self.event_log)
        self.assertEqual(
                original_log.count_nr_of_events(),
                self.event_log.count_nr_of_events())

    def test_add_foreign_activities(self):
        for unallowed_probability in [-0.1, 1.0, 1.1]:
            try:
                AddActivity('a', unallowed_probability)
                self.fail(msg='probability %r should lead to ValueError' %
                          unallowed_probability)
            except ValueError:
                pass

        original_log = self.event_log.copy()
        AddActivity('#', 0).apply(self.event_log)
        self.assertEqual(original_log, self.event_log)

        AddActivity('#', 0.1, random_seed=42).apply(self.event_log)
        self.assertLess(
                original_log.count_nr_of_events(),
                self.event_log.count_nr_of_events())

    def test_combined_noise(self):
        combined_noise = CombinedNoise([
                RemoveEvents(0.1, random_seed=42),
                SwapEvents(0.1, random_seed=42),
                AddActivity('a', 0.1, random_seed=42)
        ])

        original_log = self.event_log.copy()
        combined_noise.apply(self.event_log)
        self.assertNotEqual(original_log, self.event_log)

if __name__ == '__main__':
    unittest.main()