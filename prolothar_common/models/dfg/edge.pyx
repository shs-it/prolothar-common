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

from prolothar_common.models.dfg.node cimport Node

cdef class Edge:

    def __init__(self, Node start, Node end, int count = 0):
        self.start = start
        self.end = end
        self.count = count

    def __eq__(self, other):
        return (self.start.activity == other.start.activity and
                self.end.activity == other.end.activity and
                self.count == other.count)

    def __hash__(self):
        return hash((self.start, self.end))

    def __lt__(self, other):
        if self.start.activity < other.start.activity:
            return True
        if self.end.activity < other.end.activity:
            return True
        return self.count < other.count

    cpdef bint is_self_loop(self):
        """returns True if start and end node of this edge are identical"""
        return self.start.activity == self.end.activity