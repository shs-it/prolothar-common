# -*- coding: utf-8 -*-

import unittest
from prolothar_common.models.prefix_tree.prefix_tree import PrefixTree

class TestPrefixTree(unittest.TestCase):

    def test_create_tree_choices(self):
        sequences = [
            ["A", "B", "C"],
            ["A", "B"],
            ["A", "B", "D"],
            ["A", "B", "C"],
            ["B", "D"]
        ]

        tree = PrefixTree()
        for sequence in sequences:
            tree.append(sequence)

        self.assertEqual(5, len(tree))

        expected_dot_code = ('digraph {\n'
           '\t.0 [label="A | 4" shape=rectangle]\n'
           '\t.0 -> ".0.0" [label=4]\n'
           '\t".0.0" [label="B | 4" shape=rectangle]\n'
           '\t".0.0" -> ".0.0.1" [label=1]\n'
           '\t".0.0" -> ".0.0.0" [label=2]\n'
           '\t".0.0.0" [label="C | 2" shape=rectangle]\n'
           '\t".0.0.1" [label="D | 1" shape=rectangle]\n'
           '\t.1 [label="B | 1" shape=rectangle]\n'
           '\t.1 -> ".1.0" [label=1]\n'
           '\t".1.0" [label="D | 1" shape=rectangle]\n'
           '}')
        dot_code = tree.plot(view=False)
        self.assertEqual(expected_dot_code, dot_code)

    def test_create_tree_should_terminate(self):
        sequence_list = [
            ['STAB', 'GIES', 'BRBA', 'SORT', 'BRWA', 'LMBR', 'TMBR', 'STOE', 'STOZ', 'ZUND', 'WLVG', 'DLFG', 'WRIC', 'HSAN', 'GREX', 'DIKB', 'BUEI', 'BUAU', 'OFLK', 'OFH1', 'EZH1', 'STH1', 'USH1', 'N1O2', 'FHO2', 'BFH2', 'MAH2', 'KAPU', 'AJH2', 'ENDK', 'KU16', 'H2F4', 'STRF', 'KUST', 'LZP2', 'VERL', 'LIEF'],
            ['STAB', 'GIES', 'BRBA', 'SORT', 'BRWA', 'LMBR', 'TMBR', 'STOE', 'STOZ', 'ZUND', 'WLVG', 'DLFG', 'WRIC', 'HSAN', 'GREX', 'DIKB', 'BUEI', 'BUAU', 'OFLK', 'OFH1', 'EZH1', 'STH1', 'USH1', 'N1O2', 'FHO2', 'BFH2', 'MAH2', 'KAPU', 'AJH2', 'ENDK', 'KU16', 'H2F4', 'STRF', 'KUST', 'LZP2', 'VERL', 'LIEF'],
            ['STAB', 'GIES', 'BRBA', 'SORT', 'BRWA', 'LMBR', 'TMBR', 'STOE', 'STOZ', 'ZUND', 'WLVG', 'DLFG', 'WRIC', 'HSAN', 'GREX', 'DIKB', 'BUEI', 'BUAU', 'OFLK', 'OFH1', 'EZH1', 'STH1', 'USH1', 'N1O2', 'FHO2', 'BFH2', 'MAH2', 'KAPU', 'RIKO', 'AJH2', 'ENDK', 'KU16', 'H2F4', 'STRF', 'KUST', 'LZP2', 'VERL', 'LIEF'],
            ['STAB', 'GIES', 'BRBA', 'SORT', 'BRWA', 'LMBR', 'TMBR', 'STOE', 'STOZ', 'ZUND', 'WLVG', 'DLFG', 'WRIC', 'HSAN', 'GREX', 'DIKB', 'WAEI', 'WAAU', 'FAE2', 'OFH2', 'OFLK', 'EZH2', 'STH2', 'USH2', 'LMR3', 'TWR3', 'OER3', 'A1R3', 'OAR3', 'TAR3', 'AKR3', 'TRFA', 'BFH2', 'MAH2', 'KAPU', 'RIKO', 'AJH2', 'ENDK', 'USSU', 'KUST', 'LZP2', 'VERL', 'LIEF'],
            ['STAB', 'GIES', 'BRBA', 'SORT', 'BRWA', 'LMBR', 'TMBR', 'STOE', 'STOZ', 'ZUND', 'WLVG', 'DLFG', 'WRIC', 'HSAN', 'GREX', 'DIKB', 'BUEI', 'BUAU', 'FAE2', 'OFH2', 'OFLK', 'EZH2', 'STH2', 'USH2', 'LMR3', 'TWR3', 'OER3', 'A1R3', 'OAR3', 'TAR3', 'AKR3', 'TRFA', 'BFH2', 'MAH2', 'KAPU', 'AJH2', 'ENDK', 'USSU', 'KUST', 'LZP2', 'VERL', 'LIEF']
        ]
        tree = PrefixTree()
        for sequence in sequence_list:
            tree.append(sequence)

    def test_children_and_is_leaf(self):
        tree = PrefixTree()
        self.assertTrue(tree.is_leaf())
        self.assertEqual(0, len(tree.get_children()))

        sequences = [
            ["A", "B", "C"],
            ["A", "B"],
            ["A", "B", "D"],
            ["A", "B", "C"],
            ["B", "D"]
        ]

        tree = PrefixTree()
        for sequence in sequences:
            tree.append(sequence)

        self.assertFalse(tree.is_leaf())
        self.assertEqual(2, len(tree.get_children()))

    def test_traverse_level_order(self):
        sequences = [
            ["A", "B", "C"],
            ["A", "B"],
            ["A", "B", "D"],
            ["A", "B", "C"],
            ["B", "D"]
        ]

        tree = PrefixTree()
        for sequence in sequences:
            tree.append(sequence)

        expected_traversal_orders_list = [
            ['A', 'B', 'B', 'D', 'D', 'C'],
            ['B', 'A', 'D', 'B', 'D', 'C']
        ]
        actual_traversal_order = [node.get_symbol()
                                  for node in tree.traverse_level_order()]
        for expected_traversal_order in expected_traversal_orders_list:
            if actual_traversal_order == expected_traversal_order:
                break
        else:
            self.fail('unexpected traversal order: %r' % actual_traversal_order)

if __name__ == '__main__':
    unittest.main()
