# -*- coding: utf-8 -*-

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
     def __eq__(self, other):
         return (other is not None and 
                 self.activity == other.activity and 
                 self.edges == other.edges)
     def __hash__(self):
         return hash(self.activity)
     def __repr__(self) -> str:
         return 'Node[activity=%s, color=%s]' % (
                 self.activity, self.color)
     def is_followed_by(self, activity: str) -> bool:
         """returns True if there is edge from this node to a node with the
         given activity"""
         for edge in self.edges:
             if edge.end.activity == activity:
                 return True
         return False