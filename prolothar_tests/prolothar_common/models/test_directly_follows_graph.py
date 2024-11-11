# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.directly_follows_graph import DirectlyFollowsGraph
from prolothar_common.models.eventlog import EventLog

class TestDirectlyFollowsGraph(unittest.TestCase):

    def setUp(self):
        self.dfg = DirectlyFollowsGraph()

    def test_get_nr_nodes_and_edges(self):
        self.assertEqual(0, self.dfg.get_nr_of_edges())
        self.assertEqual(0, self.dfg.get_nr_of_nodes())

        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'C')
        self.assertEqual(3, self.dfg.get_nr_of_nodes())
        self.assertEqual(2, self.dfg.get_nr_of_edges())

    def test_filter_edges_by_local_frequency(self):
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'C')
        self.dfg.add_count('A', 'C')

        self.assertEqual(self.dfg, self.dfg.filter_edges_by_local_frequency(0.3))

        ab_dfg = DirectlyFollowsGraph()
        ab_dfg.add_count('A', 'B')
        ab_dfg.add_count('A', 'B')
        ab_dfg.add_count('A', 'B')
        ab_dfg.add_count('A', 'B')
        ab_dfg.add_node('C')
        self.assertEqual(ab_dfg, self.dfg.filter_edges_by_local_frequency(0.5))
        self.assertEqual(1, len(ab_dfg.nodes['A'].edges))

        empty_dfg = DirectlyFollowsGraph()
        empty_dfg.add_node('A')
        empty_dfg.add_node('B')
        empty_dfg.add_node('C')
        self.assertEqual(empty_dfg, self.dfg.filter_edges_by_local_frequency(0.8))

    def test_filter_edges_by_local_frequency_keep_at_least_one_outgoing_edge(self):
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'C')
        self.dfg.add_count('A', 'C')

        self.assertEqual(self.dfg, self.dfg.filter_edges_by_local_frequency(0.3))

        ab_dfg = DirectlyFollowsGraph()
        ab_dfg.add_count('A', 'B')
        ab_dfg.add_count('A', 'B')
        ab_dfg.add_count('A', 'B')
        ab_dfg.add_count('A', 'B')
        ab_dfg.add_node('C')
        self.assertEqual(ab_dfg, self.dfg.filter_edges_by_local_frequency(
            0.9, keep_at_least_one_outgoing_edge=True))
        self.assertEqual(1, len(ab_dfg.nodes['A'].edges))

    def test_filter_edges_by_absolute_count(self):
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'C')
        self.dfg.add_count('A', 'C')

        self.assertEqual(self.dfg, self.dfg.filter_edges_by_absolute_count(1))

        ab_dfg = DirectlyFollowsGraph()
        ab_dfg.add_count('A', 'B')
        ab_dfg.add_count('A', 'B')
        ab_dfg.add_count('A', 'B')
        ab_dfg.add_count('A', 'B')
        ab_dfg.add_node('C')
        self.assertEqual(ab_dfg, self.dfg.filter_edges_by_absolute_count(3))

        empty_dfg = DirectlyFollowsGraph()
        empty_dfg.add_node('A')
        empty_dfg.add_node('B')
        empty_dfg.add_node('C')
        self.assertEqual(empty_dfg, self.dfg.filter_edges_by_absolute_count(5))

    def test_get_shortest_path(self):
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'C')
        self.dfg.add_count('B', 'D')
        self.dfg.add_count('D', 'E')
        self.dfg.add_count('E', 'F')
        self.dfg.add_count('C', 'F')

        self.assertEqual(['A', 'C', 'F'],
                         self.dfg.compute_shortest_path('A', 'F'))
        self.assertEqual(['A', 'C'],
                         self.dfg.compute_shortest_path('A', 'C'))
        self.assertEqual(['A', 'B', 'D', 'E'],
                         self.dfg.compute_shortest_path('A', 'E'))
        self.assertEqual([],
                         self.dfg.compute_shortest_path('A', 'A'))
        self.assertEqual([],
                         self.dfg.compute_shortest_path('F', 'A'))

    def test_get_shortest_path_with_forbidden_edges(self):
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'C')
        self.dfg.add_count('B', 'D')
        self.dfg.add_count('D', 'E')
        self.dfg.add_count('E', 'F')
        self.dfg.add_count('C', 'F')

        self.assertEqual(
            ['A', 'B', 'D', 'E', 'F'],
            self.dfg.compute_shortest_path(
                'A', 'F', forbidden_edges=[('A', 'C')]))
        self.assertEqual(
            ['A', 'B', 'D', 'E', 'F'],
            self.dfg.compute_shortest_path(
                'A', 'F', forbidden_edges=[('C', 'F')]))
        self.assertEqual(
            [],
            self.dfg.compute_shortest_path(
                'A', 'D', forbidden_edges=[('A', 'B')]))
        self.assertEqual(
            [],
            self.dfg.compute_shortest_path(
                'A', 'D', forbidden_edges=[('B', 'D')]))

    def test_get_shortest_path_to_one_of(self):
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'C')
        self.dfg.add_count('B', 'D')
        self.dfg.add_count('D', 'E')
        self.dfg.add_count('E', 'F')
        self.dfg.add_count('C', 'F')

        self.assertEqual(
            ['A', 'C', 'F'],
            self.dfg.compute_shortest_path_to_one_of('A', set(['E', 'F'])))
        self.assertEqual(
            [],
            self.dfg.compute_shortest_path_to_one_of('B', set(['A'])))

    def test_select_nodes(self):
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'C')
        self.dfg.add_count('B', 'D')
        self.dfg.add_count('D', 'E')
        self.dfg.add_count('E', 'F')
        self.dfg.add_count('C', 'F')

        expected_dfg = DirectlyFollowsGraph()
        expected_dfg.add_count('A', 'B')
        expected_dfg.add_count('A', 'C')
        expected_dfg.add_node('E')

        self.assertEqual(expected_dfg, self.dfg.select_nodes(['A','B','C','E']))

    def test_create_from_eventlog(self):
        log = EventLog.create_from_simple_activity_log([
            ['0','1','2','4','5','4','5','1','2','6'],
            ['0','1','2','4','5','4','5','1','2','6'],
            ['0','1','2','4','5','4','5','4','5','1','2','6'],
            ['0','1','2','4','5','4','5','1','2','6'],
            ['0','1','2','4','5','1','2','6'],
            ['0','7','8','6']
        ])
        actual_dfg = DirectlyFollowsGraph.create_from_event_log(log)

        expected_dfg = DirectlyFollowsGraph()
        expected_dfg.add_count('0', '1', count=5)
        expected_dfg.add_count('0', '7', count=1)
        expected_dfg.add_count('1', '2', count=10)
        expected_dfg.add_count('2', '4', count=5)
        expected_dfg.add_count('2', '6', count=5)
        expected_dfg.add_count('4', '5', count=10)
        expected_dfg.add_count('5', '4', count=5)
        expected_dfg.add_count('5', '1', count=5)
        expected_dfg.add_count('7', '8', count=1)
        expected_dfg.add_count('8', '6', count=1)

        self.assertEqual(expected_dfg, actual_dfg)

    def test_get_largest_weakly_connected_component(self):
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'C')
        self.dfg.add_count('B', 'D')
        self.dfg.add_count('D', 'E')
        self.dfg.add_count('E', 'F')
        self.dfg.add_count('C', 'F')

        expected_largest_component = self.dfg.copy()

        self.dfg.add_count('G', 'H')

        self.assertEqual(expected_largest_component,
                         self.dfg.get_largest_weakly_connected_component())

    def test_get_count(self):
        self.dfg = DirectlyFollowsGraph()
        self.dfg.add_count('0', '0', count=3)
        self.dfg.add_count('0', '1', count=5)
        self.dfg.add_count('0', '7', count=1)
        self.dfg.add_count('1', '2', count=10)
        self.dfg.add_count('2', '4', count=5)
        self.dfg.add_count('2', '6', count=5)
        self.dfg.add_count('4', '5', count=10)
        self.dfg.add_count('5', '4', count=5)
        self.dfg.add_count('5', '1', count=5)
        self.dfg.add_count('7', '8', count=1)
        self.dfg.add_count('8', '6', count=1)

        self.assertEqual(3, self.dfg.get_count('0', '0'))
        self.assertEqual(10, self.dfg.get_count('4', '5'))
        self.assertEqual(5, self.dfg.get_count('5', '4'))
        self.assertEqual(0, self.dfg.get_count('5', '3'))
        self.assertEqual(0, self.dfg.get_count('9', '3'))

    def test_degree(self):
        log = EventLog.create_from_simple_activity_log([
            ['0','1','2','4','5','4','5','1','2','6'],
            ['0','1','2','4','5','4','5','1','2','6'],
            ['0','1','2','4','5','4','5','4','5','1','2','6'],
            ['0','1','2','4','5','4','5','1','2','6'],
            ['0','1','2','4','5','1','2','6'],
            ['0','7','8','6']
        ])
        dfg = DirectlyFollowsGraph.create_from_event_log(log)

        self.assertEqual(0, dfg.compute_indegree('0'))
        self.assertEqual(2, dfg.compute_indegree('1'))
        self.assertEqual(2, dfg.compute_indegree('4'))
        self.assertEqual(1, dfg.compute_indegree('7'))

        dfg.remove_node('0')
        self.assertEqual(1, dfg.compute_indegree('2'))
        self.assertEqual(2, dfg.compute_indegree('4'))

        dfg.remove_edge(('1', '2'))
        self.assertEqual(0, dfg.compute_indegree('2'))
        self.assertEqual(2, dfg.compute_indegree('4'))

    def test_get_source_sink_activities(self):
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'C')
        self.dfg.add_count('B', 'D')
        self.dfg.add_count('D', 'E')
        self.dfg.add_count('E', 'F')
        self.dfg.add_count('C', 'F')
        self.assertListEqual(['A'], self.dfg.get_source_activities())
        self.assertListEqual(['F'], self.dfg.get_sink_activities())

    def test_remove_not_allowed_start_end_activities(self):
        self.dfg.add_count('0', '1', count=5)
        self.dfg.add_count('0', '7', count=1)
        self.dfg.add_count('1', '2', count=10)
        self.dfg.add_count('2', '4', count=5)
        self.dfg.add_count('2', '6', count=5)
        self.dfg.add_count('4', '5', count=10)
        self.dfg.add_count('7', '8', count=1)
        self.dfg.add_count('8', '6', count=1)
        self.dfg.add_count('9', '1', count=1)

        self.dfg.remove_not_allowed_start_activities(set(['0']))
        self.dfg.remove_not_allowed_end_activities(set(['6']))

        expected_dfg = DirectlyFollowsGraph()
        expected_dfg.add_count('0', '1', count=5)
        expected_dfg.add_count('0', '7', count=1)
        expected_dfg.add_count('1', '2', count=10)
        expected_dfg.add_count('2', '6', count=5)
        expected_dfg.add_count('7', '8', count=1)
        expected_dfg.add_count('8', '6', count=1)

        self.assertEqual(expected_dfg, self.dfg)

    def test_remove_node_create_connections_false(self):
        dfg = DirectlyFollowsGraph()
        dfg.add_count('0', '1', count=5)
        dfg.add_count('0', '7', count=1)
        dfg.add_count('1', '2', count=10)
        dfg.add_count('2', '6', count=5)
        dfg.add_count('7', '8', count=1)
        dfg.add_count('8', '6', count=1)

        dfg.remove_node('2')

        expected_dfg = DirectlyFollowsGraph()
        expected_dfg.add_count('0', '1', count=5)
        expected_dfg.add_count('0', '7', count=1)
        expected_dfg.add_count('7', '8', count=1)
        expected_dfg.add_count('8', '6', count=1)

        self.assertEqual(dfg, expected_dfg)

    def test_remove_node_create_connections_true(self):
        dfg = DirectlyFollowsGraph()
        dfg.add_count('0', '1', count=5)
        dfg.add_count('0', '7', count=1)
        dfg.add_count('1', '2', count=10)
        dfg.add_count('2', '6', count=5)
        dfg.add_count('7', '8', count=1)
        dfg.add_count('8', '6', count=1)

        dfg.remove_node('2', create_connections=True)

        expected_dfg = DirectlyFollowsGraph()
        expected_dfg.add_count('0', '1', count=5)
        expected_dfg.add_count('0', '7', count=1)
        expected_dfg.add_count('1', '6', count=1)
        expected_dfg.add_count('7', '8', count=1)
        expected_dfg.add_count('8', '6', count=1)

        self.assertEqual(dfg, expected_dfg)

    def test_generate_log(self):
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'C')
        self.dfg.add_count('B', 'D')
        self.dfg.add_count('D', 'E')
        self.dfg.add_count('E', 'F')
        self.dfg.add_count('C', 'F')

        generated_log = self.dfg.generate_log(10, random_seed=42)
        self.assertEqual(10, generated_log.get_nr_of_traces())
        self.assertSetEqual(set(['A']),
                            generated_log.compute_set_of_start_activities())
        self.assertSetEqual(set(['F']),
                            generated_log.compute_set_of_end_activities())

    def test_get_reachable_activities(self):
        self.dfg.add_count('A', 'B')
        self.dfg.add_count('A', 'C')
        self.dfg.add_count('B', 'D')
        self.dfg.add_count('D', 'E')
        self.dfg.add_count('E', 'F')
        self.dfg.add_count('C', 'F')

        self.assertSetEqual({'B','C','D','E','F'},
                            self.dfg.get_reachable_activities('A'))

        self.assertSetEqual(set(), self.dfg.get_reachable_activities('F'))

        self.assertSetEqual({'F'}, self.dfg.get_reachable_activities('E'))

    def test_plot_with_random_walks(self):
        self.dfg.add_count('0', '0', count=3)
        self.dfg.add_count('0', '1', count=5)
        self.dfg.add_count('0', '7', count=1)
        self.dfg.add_count('1', '2', count=10)
        self.dfg.add_count('2', '4', count=5)
        self.dfg.add_count('2', '6', count=5)
        self.dfg.add_count('4', '5', count=10)
        self.dfg.add_count('5', '4', count=5)
        self.dfg.add_count('5', '1', count=5)
        self.dfg.add_count('7', '8', count=1)
        self.dfg.add_count('8', '6', count=1)

        dot = self.dfg.plot(random_walk_alignment=('0','6',1000), view=False).strip()

        with open('prolothar_tests/resources/dfg_plot_with_random_walk_subgraphs.txt', 'r') as f:
            expected_dot = f.read()

        dot = dot.replace(' ', '').replace('\t', '')
        expected_dot = expected_dot.replace(' ', '').replace('\t', '')
        self.assertEqual(dot, expected_dot)

    def test_plot_with_topological_order(self):
        self.dfg.add_count('0', '0', count=3)
        self.dfg.add_count('0', '1', count=5)
        self.dfg.add_count('0', '7', count=1)
        self.dfg.add_count('1', '2', count=10)
        self.dfg.add_count('2', '4', count=5)
        self.dfg.add_count('2', '6', count=5)
        self.dfg.add_count('4', '5', count=10)
        self.dfg.add_count('5', '4', count=5)
        self.dfg.add_count('5', '1', count=5)
        self.dfg.add_count('7', '8', count=1)
        self.dfg.add_count('8', '6', count=1)

        dot = self.dfg.plot(use_topological_order=True, view=False).strip()

        with open('prolothar_tests/resources/dfg_plot_with_topological_order.txt', 'r') as f:
            expected_dot = f.read()

        dot = dot.replace(' ', '').replace('\t', '')
        expected_dot = expected_dot.replace(' ', '').replace('\t', '')
        self.assertEqual(dot, expected_dot)

if __name__ == '__main__':
    unittest.main()