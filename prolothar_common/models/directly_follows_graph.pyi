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

from typing import List, Tuple, Set, Iterable, Union, Iterable

from prolothar_common.models.eventlog import EventLog
from prolothar_common.models.dfg.node import Node
from prolothar_common.models.dfg.edge import Edge

class DirectlyFollowsGraph():
    """directly-follows graph of a EventLog. Nodes in the graph correspond to
    activities and there is a edge from A to B if A is directly-followed by B.
    """

    def __init__(self):
        ...

    def add_node(self, activity: str):
        """adds a node with a given activity to this graph"""
        ...

    def remove_node(self, activity: str, create_connections=False):
        """removes a node from the graph
        Args:
            activity:
                the activity of the node that is supposed to be removed
            create_connections:
                default is False. If True, then the predecessors of the removed
                nodes are connected with the ancestors
        """
        ...

    def remove_edge(self, edge_key: Tuple[str,str]) -> Edge:
        ...

    def add_count(self, start_activity: str, end_activity: str, count=1):
        ...

    def get_nr_of_nodes(self):
        ...

    def get_nodes(self) -> Iterable[Node]:
        ...

    def get_nr_of_edges(self):
        ...

    def get_edges(self) -> Iterable[Edge]:
        ...

    def plot(self, filepath: str = None, view: bool = True, filetype: str='pdf',
             layout: str='dot', show_counts: bool = True,
             counts_as_edge_weight: bool = False, min_edge_weight: float = 1.0,
             max_edge_weight: float = 10.0, concentrate_edges: bool = False,
             random_walk_alignment: Tuple[str,str,int] = None,
             use_topological_order: bool = False):
        """
        returns the graph viz dot source code of the created graph

        Args:
            layout:
                default is dot. (dot, neato, fdp, circo)
            random_walk_alignment:
                default is None. If a 3-tuple (start_activity,end_activity,n)
                is supplied, then the nodes are temporally aligned (top nodes
                are at the beginning and bottom nodes at the end). the temporal
                position is determined by the average path position during
                random walks from start_activity to end_activity
        """
        ...

    def filter_edges_by_local_frequency(
            self, min_frequency: float, keep_at_least_one_outgoing_edge: bool = False):
        ...

    def filter_edges_by_absolute_count(self, min_count: int):
        """removes all edges in this directly-follows-graph which have a
        count less than 'min_count'
        """
        ...

    def compute_shortest_path(
            self, start_activity: str,
            end_activity: str,
            forbidden_edges: Iterable[Tuple[str,str]] = None) -> List[str]:
        """Uses breadth-first-search algorithm for computing the shortest path (
        i.e. the path with the minimal number of edges) between two activity
        nodes in the DFG. If no path is found, an empty list is returned. If
        start = end then also an empty list is returned
        """
        ...

    def compute_shortest_path_to_one_of(
            self, start_activity: str,
            end_activities: Set[str]) -> List[str]:
        """Uses breadth-first-search algorithm for computing the shortest path (
        i.e. the path with the minimal number of edges) between a start activity
        and a set of end activties of nodes in the DFG.
        If no path is found, an empty list is returned. If
        start = end then also an empty list is returned
        """
        ...

    def compute_indegree(self, activity: str) -> int:
        ...

    def get_preceeding_activities(self, activity: str) -> List[str]:
        ...

    def get_following_activities(self, activity: str) -> List[str]:
        ...

    def copy(self) -> 'DirectlyFollowsGraph':
        ...

    def join(self, other: 'DirectlyFollowsGraph'):
        """adds all nodes and edges from "other" to this DirectlyFollowsGraph
        """
        ...

    def read_counts_from_log(self, log: EventLog):
        ...

    def select_nodes(self, activities: Union[List[str],Set[str]]) -> 'DirectlyFollowsGraph':
        """returns a copy of this graph with nodes whose activity is in the
        given list
        """
        ...

    def get_source_nodes(self) -> List[Node]:
        """
        returns all nodes that have no ingoing edges. self-loops do not count
        """
        ...

    def get_source_activities(self) -> List[str]:
        """returns the activities of all source nodes"""
        ...

    def get_sink_nodes(self) -> List[Node]:
        """
        returns all nodes that have no outgoing edges. self-loops do not count
        """
        ...

    def get_sink_activities(self) -> List[str]:
        """returns the activities of all sink nodes"""
        ...

    def get_largest_weakly_connected_component(self) -> 'DirectlyFollowsGraph':
        ...

    def get_weakly_connected_components(self) -> List[List[str]]:
        """returns a list of connected components. each component is a list
        of activities in that component
        """
        ...

    def _create_weakly_connected_component_from_start(
            self, start_activity: str, unseen_activities: Set[str]) -> List[str]:
        ...

    def get_reachable_activities(self, start_activity: str) -> Set[str]:
        """returns the set of reachable nodes (activities) starting from
        the given activity
        """
        ...

    def get_activities_that_reach(self, end_activity: str) -> Set[str]:
        """
        returns all activities that can reach the given activity
        """
        ...

    def get_count(self, a: str, b: str) -> int:
        ...

    def remove_not_allowed_start_activities(
            self, allowed_start_activities: Set[str]):
        """iteratively removes source nodes whose activities are not contained
        in the given set until there are only source nodes with the given
        activities"""
        ...

    def remove_not_allowed_end_activities(
            self, allowed_end_activities: Set[str]):
        """iteratively removes sink nodes whose activities are not contained
        in the given set until there are only sink nodes with the given
        activities"""
        ...

    def rename_activity(self, old_name: str, new_name: str):
        """renames a node, i.e. updating the activity of the node and the
        edges containing this activity
        """
        ...

    def generate_log(
            self, nr_of_traces: int, start_activities = None,
            end_activities = None, random_seed = None) -> EventLog:
        """samples sequences from the directly-follows-graph.

        Args:
            nr_of_traces:
                nr of traces in the log that should be generated. must be > 0
            start_activities:
                default is None. if None, the source activities of the graph
                will be the start activities.
            end_activities:
                default is None. if None, the end activities of the graph will
                be the end activities. must be reachable from the list of
                start activities.
            random_seed:
                default is None. can be set to a fixed value for reproducible
                results.

        Raises:
            ValueError:
                if the list of start_activities or end_activities is empty
        """
        ...

    @staticmethod
    def create_from_event_log(log: EventLog) -> 'DirectlyFollowsGraph':
        ...

    @staticmethod
    def build_eventually_follows_on_first_occurence_graph(
            log: EventLog) -> 'DirectlyFollowsGraph':
        """returns a DirectlyFollowsGraph that does not store directly-follows-
        relations but the following: only the first unique activities are kept
        in all traces of the log, e.g. ABCBCD => ABCD. then, there is an edge
        between A and B iff B is eventually observed after A, i.e. there can be
        other activities occuring between A and B.
        """
        ...