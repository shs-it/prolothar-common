from prolothar_common.models.eventlog import EventLog

from prolothar_common.clustering.traces.common import ClustersAndOutliers
from prolothar_common.clustering.traces.encoder.encoder import TraceToVectorEncoder
from prolothar_common.clustering.traces.clustering_algorithm import VectorClusteringAlgorithm

class VectorBasedClustering:
    """
    clusters traces of an event log by first encoding the traces of the log as
    vectors and then apply a vector clustering algorithm
    """

    def __init__(self, encoder: TraceToVectorEncoder, clustering_algorithm: VectorClusteringAlgorithm):
        self.__encoder = encoder
        self.__clustering_algorithm = clustering_algorithm

    def cluster(self, log: EventLog) -> ClustersAndOutliers:
        return self.__clustering_algorithm.decode_label_vector(
            log.traces,
            self.__clustering_algorithm.cluster(self.__encoder.encode_log(log)))

    def __call__(self, log: EventLog):
        return self.cluster(log)
