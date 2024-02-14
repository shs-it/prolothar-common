"""
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
"""

from libcpp.list cimport list as cpplist
from cython.operator cimport preincrement, dereference

cdef class DirectedIntGraph:

    def __cinit__(self, int nr_of_nodes):
        self.graph = new Graph(nr_of_nodes)

    cpdef DirectedIntGraph copy(self):
        copy = DirectedIntGraph(0)
        del copy.graph
        copy.graph = new Graph(dereference(self.graph))
        return copy

    cpdef add_edge(self, int node_a, int node_b):
        self.graph.addEdge(node_a, node_b)

    cpdef remove_edge(self, int node_a, int node_b):
        self.graph.removeEdge(node_a, node_b)

    cpdef bint contains_edge(self, int node_a, int node_b):
        return self.graph.containsEdge(node_a, node_b)

    cpdef list find_strongly_connected_components(self):
        cdef cpplist[cpplist[int]*]* cpp_components = self.graph.findStronglyConnectedComponents()
        cdef list components = []
        cdef list component
        cdef cpplist[cpplist[int]*].iterator it = dereference(cpp_components).begin()
        cdef cpplist[int].iterator it2
        cdef cpplist[int]* cpp_component
        while it != dereference(cpp_components).end():
            cpp_component = dereference(it)
            it2 = cpp_component.begin()
            component = []
            while it2 != dereference(it).end():
                component.append(dereference(it2))
                preincrement(it2)
            components.append(component)
            preincrement(it)
            del cpp_component
        del cpp_components
        return components

    cpdef list get_ancestors(self, int node):
        return dereference(self.graph.getAdjacencyList(node))

    def __dealloc__(self):
        del self.graph