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

from prolothar_common.collections.list_utils import enumerate_reversed
from prolothar_common.models.eventlog.event cimport Event

cdef class Trace:
    def __init__(self, trace_id,
                 list events, dict attributes = None):
        """creates a new trace

        Args:
            trace_id:
                can be of any hashable type. should be a unique identifier in
                an event log
        """
        if not events:
            raise ValueError('events must not be empty')
        self.events = events
        self.attributes = attributes if attributes is not None else {}
        self.__id = trace_id

    def get_id(self):
        """returns the id attribute of this trace"""
        return self.__id

    def set_id(self, new_id):
        self.__id = new_id

    cpdef int get_first_index_of_first_matching_activity(self, set activity_set):
        """returns the index in the list of events for the first event with an
        activity contained in activity_set. return -1 if there is no matching
        event"""
        for i,event in enumerate(self.events):
            if event.activity_name in activity_set:
                return i
        return -1

    cpdef int get_last_index_of_first_matching_activity(self, set activity_set):
        """returns the index in the list of events for the last event with an
        activity contained in activity_set. return -1 if there is no matching
        event"""
        for i,event in enumerate_reversed(self.events):
            if event.activity_name in activity_set:
                return i
        return -1

    cpdef bint contains_activity(self, activity):
        """tests whether one of the events in this trace has a given activity"""
        for event in self.events:
            if event.activity_name == activity:
                return True
        return False

    def __repr__(self):
        return 'Trace(id=%s)%s' % (
                str(self.__id),
                str([e.activity_name for e in self.events]))

    def __eq__(self, other):
        return self.events == other.events and self.attributes == other.attributes

    def __hash__(self):
        return hash(self.__id)

    def __len__(self):
        return len(self.events)

    cpdef list to_activity_list(self):
        return [e.activity_name for e in self.events]

    cpdef dict to_dict(self):
        """converts this trace to a dictionary, e.g. helpful for json conversion"""
        return {
            'id': self.__id,
            'attributes': self.attributes,
            'events': [event.to_dict() for event in self.events]
        }

    @staticmethod
    def create_from_dict(d):
        """
        parses a dictionary. the format must be the same as in Trace.to_dict
        """
        events = []
        for event_dict in d['events']:
            events.append(Event.create_from_dict(event_dict))
        return Trace(d['id'], events, attributes=d['attributes'])
