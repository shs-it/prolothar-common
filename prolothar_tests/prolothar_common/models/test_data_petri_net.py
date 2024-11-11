# -*- coding: utf-8 -*-

import unittest
from prolothar_common.models.data_petri_net import DataPetriNet
from prolothar_common.models.data_petri_net import Place
from prolothar_common.models.data_petri_net import Transition
from prolothar_common.models.data_petri_net import IntVariable, FloatVariable
from prolothar_common.models.data_petri_net import Guard, LambdaGuard

class TestDataPetriNet(unittest.TestCase):

    def setUp(self):
        self.net = DataPetriNet()

    def test_data_petri_net(self):
        start_place = self.net.add_place(
                Place.with_id_label('start', nr_of_tokens=1))
        mid_place = self.net.add_place(Place.with_empty_label('mid'))
        end_place = self.net.add_place(Place.with_id_label('end'))

        t1 = self.net.add_transition(Transition('t1'))
        t2 = self.net.add_transition(Transition('t2'))

        start_time = self.net.add_variable(IntVariable('start_time', value=0))
        budget = self.net.add_variable(FloatVariable('budget', value=1))

        t1.set_guard_function(Guard.all_of([
            LambdaGuard(start_time, lambda v: v < 10),
            LambdaGuard(budget, lambda v: v > 0)
        ]))

        self.net.add_connection(start_place, t1, mid_place)
        self.net.add_connection(mid_place, t2, end_place)

        print('Initial State:')
        self.net.print_state()
        self.assertEqual(1, start_place.nr_of_tokens)
        self.assertEqual(0, mid_place.nr_of_tokens)
        self.assertEqual(0, end_place.nr_of_tokens)
        self.assertCountEqual([t1], self.net.get_fireable_transitions())
        print('====================================')

        self.net.simulate_one_timestep()
        print('State after step 1:')
        self.net.print_state()
        self.assertEqual(0, start_place.nr_of_tokens)
        self.assertEqual(1, mid_place.nr_of_tokens)
        self.assertEqual(0, end_place.nr_of_tokens)
        self.assertCountEqual([t2], self.net.get_fireable_transitions())
        print('====================================')

        self.net.simulate_one_timestep()
        print('State after step 2:')
        self.net.print_state()
        self.assertEqual(0, start_place.nr_of_tokens)
        self.assertEqual(0, mid_place.nr_of_tokens)
        self.assertEqual(1, end_place.nr_of_tokens)

        marking = {'start': 1, 'mid': 0, 'end': 0 }
        self.assertFalse(self.net.matches_marking(marking))
        self.net.set_marking(marking)
        self.assertTrue(self.net.matches_marking(marking))

    def test_data_petri_net_value_errors(self):
        try:
            self.net.add_place(Place.with_id_label('start'))
            self.net.add_place(Place.with_id_label('start'))
            self.fail('place ids must be unique')
        except ValueError:
            pass

    def test_add_transition_twice(self):
        try:
            self.net.add_transition(Transition('t1'))
            self.net.add_transition(Transition('t1'))
            self.fail('transition ids must be unique')
        except ValueError:
            pass

    def test_add_variable_twice(self):
        try:
            self.net.add_variable(IntVariable('v1'))
            self.net.add_variable(IntVariable('v1'))
            self.fail('transition ids must be unique')
        except ValueError:
            pass

    def test_add_connection_non_existing_place_or_transition(self):
        start_place = self.net.add_place(Place.with_id_label('start'))
        end_place = self.net.add_place(Place.with_id_label('end'))
        transition = self.net.add_transition(Transition('t1'))

        try:
            self.net.add_connection(Place.with_id_label('p1'),
                                    transition, end_place)
            self.fail('place1 does not exist in net')
        except ValueError:
            pass

        try:
            self.net.add_connection(start_place, Transition('t2'), end_place)
            self.fail('transition does not exist in net')
        except ValueError:
            pass

        try:
            self.net.add_connection(start_place, Transition('t2'),
                                    Place.with_id_label('p2'))
            self.fail('place2 does not exist in net')
        except ValueError:
            pass

    def test_is_worflow_net(self):
        self.assertFalse(DataPetriNet().is_workflow_net())
        self.assertTrue(create_workflow_net().is_workflow_net())
        self.assertFalse(create_two_sources_net().is_workflow_net())
        self.assertFalse(create_two_sinks_net().is_workflow_net())

    def test_transform_to_workflow_net(self):
        two_sources_net = create_two_sources_net()
        two_sources_net_transformed = two_sources_net.transform_to_workflow_net()
        self.assertFalse(two_sources_net.is_workflow_net())
        self.assertTrue(two_sources_net_transformed.is_workflow_net())

        two_sinks_net = create_two_sinks_net()
        two_sinks_net_transformed = two_sinks_net.transform_to_workflow_net()
        self.assertFalse(two_sinks_net.is_workflow_net())
        self.assertTrue(two_sinks_net_transformed.is_workflow_net())

    def test_plot(self):
        expected_dot = ('digraph {\n'
            '\tplace_start [label="" shape=circle xlabel=start]\n'
            '\tplace_end [label="" shape=circle xlabel=end]\n'
            '\ttransition_t1 [label=t1 shape=rectangle]\n'
            '\tplace_start -> transition_t1\n'
            '\ttransition_t1 -> place_end\n'
            '}')
        self.assertEqual(expected_dot,
                         create_workflow_net().plot(view=False).strip())

    def test_prune_one_transition(self):
        net = DataPetriNet()
        start_place = net.add_place(
                Place.with_id_label('start', nr_of_tokens=1))
        mid_place = net.add_place(Place.with_empty_label('mid'))
        end_place = net.add_place(Place.with_id_label('end'))

        t1 = net.add_transition(Transition('t1'))
        t2 = net.add_transition(Transition('t2', visible=False))
        net.add_connection(start_place, t1, mid_place)
        net.add_connection(mid_place, t2, end_place)
        net.prune()
        self.assertEqual(1, len(net.transitions))
        self.assertEqual(2, len(net.places))

    def test_prune_two_transition(self):
        net = DataPetriNet()
        start_place = net.add_place(
                Place.with_id_label('start', nr_of_tokens=1))
        mid_place_1 = net.add_place(Place.with_empty_label('mid1'))
        mid_place_2 = net.add_place(Place.with_empty_label('mid2'))
        end_place = net.add_place(Place.with_id_label('end'))
        t1 = net.add_transition(Transition('t1'))
        t2 = net.add_transition(Transition('t2', visible=False))
        t3 = net.add_transition(Transition('t3', visible=False))
        net.add_connection(start_place, t1, mid_place_1)
        net.add_connection(mid_place_1, t2, mid_place_2)
        net.add_connection(mid_place_2, t3, end_place)
        net.prune()
        self.assertEqual(1, len(net.transitions))
        self.assertEqual(2, len(net.places))

    def test_prune_with_selfloop(self):
        net = DataPetriNet()
        start_place = net.add_place(
                Place.with_id_label('start', nr_of_tokens=1))
        mid_place_1 = net.add_place(Place.with_empty_label('mid1'))
        end_place = net.add_place(Place.with_id_label('end'))
        t1 = net.add_transition(Transition('t1'))
        t2 = net.add_transition(Transition('t2', visible=False))
        net.add_connection(start_place, t1, mid_place_1)
        net.add_connection(mid_place_1, t1, mid_place_1)
        net.add_connection(mid_place_1, t2, end_place)
        net.prune()
        self.assertEqual(2, len(net.transitions))
        self.assertEqual(3, len(net.places))

    def test_prune_with_selfloop_and_loop(self):
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
        self.assertEqual(2, len(net.transitions))
        self.assertEqual(2, len(net.places))

    def test_prune_with_loop(self):
        net = DataPetriNet()
        places = {i+1: net.add_place(Place.with_id_label(str(i+1))) \
                  for i in range(5)}
        t1 = net.add_transition(Transition('t1'))
        t2 = net.add_transition(Transition('t2', visible=False))
        t3 = net.add_transition(Transition('t3', visible=False))
        t4 = net.add_transition(Transition('t4'))
        net.add_connection(places[1], t1, places[2])
        net.add_connection(places[2], t2, places[3])
        net.add_connection(places[3], t3, places[4])
        net.add_connection(places[4], t1, places[2])
        net.add_connection(places[4], t4, places[5])
        net.prune()
        self.assertEqual(2, len(net.transitions))
        self.assertEqual(3, len(net.places))

    def test_force_and_transition_and_marking_parallel_places(self):
        start_place = self.net.add_place(
                Place.with_id_label('start', nr_of_tokens=1))
        mid_place1 = self.net.add_place(Place.with_empty_label('mid1'))
        mid_place2 = self.net.add_place(Place.with_empty_label('mid2'))
        end_place = self.net.add_place(Place.with_id_label('end'))

        t1 = self.net.add_transition(Transition('t1'))
        t2 = self.net.add_transition(Transition('t2'))

        self.net.add_connection(start_place, t1, mid_place1)
        self.net.add_connection(start_place, t1, mid_place2)
        self.net.add_connection(mid_place1, t2, end_place)
        self.net.add_connection(mid_place2, t2, end_place)

        self.net.force_transition('t1')
        self.assertDictEqual({'start': 0, 'mid1': 1, 'mid2': 1, 'end': 0},
                             self.net.get_marking())

        self.net.force_transition('t2')
        self.assertDictEqual({'start': 0, 'mid1': 0, 'mid2': 0, 'end': 1},
                             self.net.get_marking())

        try:
            self.net.force_transition('t1')
            self.fail('transition is not firable')
        except ValueError:
            pass

def create_workflow_net():
    net = DataPetriNet()
    start_place = net.add_place(Place.with_id_label('start'))
    end_place = net.add_place(Place.with_id_label('end'))
    t1 = net.add_transition(Transition('t1'))
    net.add_connection(start_place, t1, end_place)
    return net

def create_two_sources_net():
    net = create_workflow_net()
    start_place_2 = net.add_place(Place.with_id_label('start 2'))
    net.add_connection(start_place_2, net.transitions['t1'], net.places['end'])
    return net

def create_two_sinks_net():
    net = create_workflow_net()
    end_place_2 = net.add_place(Place.with_id_label('end 2'))
    net.add_connection(net.places['start'], net.transitions['t1'], end_place_2)
    return net

if __name__ == '__main__':
    unittest.main()