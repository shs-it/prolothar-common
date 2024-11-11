# -*- coding: utf-8 -*-

import unittest
from prolothar_common.models.eventlog import EventLog, Trace, Event, ComplexEvent
import io
import pandas as pd
from datetime import datetime, timedelta

class TestEventLog(unittest.TestCase):

    def setUp(self):
        self.event_log = EventLog()

    def test_get_nr_of_traces(self):
        self.assertEqual(0, self.event_log.get_nr_of_traces())

        self.event_log.add_trace(Trace(0, [Event('start computer')]))
        self.event_log.add_trace(Trace(1, [Event('drink coffee')]))
        self.event_log.add_trace(Trace(2, [ComplexEvent('develop software', [
                Event('think'), Event('implement'), Event('test')])]))
        self.event_log.add_trace(Trace(3, [Event('shutdown computer')]))

        self.assertEqual(4, self.event_log.get_nr_of_traces())

    def test_create_trace_without_events(self):
        try:
            Trace(0, [])
            self.fail(msg='creating an empty Trace should lead to ValueError')
        except ValueError:
            pass

    def test_complex_event_without_children(self):
        try:
            ComplexEvent('complexevent', [])
            self.fail(msg=('creating a ComplexEvent without children should '
                           'lead to ValueError'))
        except ValueError:
            pass

    def test_create_from_simple_activity_log(self):
        self.maxDiff = None
        event_log = EventLog.create_from_simple_activity_log([    
            ['0', '0', '0', '1', '2', '3', '4', '5', '4', '5', '6'],
            ['0', '0', '0', '1', '2', '3', '4', '5', '4', '5', '6'],
            ['0', '0', '1', '2', '3', '4', '5', '4', '5', '4', '5', '6'],
            ['0', '0', '0', '1', '3', '2', '4', '5', '4', '5', '6'],
            ['0', '0', '1', '3', '2', '4', '5', '4', '5', '6'],
            ['0', '7', '8', '6']
        ])
        self.assertEqual(6, event_log.get_nr_of_traces())
        self.assertEqual(('==========\n'
                          'EventLog with 6 traces\n'
                          '----------\n'
                          "Trace(id=0)['0', '0', '0', '1', '2', '3', '4', '5', '4', '5', '6']\n"
                          "Trace(id=1)['0', '0', '0', '1', '2', '3', '4', '5', '4', '5', '6']\n"
                          "Trace(id=2)['0', '0', '1', '2', '3', '4', '5', '4', '5', '4', '5', '6']\n"
                          "Trace(id=3)['0', '0', '0', '1', '3', '2', '4', '5', '4', '5', '6']\n"
                          "Trace(id=4)['0', '0', '1', '3', '2', '4', '5', '4', '5', '6']\n"
                          "Trace(id=5)['0', '7', '8', '6']\n"
                          '==========\n'), repr(event_log))

    def test_to_simple_activity_log(self):
        self.event_log.add_trace(Trace(0, [Event('start computer'),
                                        Event('drink coffee'),
                                        Event('shutdown computer')]))
        self.event_log.add_trace(Trace(1, [Event('start computer'),
                                        Event('shutdown computer'),
                                        Event('go home')]))
        self.assertCountEqual(
            [['start computer', 'drink coffee', 'shutdown computer'],
             ['start computer', 'shutdown computer', 'go home']],
            self.event_log.to_simple_activity_log())

    def test_write_to_csv(self):
        self.event_log.add_trace(Trace(0, [Event('A'),
                                        Event('B'),
                                        Event('C')]))
        self.event_log.add_trace(Trace(1, [Event('A'),
                                        Event('D'),
                                        Event('C')]))
        csv_writer = io.StringIO()
        self.event_log.write_to_csv(csv_writer,
                                    trace_id_column='TraceNr',
                                    activity_column='Activity',
                                    separator=',')
        self.assertEqual(('TraceNr,Activity\n'
                          '0,A\n'
                          '0,B\n'
                          '0,C\n'
                          '1,A\n'
                          '1,D\n'
                          '1,C\n'), csv_writer.getvalue())

    def test_create_from_pandas_df(self):
        df  = pd.DataFrame([
                        [0, 'Receive Order', 'Germany'],
                        [0, 'Accept Order', 'Germany'],
                        [1, 'Receive Order', 'France'],
                        [0, 'Produce', 'Germany'],
                        [0, 'Test', 'Germany'],
                        [0, 'Deliver', 'Germany'],
                        [1, 'Reject Order', 'France'],
                     ],
                     columns=['CaseId', 'Activity', 'Location'])

        expected_event_log = EventLog()
        expected_event_log.add_trace(Trace(0, [
            Event('Receive Order', attributes={'Location': 'Germany'}),
            Event('Accept Order', attributes={'Location': 'Germany'}),
            Event('Produce', attributes={'Location': 'Germany'}),
            Event('Test', attributes={'Location': 'Germany'}),
            Event('Deliver', attributes={'Location': 'Germany'})],
            attributes={'CaseId': 0}))
        expected_event_log.add_trace(Trace(1, [
            Event('Receive Order', attributes={'Location': 'France'}),
            Event('Reject Order', attributes={'Location': 'France'})],
            attributes={'CaseId': 1}))

        actual_event_log = EventLog.create_from_pandas_df(
                df, 'CaseId', 'Activity', event_attribute_columns=['Location'])
        self.assertEqual(expected_event_log, actual_event_log)

    def test_create_from_pandas_df_with_trace_attributes(self):
        df  = pd.DataFrame([
                        [0, 'Receive Order', 'Germany'],
                        [0, 'Accept Order', 'Germany'],
                        [1, 'Receive Order', 'France'],
                        [0, 'Produce', 'Germany'],
                        [0, 'Test', 'Germany'],
                        [0, 'Deliver', 'Germany'],
                        [1, 'Reject Order', 'France'],
                     ],
                     columns=['CaseId', 'Activity', 'Location'])

        expected_event_log = EventLog()
        expected_event_log.add_trace(Trace(0, [
            Event('Receive Order'),
            Event('Accept Order'),
            Event('Produce'),
            Event('Test'),
            Event('Deliver')],
            attributes={'CaseId': 0, 'Location': 'Germany'}))
        expected_event_log.add_trace(Trace(1, [
            Event('Receive Order'),
            Event('Reject Order')],
            attributes={'CaseId': 1, 'Location': 'France'}))

        actual_event_log = EventLog.create_from_pandas_df(
                df, 'CaseId', 'Activity', trace_attribute_columns=['Location'])

        self.assertEqual(expected_event_log, actual_event_log)

    def test_compute_activity_set(self):
        self.event_log.add_trace(Trace(0, [Event('A')]))
        self.event_log.add_trace(Trace(1, [Event('B')]))
        self.event_log.add_trace(Trace(2, [ComplexEvent('C', [
                Event('C1'), Event('C2'), Event('C3')])]))
        self.event_log.add_trace(Trace(3, [Event('B')]))
        self.assertSetEqual(set(['A', 'B', 'C']),
                            self.event_log.compute_activity_set())

    def test_derive_event_duration_by_end_date(self):
        df  = pd.DataFrame([
                [0, 'Receive Order', 'Germany', datetime(2019, 1, 1, 12)],
                [0, 'Accept Order', 'Germany', datetime(2019, 1, 1, 13)],
                [0, 'Produce', 'Germany', datetime(2019, 1, 5, 18)],
                [0, 'Test', 'Germany', datetime(2019, 1, 6, 10)],
                [0, 'Deliver', 'Germany', datetime(2019, 1, 6, 12)],
            ],
            columns=['CaseId', 'Activity', 'Location', 'Enddate'])
        eventlog = EventLog.create_from_pandas_df(
            df, 'CaseId', 'Activity',
            event_attribute_columns=['Location', 'Enddate'])
        eventlog.derive_event_duration_by_end_date('Startdate', 'Enddate',
                                                   'Duration')

        expected_trace = Trace(0, [
            Event('Receive Order', attributes={'Location': 'Germany',
                                               'Startdate': datetime(2019, 1, 1, 12),
                                               'Enddate': datetime(2019, 1, 1, 12),
                                               'Duration': timedelta(0)}),
            Event('Accept Order', attributes={'Location': 'Germany',
                                              'Startdate': datetime(2019, 1, 1, 12),
                                              'Enddate': datetime(2019, 1, 1, 13),
                                              'Duration': timedelta(hours=1)}),
            Event('Produce', attributes={'Location': 'Germany',
                                              'Startdate': datetime(2019, 1, 1, 13),
                                              'Enddate': datetime(2019, 1, 5, 18),
                                              'Duration': timedelta(days=4, hours=5)}),
            Event('Test', attributes={'Location': 'Germany',
                                              'Startdate': datetime(2019, 1, 5, 18),
                                              'Enddate': datetime(2019, 1, 6, 10),
                                              'Duration': timedelta(hours=16)}),
            Event('Deliver', attributes={'Location': 'Germany',
                                              'Startdate': datetime(2019, 1, 6, 10),
                                              'Enddate': datetime(2019, 1, 6, 12),
                                              'Duration': timedelta(hours=2)})],
            attributes={'CaseId': 0})
        for event in expected_trace.events:
            event.attributes['Startdate'] = pd.Timestamp(
                    event.attributes['Startdate'])
            event.attributes['Enddate'] = pd.Timestamp(
                    event.attributes['Enddate'])
            event.attributes['Duration'] = pd.Timedelta(
                    event.attributes['Duration'])
        self.assertEqual(expected_trace, eventlog.traces[0])

    def test_join_sucessive_events_with_same_activity(self):
        df  = pd.DataFrame([
                [0, 'Receive Order', 'Germany', datetime(2019, 1, 1, 12)],
                [0, 'Accept Order', 'Germany', datetime(2019, 1, 1, 13)],
                [0, 'Produce', 'Germany', datetime(2019, 1, 2, 18)],
                [0, 'Produce', 'Germany', datetime(2019, 1, 3, 18)],
                [0, 'Produce', 'Germany', datetime(2019, 1, 4, 18)],
                [0, 'Produce', 'Germany', datetime(2019, 1, 5, 18)],
                [0, 'Test', 'Germany', datetime(2019, 1, 6, 10)],
                [0, 'Deliver', 'Germany', datetime(2019, 1, 6, 12)],
            ],
            columns=['CaseId', 'Activity', 'Location', 'Enddate'])
        eventlog = EventLog.create_from_pandas_df(
            df, 'CaseId', 'Activity',
            event_attribute_columns=['Location', 'Enddate'])
        eventlog.derive_event_duration_by_end_date('Startdate', 'Enddate',
                                                   'Duration')
        eventlog.join_sucessive_events_with_same_activity(
            startdate_attribute='Startdate', enddate_attribute='Enddate',
            duration_attribute='Duration', raise_error_for_attributes=True)

        expected_trace = Trace(0, [
            Event('Receive Order', attributes={'Location': 'Germany',
                                               'Startdate': datetime(2019, 1, 1, 12),
                                               'Enddate': datetime(2019, 1, 1, 12),
                                               'Duration': timedelta(0)}),
            Event('Accept Order', attributes={'Location': 'Germany',
                                              'Startdate': datetime(2019, 1, 1, 12),
                                              'Enddate': datetime(2019, 1, 1, 13),
                                              'Duration': timedelta(hours=1)}),
            Event('Produce', attributes={'Location': 'Germany',
                                              'Startdate': datetime(2019, 1, 1, 13),
                                              'Enddate': datetime(2019, 1, 5, 18),
                                              'Duration': timedelta(days=4, hours=5)}),
            Event('Test', attributes={'Location': 'Germany',
                                              'Startdate': datetime(2019, 1, 5, 18),
                                              'Enddate': datetime(2019, 1, 6, 10),
                                              'Duration': timedelta(hours=16)}),
            Event('Deliver', attributes={'Location': 'Germany',
                                              'Startdate': datetime(2019, 1, 6, 10),
                                              'Enddate': datetime(2019, 1, 6, 12),
                                              'Duration': timedelta(hours=2)})],
            attributes={'CaseId': 0})
        for event in expected_trace.events:
            event.attributes['Startdate'] = pd.Timestamp(
                    event.attributes['Startdate'])
            event.attributes['Enddate'] = pd.Timestamp(
                    event.attributes['Enddate'])
            event.attributes['Duration'] = pd.Timedelta(
                    event.attributes['Duration'])
        self.assertEqual(expected_trace, eventlog.traces[0])

    def test_count_nr_of_events(self):
        self.assertEqual(0, self.event_log.count_nr_of_events())

        self.event_log.add_trace(Trace(0, [Event('start computer')]))
        self.event_log.add_trace(Trace(1, [Event('drink coffee'),
                                        Event('program'),
                                        Event('program')]))
        self.event_log.add_trace(Trace(2, [Event('shutdown computer')]))

        self.assertEqual(5, self.event_log.count_nr_of_events())

    def test_compute_set_of_start_activities(self):
        self.assertSetEqual(set(), self.event_log.compute_set_of_start_activities())
        self.event_log.add_trace(Trace(3, [Event('start computer')]))
        self.event_log.add_trace(Trace(4, [Event('drink coffee'),
                                        Event('program'),
                                        Event('program')]))
        self.event_log.add_trace(Trace(5, [Event('shutdown computer')]))
        self.assertSetEqual(
                set(['start computer', 'drink coffee', 'shutdown computer']),
                self.event_log.compute_set_of_start_activities())

    def test_to_pandas_df(self):
        df  = pd.DataFrame([
                        [0, 'Receive Order', 'Germany'],
                        [0, 'Accept Order', 'Germany'],
                        [0, 'Produce', 'Germany'],
                        [0, 'Test', 'Germany'],
                        [0, 'Deliver', 'Germany'],
                        [1, 'Receive Order', 'France'],
                        [1, 'Reject Order', 'France'],
                     ],
                     columns=['CaseId', 'Activity', 'Location'])

        log = EventLog.create_from_pandas_df(
                df, 'CaseId', 'Activity', event_attribute_columns=['Location'])

        if not df.equals(log.to_pandas_df()):
            print(df)
            print(log.to_pandas_df())
            self.fail('dataframes are not equal')

    def test_to_pandas_df_with_heterogenous_event_attributes(self):
        df  = pd.DataFrame([
                        [0, 'Receive Order', 'Germany', None],
                        [0, 'Accept Order', 'Germany', None],
                        [0, 'Produce', 'Germany', None],
                        [0, 'Test', 'Germany', None],
                        [0, 'Deliver', 'Germany', None],
                        [1, 'Receive Order', 'France', 'yellow'],
                        [1, 'Reject Order', 'France', 'green'],
                     ],
                     columns=['CaseId', 'Activity', 'Location', 'XColor'])

        log = EventLog.create_from_pandas_df(
                df, 'CaseId', 'Activity', event_attribute_columns=['Location', 'XColor'],
                add_none_attributes=True)

        if not df.equals(log.to_pandas_df()):
            print(df)
            print(log.to_pandas_df())
            self.fail('dataframes are not equal')

    def test_cut_traces(self):
        self.maxDiff = None
        event_log = EventLog.create_from_simple_activity_log([
            ['0', '0', '0', '1', '2', '3', '4', '5', '4', '5', '6'],
            ['0', '0', '0', '1', '2', '3', '4', '5', '4', '5', '6'],
            ['0', '0', '1', '2', '3', '4', '5', '4', '5', '4', '5', '6'],
            ['0', '0', '0', '1', '3', '2', '4', '5', '4', '5', '6'],
            ['0', '0', '1', '3', '2', '4', '5', '4', '5', '6'],
            ['0', '7', '8', '6']
        ])

        event_log.cut_traces(['1'], ['5'])

        expected_log = EventLog.create_from_simple_activity_log([
            ['1', '2', '3', '4', '5', '4', '5'],
            ['1', '2', '3', '4', '5', '4', '5'],
            ['1', '2', '3', '4', '5', '4', '5', '4', '5'],
            ['1', '3', '2', '4', '5', '4', '5'],
            ['1', '3', '2', '4', '5', '4', '5'],
        ])

        self.assertEqual(expected_log, event_log)

    def test_filter_activities(self):
        event_log = EventLog.create_from_simple_activity_log([
            ['0', '0', '0', '1', '2', '3', '4', '5', '4', '5', '6'],
            ['0', '0', '0', '1', '2', '3', '4', '5', '4', '5', '6'],
            ['0', '0', '1', '2', '3', '4', '5', '4', '5', '4', '5', '6'],
            ['0', '0', '0', '1', '3', '2', '4', '5', '4', '5', '6'],
            ['0', '0', '1', '3', '2', '4', '5', '4', '5', '6'],
            ['0', '7', '8', '6']
        ])

        event_log.filter_activities(set(['0','1','2','4','5','6']))

        expected_log = EventLog.create_from_simple_activity_log([
            ['0', '0', '0', '1', '2', '4', '5', '4', '5', '6'],
            ['0', '0', '0', '1', '2', '4', '5', '4', '5', '6'],
            ['0', '0', '1', '2', '4', '5', '4', '5', '4', '5', '6'],
            ['0', '0', '0', '1', '2', '4', '5', '4', '5', '6'],
            ['0', '0', '1', '2', '4', '5', '4', '5', '6'],
            ['0', '6']
        ])

        self.assertEqual(expected_log, event_log)

    def test_count_follows_directly_or_indirectly(self):
        event_log = EventLog.create_from_simple_activity_log([
            ['A','B','C','A','B','A','C']
        ])
        self.assertDictEqual({
            ('A','A'): 2,
            ('A','B'): 2,
            ('A','C'): 2,
            ('B','A'): 2,
            ('B','B'): 1,
            ('B','C'): 2,
            ('C','A'): 2,
            ('C','B'): 1,
            ('C','C'): 1,
        }, event_log.count_follows_directly_or_indirectly())

    def test_keep_first_activity_occurence_only(self):
        event_log = EventLog.create_from_simple_activity_log([
            ['0', '0', '0', '1', '2', '3', '4', '5', '4', '5', '6'],
            ['0', '0', '0', '1', '2', '3', '4', '5', '4', '5', '6'],
            ['0', '0', '1', '2', '3', '4', '5', '4', '5', '4', '5', '6'],
            ['0', '0', '0', '1', '3', '2', '4', '5', '4', '5', '6'],
            ['0', '0', '1', '3', '2', '4', '5', '4', '5', '6'],
            ['0', '7', '8', '6']
        ])
        event_log.keep_first_occurence_of_activity_only()
        self.assertEqual(
            [
                ['0', '1', '2', '3', '4', '5', '6'],
                ['0', '1', '2', '3', '4', '5', '6'],
                ['0', '1', '2', '3', '4', '5', '6'],
                ['0', '1', '3', '2', '4', '5', '6'],
                ['0', '1', '3', '2', '4', '5', '6'],
                ['0', '7', '8', '6']
            ],
            event_log.to_simple_activity_log()
        )

    def test_k_folds(self):
        event_log = EventLog.create_from_simple_activity_log([
            ['0', '0', '0', '1', '2', '3', '4', '5', '4', '5', '6'],
            ['0', '0', '0', '1', '2', '3', '4', '5', '4', '5', '6'],
            ['0', '0', '1', '2', '3', '4', '5', '4', '5', '4', '5', '6'],
            ['0', '0', '0', '1', '3', '2', '4', '5', '4', '5', '6'],
            ['0', '0', '1', '3', '2', '4', '5', '4', '5', '6'],
            ['0', '7', '8', '6']
        ])

        try:
            event_log.k_folds(1)
            self.fail('ValueError expected')
        except ValueError:
            pass

        i = 0
        for train_log, test_log in event_log.k_folds(3):
            i += 1
            self.assertEqual(4, train_log.get_nr_of_traces())
            self.assertEqual(2, test_log.get_nr_of_traces())
            train_trace_ids = set(t.get_id() for t in train_log.traces)
            test_trace_ids = set(t.get_id() for t in test_log.traces)
            self.assertFalse(train_trace_ids.intersection(test_trace_ids))
            self.assertSetEqual(
                set(range(6)), train_trace_ids.union(test_trace_ids))
        self.assertEqual(3, i)

    def test_train_test_split(self):
        event_log = EventLog.create_from_simple_activity_log([
            ['0', '0', '0', '1', '2', '3', '4', '5', '4', '5', '6'],
            ['0', '0', '0', '1', '2', '3', '4', '5', '4', '5', '6'],
            ['0', '0', '1', '2', '3', '4', '5', '4', '5', '4', '5', '6'],
            ['0', '0', '0', '1', '3', '2', '4', '5', '4', '5', '6'],
            ['0', '0', '1', '3', '2', '4', '5', '4', '5', '6'],
            ['0', '7', '8', '6']
        ])

        with self.assertRaises(ValueError):
            event_log.train_test_split(-0.0001)
        with self.assertRaises(ValueError):
            event_log.train_test_split(1.0001)

        train_log, test_log = event_log.train_test_split(0.0)
        self.assertEqual((6, 0), (len(train_log), len(test_log)))
        train_log, test_log = event_log.train_test_split(1.0)
        self.assertEqual((0, 6), (len(train_log), len(test_log)))
        train_log, test_log = event_log.train_test_split(0.5)
        self.assertEqual((3, 3), (len(train_log), len(test_log)))
        train_log, test_log = event_log.train_test_split(0.2)
        self.assertEqual((4, 2), (len(train_log), len(test_log)))

    def test_to_and_from_dict(self):
        log = EventLog()
        log.add_trace(Trace(0, [
            Event('Receive Order', attributes={'Location': 'Germany'}),
            Event('Produce', attributes={'Location': 'Germany'}),
            Event('Deliver', attributes={'Location': 'Italy'})],
            attributes={'CaseId': 0}))
        log.add_trace(Trace(1, [
            Event('Receive Order', attributes={'Location': 'France'}),
            Event('Reject Order', attributes={'Location': 'France'})],
            attributes={'CaseId': 1}))

        actual_dict = log.to_dict()

        expected_dict = {
            'traces': [
                {
                    'id': 0,
                    'events': [
                        {
                            'activity_name': 'Receive Order',
                            'attributes': {
                                'Location': 'Germany'
                            }
                        },
                        {
                            'activity_name': 'Produce',
                            'attributes': {
                                'Location': 'Germany'
                            }
                        },
                        {
                            'activity_name': 'Deliver',
                            'attributes': {
                                'Location': 'Italy'
                            }
                        }
                    ],
                    'attributes': {
                        'CaseId': 0
                    }
                },
                {
                    'id': 1,
                    'events': [
                        {
                            'activity_name': 'Receive Order',
                            'attributes': {
                                'Location': 'France'
                            }
                        },
                        {
                            'activity_name': 'Reject Order',
                            'attributes': {
                                'Location': 'France'
                            }
                        }
                    ],
                    'attributes': {
                        'CaseId': 1
                    }
                }
            ]
        }

        self.assertDictEqual(expected_dict, actual_dict)

        reparsed_log = EventLog.create_from_dict(expected_dict)
        self.assertEqual(log, reparsed_log)

if __name__ == '__main__':
    unittest.main()