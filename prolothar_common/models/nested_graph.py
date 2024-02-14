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

from typing import Set, List, Dict

class NestedGraph():

    class Node():
        def __init__(self, id: str, label: str, parent: str = None,
                     attributes: Dict = None):
            self.id = id
            self.label = label
            self.parent = parent
            self.attributes = attributes if attributes is not None else {}

        def __eq__(self, other: 'NestedGraph.Node') -> bool:
            return (isinstance(other, NestedGraph.Node) and
                    self.id == other.id and
                    self.parent == other.parent and
                    self.attributes == other.attributes)

        def __hash__(self):
            return hash(self.id)

        def __repr__(self):
            s = '<Node %s, label=%s' % (self.id, self.label)
            if self.parent is not None:
                s += ', parent=' + self.parent
            if self.attributes:
                s += ', attributes=%r' % self.attributes
            return s + '>'

    class Edge():
        def __init__(self, id:str, source: str, target: str,
                     attributes: Dict = None):
            self.id = id
            self.source = source
            self.target = target
            self.attributes = attributes if attributes is not None else {}

        def __eq__(self, other: 'NestedGraph.Edge') -> bool:
            return (isinstance(other, NestedGraph.Edge) and
                    self.id == other.id and
                    self.source == other.source and
                    self.target == other.target and
                    self.attributes == other.attributes)

        def __hash__(self):
            return hash(self.id)

        def __repr__(self):
            return '<Edge %s, %s => %s>' % (self.id, self.source, self.target)

    def __init__(self):
        self._nodes = dict()
        self._edges = set()

    def add_node(self, node: Node):
        self._nodes[node.id] = node

    def add_edge(self, edge: Edge):
        self._edges.add(edge)

    def remove_edge(self, edge: Edge):
        self._edges.remove(edge)

    def get_nodes(self) -> Set['NestedGraph.Node']:
        return self._nodes.values()

    def get_edges(self) -> Set['NestedGraph.Edge']:
        return self._edges

    def get_node_by_id(self, id: str) -> 'NestedGraph.Node':
        return self._nodes[id]

    def get_nodes_by_label(self, label: str) -> List['NestedGraph.Node']:
        return [node for node in self._nodes.values() if node.label == label]

    def get_edge_by_source_and_target(
            self, source_id: str, target_id: str) -> 'NestedGraph.Edge':
        for edge in self._edges:
            if edge.source == source_id and edge.target == target_id:
                return edge
        raise ValueError('edge could not be found')

    def has_children(self, node_id: str) -> bool:
        for node in self._nodes.values():
            if node.parent == node_id:
                return True
        return False

    def get_low_level_sink_nodes(self, node_id: str) -> List['NestedGraph.Node']:
        if not self.has_children(node_id):
            return [self.get_node_by_id(node_id)]
        else:
            low_level_sink_nodes = []
            for sink in self.get_subgraph(node_id).get_sink_nodes():
                if not self.has_children(sink.id):
                    low_level_sink_nodes.append(sink)
                else:
                    low_level_sink_nodes.extend(self.get_low_level_sink_nodes(sink.id))
            return low_level_sink_nodes

    def get_low_level_source_nodes(self, node_id: str) -> List['NestedGraph.Node']:
        if not self.has_children(node_id):
            return [self.get_node_by_id(node_id)]
        else:
            low_level_source_nodes = []
            for sink in self.get_subgraph(node_id).get_source_nodes():
                if not self.has_children(sink.id):
                    low_level_source_nodes.append(sink)
                else:
                    low_level_source_nodes.extend(self.get_low_level_source_nodes(sink.id))
            return low_level_source_nodes

    def get_subgraph(self, node_id: str):
        subgraph = NestedGraph()
        for node in self.get_children(node_id):
            subgraph.add_node(node)
            for edge in self.get_outgoing_edges(node.id):
                subgraph.add_edge(edge)
        return subgraph

    def get_outgoing_edges(self, node_id: str):
        return [edge for edge in self._edges if edge.source == node_id]

    def get_ingoing_edges(self, node_id: str):
        return [edge for edge in self._edges if edge.target == node_id]

    def get_children(self, node_id: str) -> List['NestedGraph.Node']:
        children = []
        for node in self._nodes.values():
            if node.parent == node_id:
                children.append(node)
        return children

    def get_source_nodes(self) -> List['NestedGraph.Node']:
        sources = []
        for node in self._nodes.values():
            if len(self.get_ingoing_edges(node.id)) == 0:
                sources.append(node)
        return sources

    def get_sink_nodes(self) -> List['NestedGraph.Node']:
        sinks = []
        for node in self._nodes.values():
            if len(self.get_outgoing_edges(node.id)) == 0:
                sinks.append(node)
        return sinks

    def replace_high_level_edges_by_low_level_edges(self):
        """removes all edges from nodes with children and replaces them
        by edges between children at the lowest level"""
        edges_to_remove = set()
        edges_to_add = set()

        for edge in self.get_edges():
            start_node = self.get_node_by_id(edge.source)
            end_node = self.get_node_by_id(edge.target)

            if self.has_children(start_node.id) or self.has_children(end_node.id):
                edges_to_remove.add(edge)
                self._add_low_level_edges(start_node, end_node, edges_to_add)

        for edge in edges_to_remove:
            self.remove_edge(edge)

        for edge in edges_to_add:
            self.add_edge(edge)

    def to_dict(self) -> Dict:
        """returns a dictionary with the following structure:
        {
            nodes: [{id: id, label: label, parent?: parent, attribute1: attribute1, ...}],
            edges: [{id: id, source: source, target: target, attribute1: attribute1, ...}]
        }
        """
        d = {'nodes': [], 'edges': []}

        for node in self.get_nodes():
            node_dict = {}
            node_dict['id'] = node.id
            node_dict['label'] = node.label
            if node.parent is not None:
                node_dict['parent'] = node.parent
            for key,value in node.attributes.items():
                node_dict[key] = value
            d['nodes'].append(node_dict)

        for edge in self.get_edges():
            edge_dict = {}
            edge_dict['id'] = edge.id
            edge_dict['source'] = edge.source
            edge_dict['target'] = edge.target
            for key,value in edge.attributes.items():
                edge_dict[key] = value
            d['edges'].append(edge_dict)

        return d

    def _add_low_level_edges(self, start_node: 'NestedGraph.Node',
                             end_node: 'NestedGraph.Node',
                             edges_to_add: Set['NestedGraph.Edge']):
        new_start_nodes = self.get_low_level_sink_nodes(start_node.id)
        new_end_nodes = self.get_low_level_source_nodes(end_node.id)

        for new_start_node in new_start_nodes:
            for new_end_node in new_end_nodes:
                edges_to_add.add(NestedGraph.Edge(
                    '%s->%s' % (new_start_node.id, new_end_node.id),
                    new_start_node.id, new_end_node.id))

    def __eq__(self, other: 'NestedGraph'):
        return (isinstance(other, NestedGraph) and
                self._nodes == other._nodes and
                self._edges == other._edges)

    def __repr__(self) -> str:
        s = 'NestedGraph\n'
        s += 'Nodes: %r\n' % self._nodes.values()
        s += 'Edges: %r\n' % self._edges
        return s

    @staticmethod
    def from_dict(dictionary: Dict) -> 'NestedGraph':
        """creates a NestedGraph from a dictionary with the following structure:
        {
            nodes: [{id: id, label: label, parent?: parent, attribute1: attribute1, ...}],
            edges: [{id: id, source: source, target: target, attribute1: attribute1, ...}]
        }
        """
        graph = NestedGraph()
        for node in dictionary['nodes']:
            graph.add_node(NestedGraph.Node(
                node['id'], node['label'], parent=node.get('parent', None),
                attributes={key: value for key, value in node.items()
                            if key not in ['id', 'label', 'parent']}
            ))
        for edge in dictionary['edges']:
            graph.add_edge(NestedGraph.Edge(
                edge['id'], edge['source'], edge['target'],
                attributes={key: value for key, value in edge.items()
                            if key not in ['id', 'source', 'target']}
            ))
        return graph
