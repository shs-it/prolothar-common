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

import random
from typing import Dict
from abc import ABC, abstractmethod
from copy import deepcopy
from graphviz import Digraph
import prolothar_common.gviz_utils as gviz_utils

class Variable(ABC):
    def __init__(self, name: str, value=None):
        self.name = name
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    @abstractmethod
    def get_value_as_number(self) -> float:
        pass

    @abstractmethod
    def get_lower_bound_as_number(self) -> float:
        pass

    @abstractmethod
    def get_upper_bound_as_number(self) -> float:
        pass

class IntVariable(Variable):
    def __init__(self, name: str, value=None, lower_bound=None, upper_bound=None):
        super().__init__(name, value)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get_value_as_number(self) -> float:
        return self.get_value()

    def get_lower_bound_as_number(self) -> float:
        return self.lower_bound

    def get_upper_bound_as_number(self) -> float:
        return self.upper_bound

class FloatVariable(Variable):
    def __init__(self, name: str, value=None, lower_bound=None, upper_bound=None):
        super().__init__(name, value)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get_value_as_number(self) -> float:
        return self.get_value()

    def get_lower_bound_as_number(self) -> float:
        return self.lower_bound

    def get_upper_bound_as_number(self) -> float:
        return self.upper_bound

class BoolVariable(Variable):
    def __init__(self, name: str, value=None):
        super().__init__(name, value)

    def get_value_as_number(self) -> float:
        return 1 if self.value else 0

    def get_lower_bound_as_number(self) -> float:
        return 0

    def get_upper_bound_as_number(self) -> float:
        return 1

class Guard(ABC):
    def __init__(self, variable: Variable, accept_function):
        self.variable_id = variable.name
    @abstractmethod
    def accept(self, variables, variables_prime):
        pass
    @staticmethod
    def all_of(guard_list):
        return AllOfGuard(guard_list)

class LambdaGuard(Guard):
    def __init__(self, variable: Variable, accept_function):
        self.variable = variable
        self.accept_function = accept_function
    def accept(self):
        return self.accept_function(self.variable.value)

class EqualGuard(Guard):
    def __init__(self, variable: Variable, compareValue):
        self.variable = variable
        self.compareValue = compareValue
    def accept(self):
        return self.variable.value == self.compareValue

class SmallerGuard(Guard):
    def __init__(self, variable: Variable, compareValue):
        self.variable = variable
        self.compareValue = compareValue
    def accept(self):
        return self.variable.value < self.compareValue

class SmallerOrEqualGuard(Guard):
    def __init__(self, variable: Variable, compareValue):
        self.variable = variable
        self.compareValue = compareValue
    def accept(self):
        return self.variable.value <= self.compareValue

class GreaterGuard(Guard):
    def __init__(self, variable: Variable, compareValue):
        self.variable = variable
        self.compareValue = compareValue
    def accept(self):
        return self.variable.value > self.compareValue

class GreaterOrEqualGuard(Guard):
    def __init__(self, variable: Variable, compareValue):
        self.variable = variable
        self.compareValue = compareValue
    def accept(self):
        return self.variable.value >= self.compareValue

class TrueGuard(Guard):
    def __init__(self, variable: Variable):
        self.variable = variable
    def accept(self):
        return self.variable.value

class FalseGuard(Guard):
    def __init__(self, variable: Variable):
        self.variable = variable
    def accept(self):
        return not self.variable.value

class AllOfGuard(Guard):
    def __init__(self, guard_list):
        self.guard_list = guard_list
    def accept(self):
        for guard in self.guard_list:
            if not guard.accept():
                return False
        return True

class AcceptAlwaysGuard():
    def accept(self):
        return True

