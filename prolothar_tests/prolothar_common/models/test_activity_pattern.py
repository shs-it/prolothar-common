# -*- coding: utf-8 -*-

import unittest
from prolothar_common.models.activity_pattern import ActivityPattern
from prolothar_common.models.activity_pattern import sequence, choice, parallel
from prolothar_common.models.activity_pattern import interleaving, unbounded_repetition
from prolothar_common.models.activity_pattern import choice_list
from prolothar_common.models.data_petri_net import DataPetriNet, Transition, Place
from prolothar_common.models.data_petri_net import SmallerOrEqualGuard, FalseGuard, GreaterOrEqualGuard
from prolothar_common.models.data_petri_net import IntVariable, BoolVariable

class TestActivityPattern(unittest.TestCase):

    def test_create_valid_activity_pattern(self):
        self._create_activity_pattern_A()
        self._create_activity_pattern_B()

    def test_create_activity_pattern_with_insufficient_name_mapping(self):
        try:
            ActivityPattern(self._create_petri_net_A(),
                            {Transition('start computer'): 'lazy day'})
            self.fail(msg='insufficient name mapping should raise ValueError')
        except ValueError:
            pass

    def test_sequence(self):
        sequence_pattern = sequence(self._create_activity_pattern_A(),
                                    self._create_activity_pattern_B())
        self.assertTrue(sequence_pattern.data_petri_net.is_workflow_net())

    def test_choice(self):
        choice_pattern = choice(self._create_activity_pattern_A(),
                                self._create_activity_pattern_B())
        self.assertTrue(choice_pattern.data_petri_net.is_workflow_net())

    def test_choice_list(self):
        choice_pattern = choice_list([self._create_activity_pattern_A(),
                                      self._create_activity_pattern_B(),
                                      self._create_activity_pattern_C()])
        self.assertTrue(choice_pattern.data_petri_net.is_workflow_net())

    def test_parallel(self):
        parallel_pattern = parallel(self._create_activity_pattern_A(),
                                    self._create_activity_pattern_B())
        self.assertTrue(parallel_pattern.data_petri_net.is_workflow_net())
        self.assertEqual(8, len(parallel_pattern.data_petri_net.transitions))
        self.assertEqual(10, len(parallel_pattern.data_petri_net.places))

    def test_interleaving(self):
        interleaving_pattern = interleaving(self._create_activity_pattern_A(),
                                            self._create_activity_pattern_B())
        self.assertTrue(interleaving_pattern.data_petri_net.is_workflow_net())

    def test_unbounded_repetition(self):
        repetition_pattern = unbounded_repetition(self._create_activity_pattern_A())
        self.assertTrue(repetition_pattern.data_petri_net.is_workflow_net())

    def _create_activity_pattern_A(self) -> ActivityPattern:
        return ActivityPattern(self._create_petri_net_A(),
                               'lazy day')

    def _create_activity_pattern_B(self) -> ActivityPattern:
        return ActivityPattern(self._create_petri_net_B(),
                               'diligent day')

    def _create_activity_pattern_C(self) -> ActivityPattern:
        return ActivityPattern(self._create_petri_net_C(),
                               'holiday')

    def _create_petri_net_A(self) -> DataPetriNet:
        net = DataPetriNet()

        start_place = net.add_place(
                Place.with_id_label('start', nr_of_tokens=1))
        mid_place_1 = net.add_place(Place.with_empty_label('mid_1'))
        mid_place_2 = net.add_place(Place.with_empty_label('mid_2'))
        end_place = net.add_place(Place.with_id_label('end'))

        start_computer = net.add_transition(Transition('start computer'))
        drink_coffee = net.add_transition(Transition('drink coffee'))
        shutdown_computer = net.add_transition(Transition('shutdown computer'))

        time = net.add_variable(IntVariable('time', lower_bound=0, upper_bound=24))

        start_computer.set_guard_function(
            SmallerOrEqualGuard(time, 9))
        shutdown_computer.set_guard_function(
            GreaterOrEqualGuard(time, 16))

        net.add_connection(start_place, start_computer, mid_place_1)
        net.add_connection(mid_place_1, drink_coffee, mid_place_2)
        net.add_connection(mid_place_2, shutdown_computer, end_place)

        return net

    def _create_petri_net_B(self) -> DataPetriNet:
        net = DataPetriNet()

        start_place = net.add_place(
                Place.with_id_label('start', nr_of_tokens=1))
        mid_place_1 = net.add_place(Place.with_empty_label('mid_1'))
        mid_place_2 = net.add_place(Place.with_empty_label('mid_2'))
        end_place = net.add_place(Place.with_id_label('end'))

        start_computer = net.add_transition(Transition('start computer'))
        program = net.add_transition(Transition('program'))
        shutdown_computer = net.add_transition(Transition('shutdown computer'))

        time = net.add_variable(IntVariable('time', lower_bound=0, upper_bound=24))
        tired = net.add_variable(BoolVariable('tired'))

        start_computer.set_guard_function(
            SmallerOrEqualGuard(time, 9))
        program.set_guard_function(FalseGuard(tired))
        shutdown_computer.set_guard_function(
            GreaterOrEqualGuard(time, 16))

        net.add_connection(start_place, start_computer, mid_place_1)
        net.add_connection(mid_place_1, program, mid_place_2)
        net.add_connection(mid_place_2, shutdown_computer, end_place)

        return net

    def _create_petri_net_C(self) -> DataPetriNet:
        net = DataPetriNet()

        start_place = net.add_place(
                Place.with_id_label('start', nr_of_tokens=1))
        end_place = net.add_place(Place.with_id_label('end'))

        holiday = net.add_transition(Transition('holiday'))

        net.add_connection(start_place, holiday, end_place)

        return net

if __name__ == '__main__':
    unittest.main()