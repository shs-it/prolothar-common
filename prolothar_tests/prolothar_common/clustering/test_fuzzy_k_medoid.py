# -*- coding: utf-8 -*-

import unittest

from prolothar_common.clustering.fuzzy_k_medoid import FuzzyKMedoid
import numpy as np

class TestFuzzyKMedoid(unittest.TestCase):

    def test_cluster(self):
        objects = [
            np.array([1,2,3]), np.array([7,8,9]),
            np.array([1,2,2]), np.array([7,8,10]),
            np.array([2,2,3]), np.array([6,8,9])
        ]
        membership_matrix,medoids = FuzzyKMedoid(
                lambda x,y: np.linalg.norm(x-y), random_seed=42).cluster(
                        objects, number_of_clusters=2)

        self.assertSetEqual(set([0,1]), set(medoids))
        self.assertTrue(np.array_equal(
                np.array([1] * len(objects)),
                np.sum(membership_matrix, axis=1)))

if __name__ == '__main__':
    unittest.main()