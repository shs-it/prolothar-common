# -*- coding: utf-8 -*-

import unittest

from prolothar_common.clustering.k_medoid import KMedoid
import numpy as np

class TestFuzzyKMedoid(unittest.TestCase):

    def test_cluster(self):
        objects = [
            np.array([1,2,3]), np.array([7,8,9]),
            np.array([1,2,2]), np.array([7,8,10]),
            np.array([2,2,3]), np.array([8,8,9])
        ]
        membership_vector,medoids = KMedoid(
                lambda x,y: np.linalg.norm(x-y), random_seed=42).cluster(
                        objects, number_of_clusters=2)

        self.assertSetEqual(set([1,4]), set(medoids))
        self.assertListEqual([1,0,1,0,1,0], membership_vector)

if __name__ == '__main__':
    unittest.main()