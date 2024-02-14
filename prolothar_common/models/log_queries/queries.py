# -*- coding: utf-8 -*-

"""common interface to all log queries"""

from prolothar_common.models.log_queries.query import Query
from prolothar_common.models.eventlog import Trace
from prolothar_common.collections import list_utils

from typing import Iterable, Callable, Any, Dict

class TraceContainsNoneOfTheseActivities(Query):
    def __init__(self, activities: Iterable[str]):
        self.__activities = activities
    def matches_trace(self, trace: Trace) -> bool:
        for activity in self.__activities:
            if trace.contains_activity(activity):
                return False
        return True

class TraceContainsActivity(Query):
    def __init__(self, activity: str):
        self.__activity = activity
    def matches_trace(self, trace: Trace) -> bool:
        return trace.contains_activity(self.__activity)

class TraceContainsActivityWith(Query):
    """like TraceContainsActivity but with an additional condition on the
    attributes of the matching event
    """
    def __init__(
            self, activity: str,
            attributes_matcher: Callable[[Dict[str,Any]], bool]):
        self.__activity = activity
        self.__attributes_matcher = attributes_matcher
    def matches_trace(self, trace: Trace) -> bool:
        for event in trace.events:
            if event.activity_name == self.__activity \
            and self.__attributes_matcher(event.attributes):
                return True
        return False

class TraceContainsAllOfTheseActivities(Query):
    def __init__(self, activities: Iterable[str]):
        self.__activities = activities
    def matches_trace(self, trace: Trace) -> bool:
        for activity in self.__activities:
            if not trace.contains_activity(activity):
                return False
        return True

class TraceContainsSubsequence(Query):
    """all activities must occur and if they occur, they must follow
    in the given sequence without other activities in between"""
    def __init__(self, activities: Iterable[str]):
        self.__activities = list(activities)
    def matches_trace(self, trace: Trace) -> bool:
        return list_utils.is_sublist_bm(trace.to_activity_list(),
                                        self.__activities)
