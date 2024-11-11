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

from typing import List
from dataclasses import dataclass

@dataclass
class Node:
     """a node of a directly follows graph"""
     activity: str
     edges: List = None
     ingoing_edges: List = None
     color: str = 'white'
     fontcolor: str = 'black'
     def is_followed_by(self, activity: str) -> bool:
         """returns True if there is edge from this node to a node with the
         given activity"""
         ...