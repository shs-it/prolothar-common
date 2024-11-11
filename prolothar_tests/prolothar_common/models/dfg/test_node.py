# -*- coding: utf-8 -*-

import unittest

from prolothar_common.models.dfg.node import Node

class TestNode(unittest.TestCase):

    def test_add_pattern_to_node(self):
        node = Node('Test')
        node.pattern = 'abc*'
        self.assertEqual(node.activity, 'Test')

if __name__ == '__main__':
    unittest.main()