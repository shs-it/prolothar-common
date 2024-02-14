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

from typing import List, Dict, Union
from prolothar_common.models.data_petri_net import DataPetriNet, Transition, Place
from prolothar_common.models.data_petri_net import make_id_unique

HighLevelActivityMap = Dict[Transition,str]

class ActivityPattern:
    """a activity pattern as defined in "Guided Process Discovery - A pattern
    based Approach"
    """
    def __init__(self, data_petri_net: DataPetriNet,
                 high_level_activity_map: Union[str, HighLevelActivityMap]):
        """creates a new activity pattern

        Args:
            - data_petri_net: the actual pattern expressed by a data petri net
            - high_level_activity_map a dictionary that assigns a high level
            activity name to a given transition of the data petri net. if all
            transitions should be mapped to the same high level activity name,
            a string can be passed to this constructor.

        Raises:
            - ValueError if the high_level_activity_map does not assign a
            high level activity name to all transitions in the data petri net
        """
        self.data_petri_net = data_petri_net
        if not self.data_petri_net.is_workflow_net():
            self.data_petri_net = self.data_petri_net.transform_to_workflow_net()
        if isinstance(high_level_activity_map, str):
            self.high_level_activity_map = {}
            for transition in data_petri_net.transitions.values():
                self.high_level_activity_map[transition] = high_level_activity_map
        elif isinstance(high_level_activity_map, dict):
            self.high_level_activity_map = high_level_activity_map

            for transition in data_petri_net.transitions.values():
                if (transition.visible
                    and transition not in self.high_level_activity_map):
                    raise ValueError(('visible transition %r has no high level '
                                      'activity mapping') % transition.id)
        else:
            raise TypeError('high_level_activity_map should be str or dict')

    def copy(self):
        return ActivityPattern(self.data_petri_net.copy(),
                               dict(self.high_level_activity_map))

    def get_standard_initial_marking(self):
        initial_marking = self.get_all_zeros_marking()
        start_place = self.data_petri_net.get_source_sink_places()[0].pop()
        initial_marking[start_place.id] = 1
        return initial_marking

    def get_standard_final_marking(self):
        final_marking = self.get_all_zeros_marking()
        end_place = self.data_petri_net.get_source_sink_places()[1].pop()
        final_marking[end_place.id] = 1
        return final_marking

    def get_all_zeros_marking(self):
        marking = {}
        for place_id in self.data_petri_net.places.keys():
            marking[place_id] = 0
        return marking

    def prune(self):
        self.data_petri_net.prune()
        pruned_transitions = []
        for transition in self.high_level_activity_map.keys():
            if transition.id not in self.data_petri_net.transitions:
                pruned_transitions.append(transition)
        for transition in pruned_transitions:
            self.high_level_activity_map.pop(transition)

def sequence(ap_1: ActivityPattern, ap_2: ActivityPattern) -> ActivityPattern:
    _, end_place_ap_1, start_place_ap_2, _, high_level_activity_map,\
        data_petri_net = _prepare_composition(ap_1, ap_2)

    sequence_transition = data_petri_net.add_transition(Transition(
            end_place_ap_1.id + ',' + start_place_ap_2.id,
            visible=False))
    data_petri_net.add_connection(end_place_ap_1,
                                  sequence_transition,
                                  start_place_ap_2)

    return ActivityPattern(data_petri_net, high_level_activity_map)

def choice(ap_1: ActivityPattern, ap_2: ActivityPattern) -> ActivityPattern:
    start_place_ap_1, end_place_ap_1, start_place_ap_2, end_place_ap_2,\
    high_level_activity_map, data_petri_net = _prepare_composition(ap_1, ap_2)

    new_start_place = data_petri_net.add_place(Place.with_empty_label(
        start_place_ap_1.id + ',' + start_place_ap_2.id))

    transition_to_ap_1 = data_petri_net.add_transition(Transition(
            make_id_unique(start_place_ap_1.id, data_petri_net.transitions),
            visible=False))
    transition_to_ap_2 = data_petri_net.add_transition(Transition(
            make_id_unique(start_place_ap_2.id, data_petri_net.transitions),
            visible=False))

    data_petri_net.add_connection(new_start_place, transition_to_ap_1, start_place_ap_1)
    data_petri_net.add_connection(new_start_place, transition_to_ap_2, start_place_ap_2)

    #there are two end places now => transform to workflow net with one end
    data_petri_net = data_petri_net.transform_to_workflow_net()

    return ActivityPattern(data_petri_net, high_level_activity_map)

