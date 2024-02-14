# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.nested_graph import NestedGraph


class TestNestedGraph(unittest.TestCase):

    def setUp(self):
        self.nested_graph = NestedGraph()
        self.nested_graph.add_node(NestedGraph.Node(
            '0', '[A,B,C]', attributes={'pattern_type': 'Sequence'}))
        self.nested_graph.add_node(NestedGraph.Node(
            '0.0', 'A', parent='0', attributes={'pattern_type': 'Singleton'}))
        self.nested_graph.add_node(NestedGraph.Node(
            '0.1', 'B', parent='0', attributes={'pattern_type': 'Singleton'}))
        self.nested_graph.add_node(NestedGraph.Node(
            '0.2', 'C', parent='0', attributes={'pattern_type': 'Singleton'}))
        self.nested_graph.add_node(NestedGraph.Node(
            '1', '([D,F]|[E,G?])', attributes={'pattern_type': 'Choice'}))
        self.nested_graph.add_node(NestedGraph.Node(
            '1.0', '[D,F]', parent='1', attributes={'pattern_type': 'Sequence'}))
        self.nested_graph.add_node(NestedGraph.Node(
            '1.0.0', 'D', parent='1.0', attributes={'pattern_type': 'Singleton'}))
        self.nested_graph.add_node(NestedGraph.Node(
            '1.0.1', 'F', parent='1.0', attributes={'pattern_type': 'Singleton'}))
        self.nested_graph.add_node(NestedGraph.Node(
            '1.1', '[E,G?]', parent='1', attributes={'pattern_type': 'Sequence'}))
        self.nested_graph.add_node(NestedGraph.Node(
            '1.1.0', 'E', parent='1.1', attributes={'pattern_type': 'Singleton'}))
        self.nested_graph.add_node(NestedGraph.Node(
            '1.1.1', 'G?', parent='1.1', attributes={'pattern_type': 'Optional'}))
        self.nested_graph.add_node(NestedGraph.Node(
            '1.1.1.0', 'G', parent='1.1.1', attributes={'pattern_type': 'Singleton'}))
        self.nested_graph.add_node(NestedGraph.Node(
            '2', '[H,I]', attributes={'pattern_type': 'Sequence'}))
        self.nested_graph.add_node(NestedGraph.Node(
            '2.0', 'H', parent='2', attributes={'pattern_type': 'Singleton'}))
        self.nested_graph.add_node(NestedGraph.Node(
            '2.1', 'I', parent='2', attributes={'pattern_type': 'Singleton'}))
        self.nested_graph.add_edge(NestedGraph.Edge(
            '0.0->0.1', '0.0', '0.1'))
        self.nested_graph.add_edge(NestedGraph.Edge(
            '0.1->0.2', '0.1', '0.2'))
        self.nested_graph.add_edge(NestedGraph.Edge(
            '0.2->1.0.0', '0.2', '1.0.0'))
        self.nested_graph.add_edge(NestedGraph.Edge(
            '0.2->1.1.0', '0.2', '1.1.0'))
        self.nested_graph.add_edge(NestedGraph.Edge(
            '1.0.0->1.0.1', '1.0.0', '1.0.1'))
        self.nested_graph.add_edge(NestedGraph.Edge(
            '1.1.0->1.1.1.0', '1.1.0', '1.1.1.0'))
        self.nested_graph.add_edge(NestedGraph.Edge(
            '1.0.1->2.0', '1.0.1', '2.0'))
        self.nested_graph.add_edge(NestedGraph.Edge(
            '1.1.1.0->2.0', '1.1.1.0', '2.0'))
        self.nested_graph.add_edge(NestedGraph.Edge(
            '2.0->2.1', '2.0', '2.1'))

    def test_get_nodes_by_label(self):
        self.assertListEqual(
            [NestedGraph.Node('0.0', 'A', parent='0',
                              attributes={'pattern_type': 'Singleton'})],
            self.nested_graph.get_nodes_by_label('A'))

    def test_from_and_to_dict(self):
        self.assertEqual(
            self.nested_graph,
            NestedGraph.from_dict(self.nested_graph.to_dict())
        )

if __name__ == '__main__':
    unittest.main()
