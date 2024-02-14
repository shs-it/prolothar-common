from prolothar_common.models.diintgraph.graph cimport Graph

cdef class DirectedIntGraph:

    cdef Graph *graph

    cpdef add_edge(self, int node_a, int node_b)
    cpdef remove_edge(self, int node_a, int node_b)
    cpdef bint contains_edge(self, int node_a, int node_b)

    cpdef list find_strongly_connected_components(self)
    cpdef list get_ancestors(self, int node)
    cpdef DirectedIntGraph copy(self)
