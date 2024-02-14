# -*- coding: utf-8 -*-

import unittest
from prolothar_common.models.eventlog import EventLog
from prolothar_common.models.log_statistics import LogStatistics
import pandas as pd
import numpy as np

class TestLogStatistics(unittest.TestCase):

    def setUp(self) -> None:
        csv_log = pd.read_csv(
                'prolothar_tests/resources/logs/example_log_for_statistics.csv',
                delimiter=',')
        event_log = EventLog.create_from_pandas_df(
                csv_log, 'TraceId', 'Activity', event_attribute_columns=['Duration'])
        self.log_statistics = LogStatistics(event_log)

    def test_compute_activity_statistics_df(self):
        df = self.log_statistics.compute_activity_statistics_df(
                trace_id_attribute='TraceId',
                continuous_event_attributes=['Duration'])

        self.assertCountEqual(
                ['Bathroom', 'Breakfast', 'Dinner', 'Sleeping', 'StandUp', 'Work'],
                df.index)
        self.assertListEqual(
                [5, 4, 5, 6, 6, 4],
                df['support'].values.tolist())
        self.assertListEqual(
                [5, 4, 5, 5, 5, 4],
                df['traces'].values.tolist())
        self.assertTrue(np.isclose(
                [5/30, 4/30, 5/30, 6/30, 6/30, 4/30],
                df['frequency'].values
                ).all())
        self.assertListEqual(
                [1.0, 0.8, 1.0, 1.0, 1.0, 0.8],
                df['frequency_traces'].values.tolist())
        self.assertListEqual(
                [15, 15, 30, 30, 5, 490],
                df['min(Duration)'].values.tolist())
        self.assertListEqual(
                [25, 30, 60, 800, 30, 600],
                df['max(Duration)'].values.tolist())
        self.assertTrue(np.isclose(
                [22.0, 18.75, 37, 438.33333, 10, 542.5],
                df['mean(Duration)'].values
                ).all())
        self.assertListEqual(
                [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                df['P(a|start)'].values.tolist())
        self.assertListEqual(
                [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                df['P(a|end)'].values.tolist())
        self.assertTrue(np.isclose(
                [0.0, 0.0, 0.0, 0.0, 5/6, 0.0],
                df['P(start|a)'].values.tolist()).all())
        self.assertTrue(np.isclose(
                [0.0, 0.0, 0.0, 5/6, 0.0, 0.0],
                df['P(end|a)'].values.tolist()).all())

    def test_compute_variant_statistics_df(self):
        df = self.log_statistics.compute_variant_statistics_df()
        self.assertEqual(3, len(df))
        self.assertEqual(5, sum(df['Count']))

    def test_compute_trace_statistics(self):
        trace_statistics = self.log_statistics.compute_trace_statistics()
        self.assertEqual(trace_statistics.nr_of_traces, 5)
        self.assertEqual(trace_statistics.nr_of_variants, 3)
        self.assertEqual(trace_statistics.min_trace_length, 5)
        self.assertEqual(trace_statistics.average_trace_length, 6)
        self.assertEqual(trace_statistics.max_trace_length, 7)

if __name__ == '__main__':
    unittest.main()