class Place():
    def __init__(self, id: str, label: str, nr_of_tokens=0):
        self.id = id
        self.label = label
        if nr_of_tokens < 0:
            raise ValueError('nr_of_tokens must not be < 0')
        self.nr_of_tokens=nr_of_tokens
        self.transitions = set()
    def add_transition(self, transition):
        self.transitions.add(transition)
    def increment_nr_of_tokens(self):
        self.nr_of_tokens += 1
    def decrement_nr_of_tokens(self):
        if self.nr_of_tokens <= 0:
            raise ValueError('no token available')
        self.nr_of_tokens -= 1
    def __repr__(self):
        return '<Place, id=%s, label=%s, nr_of_tokens=%r>' % (
                self.id, self.label, self.nr_of_tokens)

    @staticmethod
    def with_id_label(id: str, nr_of_tokens=0):
        return Place(id, id, nr_of_tokens=nr_of_tokens)
    @staticmethod
    def with_empty_label(id: str, nr_of_tokens=0):
        return Place(id, '', nr_of_tokens=nr_of_tokens)

class Transition():
    id: str = None
    def __init__(self, id: str, label: str = None, visible: bool = True):
        self.id = id
        if label is None:
            self.label = id
        else:
            self.label = label
        self.visible = visible
        self.start_places = set()
        self.end_places = set()
        self.guard_function = AcceptAlwaysGuard()
    def add_start_place(self, place: Place):
        self.start_places.add(place)
    def add_end_place(self, place: Place):
        self.end_places.add(place)
    def set_guard_function(self, guard: Guard):
        self.guard_function = guard
        if self.guard_function is None:
            self.guard_function = AcceptAlwaysGuard()
    def can_fire(self):
        return self.guard_function.accept()
    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other):
        return self.id == other.id
    def __repr__(self):
        return '<Transition, id=%s, label=%s, visible=%r>' % (
                self.id, self.label, self.visible)

Marking = Dict[str,int]

