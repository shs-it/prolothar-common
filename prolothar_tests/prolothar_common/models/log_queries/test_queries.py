# -*- coding: utf-8 -*-

import unittest
from prolothar_common.models.eventlog import EventLog
from prolothar_common.models.log_queries.queries import Query
from prolothar_common.models.log_queries.queries import TraceContainsNoneOfTheseActivities
from prolothar_common.models.log_queries.queries import TraceContainsAllOfTheseActivities
from prolothar_common.models.log_queries.queries import TraceContainsActivity
from prolothar_common.models.log_queries.queries import TraceContainsSubsequence
from prolothar_common.models.log_queries.queries import TraceContainsActivityWith

class TestQueries(unittest.TestCase):

    def setUp(self):
        self.event_log = EventLog.create_from_simple_activity_log([
            [0,0,0,1,2,3,4,5,4,5,6],
            [0,0,0,1,2,3,4,5,4,5,6],
            [0,0,1,2,3,4,5,4,5,4,5,6],
            [0,0,0,1,3,2,4,5,4,5,6],
            [0,0,1,3,2,4,5,4,5,6],
            [0,7,8,6]
        ])
        self.event_log.traces[1].events[6].attributes['a'] = 1

    def __assertResultCount(self, expected_result_count: int, query: Query):
        self.assertEqual(expected_result_count,
                         query.execute(self.event_log).get_nr_of_traces())

    def test_trace_contains_none_of_these_activities(self):
        self.__assertResultCount(5, TraceContainsNoneOfTheseActivities([7,8]))
        self.__assertResultCount(1, TraceContainsNoneOfTheseActivities([1,5]))
        self.__assertResultCount(0, TraceContainsNoneOfTheseActivities([7,1,5]))

    def test_trace_contains_activity(self):
        self.__assertResultCount(1, TraceContainsActivity(7))
        self.__assertResultCount(5, TraceContainsActivity(1))
        self.__assertResultCount(0, TraceContainsActivity(9))

    def test_trace_contains_all_of_these_activities(self):
        self.__assertResultCount(1, TraceContainsAllOfTheseActivities([7,8]))
        self.__assertResultCount(0, TraceContainsAllOfTheseActivities([1,7]))
        self.__assertResultCount(5, TraceContainsAllOfTheseActivities([1,5]))
        self.__assertResultCount(6, TraceContainsAllOfTheseActivities([0,6]))

    def test_trace_contains_subsequence(self):
        self.__assertResultCount(3, TraceContainsSubsequence([1,2,3]))
        self.__assertResultCount(0, TraceContainsSubsequence([1,7]))
        self.__assertResultCount(0, TraceContainsSubsequence([0,6]))

    def test_or(self):
        query = (TraceContainsSubsequence([1,2,3]) |
                 TraceContainsAllOfTheseActivities([7,8]))
        self.__assertResultCount(4, query)

    def test_and(self):
        query = (TraceContainsSubsequence([1,2,3]) &
                 TraceContainsAllOfTheseActivities([7,8]))
        self.__assertResultCount(0, query)

    def test_invert(self):
        query = ~TraceContainsSubsequence([1,2,3])
        self.__assertResultCount(3, query)

    def test_trace_contains_activity_with(self):
        query = TraceContainsActivityWith(
                4, lambda attributes: attributes.get('a', 0) == 1)
        self.__assertResultCount(1, query)

if __name__ == '__main__':
    unittest.main()