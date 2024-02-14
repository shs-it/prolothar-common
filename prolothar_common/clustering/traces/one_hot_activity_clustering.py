# -*- coding: utf-8 -*-

from prolothar_common.models.eventlog import EventLog
from prolothar_common.clustering.traces.common import ClustersAndOutliers
from prolothar_common.clustering.traces.vector_based_clustering import VectorBasedClustering
from prolothar_common.clustering.traces.encoder import ActivityOneHotEncoding
from prolothar_common.clustering.traces.clustering_algorithm import SklearnClustering

from sklearn.cluster import DBSCAN, OPTICS

def dbscan(log: EventLog, epsilon=0.5) -> ClustersAndOutliers:
    """returns a tuple with the first component being a list of clusters,
    each cluster consisting of a list of traces, and the second component
    being a list of traces which are detected as outliers"""
    return VectorBasedClustering(
        ActivityOneHotEncoding(), SklearnClustering(DBSCAN(eps=epsilon))
    ).cluster(log)

def optics(log: EventLog) -> ClustersAndOutliers:
    return VectorBasedClustering(
        ActivityOneHotEncoding(), SklearnClustering(OPTICS())
    ).cluster(log)
