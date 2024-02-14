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

from prolothar_common.clustering.fuzzy_k_medoid import FuzzyKMedoid
from prolothar_common.clustering.k_medoid import KMedoid
from prolothar_common.models.eventlog import EventLog
from prolothar_common.models.directly_follows_graph import DirectlyFollowsGraph

class ActivityKMedoid:
    """reimplementation of the idea of "Process Mining: Fuzzy Clustering and
    Performance Visualization"""

    def __init__(self, log: EventLog, fuzzy=False):
        """creates a new instance of the clustering algorithm for clustering
        activities of the given log"""
        self.__activities = list(log.compute_activity_set())
        self.__dfg = DirectlyFollowsGraph.create_from_event_log(log)
        self.__max_count = max([edge.count for edge in self.__dfg.get_edges()])
        self.__fuzzy = fuzzy

    def cluster_activities(self, nr_of_clusters: int, random_seed: int = None):
        """returns a dictionary giving the cluster membership probabilities for
        all activities and a list containing the cluster medoids"""
        if self.__fuzzy:
            membership_dict, cluster_medoids = self.__fuzzy_clustering(
                    nr_of_clusters, random_seed=random_seed)
        else:
            membership_dict, cluster_medoids = self.__nonfuzzy_clustering(
                    nr_of_clusters, random_seed=random_seed)

        return membership_dict, [self.__activities[i] for i in cluster_medoids]

    def __fuzzy_clustering(self, nr_of_clusters, random_seed=False):
        fuzzy_k_medoid = FuzzyKMedoid(
                self.__compute_activity_dissimilarity, random_seed=random_seed)

        membership_matrix, cluster_medoids = fuzzy_k_medoid.cluster(
                self.__activities, number_of_clusters=nr_of_clusters)

        membership_dict = {
            activity: membership_matrix[i,:]
            for i,activity in enumerate(self.__activities)
        }

        return membership_dict, cluster_medoids

    def __nonfuzzy_clustering(self, nr_of_clusters, random_seed=False):
        k_medoid = KMedoid(self.__compute_activity_dissimilarity,
                           random_seed=random_seed)

        membership_vector, cluster_medoids = k_medoid.cluster(
                self.__activities, number_of_clusters=nr_of_clusters)

        membership_dict = {
            activity: membership_vector[i]
            for i,activity in enumerate(self.__activities)
        }

        return membership_dict, cluster_medoids

    def __compute_activity_dissimilarity(self, a: str, b: str) -> float:
        return 1 - self.__compute_activity_similiarity(a,b)

    def __compute_activity_similiarity(self, a: str, b: str) -> float:
        if a == b:
            return 1
        return ((self.__dfg.get_count(a,b) + self.__dfg.get_count(b,a) + 1) /
               (1 + 2 * self.__max_count))