class DataPetriNet():
    """
    implements the data petri net model from
    "Balanced multi-perspective checking of process conformance"
    """

    def __init__(self):
        self.places = dict()
        self.transitions = dict()
        self.variables = dict()

    def add_place(self, place: Place):
        if place.id in self.places:
            raise ValueError('place %r does already exist' % place.id)
        self.places[place.id] = place
        return place

    def add_transition(self, transition: Transition):
        if transition.id in self.transitions:
            raise ValueError('transition %r does already exist' % transition.id)
        self.transitions[transition.id] = transition
        return transition

    def add_variable(self, variable: Variable):
        if variable.name in self.variables:
            raise ValueError('variable %r does already exist' % variable.name)
        self.variables[variable.name] = variable
        return variable

    def add_connection(self, start_place: Place, transition: Transition,
                       end_place: Place):
        if start_place.id not in self.places:
            raise ValueError('start_place %r is not in net' % start_place.id)
        if end_place.id not in self.places:
            raise ValueError('end_place %r is not in net' % end_place.id)
        if transition.id not in self.transitions:
            raise ValueError('transition %r is not in net' % transition.id)
        start_place.add_transition(transition)
        transition.add_start_place(start_place)
        transition.add_end_place(end_place)

    def simulate_one_timestep(self):
        firings_per_transitions = dict()

        for place in filter(lambda p: p.nr_of_tokens > 0, self.places.values()):
            fireable_transitions_for_place = list(filter(
                    lambda t: t.can_fire(),
                    place.transitions))
            if fireable_transitions_for_place:
                selected_transition = random.choice(
                        fireable_transitions_for_place)
                if not selected_transition in firings_per_transitions:
                    firings_per_transitions[selected_transition] = 1
                else:
                    firings_per_transitions[selected_transition] += 1

        for transition,firings in firings_per_transitions.items():
            if firings >= len(transition.start_places):
                self._fire_transition(transition)

    def get_fireable_transitions(self, ignore_guards=False):
        fireable_transitions = []
        for transition in self.transitions.values():
            if ((ignore_guards or transition.can_fire()) and
                sum(map(lambda p: p.nr_of_tokens, transition.start_places)) == len(transition.start_places)):
                fireable_transitions.append(transition)
        return fireable_transitions

    def get_marking(self) -> Marking:
        marking = {}
        for place in self.places.values():
            marking[place.id] = place.nr_of_tokens
        return marking

    def set_marking(self, marking: Marking):
        for place_id, nr_of_tokens in marking.items():
            self.places[place_id].nr_of_tokens = nr_of_tokens

    def matches_marking(self, marking: Marking) -> bool:
        for place_id, nr_of_tokens in marking.items():
            if not self.places[place_id].nr_of_tokens == nr_of_tokens:
                return False
        return True

    def _fire_transition(self, transition: Transition):
        for place in transition.start_places:
            place.decrement_nr_of_tokens()
        for place in transition.end_places:
            place.increment_nr_of_tokens()

    def force_transition(self, transition_id: str):
        """fires a transition given its id. ignores guards and variables

        Raises:
            ValueError: if there is no transition with the given id or if
            the preset of places of the transition has not enough tokens
            for firing the transition
        """
        if transition_id not in self.transitions:
            raise ValueError('transition %r is not in net' % transition_id)
        self._fire_transition(self.transitions[transition_id])

    def print_state(self, print_function=print):
        print_function('Places:')
        for place in self.places.values():
            print_function('\t<id=%r,label=%r,tokens=%r>' % (
                           place.id, place.label, place.nr_of_tokens))
        print_function('Variables:')
        for variable in self.variables.values():
            print_function('\t<name=%r,value=%r>' % (
                           variable.name, variable.value))

    def is_workflow_net(self):
        """returns True iff this net has exactly one source and one sink place
        """
        source_places, sink_places = self.get_source_sink_places()
        return (len(self.places) >= 2
                and len(source_places) == 1
                and len(sink_places) == 1)

    def get_source_sink_places(self):
        places_before_transitions = set()
        places_after_transitions = set()
        for transition in self.transitions.values():
            places_before_transitions = places_before_transitions.union(
                    transition.start_places)
            places_after_transitions = places_after_transitions.union(
                    transition.end_places)
        source_places = places_before_transitions.difference(places_after_transitions)
        sink_places = places_after_transitions.difference(places_before_transitions)
        return source_places, sink_places

    def transform_to_workflow_net(self):
        """returns a copy of this net and if necessary adds invisible
        transitions and places to make this net a workflow net
        """
        copy = self.copy()
        source_places, sink_places = copy.get_source_sink_places()
        if len(source_places) > 1:
            _introduce_new_source_place(copy, source_places)
        if len(sink_places) > 1:
            _introduce_new_sink_place(copy, sink_places)

        return copy

    def copy(self):
        copy = DataPetriNet()
        for place in self.places.values():
            copy.add_place(Place(place.id, place.label, place.nr_of_tokens))
        for transition in self.transitions.values():
            t = copy.add_transition(Transition(transition.id, label=transition.label,
                                               visible=transition.visible))
            t.guard_function = transition.guard_function
        for place in self.places.values():
            for transition in place.transitions:
                copy.places[place.id].transitions.add(copy.transitions[transition.id])
        for transition in self.transitions.values():
            for place in transition.start_places:
                copy.transitions[transition.id].start_places.add(copy.places[place.id])
            for place in transition.end_places:
                copy.transitions[transition.id].end_places.add(copy.places[place.id])

        copy.variables = deepcopy(self.variables)
        return copy

    def plot(self, filepath=None, view=True, filetype: str = 'pdf',
             show_labels_of_invisible_transitions=False):
        """
        returns the graph viz dot source code of the created graph
        """
        graph = Digraph()
        for place in self.places.values():
            graph.node('place_' + place.id, xlabel=place.label, shape='circle',
                       label='' if place.nr_of_tokens == 0 else str(place.nr_of_tokens))
        for transition in self.transitions.values():
            graph.node('transition_' + transition.id, label=transition.label,
                       shape='rectangle',
                       style=None if transition.visible else 'filled',
                       fillcolor='black' if not transition.visible and not show_labels_of_invisible_transitions else None)
            for place in transition.start_places:
                graph.edge('place_' + place.id, 'transition_' + transition.id)
            for place in transition.end_places:
                graph.edge('transition_' + transition.id, 'place_' + place.id)
        return gviz_utils.plot_graph(graph, filepath=filepath, view=view,
                                     filetype=filetype)

    def prune(self):
        """removes redundant invisible transitions without guards
        and also reduces the number of places.
        see also 6 stages in http://archives.njit.edu/vol01/etd/1990s/1993/njit-etd1993-006/njit-etd1993-006.pdf
        """
        remaining_transitions = {}
        remaining_places = {}
        source_places, sink_places = self.get_source_sink_places()
        for transition in self.transitions.values():
            if _can_transition_be_pruned(transition, source_places, sink_places):
                self._prune_transition(transition)
            else:
                remaining_transitions[transition.id] = transition
        self.transitions = remaining_transitions
        for transition in self.transitions.values():
            for place in transition.start_places:
                remaining_places[place.id] = place
            for place in transition.end_places:
                remaining_places[place.id] = place
        self.places = remaining_places

    def _prune_transition(self, t):
        for start_place in list(t.start_places):
            t.start_places.remove(start_place)
            start_place.transitions.remove(t)
            for end_place in list(t.end_places):
                t.end_places.remove(end_place)
                for predecessor_transition in filter(
                        lambda tr: start_place in tr.end_places,
                        self.transitions.values()):
                    predecessor_transition.end_places.add(end_place)
                    if not start_place.transitions:
                        predecessor_transition.end_places.remove(start_place)

    def has_guards(self):
        for transition in self.transitions.values():
            if (transition  is not None and
                not isinstance(transition.guard_function, AcceptAlwaysGuard)):
                return True
        return False

