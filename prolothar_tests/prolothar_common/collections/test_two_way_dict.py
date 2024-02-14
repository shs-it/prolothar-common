# -*- coding: utf-8 -*-

import unittest
from dhcollections.two_way_dict import TwoWayDict

class TestTwoWayDict(unittest.TestCase):
    
    def setUp(self):
        self.dict = TwoWayDict()
        
    def test_look_up(self):
        self.dict[0] = 'Bool'
        self.dict[0] = 'George Bool'
        self.dict[1] = 'Alan Turing'
        self.dict[2] = 'Alan Turing'
        
        self.assertCountEqual('George Bool', self.dict[0])
        self.assertCountEqual('Alan Turing', self.dict[1])
        self.assertCountEqual('Alan Turing', self.dict[2])
        
    def test_inverse_look_up(self):
        self.dict[0] = 'Bool'
        self.dict[0] = 'George Bool'
        self.dict[1] = 'Alan Turing'
        self.dict[2] = 'Alan Turing'
        
        self.assertCountEqual([1,2], self.dict.inverse('Alan Turing'))
        
    def test_contains(self):
        self.assertFalse(4711 in self.dict)
        self.dict[4711] = 42
        self.assertTrue(4711 in self.dict)
            
if __name__ == '__main__':
    unittest.main()       