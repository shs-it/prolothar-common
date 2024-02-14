# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.diintgraph import DirectedIntGraph

class TestDirectedIntGraph(unittest.TestCase):

    def test_build_and_query_graph(self):
        graph = DirectedIntGraph(5)
        graph.add_edge(0,1)
        graph.add_edge(1,2)
        graph.add_edge(2,0)
        graph.add_edge(3,4)
        graph.add_edge(4,3)
        components = graph.find_strongly_connected_components()
        self.assertCountEqual([set([0,1,2]),set([3,4])], list(map(set, components)))

        self.assertEqual([1], graph.get_ancestors(0))
        self.assertEqual([4], graph.get_ancestors(3))
        self.assertTrue(graph.contains_edge(0, 1))
        self.assertTrue(graph.contains_edge(1, 2))
        self.assertFalse(graph.contains_edge(3, 2))

        graph.remove_edge(1, 2)
        self.assertFalse(graph.contains_edge(1, 2))

    def test_copy(self):
        graph = DirectedIntGraph(5)
        graph.add_edge(0,1)
        graph.add_edge(1,2)
        graph.add_edge(2,0)
        graph.add_edge(2,1)
        graph.add_edge(3,4)
        graph.add_edge(4,3)

        copy = graph.copy()
        graph.add_edge(2,3)

        self.assertEqual([1], copy.get_ancestors(0))
        self.assertEqual([0,1], copy.get_ancestors(2))
        self.assertEqual([4], copy.get_ancestors(3))

        copy.add_edge(0,2)
        self.assertEqual([1,2], copy.get_ancestors(0))
        self.assertEqual([1], graph.get_ancestors(0))


if __name__ == '__main__':
    unittest.main()