def _can_transition_be_pruned(t, source_places, sink_places):
    def place_has_self_loop(place):
        for transition in place.transitions:
            if place in transition.end_places:
                return True
        return False
    def start_place_allows_pruning(start_place, end_place):
        return (not place_has_self_loop(start_place) and (
                next(iter(t.start_places)) not in source_places) and
                len(start_place.transitions) == 1)
    def end_place_allows_pruning(start_place, end_place):
        return end_place not in sink_places or len(start_place.transitions) == 1
    return (not t.visible and
            len(t.start_places) == 1 and
            len(t.end_places) == 1 and
            start_place_allows_pruning(
                    next(iter(t.start_places)), next(iter(t.end_places))) and
            end_place_allows_pruning(
                    next(iter(t.start_places)), next(iter(t.end_places))) and
            isinstance(t.guard_function, AcceptAlwaysGuard))


def _introduce_new_source_place(net, old_source_places):
    new_source_place = net.add_place(Place.with_empty_label(
                ','.join(map(lambda p: p.id, old_source_places))))
    for old_source_place in old_source_places:
        t = net.add_transition(Transition(old_source_place.id,
                                          visible=False))
        net.add_connection(new_source_place, t, old_source_place)

def _introduce_new_sink_place(net, old_sink_places):
    new_sink_place = net.add_place(Place.with_empty_label(
                ','.join(map(lambda p: p.id, old_sink_places))))
    for old_sink_place in old_sink_places:
        t = net.add_transition(Transition(make_id_unique(old_sink_place.id,
                                                         net.transitions),
                                          visible=False))
        net.add_connection(old_sink_place, t, new_sink_place)

def make_id_unique(old_id: str, existing_ids):
    """
    takes an existing identifier and tests whether it exists in a set (or as a
    key in a dictionary). If yes, then "'" is appended to the identifier
    until it does not occur in the set anymore.
    """
    new_id = old_id
    while new_id in existing_ids:
        new_id += "'"
    return new_id