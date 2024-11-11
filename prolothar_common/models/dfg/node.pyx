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

cdef class Node:
     """a node of a directly follows graph"""

     def __init__(self, str activity, list edges = None, list ingoing_edges = None, str color = 'white', str fontcolor = 'black'):
        self.activity = activity
        self.edges = edges
        self.ingoing_edges = ingoing_edges
        self.color = color
        self.fontcolor = fontcolor

     def __eq__(self, other):
         return (other is not None and
                 self.activity == other.activity and
                 self.edges == other.edges)

     def __hash__(self):
         return hash(self.activity)

     def __repr__(self) -> str:
         return 'Node[activity=%s, color=%s]' % (
                 self.activity, self.color)

     cpdef bint is_followed_by(self, str activity):
         """returns True if there is edge from this node to a node with the
         given activity"""
         for edge in self.edges:
             if edge.end.activity == activity:
                 return True
         return False