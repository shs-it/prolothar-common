from typing import List, Any, Tuple
from abc import ABC, abstractmethod

import numpy as np
from sklearn.base import ClusterMixin

ClustersAndOutliers = Tuple[List[List[Any]], List[Any]]

class VectorClusteringAlgorithm(ABC):
    """
    interface to vector based clustering algorithms
    """

    @abstractmethod
    def cluster(self, matrix: np.ndarray) -> np.ndarray:
        """
        clusters the row vectors of the given matrix

        Parameters
        ----------
        matrix : np.ndarray
            2-d shape matrix

        Returns
        -------
        np.ndarray
            a vector with cluster indices of the instances with
            - -1 means outlier
            - >= 0 is a cluster index
        """

    def decode_label_vector(
        self, instances: List[Any], label_vector: np.ndarray) -> ClustersAndOutliers:
        """
        translates the given label vector by separating a list of instances
        into a list of clusters and a set of

        Parameters
        ----------
        instances : List[Any]
            a list of instances with the same length as the label vector
        label_vector : np.ndarray
            a vector with cluster indices of the instances with
            - -1 means outlier
            - >= 0 is a cluster index

        Returns
        -------
        ClustersAndOutliers
        """
        clusters = [[] for i in range(max(label_vector)+1)]
        outliers = []

        for instance,label in zip(instances, label_vector):
            if label < 0:
                outliers.append(instance)
            else:
                clusters[label].append(instance)

        return clusters, outliers

class SklearnClustering(VectorClusteringAlgorithm):
    """
    template to plugin sklearn clustering algorithms
    """

    def __init__(self, sklearner: ClusterMixin):
        self.__sklearner = sklearner

    def cluster(self, matrix: np.ndarray) -> np.ndarray:
        return self.__sklearner.fit(matrix).labels_
