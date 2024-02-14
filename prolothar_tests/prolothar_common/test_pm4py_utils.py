# -*- coding: utf-8 -*-

import unittest

import pandas as pd

from prolothar_common.pm4py_utils import convert_data_petri_net_to_pm4py
from prolothar_common.pm4py_utils import convert_eventlog_to_pm4py
from prolothar_common.pm4py_utils import convert_pm4py_log
from prolothar_common.pm4py_utils import convert_pm4py_to_data_petri_net

from prolothar_common.models.data_petri_net import DataPetriNet
from prolothar_common.models.data_petri_net import Place
from prolothar_common.models.data_petri_net import Transition

from prolothar_common.models.eventlog import EventLog

from prolothar_common.models.activity_pattern import ActivityPattern
from prolothar_common.models.activity_pattern import parallel

class TestPm4pyUtils(unittest.TestCase):

    def test_convert_data_petri_net_to_pm4py_and_back(self):
        petri_net = DataPetriNet()
        start_place = petri_net.add_place(
                Place.with_id_label('start', nr_of_tokens=1))
        mid_place = petri_net.add_place(Place.with_empty_label('mid'))
        end_place = petri_net.add_place(Place.with_id_label('end'))

        t1 = petri_net.add_transition(Transition('t1'))
        t2 = petri_net.add_transition(Transition('t2', visible=False))

        petri_net.add_connection(start_place, t1, mid_place)
        petri_net.add_connection(mid_place, t2, end_place)

        pm4py_net, initial_marking, final_marking = convert_data_petri_net_to_pm4py(petri_net)

        self.assertTrue(pm4py_net is not None)
        self.assertTrue(initial_marking is not None)
        self.assertTrue(final_marking is not None)
        self.assertTrue(pm4py_net.places, msg='Places should not be empty')
        self.assertTrue(pm4py_net.transitions, msg='Transitions should not be empty')
        self.assertTrue(pm4py_net.arcs, msg='Arcs should not be empty')
        self.assertCountEqual(["pstart->(tt1, 't1')", 'pmid->(tt2, None)',
                               "(tt1, 't1')->pmid", '(tt2, None)->pend'],
                              list(map(str, pm4py_net.arcs)))
        self.assertEqual("['pstart:1']", str(initial_marking))
        self.assertEqual("['pend:1']", str(final_marking))

        petri_net_back = convert_pm4py_to_data_petri_net(
                pm4py_net, initial_marking)
        self.assertTrue(petri_net_back is not None)
        self.assertEqual(len(petri_net.places), len(petri_net_back.places))
        self.assertEqual(len(petri_net.transitions), len(petri_net_back.transitions))

    def test_convert_data_petri_net_to_pm4py_with_self_loop(self):
        net = DataPetriNet()
        start_place = net.add_place(
                Place.with_id_label('start', nr_of_tokens=1))
        mid_place_1 = net.add_place(Place.with_empty_label('mid1'))
        t1 = net.add_transition(Transition('t1'))
        t2 = net.add_transition(Transition('t2', visible=False))
        net.add_connection(start_place, t1, mid_place_1)
        net.add_connection(mid_place_1, t1, mid_place_1)
        net.add_connection(mid_place_1, t2, start_place)
        net.prune()

        pm4py_net = convert_data_petri_net_to_pm4py(net)[0]
        self.assertCountEqual(["pmid1->(tt1, 't1')", "pstart->(tt1, 't1')", '(tt2, None)->pstart',
                               'pmid1->(tt2, None)', "(tt1, 't1')->pmid1"],
                              list(map(str, pm4py_net.arcs)))

    def test_convert_data_petri_net_to_pm4py_with_choice_and_multi_labels(self):
        petri_net = DataPetriNet()
        p1 = petri_net.add_place(Place.with_empty_label('1'))
        p2 = petri_net.add_place(Place.with_empty_label('2'))
        p3 = petri_net.add_place(Place.with_empty_label('3'))
        t1 = petri_net.add_transition(Transition('T_Admission IC'))
        t2 = petri_net.add_transition(Transition('T_Admission NC'))
        t3 = petri_net.add_transition(Transition('t1', visible=False))
        t4 = petri_net.add_transition(Transition('t2', visible=False))
        petri_net.add_connection(p1, t3, p2)
        petri_net.add_connection(p2, t1, p2)
        petri_net.add_connection(p2, t2, p2)
        petri_net.add_connection(p2, t4, p3)

        pm4py_net = convert_data_petri_net_to_pm4py(petri_net)[0]
        self.assertCountEqual(["(tT_Admission NC, 'T_Admission NC')->p2", "p1->(tt1, None)",
                               "(tt1, None)->p2", "p2->(tT_Admission NC, 'T_Admission NC')",
                               'p2->(tt2, None)', "p2->(tT_Admission IC, 'T_Admission IC')",
                               '(tt2, None)->p3', "(tT_Admission IC, 'T_Admission IC')->p2"],
                              list(map(str, pm4py_net.arcs)))

    def test_convert_data_petri_net_to_pm4py_with_parallel(self):
        petri_net = DataPetriNet()
        p1 = petri_net.add_place(Place.with_empty_label('1'))
        p2 = petri_net.add_place(Place.with_empty_label('2'))
        t1 = petri_net.add_transition(Transition('Return ER'))
        petri_net.add_connection(p1, t1, p2)
        ap = ActivityPattern(petri_net, 'Return ER')

        petri_net = parallel(ap, ap).data_petri_net

        pm4py_net = convert_data_petri_net_to_pm4py(petri_net)[0]
        self.assertCountEqual(["p2'->(t2,2', None)", "(tReturn ER, 'Return ER')->p2",
                               "(t1, None)->p1'", "(t2,2', None)->p2,2'",
                               "p2->(t2,2', None)", "p1->(tReturn ER, 'Return ER')",
                               "p1,1'->(t1, None)", "p1'->(tReturn ER', 'Return ER')",
                               '(t1, None)->p1', "(tReturn ER', 'Return ER')->p2'"],
                              list(map(str, pm4py_net.arcs)))

    def test_convert_eventlog_to_pm4py(self):
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
        log = EventLog.create_from_pandas_df(
                df, 'CaseId', 'Activity', trace_attribute_columns=['Location'])

        pm4py_log = convert_eventlog_to_pm4py(log)
        self.assertTrue(pm4py_log is not None)
        self.assertEqual(2, len(pm4py_log))

    def test_convert_pm4py_log(self):
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
        log = EventLog.create_from_pandas_df(
                df, 'CaseId', 'Activity', trace_attribute_columns=['Location'])

        pm4py_log = convert_eventlog_to_pm4py(log)
        converted_log = convert_pm4py_log(pm4py_log)

        self.assertTrue(converted_log is not None)
        self.assertEqual(2, converted_log.get_nr_of_traces())
        self.assertEqual('Germany', converted_log.traces[0].attributes['Location'])

if __name__ == '__main__':
    unittest.main()