def choice_list(choices: List[ActivityPattern]) -> ActivityPattern:
    """this method is an alternative to "choice" method if many different
    choices have to be combined. Applying the choice method subsequently on
    pairs of activitiy patterns would lead to a large number of invisible
    transitions and therefore cause performance issues during alignment
    computation
    """
    #store a copy of choices such that we can make transitions unique without
    #sideffects for the caller of the method
    copy_of_choices = [choice.copy() for choice in choices]

    temp_high_level_activity_map = {}

    #first we have to make the ids of the transitions unique such that we can
    #later join the petri nets
    transition_ids = set()
    for choice in copy_of_choices:
        transition_id_mappings = {}
        for transition_id, transition in choice.data_petri_net.transitions.items():
            while transition_id in transition_ids:
                transition_id = transition_id + "'"
            transition_ids.add(transition_id)
            if transition in choice.high_level_activity_map:
                temp_high_level_activity_map[transition_id] = choice.high_level_activity_map[transition]
            transition.id = transition_id
        for old_transition_id, new_transition_id in transition_id_mappings.items():
            if old_transition_id != new_transition_id:
                t = choice.data_petri_net.transitions.pop(old_transition_id)
                choice.data_petri_net.transitions[new_transition_id] = t

    #the places also must be unique
    place_ids = set()
    for choice in copy_of_choices:
        place_id_mappings = {}
        for place_id, place in choice.data_petri_net.places.items():
            while place_id in place_ids:
                place_id = place_id + "'"
            place_ids.add(place_id)
            place_id_mappings[place.id] = place_id
            place.id = place_id
        for old_place_id, new_place_id in place_id_mappings.items():
            if old_place_id != new_place_id:
                place = choice.data_petri_net.places.pop(old_place_id)
                choice.data_petri_net.places[new_place_id] = place

    #we have to collect the old start and end places
    old_start_places = []
    old_end_places = []
    for choice in copy_of_choices:
        sources, sinks = choice.data_petri_net.get_source_sink_places()
        #again, we know that each activity pattern is a workflow net with
        #exactly one source and one sink (constructor requirement)
        old_start_places.append(sources.pop())
        old_end_places.append(sinks.pop())

    #the new petri net will have all transitions and places of the activity patterns
    data_petri_net = DataPetriNet()
    for choice in copy_of_choices:
        for transition in choice.data_petri_net.transitions.values():
            data_petri_net.add_transition(transition)
        for place in choice.data_petri_net.places.values():
            data_petri_net.add_place(place)

    #we add the new start place, which will have an invisible
    #transition for each of the old start places
    new_start_place = data_petri_net.add_place(Place.with_empty_label(
        ','.join(map(lambda p: p.id, old_start_places))))
    for old_start_place in old_start_places:
        transition = data_petri_net.add_transition(Transition(
                new_start_place.id + ',' + old_start_place.id, visible=False))
        data_petri_net.add_connection(new_start_place, transition, old_start_place)

    #we add the new end place, which will have an invisible
    #transition for each of the old end places
    new_end_place = data_petri_net.add_place(Place.with_empty_label(
        ','.join(map(lambda p: p.id, old_end_places))))
    for old_end_place in old_end_places:
        transition = data_petri_net.add_transition(Transition(
                old_end_place.id + ',' + new_end_place.id, visible=False))
        data_petri_net.add_connection(old_end_place, transition, new_end_place)

    #we were only able to save the transition id in the high_level_activity_map,
    #but we expect the transition object with all its attributes
    high_level_activity_map = {}
    for transition_id, activity_name in temp_high_level_activity_map.items():
        high_level_activity_map[data_petri_net.transitions[transition_id]] = activity_name

    return ActivityPattern(data_petri_net, high_level_activity_map)

