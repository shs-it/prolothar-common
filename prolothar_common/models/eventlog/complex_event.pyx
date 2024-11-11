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

from prolothar_common.models.eventlog.event cimport Event

cdef class ComplexEvent(Event):
    """a complex event that exists of a list of subevents or children
    """
    def __init__(self, str activity_name, list children,
                 dict attributes = None, str transition_id = None):
        super().__init__(activity_name, attributes=attributes, transition_id=transition_id)
        if not children:
            raise ValueError('children must not be empty')
        self.children = children

    def __eq__(self, other):
        return (self.activity_name == other.activity_name and
                self.children == other.children and
                self.attributes == other.attributes)

    def __hash__(self):
        return hash(self.activity_name)