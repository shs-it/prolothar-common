# -*- coding: utf-8 -*-

import unittest
from dhcollections.set_similarity import sorensen_dice_coefficient
from dhcollections.set_similarity import jaccard_index
from dhcollections.set_similarity import overlap_coefficient

class TestSetSimilarity(unittest.TestCase):
    
    def test_sorensen_dice_coefficient(self):
        self.assertEqual(1.0, sorensen_dice_coefficient(set(), set()))
        self.assertEqual(0.25, sorensen_dice_coefficient(
                {'ni','ig','gh','ht'}, {'na','ac','ch','ht'}))
    
    def test_jaccard_index(self):
        self.assertEqual(1.0, jaccard_index(set(), set()))
        self.assertAlmostEqual(0.429, jaccard_index(
                {1,2,3,4,7}, {1,4,5,7,9}), delta=0.001)
    
    def test_overlap_coefficient(self):
        self.assertEqual(1.0, overlap_coefficient(set(), set()))
        self.assertAlmostEqual(0.333, overlap_coefficient(
                {1,2,3}, {1,4,5,7,9}), delta=0.001)
            
if __name__ == '__main__':
    unittest.main()     