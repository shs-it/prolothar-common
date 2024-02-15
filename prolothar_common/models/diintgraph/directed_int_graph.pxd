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

from prolothar_common.models.diintgraph.graph cimport Graph

cdef class DirectedIntGraph:

    cdef Graph *graph

    cpdef add_edge(self, int node_a, int node_b)
    cpdef remove_edge(self, int node_a, int node_b)
    cpdef bint contains_edge(self, int node_a, int node_b)

    cpdef list find_strongly_connected_components(self)
    cpdef list get_ancestors(self, int node)
    cpdef DirectedIntGraph copy(self)