def parallel(ap_1: ActivityPattern, ap_2: ActivityPattern) -> ActivityPattern:
    start_place_ap_1, end_place_ap_1, start_place_ap_2, end_place_ap_2,\
    high_level_activity_map, data_petri_net = _prepare_composition(ap_1, ap_2)

    new_start_place = data_petri_net.add_place(Place.with_empty_label(
        start_place_ap_1.id + ',' + start_place_ap_2.id))

    parallel_transition = data_petri_net.add_transition(Transition(
            start_place_ap_1.id, visible=False))

    data_petri_net.add_connection(new_start_place, parallel_transition, start_place_ap_1)
    data_petri_net.add_connection(new_start_place, parallel_transition, start_place_ap_2)

    #there are two end places now => add common end transition and place
    new_end_place = data_petri_net.add_place(Place.with_empty_label(
            end_place_ap_1.id + ',' + end_place_ap_2.id))
    transition_to_new_end_place = data_petri_net.add_transition(Transition(
            end_place_ap_1.id + ',' + end_place_ap_2.id, visible=False))
    data_petri_net.add_connection(end_place_ap_1, transition_to_new_end_place, new_end_place)
    data_petri_net.add_connection(end_place_ap_2, transition_to_new_end_place, new_end_place)

    return ActivityPattern(data_petri_net, high_level_activity_map)

def interleaving(ap_1: ActivityPattern, ap_2: ActivityPattern) -> ActivityPattern:
    start_place_ap_1, end_place_ap_1, start_place_ap_2, end_place_ap_2,\
    high_level_activity_map, data_petri_net = _prepare_composition(ap_1, ap_2)

    new_start_place = data_petri_net.add_place(Place.with_empty_label(
        start_place_ap_1.id + ',' + start_place_ap_2.id))

    start_transition = data_petri_net.add_transition(Transition(
            start_place_ap_1.id + ',' + start_place_ap_2.id, visible=False))

    interleaving_place = data_petri_net.add_place(Place.with_empty_label(
        start_place_ap_1.id + ',' + start_place_ap_2.id + ',px'))

    new_end_place = data_petri_net.add_place(Place.with_empty_label(
            end_place_ap_1.id + ',' + end_place_ap_2.id))
    end_transition = data_petri_net.add_transition(Transition(
            end_place_ap_1.id + ',' + end_place_ap_2.id, visible=False))

    new_start_place_ap_1 = data_petri_net.add_place(Place.with_empty_label(
        start_place_ap_1.id + "_"))
    new_start_transition_ap_1 = data_petri_net.add_transition(Transition(
            start_place_ap_1.id + "_", visible=False))
    new_start_place_ap_2 = data_petri_net.add_place(Place.with_empty_label(
        start_place_ap_2.id + "_"))
    new_start_transition_ap_2 = data_petri_net.add_transition(Transition(
            start_place_ap_2.id + "_", visible=False))

    new_end_place_ap_1 = data_petri_net.add_place(Place.with_empty_label(
        end_place_ap_1.id + "_"))
    new_end_transition_ap_1 = data_petri_net.add_transition(Transition(
            end_place_ap_1.id + "_", visible=False))
    new_end_place_ap_2 = data_petri_net.add_place(Place.with_empty_label(
        end_place_ap_2.id + "_"))
    new_end_transition_ap_2 = data_petri_net.add_transition(Transition(
            end_place_ap_2.id + "_", visible=False))

    data_petri_net.add_connection(new_start_place, start_transition, new_start_place_ap_1)
    data_petri_net.add_connection(new_start_place, start_transition, new_start_place_ap_2)
    data_petri_net.add_connection(new_start_place, start_transition, interleaving_place)

    data_petri_net.add_connection(new_start_place_ap_1, new_start_transition_ap_1, start_place_ap_1)
    data_petri_net.add_connection(new_start_place_ap_1, new_start_transition_ap_1, interleaving_place)

    data_petri_net.add_connection(new_start_place_ap_2, new_start_transition_ap_2, start_place_ap_2)
    data_petri_net.add_connection(new_start_place_ap_2, new_start_transition_ap_2, interleaving_place)

    data_petri_net.add_connection(end_place_ap_1, new_end_transition_ap_1, new_end_place_ap_1)
    data_petri_net.add_connection(end_place_ap_1, new_end_transition_ap_1, interleaving_place)

    data_petri_net.add_connection(end_place_ap_2, new_end_transition_ap_2, new_end_place_ap_2)
    data_petri_net.add_connection(end_place_ap_2, new_end_transition_ap_2, interleaving_place)

    data_petri_net.add_connection(new_end_place_ap_1, end_transition, new_end_place)
    data_petri_net.add_connection(new_end_place_ap_2, end_transition, new_end_place)

    data_petri_net.add_connection(interleaving_place, end_transition, new_end_place)
    data_petri_net.add_connection(interleaving_place, new_start_transition_ap_1, start_place_ap_1)
    data_petri_net.add_connection(interleaving_place, new_start_transition_ap_2, start_place_ap_2)

    return ActivityPattern(data_petri_net, high_level_activity_map)

