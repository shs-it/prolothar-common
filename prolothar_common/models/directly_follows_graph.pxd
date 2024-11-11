from prolothar_common.models.dfg.node cimport Node
from prolothar_common.models.dfg.edge cimport Edge

cdef class DirectlyFollowsGraph():
    """directly-follows graph of a EventLog. Nodes in the graph correspond to
    activities and there is a edge from A to B if A is directly-followed by B.
    """
    cdef public dict edges
    cdef public dict nodes

    cpdef add_node(self, str activity)
    cpdef remove_node(self, str activity, bint create_connections=?)
    cpdef add_count(self, str start_activity, str end_activity, int count=?)
    cpdef int get_nr_of_nodes(self)
    cpdef int get_nr_of_edges(self)
    cpdef filter_edges_by_local_frequency(self, float min_frequency, bint keep_at_least_one_outgoing_edge=?)
    #def compute_shortest_path(self, start_activity: str, end_activity: str, forbidden_edges: Iterable[Tuple[str,str]] = None) -> List[str]
    cpdef list compute_shortest_path(self, str start_activity, str end_activity, object forbidden_edges = ?)
    cpdef list compute_shortest_path_to_one_of(self, str start_activity, set end_activities)
    cpdef set get_reachable_activities(self, str start_activity)
    cpdef list get_preceeding_activities(self, str activity)
    cpdef list get_following_activities(self, str activity)
    cpdef int compute_indegree(self, str activity)
    cpdef Edge remove_edge(self, tuple edge_key)
    cpdef DirectlyFollowsGraph copy(self)
    cpdef join(self, DirectlyFollowsGraph other)
