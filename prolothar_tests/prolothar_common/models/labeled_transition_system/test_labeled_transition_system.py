# -*- coding: utf-8 -*-

import unittest
from prolothar_common.models.eventlog import EventLog
from prolothar_common.models.labeled_transition_system import LabeledTransitionSystem
from prolothar_common.models.labeled_transition_system.state_representation import last_abstraction
from prolothar_common.models.labeled_transition_system.state_representation import set_abstraction
from prolothar_common.models.labeled_transition_system.state_representation import list_abstraction
from prolothar_common.models.labeled_transition_system.state_representation import last_n_abstraction

class TestPrefixTree(unittest.TestCase):

    def test_create_with_last_abstraction(self):
        eventlog = EventLog.create_from_simple_activity_log([
            ["A", "B", "C", "F"],
            ["A", "B", "D", "F"],
            ["A", "B", "E", "F"],
        ])

        transition_system = LabeledTransitionSystem(
            state_representation_function=last_abstraction)
        for trace in eventlog:
            transition_system.add_trace(trace)

        self.assertEqual(7, transition_system.get_nr_of_states())
        self.assertEqual(
            {
                (None, 'A', 'A'), ('B', 'C', 'C'), ('E', 'F', 'F'), ('C', 'F', 'F'),
                ('B', 'E', 'E'), ('A', 'B', 'B'), ('D', 'F', 'F'), ('B', 'D', 'D')
            },
            set(transition_system.transition_iterator())
        )
        self.assertEqual(8, transition_system.get_nr_of_transitions())

        transition_system.plot()
        transition_system.plot(use_state_representation_for_labels=True)

    def test_create_with_set_abstraction(self):
        eventlog = EventLog.create_from_simple_activity_log([
            ["A", "B", "C", "F"],
            ["A", "B", "D", "F"],
            ["A", "B", "E", "F"],
        ])

        transition_system = LabeledTransitionSystem(
            state_representation_function=set_abstraction)
        for trace in eventlog:
            transition_system.add_trace(trace)

        self.assertEqual(9, transition_system.get_nr_of_states())
        self.assertEqual(
            {
                (frozenset([]), 'A', frozenset(['A'])),
                (frozenset(['A']), 'B', frozenset(['A', 'B'])),
                (frozenset(['A', 'B']), 'C', frozenset(['A', 'B', 'C'])),
                (frozenset(['A', 'B']), 'D', frozenset(['A', 'B', 'D'])),
                (frozenset(['A', 'B']), 'E', frozenset(['A', 'B', 'E'])),
                (frozenset(['A', 'B', 'C']), 'F', frozenset(['A', 'B', 'C', 'F'])),
                (frozenset(['A', 'B', 'D']), 'F', frozenset(['A', 'B', 'D', 'F'])),
                (frozenset(['A', 'B', 'E']), 'F', frozenset(['A', 'B', 'E', 'F'])),
            },
            set(transition_system.transition_iterator())
        )
        self.assertEqual(8, transition_system.get_nr_of_transitions())

        transition_system.plot()
        transition_system.plot(use_state_representation_for_labels=True)

    def test_create_with_list_abstraction(self):
        eventlog = EventLog.create_from_simple_activity_log([
            ["A", "B", "C", "F"],
            ["A", "B", "D", "F"],
            ["A", "B", "E", "F"],
        ])

        transition_system = LabeledTransitionSystem(
            state_representation_function=list_abstraction)
        for trace in eventlog:
            transition_system.add_trace(trace)

        self.assertEqual(9, transition_system.get_nr_of_states())
        self.assertEqual(
            {
                (tuple([]), 'A', tuple(['A'])),
                (tuple(['A']), 'B', tuple(['A', 'B'])),
                (tuple(['A', 'B']), 'C', tuple(['A', 'B', 'C'])),
                (tuple(['A', 'B']), 'D', tuple(['A', 'B', 'D'])),
                (tuple(['A', 'B']), 'E', tuple(['A', 'B', 'E'])),
                (tuple(['A', 'B', 'C']), 'F', tuple(['A', 'B', 'C', 'F'])),
                (tuple(['A', 'B', 'D']), 'F', tuple(['A', 'B', 'D', 'F'])),
                (tuple(['A', 'B', 'E']), 'F', tuple(['A', 'B', 'E', 'F'])),
            },
            set(transition_system.transition_iterator())
        )
        self.assertEqual(8, transition_system.get_nr_of_transitions())
        self.assertCountEqual([tuple([])], transition_system.get_start_states())
        self.assertCountEqual([
            tuple(['A', 'B', 'C', 'F']),
            tuple(['A', 'B', 'D', 'F']),
            tuple(['A', 'B', 'E', 'F']),
        ], transition_system.get_end_states())
        self.assertCountEqual(
            [(tuple([]), 'A', tuple(['A']))],
            transition_system.yield_outgoing_transitions(tuple([]))
        )
        self.assertEqual(
            ('A', 'B', 'C'),
            transition_system.get_next_state(('A', 'B'), 'C')
        )

        transition_system.plot()
        transition_system.plot(use_state_representation_for_labels=True)

    def test_create_with_last_n_abstraction(self):
        eventlog = EventLog.create_from_simple_activity_log([
            ["A", "B", "C", "F"],
            ["A", "B", "D", "F"],
            ["A", "B", "E", "F"],
        ])

        transition_system = LabeledTransitionSystem(
            state_representation_function=last_n_abstraction(1))
        for trace in eventlog:
            transition_system.add_trace(trace)
        self.assertEqual(7, transition_system.get_nr_of_states())
        self.assertEqual(
            {
                (tuple(), 'A', ('A',)), (('B',), 'C', ('C',)), (('E',), 'F', ('F',)), (('C',), 'F', ('F',)),
                (('B',), 'E', ('E',)), (('A',), 'B', ('B',)), (('D',), 'F', ('F',)), (('B',), 'D', ('D',))
            },
            set(transition_system.transition_iterator())
        )
        self.assertEqual(8, transition_system.get_nr_of_transitions())

        transition_system = LabeledTransitionSystem(
            state_representation_function=last_n_abstraction(2))
        for trace in eventlog:
            transition_system.add_trace(trace)
        self.assertEqual(9, transition_system.get_nr_of_states())
        self.assertEqual(
            {
                (tuple(), 'A', ('A',)), (('A', 'B'), 'C', ('B', 'C')),
                (('B', 'E'), 'F', ('E', 'F')), (('B', 'C'), 'F', ('C', 'F')),
                (('A', 'B'), 'E', ('B', 'E')), (('A',), 'B', ('A','B')),
                (('B', 'D'), 'F', ('D', 'F')), (('A', 'B'), 'D', ('B', 'D'))
            },
            set(transition_system.transition_iterator())
        )
        self.assertEqual(8, transition_system.get_nr_of_transitions())


if __name__ == '__main__':
    unittest.main()
