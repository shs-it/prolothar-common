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

from typing import Callable, Hashable, Dict, Set, Tuple, Iterator, List
from collections import defaultdict

from graphviz import Digraph
import prolothar_common.gviz_utils as gviz_utils

from prolothar_common.func_tools import Min
from prolothar_common.models.labeled_transition_system.state_representation import set_abstraction
from prolothar_common.models.eventlog import Trace

State = Hashable
Transition = Tuple[State, Hashable, State]

class LabeledTransitionSystem:
    """
    implements a labeled transition system as defined in
    "Time and Activity Sequence Prediction of Business Process Instances"
    https://andrea.burattin.net/public-files/publications/2018-computing.pdf
    """

    def __init__(self, state_representation_function: Callable[[List[Hashable]], State] = set_abstraction):
        self.__state_representation_function = state_representation_function
        self.__states: Set[State] = set()
        self.__start_states: Set[State] = set()
        self.__end_states: Set[State] = set()
        self.__transition_relation: Dict[State, Dict[Hashable, State]] = defaultdict(dict)

    def add_trace(self, trace: Trace):
        """
        adds a trace to this transition system

        Parameters
        ----------
        trace : Trace
            all prefixes from this trace will be added to this transition
            system
        """
        self.add_sequence([event.activity_name for event in trace.events])

    def add_sequence(self, sequence: List[Hashable]):
        """
        adds a trace to this transition system

        Parameters
        ----------
        trace : Trace
            all prefixes from this trace will be added to this transition
            system
        """
        start_state = self.__state_representation_function([])
        self.__add_state(start_state, True, len(sequence) == 0)
        last_state = start_state
        for i in range(1, len(sequence) + 1):
            state = self.__state_representation_function(sequence[:i])
            self.__add_state(state, False, i == len(sequence))
            self.__add_transition(last_state, sequence[i-1], state)
            last_state = state

    def __add_state(self, state: State, start_state: bool, end_state: bool):
        self.__states.add(state)
        if start_state:
            self.__start_states.add(state)
        if end_state:
            self.__end_states.add(state)

    def __add_transition(
            self, state: State, event: Hashable, next_state: State):
        self.__transition_relation[state][event] = next_state

    def get_states(self) -> Set[State]:
        return self.__states

    def get_start_states(self) -> Set[State]:
        return self.__start_states

    def get_end_states(self) -> Set[State]:
        return self.__end_states

    def yield_outgoing_transitions(self, state: State) -> Iterator[Transition]:
        for event, next_state in self.__transition_relation[state].items():
            yield (state, event, next_state)

    def get_next_state(self, state: State, event: Hashable) -> State:
        return self.__transition_relation[state][event]

    def get_nr_of_states(self) -> int:
        """
        returns the number of states in this transition system
        """
        return len(self.__states)

    def get_nr_of_transitions(self) -> int:
        """
        returns the number of transitions in this transition system
        """
        nr_of_transitions = 0
        for transition_dict in self.__transition_relation.values():
            nr_of_transitions += len(transition_dict)
        return nr_of_transitions

    def transition_iterator(self) -> Iterator[Transition]:
        """
        yields (state, event, next_state) tuples
        """
        for state, event_next_state_dict in self.__transition_relation.items():
            for event, next_state in event_next_state_dict.items():
                yield (state, event, next_state)

    def plot(
        self, filepath: str = None, view: bool = True, filetype: str='pdf',
        layout: str='dot', use_state_representation_for_labels: bool = False):
        """
        returns the graph viz dot source code of this transition system

        Args:
            layout:
                default is dot. (dot, neato, fdp, circo)
        """
        graph = Digraph()

        state_node_id_dict = {}
        for i, state in enumerate(sorted(
                self.__states,
                key=lambda x: Min if x is None else x)):
            node_id = f's{i}'
            state_node_id_dict[state] = node_id
            if use_state_representation_for_labels:
                node_shape = 'rectangle'
                if isinstance(state, frozenset):
                    node_label = str(set(state))
                else:
                    node_label = str(state)
            else:
                node_label = node_id
                node_shape = 'circle'
            if state in self.__end_states:
                number_of_border_lines = 2
            else:
                number_of_border_lines = 1
            graph.node(
                node_id, shape=node_shape, label=node_label,
                peripheries=str(number_of_border_lines))

        for i, transition in enumerate(self.transition_iterator()):
            graph.edge(
                state_node_id_dict[transition[0]],
                state_node_id_dict[transition[2]],
                label=str(transition[1]))

        return gviz_utils.plot_graph(graph, view=view, filepath=filepath,
                                     filetype=filetype, layout=layout)