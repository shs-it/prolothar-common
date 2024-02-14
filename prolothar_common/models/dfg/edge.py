# -*- coding: utf-8 -*-

from dataclasses import dataclass
from prolothar_common.models.dfg.node import Node

@dataclass
class Edge:
    start: Node
    end: Node
    count: int = 0

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

    def is_self_loop(self) -> bool:
        """returns True if start and end node of this edge are identical"""
        return self.start.activity == self.end.activity