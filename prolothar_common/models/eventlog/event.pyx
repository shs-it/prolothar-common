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

from frozendict import frozendict

cdef class Event():
    def __init__(self, str activity_name, dict attributes = None,
                 str transition_id = None):
        self.activity_name = activity_name
        self.attributes = attributes if attributes is not None else {}
        self.transition_id = transition_id

    def __repr__(self):
        return '<Event, Activity: %s, transition: %s, attributes=%s>' % (
                self.activity_name, self.transition_id, self.attributes)

    def __eq__(self, other):
        return ((self.activity_name is None and other.activity_name is None or
                self.activity_name == other.activity_name) and
                self.transition_id == other.transition_id and
                self.attributes == other.attributes)

    def __hash__(self):
        return hash((self.activity_name, frozendict(self.attributes)))

    cpdef dict to_dict(self):
        """converts this event to a dictionary, e.g. helpful for json conversion"""
        return {
            'activity_name': self.activity_name,
            'attributes': self.attributes
        }

    @staticmethod
    def create_from_dict(d: dict) -> Event:
        """
        parses a dictionary. the format must be the same as in Event.to_dict
        """
        return Event(d['activity_name'], attributes=d['attributes'])