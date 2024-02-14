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

"""
utils for compatibility to the pm4py library
"""

from typing import Tuple

from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils as utils
from pm4py.objects.petri_net.obj import Marking
from pm4py.objects.log.obj import EventLog as Pm4pyEventLog
from pm4py.objects.log.obj import Trace as Pm4PyTrace
from pm4py.objects.log.obj import Event as Pm4PyEvent

from prolothar_common.models.data_petri_net import DataPetriNet, Transition, Place
from prolothar_common.models.eventlog import EventLog, Trace, Event

CONCEPT_NAME = 'concept:name'

def convert_data_petri_net_to_pm4py(
        data_petri_net: DataPetriNet) -> Tuple[PetriNet, Marking, Marking]:
    """converts a DataPetriNet model with code from this project to a PetriNet
    from pm4py
    Args:
        data_petri_net:
            the DataPetriNet to convert
    """
    pm4py_net = PetriNet()

    places_dict = _add_places_to_pm4py_net(data_petri_net, pm4py_net)

    _add_transitions_to_pm4py_net(data_petri_net, pm4py_net, places_dict)

    initial_marking, final_marking = _create_markings(data_petri_net, places_dict)

    return pm4py_net, initial_marking, final_marking

def _add_places_to_pm4py_net(data_petri_net: DataPetriNet, pm4py_net: PetriNet):
    places_dict = {}
    for place in data_petri_net.places.values():
        pm4py_place = PetriNet.Place('p' + place.id)
        pm4py_net.places.add(pm4py_place)
        places_dict[place.id] = pm4py_place
    return places_dict

def _add_transitions_to_pm4py_net(data_petri_net: DataPetriNet,
                                  pm4py_net: PetriNet, places_dict):
    for transition in data_petri_net.transitions.values():
        _add_transition_to_pm4py_net(transition, pm4py_net, places_dict)

def _add_transition_to_pm4py_net(transition: Transition, pm4py_net: PetriNet,
                                 places_dict):
    added_arcs = set()
    transition_label = None
    if transition.visible:
        transition_label = transition.label
    pm4py_transition = PetriNet.Transition(
            't' + transition.id, transition_label)
    pm4py_net.transitions.add(pm4py_transition)
    for start_place in transition.start_places:
        for end_place in transition.end_places:
            if (start_place.id, transition.id) not in added_arcs:
                added_arcs.add((start_place.id, transition.id))
                utils.add_arc_from_to(places_dict[start_place.id],
                                      pm4py_transition,
                                      pm4py_net)
            if (transition.id, end_place.id) not in added_arcs:
                added_arcs.add((transition.id, end_place.id))
                utils.add_arc_from_to(pm4py_transition,
                                      places_dict[end_place.id],
                                      pm4py_net)

def _create_markings(data_petri_net: DataPetriNet,
                     places_dict):
    initial_marking = Marking()
    final_marking = Marking()
    sources, sinks = data_petri_net.get_source_sink_places()
    for source in sources:
        initial_marking[places_dict[source.id]] = 1
    for sink in sinks:
        final_marking[places_dict[sink.id]] = 1
    return initial_marking, final_marking

def convert_pm4py_to_data_petri_net(
        pm4py_net: PetriNet, initial_marking: Marking) -> DataPetriNet:
    """converts a PetriNet from the pm4py library to a DataPetriNet of this
    project
    """
    petri_net = DataPetriNet()
    for place in pm4py_net.places:
        petri_net.add_place(Place.with_empty_label(
                place.name, nr_of_tokens=initial_marking[place]))
    for transition in pm4py_net.transitions:
        petri_net.add_transition(Transition(
                transition.name, transition.label,
                visible=transition.label is not None))
    for arc in pm4py_net.arcs:
        if isinstance(arc.source, PetriNet.Place):
            transition = petri_net.transitions[arc.target.name]
            place = petri_net.places[arc.source.name]
            place.add_transition(transition)
            transition.add_start_place(place)
        else:
            transition = petri_net.transitions[arc.source.name]
            place = petri_net.places[arc.target.name]
            transition.add_end_place(place)
    return petri_net

def convert_eventlog_to_pm4py(log: EventLog) -> Pm4pyEventLog:
    """converts an EventLog model with code from this project to a EventLog
    from pm4py"""
    return Pm4pyEventLog([convert_trace_to_pm4py(t) for t in log.traces])

def convert_trace_to_pm4py(trace: Trace):
    """converts a Trace model with code from this project to a Trace
    from pm4py"""
    def _convert_event_to_pm4py(event: Event):
        return Pm4PyEvent({CONCEPT_NAME: event.activity_name})
    attributes = {CONCEPT_NAME: trace.get_id()}
    for key, value in trace.attributes.items():
        attributes[key] = value
    return Pm4PyTrace([_convert_event_to_pm4py(e) for e in trace.events],
                      attributes=attributes)

def convert_pm4py_log(pm4py_log: Pm4pyEventLog,
                      activity_attribute=CONCEPT_NAME,
                      trace_id_attribute=CONCEPT_NAME) -> EventLog:
    """converts an event log model from pm4py to an event log model of this
    project"""
    log = EventLog()
    for trace in pm4py_log:
        log.add_trace(Trace(trace.attributes[trace_id_attribute],
                            [Event(e[activity_attribute], attributes=dict(e))
                             for e in trace], attributes=trace.attributes))
    return log
