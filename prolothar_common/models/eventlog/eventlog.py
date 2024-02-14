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

from typing import List
from typing import Dict
from typing import Set
from typing import Tuple
from typing import Generator
from typing import Iterator
from random import Random
import io
from collections import Counter
from more_itertools import pairwise
import pandas as pd

from sklearn.model_selection import KFold
from prolothar_common.models.eventlog.trace import Trace
from prolothar_common.models.eventlog.event import Event

ActivityLog = List[List[str]]

class EventLog():
    def __init__(self):
        self.traces = []

    def add_trace(self, trace: Trace):
        self.traces.append(trace)

    def add_traces(self, trace_list: List[Trace]):
        self.traces.extend(trace_list)

    def get_nr_of_traces(self):
        return len(self.traces)

    def __len__(self):
        return len(self.traces)

    def __iter__(self) -> Iterator[Trace]:
        return iter(self.traces)

    def __repr__(self):
        writer = io.StringIO()
        writer.write('==========\n')
        writer.write('EventLog with %r traces\n' % self.get_nr_of_traces())
        writer.write('----------\n')
        for trace in self.traces:
            writer.write(repr(trace) + '\n')
        writer.write('==========\n')
        return writer.getvalue()

    def __eq__(self, other):
        return Counter(self.traces) == Counter(other.traces)

    def to_simple_activity_log(self) -> ActivityLog:
        activity_log = []
        for trace in self.traces:
            activity_log.append([
                event.activity_name for event in trace.events
            ])
        return activity_log

    def write_to_csv(self, csv_writer, trace_id_column='CaseId',
                     activity_column='Activity', separator=';'):
        """writes the content of this log into csv format
        Args:
            csv_writer:
                any object that offers a "write"-method
            trace_id_column:
                name will be printed in the header line. the trace id itself will be
                an increasing integer
            activity_column:
                name will be printed in the header line.
        """
        csv_writer.write(trace_id_column)
        csv_writer.write(separator)
        csv_writer.write(activity_column)
        csv_writer.write('\n')
        for i,trace in enumerate(self.traces):
            for event in trace.events:
                csv_writer.write(str(i))
                csv_writer.write(separator)
                csv_writer.write(event.activity_name)
                csv_writer.write('\n')

    def to_dict(self) -> Dict:
        """
        converts this eventlog to a dictionary. example use case: json export

        Returns
        -------
        Dict
            event log in dictionary form.
        """
        return {'traces': [trace.to_dict() for trace in self.traces]}

    def copy(self) -> 'EventLog':
        copy = EventLog()
        for trace in self.traces:
            copy.add_trace(Trace(trace.get_id(), list(trace.events),
                                 dict(trace.attributes)))
        return copy

    def compute_activity_set(self) -> Set[str]:
        """returns a set of all activity names. in case of complex events,
        only the activity name of the complex event is returned, not the
        activities of the children's events
        """
        activity_set = set()
        for trace in self.traces:
            for event in trace.events:
                activity_set.add(event.activity_name)
        return activity_set

    def derive_event_duration_by_end_date(
            self, attribute_start_date: str, attribute_end_date: str,
            attribute_duration: str):
        for trace in self.traces:
            #first event is special: start date = end date => duration 0
            if attribute_start_date not in trace.events[0].attributes:
                trace.events[0].attributes[attribute_start_date] = \
                    trace.events[0].attributes[attribute_end_date]
            trace.events[0].attributes[attribute_duration] = \
                    trace.events[0].attributes[attribute_end_date] - \
                    trace.events[0].attributes[attribute_start_date]
            if trace.events[0].attributes[attribute_duration].total_seconds() < 0:
                raise ValueError('events must be sorted!')
            for last_event, next_event in pairwise(trace.events):
                if attribute_start_date not in next_event.attributes:
                    next_event.attributes[attribute_start_date] = \
                        last_event.attributes[attribute_end_date]
                next_event.attributes[attribute_duration] = \
                    next_event.attributes[attribute_end_date] - \
                    next_event.attributes[attribute_start_date]
                if next_event.attributes[attribute_duration].total_seconds() < 0:
                    raise ValueError('events must be sorted!')

    def join_sucessive_events_with_same_activity(
            self, startdate_attribute=None, enddate_attribute=None,
            duration_attribute=None, raise_error_for_attributes=True,
            activity_blacklist: Set=frozenset()):
        """
        joins sucessive events with the same activity,
        e.g. [A, A, A, B, A] is reduced to [A, B, A]

        Parameters
        ----------
        startdate_attribute : [type], optional
            can be used to set the startdate attribute correctly while
            merging events, by default None
        enddate_attribute : [type], optional
            can be used to set the enddate attribute correctly while
            merging events, by default None
        duration_attribute : [type], optional
            can be used to set the duration attribute correctly while
            merging events, by default None
        raise_error_for_attributes : bool, optional
            If True raises a ValueError if attributes of merged events do not
            agree, by default True
        activity_blacklist : Set, optional
            can be used to protect certain events from being merged, by default set()
        """
        for trace in self.traces:
            event_list = [trace.events[0]]
            for event in trace.events[1:]:
                if event_list[-1].activity_name == event.activity_name \
                and event.activity_name not in activity_blacklist:
                    _join_events(
                        event_list[-1], event,
                        startdate_attribute=startdate_attribute,
                        enddate_attribute=enddate_attribute,
                        duration_attribute=duration_attribute,
                        raise_error_for_attributes=raise_error_for_attributes)
                else:
                    event_list.append(event)
            trace.events = event_list

    def count_nr_of_events(self) -> int:
        nr_of_events = 0
        for trace in self.traces:
            nr_of_events += len(trace)
        return nr_of_events

    def compute_activity_supports(self) -> Dict[str, int]:
        support_counter = Counter()
        for trace in self.traces:
            for event in trace.events:
                support_counter[event.activity_name] += 1
        return support_counter

    def compute_set_of_start_activities(self) -> Set[str]:
        """returns a set with activities which occur at the beginning of a trace
        """
        start_activities = set()
        for trace in self.traces:
            start_activities.add(trace.events[0].activity_name)
        return start_activities

    def compute_set_of_end_activities(self) -> Set[str]:
        """returns a set with activities which occur at the end of a trace
        """
        end_activities = set()
        for trace in self.traces:
            end_activities.add(trace.events[-1].activity_name)
        return end_activities

    def to_pandas_df(self, append_trace_id_column: bool = False) -> pd.DataFrame:
        """creats a pandas dataframe of this eventlog. every line is one event.
        Args:
            - append_trace_id_column:
                default is False. If True, then a column 'trace' is added to
                the dataframe. This is only necessary if the attributes of a
                traces do not contain the trace id
        """
        rows = []
        for trace in self.traces:
            for event in trace.events:
                row = []
                if append_trace_id_column:
                    row.append(trace.get_id())
                for _,trace_attribute in sorted(trace.attributes.items()):
                    row.append(trace_attribute)
                row.append(event.activity_name)
                for _,event_attribute in sorted(event.attributes.items()):
                    row.append(event_attribute)
                rows.append(row)

        columns = []
        if append_trace_id_column:
            columns.append('trace')
        columns.extend(sorted(self.traces[0].attributes.keys()))
        columns.append('Activity')
        columns.extend(sorted(self.traces[0].events[0].attributes.keys()))
        return pd.DataFrame(rows, columns=columns)

    def cut_traces(self, start_activities: Set[str] = None,
                   end_activities: Set[str] = None):
        if start_activities is not None:
            if not isinstance(start_activities, set):
                start_activities = set(start_activities)
            for trace in self.traces:
                trace.events = trace.events[
                        trace.get_first_index_of_first_matching_activity(
                                start_activities):]
        if end_activities is not None:
            if not isinstance(end_activities, set):
                end_activities = set(end_activities)
            for trace in self.traces:
                trace.events = trace.events[:
                        trace.get_last_index_of_first_matching_activity(
                                end_activities)+1]

        self.traces = list(filter(lambda t: len(t) > 0, self.traces))

    def filter_activities(self, allowed_activities: Set[str],
                          remove_empty_traces: bool = True):
        """removes all activities which are not contained in a given set and
        removes all empty traces if parameter "remove_empty_traces" is not set
        to False.
        """
        for trace in self.traces:
            trace.events = list(filter(
                    lambda e: e.activity_name in allowed_activities,
                    trace.events))
        if remove_empty_traces:
            self.traces = [t for t in self.traces if len(t) > 0]

    def count_follows_directly_or_indirectly(self) -> Dict[Tuple[str,str],int]:
        """counts how often activities are followed directly or indirectly

        Returns:
            a dictionary with keys being activity tuples (A,B) and values being
            the number of times A,?,B occurs in the log, with ? being any
            sequence of activities without A.
        """
        counter = Counter()

        for trace in self.traces:
            seen_activities = set()
            for event in trace.events:
                for activity in seen_activities:
                    counter[(activity,event.activity_name)] += 1
                seen_activities.add(event.activity_name)

        activity_set = self.compute_activity_set()
        for a in activity_set:
            for b in activity_set:
                if (a,b) not in counter:
                    counter[(a,b)] = 0

        return dict(counter)

    def add_start_activity_to_every_trace(self, activity: str):
        """adds the given activity to all traces as a new start activity"""
        for trace in self.traces:
            trace.events.insert(0, Event(activity))

    def add_end_activity_to_every_trace(self, activity: str):
        """adds the given activity to all traces as a new end/last activity"""
        for trace in self.traces:
            trace.events.append(Event(activity))

    def keep_first_occurence_of_activity_only(self):
        """modifies the log such that in each trace activities only accur once,
        i.e. ABCDEAJD is reduced to ABCDEJ
        """
        for trace in self.traces:
            activity_set = set()
            filtered_event_list = []
            for event in trace.events:
                if event.activity_name not in activity_set:
                    activity_set.add(event.activity_name)
                    filtered_event_list.append(event)
            trace.events = filtered_event_list

    def train_test_split(
            self, testset_proportion: float,
            random: Random = None) -> Tuple['EventLog', 'EventLog']:
        """
        splits this log into a train and test log

        Parameters
        ----------
        testset_proportion : float
            minimal proportion of the testset
        random : Random (optional)
            random generator used to determine which trace goes to which set.
            default is None, i.e. a new instance of Random

        Returns
        -------
        a tuple with train_log, test_log

        Raises
        ------
        ValueError
            if test_proportion not in interval [0.0, 1.0]
        """
        if not 0.0 <= testset_proportion <= 1.0:
            raise ValueError(('testset_proportion must be in [0.0,1.0] '
                              'but was %r') % testset_proportion)
        if random is None:
            random = Random()

        train_log = EventLog()
        test_log = EventLog()

        train_log.traces = list(self.traces)
        random.shuffle(train_log.traces)

        split_index = int(len(train_log) * (1 - testset_proportion))
        test_log.traces = train_log.traces[split_index:]
        train_log.traces = train_log.traces[:split_index]

        return train_log, test_log

    def k_folds(self, k: int) -> Generator[Tuple['EventLog','EventLog'],
                                           None, None]:
        """
        generates k-folds for crossvalidation

        Parameters
        ----------
        k : int
            number of splits. must not be < 2.

        Raises
        ------
        ValueError
            if k < 2

        Yields
        ------
        train_log : EventLog
            the train part of one split.
        test_log : EventLog
            the test part of one split.
        """

        if k < 2:
            raise ValueError("k must not be < 2 but was %d" % k)
        return self.__k_folds(k)

    def __k_folds(self, k :int) -> Generator[Tuple['EventLog','EventLog'],
                                               None, None]:
        for train_index, test_index in KFold(n_splits=k).split(self.traces):
            train_log = EventLog()
            train_log.traces = [self.traces[i] for i in train_index]
            test_log = EventLog()
            test_log.traces = [self.traces[i] for i in test_index]
            yield train_log, test_log

    @staticmethod
    def create_from_simple_activity_log(activity_log: ActivityLog):
        event_log = EventLog()
        for i,trace in enumerate(activity_log):
            event_log.add_trace(Trace(i, [
                Event(activity) for activity in trace
            ]))
        return event_log

    @staticmethod
    def create_from_pandas_df(df, case_id_column: str, activity_column:str,
                              event_attribute_columns: List[str] = None,
                              trace_attribute_columns: List[str] = None,
                              add_none_attributes: bool = False):
        if event_attribute_columns is None:
            event_attribute_columns = []
        if trace_attribute_columns is None:
            trace_attribute_columns = []

        event_log = EventLog()
        for row in df.groupby(case_id_column).agg(list).itertuples():
            events = [Event(activity) for activity in getattr(row, activity_column)]
            for attribute in event_attribute_columns:
                for event, attribute_value in zip(events, getattr(row, attribute)):
                    if add_none_attributes or attribute_value is not None:
                        event.attributes[attribute] = attribute_value
            trace_attributes = {case_id_column: row.Index}
            for column in trace_attribute_columns:
                trace_attributes[column] = getattr(row, column)[0]
            event_log.add_trace(Trace(row.Index, events, trace_attributes))
        return event_log

    @staticmethod
    def create_from_dict(d):
        """
        parses a dictionary. the format must be the same as in EventLog.to_dict
        """
        log = EventLog()
        for trace_dict in d['traces']:
            log.add_trace(Trace.create_from_dict(trace_dict))
        return log

def _join_events(event_a, event_b, startdate_attribute=None,
                 enddate_attribute=None, duration_attribute=None,
                 raise_error_for_attributes=True):
    #if successive events have different attribute values, we do not want to lose
    #these value except we are told so by setting raise_error_for_attributes to False
    if raise_error_for_attributes:
        for attribute_name in set(event_a.attributes.keys()).union(
                set(event_b.attributes.keys())):
            if (attribute_name != startdate_attribute and
                attribute_name != enddate_attribute and
                attribute_name != duration_attribute and
                not event_a.attributes[attribute_name] == event_b.attributes[attribute_name]):
                raise ValueError('Cannot join %r and %r due to different attribute values for %s' % (
                        event_a, event_b, attribute_name))
    if enddate_attribute is not None:
        event_a.attributes[enddate_attribute] = event_b.attributes[enddate_attribute]
    if duration_attribute is not None:
        if startdate_attribute is not None and enddate_attribute is not None:
            event_a.attributes[duration_attribute] = \
                event_a.attributes[enddate_attribute] - \
                event_a.attributes[startdate_attribute]
        else:
            event_a.attributes[duration_attribute] = \
                event_a.attributes[duration_attribute] + \
                event_b.attributes[duration_attribute]
