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

DissimilarityFunction = Callable[[Any,Any], float]

class KMedoid():
    """implementation of the fuzzy k medoid algorithm (PAM).
    see https://towardsdatascience.com/k-medoids-clustering-on-iris-data-set-1931bf781e05
    """

    def __init__(self, dissimilarity_function: DissimilarityFunction,
                 random_seed: int = None, dissimilarity_mode: bool = True):
        """creates a new instance of the clustering algorithm

        Args:
            dissimilarity_function:
                a function computing a dissimilarity value between for
                any two objects given to the "cluster"-method
            random_seed:
                seed to initialize the random generator used in this class.
                can be set to an integer value to get reproducible results
            dissimilarity_mode:
                default is True. If False, then the dissimilarity function is
                a similarity function, which will be considered when selecting
                medoids
        """
        self.__dissimilarity_function = dissimilarity_function
        self.__random_generator = Random(random_seed)
        self.__dissimilarity_mode = dissimilarity_mode

    def cluster(self, objects: List[Any],
                number_of_clusters: int = None):
        """returns a list of labels of length n and the indices of the cluster
        medoids (list of size c)"""
        cluster_center_indices = self.__randomly_select_cluster_centers(
                objects, number_of_clusters)
        dissimilarity_matrix = self.__compute_dissimilarity_matrix(objects)
        while True:
            if self.__dissimilarity_mode:
                #select medoids minimizing distance
                memberships = np.argmin(
                        dissimilarity_matrix[:,cluster_center_indices], axis=1)
            else:
                #select medoids maximizing similarity
                memberships = np.argmax(
                        dissimilarity_matrix[:,cluster_center_indices], axis=1)
            new_cluster_center_indices = self.__recompute_cluster_centers(
                    cluster_center_indices, objects, memberships,
                    dissimilarity_matrix)
            if new_cluster_center_indices == cluster_center_indices:
                break
            cluster_center_indices = new_cluster_center_indices
        return memberships.tolist(),cluster_center_indices

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

    def __compute_dissimilarity_matrix(self, objects: List[Any]):
        return np.array([[self.__dissimilarity_function(x1,x2) for x1 in objects]
                         for x2 in objects])

    def __recompute_cluster_centers(
            self, cluster_center_indices, objects, memberships,
            dissimilarity_matrix) -> List[int]:
        new_cluster_center_indices = list(cluster_center_indices)

        for i,center_index in enumerate(cluster_center_indices):
            sum_of_distances = np.sum(dissimilarity_matrix[:,center_index])

            for point_in_cluster in np.argwhere(memberships == i).flatten():
                new_sum_of_distances = np.sum(dissimilarity_matrix[
                        :,point_in_cluster])
                if new_sum_of_distances < sum_of_distances:
                    sum_of_distances = new_sum_of_distances
                    new_cluster_center_indices[i] = point_in_cluster

        return new_cluster_center_indices





