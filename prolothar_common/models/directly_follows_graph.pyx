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

from typing import List, Tuple, Set, Dict, Iterable, Union, Iterable
from random import Random
import random
from collections import deque
from graphviz import Digraph

from prolothar_common.models.eventlog import EventLog, Trace, Event
import prolothar_common.gviz_utils as gviz_utils
from prolothar_common.experiments.statistics import Statistics

cdef class DirectlyFollowsGraph():

    __DEFAULT_ZERO_EDGE = Edge(None, None, 0)

    def __init__(self):
        self.edges = {}
        self.nodes = {}

    cpdef add_node(self, str activity):
        if activity not in self.nodes:
            self.nodes[activity] = Node(
                activity, 
                edges=[], 
                ingoing_edges=[]
            )

    cpdef remove_node(self, str activity, bint create_connections=False):
        """removes a node from the graph
        Args:
            activity:
                the activity of the node that is supposed to be removed
            create_connections:
                default is False. If True, then the predecessors of the removed
                nodes are connected with the ancestors
        """
        if create_connections:
            for predecessor in self.get_preceeding_activities(activity):
                for ancestor in self.get_following_activities(activity):
                    self.add_count(predecessor, ancestor)

        node = self.nodes.pop(activity)
        cdef set edge_keys_to_delete = set()
        for edge in node.edges:
            edge_keys_to_delete.add((
                (<Edge>edge).start.activity, 
                (<Edge>edge).end.activity
            ))
        for edge in node.ingoing_edges:
            edge_keys_to_delete.add((
                (<Edge>edge).start.activity,
                (<Edge>edge).end.activity
            ))
        for edge_key in edge_keys_to_delete:
            self.remove_edge(<tuple>edge_key)

    cpdef Edge remove_edge(self, tuple edge_key):
        cdef Edge edge
        if edge_key in self.edges:
            edge = self.edges.pop(edge_key)
            edge.start.edges.remove(edge)
            edge.end.ingoing_edges.remove(edge)
            return edge
        return None

    cpdef add_count(self, str start_activity, str end_activity, int count=1):
        self.add_node(start_activity)
        self.add_node(end_activity)
        edge = (start_activity, end_activity)
        if edge not in self.edges:
            self.edges[edge] = Edge(start=self.nodes[start_activity],
                                    end=self.nodes[end_activity])
            self.nodes[start_activity].edges.append(self.edges[edge])
            self.nodes[end_activity].ingoing_edges.append(self.edges[edge])
        self.edges[edge].count += count

    cpdef int get_nr_of_nodes(self):
        return len(self.nodes)

    def get_nodes(self) -> Iterable[Node]:
        return self.nodes.values()

    cpdef int get_nr_of_edges(self):
        return len(self.edges)

    def get_edges(self) -> Iterable[Edge]:
        return self.edges.values()

    def __eq__(self, other):
        return isinstance(other, DirectlyFollowsGraph) and \
               self.plot(view=False) == other.plot(view=False)

    def __repr__(self):
        return self.plot(view=False)

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
        graph = Digraph()
        if concentrate_edges:
            graph.attr('graph', concentrate='true')

        self.__plot_nodes(graph, random_walk_alignment, use_topological_order)

        self.__plot_edges(graph, show_counts, counts_as_edge_weight,
            min_edge_weight, max_edge_weight)

        return gviz_utils.plot_graph(graph, view=view, filepath=filepath,
                                     filetype=filetype, layout=layout)

    def __plot_nodes(
            self, graph: Digraph, random_walk_alignment: Union[None,Tuple[str,str,int]],
            use_topological_order: bool):
        if random_walk_alignment is not None and use_topological_order:
            raise NotImplementedError()
        if random_walk_alignment is not None:
            self.__add_node_groups_to_graph(
                self.__compute_random_walk_based_node_groups(
                    random_walk_alignment), graph)
        elif use_topological_order:
            self.__add_node_groups_to_graph(
                self.__compute_topological_order_node_groups(), graph)
        else:
            self.__add_nodes_to_graph(self.nodes.values(), graph)

    def __add_node_groups_to_graph(
            self, node_groups: Dict[int,List[Node]], graph: Digraph):
        for i,node_group in sorted(node_groups.items(),
                           key = lambda v: v[0]):
            with graph.subgraph() as subgraph:
                subgraph.attr('graph', rank='same')
                self.__add_nodes_to_graph(node_group, subgraph)

    def __compute_random_walk_based_node_groups(
            self, random_walk_alignment: Tuple[str,str,int]) -> Dict[int,List[Node]]:
        statistics_dict = {
                activity: Statistics() for activity in self.nodes
        }
        for _ in range(random_walk_alignment[2]):
            self.__do_random_walk(random_walk_alignment[0],
                                  random_walk_alignment[1],
                                  statistics_dict)
        for node in sorted(self.get_nodes(),
               key=lambda v: statistics_dict[v.activity].mean()):
            statistics_dict[node.activity] = round(
                    statistics_dict[node.activity].mean())

        node_groups = { i: [] for i in statistics_dict.values() }
        for node in self.get_nodes():
            node_groups[statistics_dict[node.activity]].append(node)
        return node_groups

    def __compute_topological_order_node_groups(self) -> Dict[int,List[Node]]:
        node_groups = {}
        i = 0

        dfg = self.copy()
        sources = dfg.get_source_nodes()
        while sources:
            node_groups[i] = []
            for src in sources:
                node_groups[i].append(src)
                for edge_to_next_src in list(src.edges):
                    for cyclic_edge in list(edge_to_next_src.end.ingoing_edges):
                        dfg.remove_edge((cyclic_edge.start.activity,
                                         cyclic_edge.end.activity))
                dfg.remove_node(src.activity)
            sources = dfg.get_source_nodes()
            i += 1
        return node_groups

    def __add_nodes_to_graph(self, nodes: Iterable[Node], graph: Digraph):
        for node in sorted(nodes, key=lambda n: n.activity):
            graph.node(node.activity, shape='rectangle', style='filled',
                       fillcolor=node.color, fontcolor=node.fontcolor)

    def __do_random_walk(self, start_activity: str, end_activity: str,
                         statistics_dict: Dict[str, Statistics]):
        i = 0
        visited = set()
        current = self.nodes[start_activity]
        visited.add(current.activity)
        i += 1
        while current.activity != end_activity:
            unvisited_choices = [edge for edge in current.edges
                                 if edge.end.activity not in visited]
            if not unvisited_choices:
                break
            current = random.choice(unvisited_choices).end
            visited.add(current.activity)
            statistics_dict[current.activity].push(i)
            i += 1

    def __plot_edges(
            self, graph: Digraph, show_counts: bool, counts_as_edge_weight: bool,
            min_edge_weight: float, max_edge_weight: float):

        if self.edges:
            min_edge_count = min(edge.count for edge in self.get_edges())
            max_edge_count = max(edge.count for edge in self.get_edges())

        for edge in sorted(self.edges.values(),
                       key = lambda e: (e.start.activity, e.end.activity)):
            graph.edge(edge.start.activity, edge.end.activity,
                       label=str(edge.count) if show_counts else '',
                       penwidth=self.__compute_edge_weight(
                               edge, counts_as_edge_weight, min_edge_weight,
                               max_edge_weight, min_edge_count, max_edge_count))

    def __compute_edge_weight(
            self, edge, counts_as_edge_weight: bool, min_edge_weight: float,
            max_edge_weight: float, min_edge_count: float,
            max_edge_count) -> str:
        if counts_as_edge_weight:
            if max_edge_count != min_edge_count:
                return str((edge.count - min_edge_count) /
                           (max_edge_count - min_edge_count) *
                           (max_edge_weight - min_edge_weight) + min_edge_weight)
            else:
                return '1.0'
        else:
            return '1.0'

    cpdef filter_edges_by_local_frequency(
            self, float min_frequency, bint keep_at_least_one_outgoing_edge = False):
        cdef DirectlyFollowsGraph filtered_dfg = self.copy()
        for edge_key in list(filtered_dfg.edges.keys()):
            filtered_dfg.remove_edge(<tuple>edge_key)
        cdef Node node
        cdef Edge edge
        for node in self.nodes.values():
            total_count_of_node = 0
            for edge in node.edges:
                total_count_of_node += edge.count
            for edge in node.edges:
                if total_count_of_node > 0 \
                and edge.count / total_count_of_node >= min_frequency:
                    filtered_dfg.add_count(edge.start.activity,
                                           edge.end.activity, count=edge.count)
        cdef Node unfiltered_node
        for node in filtered_dfg.get_nodes():
            if not node.edges and keep_at_least_one_outgoing_edge:
                unfiltered_node = self.nodes[node.activity]
                if unfiltered_node.edges:
                    max_edge = DirectlyFollowsGraph.__DEFAULT_ZERO_EDGE 
                    for edge in unfiltered_node.edges:
                        if edge.count > max_edge.count:
                            max_edge = edge
                    filtered_dfg.add_count(max_edge.start.activity,
                                           max_edge.end.activity, count=max_edge.count)
        return filtered_dfg

    def filter_edges_by_absolute_count(self, min_count: int):
        """removes all edges in this directly-follows-graph which have a
        count less than 'min_count'
        """
        cdef DirectlyFollowsGraph filtered_dfg = self.copy()
        for edge_key in list(filtered_dfg.edges.keys()):
            filtered_dfg.remove_edge(<tuple>edge_key)
        cdef Edge edge
        for edge in self.edges.values():
            if edge.count >= min_count:
                filtered_dfg.add_count(edge.start.activity,
                                       edge.end.activity, count=edge.count)
        return filtered_dfg

    cpdef list compute_shortest_path(self, str start_activity, str end_activity, object forbidden_edges = None):
        """Uses breadth-first-search algorithm for computing the shortest path (
        i.e. the path with the minimal number of edges) between two activity
        nodes in the DFG. If no path is found, an empty list is returned. If
        start = end then also an empty list is returned.

        forbidden_edges: Iterable[Tuple[str,str]]
        result: List[str]
        """
        #https://codereview.stackexchange.com/questions/193410/breadth-first-search-implementation-in-python-3-to-find-path-between-two-given-n
        if start_activity not in self.nodes:
            raise ValueError('start activity %s not in DFG' % start_activity)

        if start_activity == end_activity:
            return []

        cdef list removed_edges = []
        if forbidden_edges is not None:
            for edge_key in forbidden_edges:
                removed_edges.append(self.remove_edge(<tuple>edge_key))

        cdef set visited = {start_activity}
        queue = deque([(start_activity, [])])

        cdef str current_activity
        cdef list path
        cdef str neighbor
        cdef Edge edge
        try:
            while queue:
                current_activity, path = queue.popleft()
                visited.add(current_activity)
                #sorted makes the choice reproducible
                for neighbor in sorted(self.get_following_activities(current_activity)):
                    if neighbor == end_activity:
                        return path + [current_activity, neighbor]
                    if neighbor not in visited:
                        queue.append((neighbor, path + [current_activity]))
                        visited.add(neighbor)

            # no path found
            return []
        finally:
            for edge in removed_edges:
                self.add_count(edge.start.activity, edge.end.activity,
                               count=edge.count)

    cpdef list compute_shortest_path_to_one_of(self, str start_activity, set end_activities):
        """Uses breadth-first-search algorithm for computing the shortest path (
        i.e. the path with the minimal number of edges) between a start activity
        and a set of end activties of nodes in the DFG.
        If no path is found, an empty list is returned. If
        start = end then also an empty list is returned

        result: List[str]
        """
        #https://codereview.stackexchange.com/questions/193410/breadth-first-search-implementation-in-python-3-to-find-path-between-two-given-n
        if start_activity not in self.nodes:
            raise ValueError('start activity %s not in DFG' % start_activity)

        if start_activity in end_activities:
            return []

        cdef set visited = {start_activity}
        queue = deque([(start_activity, [])])

        cdef str current_activity
        cdef list path
        while queue:
            current_activity, path = queue.popleft()
            visited.add(current_activity)
            #sorted makes the choice reproducible
            for neighbor in sorted(self.get_following_activities(current_activity)):
                if neighbor in end_activities:
                    return path + [current_activity, neighbor]
                if neighbor not in visited:
                    queue.append((neighbor, path + [current_activity]))
                    visited.add(neighbor)

        # no path found
        return []

    cpdef int compute_indegree(self, str activity):
        return len((<Node>self.nodes[activity]).ingoing_edges)

    cpdef list get_preceeding_activities(self, str activity):
        cdef list result = []
        for edge in (<Node>self.nodes[activity]).ingoing_edges:
            result.append((<Edge>edge).start.activity)
        return result

    cpdef list get_following_activities(self, str activity):
        cdef list result = []
        for edge in (<Node>self.nodes[activity]).edges:
            result.append((<Edge>edge).end.activity)
        return result

    cpdef DirectlyFollowsGraph copy(self):
        cdef DirectlyFollowsGraph copy = DirectlyFollowsGraph()
        copy.join(self)
        return copy

    cpdef join(self, DirectlyFollowsGraph other):
        """adds all nodes and edges from "other" to this DirectlyFollowsGraph
        """
        for node in other.nodes.values():
            self.add_node((<Node>node).activity)
        for edge_key, edge in other.edges.items():
            self.edges[edge_key] = Edge(
                    self.nodes[edge.start.activity],
                    self.nodes[edge.end.activity],
                    edge.count)
        for edge_key, edge in other.edges.items():
            (<Node>self.nodes[(<Edge>edge).start.activity]).edges.append(self.edges[edge_key])
        for edge_key, edge in other.edges.items():
            (<Node>self.nodes[(<Edge>edge).end.activity]).ingoing_edges.append(self.edges[edge_key])

    def read_counts_from_log(self, log: EventLog):
        for trace in log.traces:
            if len(trace) > 0:
                self.add_node(trace.events[0].activity_name)
            for i in range(len(trace.events) - 1):
                self.add_node(trace.events[i].activity_name)
                self.add_count(
                    trace.events[i].activity_name,
                    trace.events[i+1].activity_name)

    def select_nodes(self, activities: Union[List[str],Set[str]]) -> 'DirectlyFollowsGraph':
        """returns a copy of this graph with nodes whose activity is in the
        given list
        """
        if not isinstance(activities, set):
            activities = set(activities)
        copy = self.copy()
        for node in list(copy.get_nodes()):
            if node.activity not in activities:
                copy.remove_node(node.activity)
        return copy

    def get_source_nodes(self) -> List[Node]:
        """
        returns all nodes that have no ingoing edges. self-loops do not count
        """
        return [node for node in self.get_nodes()
                if self.compute_indegree(node.activity) == 0 or (
                        self.compute_indegree(node.activity) == 1 and
                        node.is_followed_by(node.activity))]

    def get_source_activities(self) -> List[str]:
        """returns the activities of all source nodes"""
        return [node.activity for node in self.get_source_nodes()]

    def get_sink_nodes(self) -> List[Node]:
        """
        returns all nodes that have no outgoing edges. self-loops do not count
        """
        return [node for node in self.get_nodes()
                if len(node.edges) == 0 or (
                        len(node.edges) == 1 and node.is_followed_by(node.activity))]

    def get_sink_activities(self) -> List[str]:
        """returns the activities of all sink nodes"""
        return [node.activity for node in self.get_sink_nodes()]

    def get_largest_weakly_connected_component(self) -> 'DirectlyFollowsGraph':
        largest_component = []
        max_component_size = 0
        for component in self.get_weakly_connected_components():
            if len(component) > max_component_size:
                max_component_size = len(component)
                largest_component = component

        return self.select_nodes(largest_component)

    def get_weakly_connected_components(self) -> List[List[str]]:
        """returns a list of connected components. each component is a list
        of activities in that component
        """
        unseen_activities = set(self.nodes.keys())
        connected_components = []
        while unseen_activities:
            start_activity = next(iter(unseen_activities))
            unseen_activities.remove(start_activity)
            connected_components.append(
                    self._create_weakly_connected_component_from_start(
                            start_activity, unseen_activities))
        return connected_components

    def _create_weakly_connected_component_from_start(
            self, start_activity: str, unseen_activities: Set[str]) -> List[str]:
        connected_component = []
        next_activities = [start_activity]
        while next_activities:
            activity = next_activities.pop()
            connected_component.append(activity)
            for next_activity in (
                    self.get_preceeding_activities(activity) +
                    self.get_following_activities(activity)):
                if next_activity in unseen_activities:
                    unseen_activities.remove(next_activity)
                    next_activities.append(next_activity)
        return connected_component

    cpdef set get_reachable_activities(self, str start_activity):
        """
        returns the set of reachable nodes (activities) starting from
        the given activity
        """
        cdef set reachable_activities = set()
        cdef set next_activities = set(self.get_following_activities(start_activity))
        while next_activities:
            activity = next_activities.pop()
            reachable_activities.add(activity)
            for following_activity in self.get_following_activities(<str>activity):
                if following_activity not in reachable_activities:
                    next_activities.add(following_activity)
        return reachable_activities

    def get_activities_that_reach(self, end_activity: str) -> Set[str]:
        """
        returns all activities that can reach the given activity
        """
        activities_that_reach = set()
        next_activities = set(self.get_preceeding_activities(end_activity))
        while next_activities:
            activity = next_activities.pop()
            activities_that_reach.add(activity)
            for preceding_activity in self.get_preceeding_activities(activity):
                if preceding_activity not in activities_that_reach:
                    next_activities.add(preceding_activity)
        return activities_that_reach

    def get_count(self, a: str, b: str) -> int:
        edge_key = (a,b)
        return self.edges.get(edge_key, DirectlyFollowsGraph.__DEFAULT_ZERO_EDGE).count

    def remove_not_allowed_start_activities(
            self, allowed_start_activities: Set[str]):
        """iteratively removes source nodes whose activities are not contained
        in the given set until there are only source nodes with the given
        activities"""
        source_removed = True
        while source_removed:
            source_removed = False
            for activity in self.get_source_activities():
                if activity not in allowed_start_activities:
                    self.remove_node(activity)
                    source_removed = True

    def remove_not_allowed_end_activities(
            self, allowed_end_activities: Set[str]):
        """iteratively removes sink nodes whose activities are not contained
        in the given set until there are only sink nodes with the given
        activities"""
        sink_removed = True
        while sink_removed:
            sink_removed = False
            for activity in self.get_sink_activities():
                if activity not in allowed_end_activities:
                    self.remove_node(activity)
                    sink_removed = True

    def rename_activity(self, old_name: str, new_name: str):
        """renames a node, i.e. updating the activity of the node and the
        edges containing this activity
        """
        node = self.nodes[old_name]
        self.nodes[new_name] = node
        self.nodes.pop(old_name)
        node.activity = new_name
        for ingoing_edge in node.ingoing_edges:
            if ingoing_edge.is_self_loop():
                self.edges.pop((old_name, old_name))
            else:
                self.edges.pop((ingoing_edge.start.activity, old_name))
            self.edges[(ingoing_edge.start.activity, new_name)] = ingoing_edge
        for outgoing_edge in node.edges:
            if not outgoing_edge.is_self_loop():
                self.edges.pop((old_name, outgoing_edge.end.activity))
                self.edges[(new_name, outgoing_edge.end.activity)] = outgoing_edge

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
        random_generator = Random(random_seed)
        if start_activities is None:
            start_activities = self.get_source_activities()
        if end_activities is None:
            end_activities = self.get_sink_activities()
        if not start_activities:
            raise ValueError('start activities must not be empty')
        if not end_activities:
            raise ValueError('end activities must not be empty')
        log = EventLog()
        for i in range(nr_of_traces):
            events_in_trace = []
            current_activity = None
            next_possible_activities = start_activities
            while True:
                current_activity = random_generator.choice(
                        next_possible_activities)
                next_possible_activities = self.get_following_activities(
                        current_activity)
                events_in_trace.append(Event(current_activity))
                if current_activity in end_activities:
                    break
            log.add_trace(Trace(i, events_in_trace))
        return log

    @staticmethod
    def create_from_event_log(log: EventLog) -> 'DirectlyFollowsGraph':
        dfg = DirectlyFollowsGraph()
        dfg.read_counts_from_log(log)
        return dfg

    @staticmethod
    def build_eventually_follows_on_first_occurence_graph(
            log: EventLog) -> 'DirectlyFollowsGraph':
        """returns a DirectlyFollowsGraph that does not store directly-follows-
        relations but the following: only the first unique activities are kept
        in all traces of the log, e.g. ABCBCD => ABCD. then, there is an edge
        between A and B iff B is eventually observed after A, i.e. there can be
        other activities occuring between A and B.
        """
        filtered_log = log.copy()
        filtered_log.keep_first_occurence_of_activity_only()
        follows_graph = DirectlyFollowsGraph()
        for trace in filtered_log.traces:
            for i,event in enumerate(trace.events):
                for following_event in trace.events[i+1:]:
                    follows_graph.add_count(event.activity_name,
                                            following_event.activity_name)
        return follows_graph