'''
    This file is part of Prolothar-Common (More Info: https://github.com/shs-it/prolothar-common).

    Prolothar-Common is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Prolothar-Common is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Prolothar-Common. If not, see <https://www.gnu.org/licenses/>.
'''

from typing import List, Callable, Any
from random import Random
import numpy as np
from math import exp

DissimilarityFunction = Callable[[Any,Any], float]

class FuzzyKMedoid():
    """implementation of the fuzzy k medoid algorithm as explained in
    http://individual.utoronto.ca/_zihayatm/Papers/HIS.pdf
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.41.2622&rep=rep1&type=pdf"""

    def __init__(self, dissimilarity_function: DissimilarityFunction,
                 coefficient: float = 0.1, random_seed: int = None):
        """creates a new instance of the clustering algorithm

        Args:
            dissimilarity_function:
                a function computing a dissimilarity value between for
                any two objects given to the "cluster"-method
            coefficient:
                the lambda coefficient in the paper
            random_seed:
                seed to initialize the random generator used in this class.
                can be set to an integer value to get reproducible results
        """
        self.__dissimilarity_function = dissimilarity_function
        self.__coefficient = coefficient
        self.__random_generator = Random(random_seed)

    def cluster(self, objects: List[Any],
                number_of_clusters: int = None):
        """returns the membership matrix U (nxc) and the indices of the cluster
        medoids (list of size c)"""
        cluster_center_indices = self.__randomly_select_cluster_centers(
                objects, number_of_clusters)
        dissimilarity_matrix = self.__compute_dissimilarity_matrix(objects)
        P = None
        while True:
            membership_matrix = self.__compute_degree_of_membership_matrix(
                    cluster_center_indices, objects, dissimilarity_matrix)
            P_new = np.sum(np.multiply(
                    membership_matrix,
                    dissimilarity_matrix[:,cluster_center_indices]))
            if P is not None and np.isclose(P_new, P):
                break
            P = P_new
            cluster_center_indices = self.__recompute_cluster_centers(
                    cluster_center_indices, objects, membership_matrix,
                    dissimilarity_matrix)
        return membership_matrix,cluster_center_indices

    def __randomly_select_cluster_centers(
                self, objects: List[Any],
                number_of_clusters: int) -> List[int]:
        if number_of_clusters is None:
            number_of_clusters = len(objects)
        if number_of_clusters <= 0:
            raise ValueError(
                    'number_of_clusters must not be <= 0 but was %d'
                    % number_of_clusters)
        if number_of_clusters > len(objects):
            raise ValueError(
                    'number_of_clusters must not be > len(objects) but was %d'
                    % number_of_clusters)
        cluster_center_indices = list(range(len(objects)))
        self.__random_generator.shuffle(cluster_center_indices)
        return cluster_center_indices[:number_of_clusters]

    def __compute_degree_of_membership_matrix(
            self, cluster_center_indices: List[int], objects: List[Any],
            dissimilarity_matrix):
        def compute_u(i,j):
            return exp(-dissimilarity_matrix[i,j] / self.__coefficient) / sum(
                    exp(-dissimilarity_matrix[i,t] / self.__coefficient)
                    for t in cluster_center_indices)
        return np.array([
                [compute_u(i,z) for j,z in enumerate(cluster_center_indices)]
                for i,x in enumerate(objects)
               ])

    def __compute_dissimilarity_matrix(self, objects: List[Any]):
        return np.array([[self.__dissimilarity_function(x1,x2) for x1 in objects]
                         for x2 in objects])

    def __recompute_cluster_centers(
            self, cluster_center_indices, objects, membership_matrix,
            dissimilarity_matrix) -> List[int]:
        Q = np.matmul(np.transpose(membership_matrix), dissimilarity_matrix)
        return list(np.argmin(Q, axis=1))