def unbounded_repetition(ap: ActivityPattern) -> ActivityPattern:
    high_level_activity_map = dict(ap.high_level_activity_map)
    data_petri_net = ap.data_petri_net.copy()

    start_places, end_places = data_petri_net.get_source_sink_places()
    #the acitivity pattern consists of a workflow net (constructor requirement!)
    #=> we know there is exactly one start and end place
    start_place = start_places.pop()
    end_place = end_places.pop()

    new_start_place = data_petri_net.add_place(Place.with_empty_label(
        make_id_unique(start_place.id, data_petri_net.places)))
    new_end_place = data_petri_net.add_place(Place.with_empty_label(
            make_id_unique(end_place.id, data_petri_net.places)))

    new_start_transition = data_petri_net.add_transition(Transition(
        make_id_unique(start_place.id, data_petri_net.transitions),
        visible=False))
    new_end_transition = data_petri_net.add_transition(Transition(
        make_id_unique(end_place.id, data_petri_net.transitions),
        visible=False))
    repeat_transition = data_petri_net.add_transition(Transition(
        make_id_unique(start_place.id + ',' + end_place.id,
                       data_petri_net.transitions),
        visible=False))

    data_petri_net.add_connection(new_start_place, new_start_transition, start_place)
    data_petri_net.add_connection(end_place, new_end_transition, new_end_place)
    data_petri_net.add_connection(end_place, repeat_transition, start_place)

    return ActivityPattern(data_petri_net, high_level_activity_map)

def _prepare_composition(ap_1: ActivityPattern, ap_2: ActivityPattern):
    ap_1_copy = ap_1.data_petri_net.copy()
    ap_2_copy = ap_2.data_petri_net.copy()
    start_places_ap_1, end_places_ap_1 = ap_1_copy.get_source_sink_places()
    start_places_ap_2, end_places_ap_2 = ap_2_copy.get_source_sink_places()
    high_level_activity_map = dict(ap_1.high_level_activity_map)

    for place in ap_2_copy.places.values():
        place.id = make_id_unique(place.id, ap_1_copy.places)
        ap_1_copy.add_place(place)
    for transition in ap_2_copy.transitions.values():
        if transition.visible:
            high_level_activity_name = ap_2.high_level_activity_map[transition]
        transition.id = make_id_unique(transition.id, ap_1_copy.transitions)
        ap_1_copy.add_transition(transition)
        if transition.visible:
            high_level_activity_map[transition] = high_level_activity_name

    #both acitivity patterns consist of workflow nets (constructor requirement!)
    #=> we know there is one start and end place in each of the patterns
    start_place_ap_1 = start_places_ap_1.pop()
    end_place_ap_1 = end_places_ap_1.pop()
    start_place_ap_2 = start_places_ap_2.pop()
    end_place_ap_2 = end_places_ap_2.pop()

    return start_place_ap_1, end_place_ap_1,\
           start_place_ap_2, end_place_ap_2,\
           high_level_activity_map, ap_1_copy

