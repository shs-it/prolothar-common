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

from abc import ABC, abstractmethod

from prolothar_common.models.eventlog import EventLog, Trace

class Query(ABC):
    """abstract query on a EventLog that returns Traces matching the query"""

    def execute(self, log: EventLog) -> EventLog:
        """returns a EventLog with traces matching these query. The traces
        are not copied from the original log, so any changes made on these
        traces will also be observed in the original log. This can be prevented
        by copying the log after the query.
        """
        filtered_log = EventLog()
        filtered_log.traces = [trace for trace in log.traces
                               if self.matches_trace(trace)]
        return filtered_log

    @abstractmethod
    def matches_trace(self, trace: Trace) -> bool:
        """returns True iff the given trace matches the query criterion"""
        pass

    def __and__(self, other: 'Query'):
        return And(self, other)

    def __or__(self, other: 'Query'):
        return Or(self, other)

    def __invert__(self):
        return Invert(self)

class And(Query):
    def __init__(self, left: Query, right: Query):
        self.__left = left
        self.__right = right
    def matches_trace(self, trace: Trace) -> bool:
        return (self.__left.matches_trace(trace)
                and self.__right.matches_trace(trace))

class Or(Query):
    """inclusive OR operator"""
    def __init__(self, left: Query, right: Query):
        self.__left = left
        self.__right = right
    def matches_trace(self, trace: Trace) -> bool:
        return (self.__left.matches_trace(trace)
                or self.__right.matches_trace(trace))

class Invert(Query):
    """Inverts a query"""
    def __init__(self, query: Query):
        self.__query = query
    def matches_trace(self, trace: Trace) -> bool:
        return not self.__query.matches_trace(trace)
