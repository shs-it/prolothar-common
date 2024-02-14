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

from typing import List, Generator
from collections import deque
from graphviz import Digraph
import prolothar_common.gviz_utils as gviz_utils

class PrefixTree:
    """efficient prefix tree storage for sequence databases"""

    def __init__(self, node_id: str = ''):
        """creates a new, empty prefix tree.
        Args:
            node_id: is used internally. do not use this parameter if you want
            to create a new tree.
        """
        self.__id = node_id
        self.__nr_of_sequences = 0
        self.__children = []
        self.__symbol = None

    def append(self, sequence: List[str]):
        """appends the given sequence to this tree"""
        if sequence:
            i = self.__find_insertion_point(sequence[0])
            if i >= len(self.__children):
                self.__children.append(self.__create_child(sequence))
            elif self.__children[i].__symbol == sequence[0]:
                self.__children[i].append(sequence[1:])
            else:
                self.__children.insert(i, self.__create_child(sequence))
        self.__nr_of_sequences += 1

    def __find_insertion_point(self, symbol: str) -> int:
        if not self.__children:
            return 0
        start_index = 0
        end_index = len(self.__children)
        while start_index < end_index:
            mid_index = (start_index + end_index) // 2
            mid_symbol = self.__children[mid_index].__symbol
            if mid_symbol == symbol:
                return mid_index
            elif mid_symbol < symbol:
                end_index = mid_index
            else:
                start_index = mid_index + 1
        return start_index

    def __create_child(self, sequence: List[str]) -> 'PrefixTree':
        child = PrefixTree(node_id = self.__id + '.' + str(len(self.__children)))
        child.__symbol = sequence[0]
        child.append(sequence[1:])
        return child

    def __len__(self) -> int:
        """returns the number of sequences in this tree"""
        return self.__nr_of_sequences

    def is_leaf(self) -> bool:
        """
        returns true if this node has no children
        """
        return not self.__children

    def get_children(self) -> List['PrefixTree']:
        return self.__children

    def get_node_id(self) -> str:
        return self.__id

    def get_nr_of_sequences(self) -> int:
        return self.__nr_of_sequences

    def get_symbol(self) -> int:
        return self.__symbol

    def traverse_level_order(self) -> Generator['PrefixTree', None, None]:
        """
        traverses the tree in levelorder, i.e. using breadth-first search.
        the root node (self) is excluded.
        """
        queue = deque()
        queue.extendleft(self.get_children())
        while queue:
            node = queue.pop()
            yield node
            queue.extendleft(node.get_children())

    def plot(self, filepath: str = None, view: bool = True, filetype: str='pdf',
         layout: str='dot'):
        """
        returns the graph viz dot source code of the created graph

        Args:
            layout:
                default is dot. (dot, neato, fdp, circo)
        """
        graph = Digraph()

        remaining_nodes = list(self.__children)
        while remaining_nodes:
            node = remaining_nodes.pop()
            graph.node(node.__id, shape='rectangle', label='%s | %d' % (
                    node.__symbol, len(node)))
            for j,child in enumerate(node.__children):
                graph.edge(node.__id, child.__id, label=str(len(child)))
            remaining_nodes.extend(node.__children)

        return gviz_utils.plot_graph(graph, view=view, filepath=filepath,
                                     filetype=filetype, layout=layout)

