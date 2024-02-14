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

from prolothar_common.models.eventlog.event import Event
from typing import Hashable

class Trace:
    events: list[Event]
    attributes: dict

    def __init__(self, trace_id: Hashable, events: list[Event], attributes: dict[str, object] = None): ...
    def get_id(self) -> Hashable: ...
    def get_first_index_of_first_matching_activity(self, activity_set: set) -> int: ...
    def get_last_index_of_first_matching_activity(self, activity_set: set) -> int: ...
    def contains_activity(self, activity: object) -> bool: ...
    def to_dict(self) -> dict: ...
    def to_activity_list(self) -> list: ...