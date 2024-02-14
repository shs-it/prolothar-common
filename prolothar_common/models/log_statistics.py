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

import pandas as pd

from prolothar_common.experiments.statistics import Statistics
from prolothar_common.models.eventlog import EventLog

from typing import Union, Iterable, Dict

from collections import Counter, defaultdict

def _mean(x):
    return x.mean()

def _min(x):
    return x.min()

def _max(x):
    return x.max()

class TraceStatistics:
    """
    statistics about traces in an eventlog
    """

    def __init__(self, log: EventLog):
        self.nr_of_traces = len(log)
        self.nr_of_variants = len(set(tuple(trace.to_activity_list()) for trace in log))
        trace_length_statistics = Statistics(len(trace) for trace in log)
        self.min_trace_length = int(trace_length_statistics.minimum())
        self.average_trace_length = trace_length_statistics.mean()
        self.max_trace_length = int(trace_length_statistics.maximum())

class LogStatistics():
    """
    computes different statistics on a given EventLog
    """

    def __init__(self, log: EventLog):
        """
        creates a new LogStatistics object for a given EventLog.
        the constructor does only set the EventLog, but does not compute anything, yet.

        Parameters
        ----------
        log : EventLog
            the EventLog on which we want to compute different statistics
        """
        self.log = log

    def compute_activity_statistics_df(
            self, trace_id_attribute: str = None,
            continuous_event_attributes: Union[Iterable[str],None] = None) -> pd.DataFrame:
        """
        computes statistics about activities in the event log

        Parameters
        ----------
        trace_id_attribute : str, optional
            if the trace attributes contain the trace id, set it to this attribute name.
            by default None => the trace id is read from trace.get_id()
        continuous_event_attributes : Union[Iterable[str],None], optional
            set this to a list or set of event attributes for which you want to
            compute statistics (max/min/mean), by default None

        Returns
        -------
        pd.DataFrame
            a dataframe with activities as indices and different statistics as columns
        """

        append_trace_id_column = False
        if trace_id_attribute is None:
            trace_id_attribute = 'trace'
            append_trace_id_column = True

        aggregation_dict = {}
        aggregation_dict['support'] = pd.NamedAgg(
                column=trace_id_attribute, aggfunc='count')
        aggregation_dict['traces'] = pd.NamedAgg(
                column=trace_id_attribute, aggfunc='nunique')

        self.__compute_statistics_for_event_attributes(
                continuous_event_attributes, aggregation_dict)

        activity_statistics = self.log.to_pandas_df(
                append_trace_id_column=append_trace_id_column).groupby(
            ['Activity']
        ).agg(**aggregation_dict)

        activity_statistics['frequency'] = activity_statistics['support'] / activity_statistics['support'].sum()
        activity_statistics['frequency_traces'] = activity_statistics['traces'] / self.log.get_nr_of_traces()

        activity_statistics = self.__compute_start_end_activity_statistics(
                activity_statistics)

        return activity_statistics

    def __compute_statistics_for_event_attributes(
            self, continuous_event_attributes, aggregation_dict: Dict):
        if continuous_event_attributes is not None:
            for attribute in continuous_event_attributes:
                for agg_op in [('min',_min), ('max',_max), ('mean',_mean)]:
                    aggregation_dict[
                            '%s(%s)' % (agg_op[0], attribute)
                        ] = pd.NamedAgg(column=attribute, aggfunc=agg_op[1])

    def __compute_start_end_activity_statistics(
            self, activity_statistics: pd.DataFrame) -> pd.DataFrame:
        start_counter = Counter()
        end_counter = Counter()

        for trace in self.log.traces:
            start_counter[trace.events[0].activity_name] += 1
            end_counter[trace.events[-1].activity_name] += 1

        activity_statistics['P(a|start)'] = [
                start_counter[activity] / self.log.get_nr_of_traces()
                for activity in activity_statistics.index
        ]
        activity_statistics['P(a|end)'] = [
                end_counter[activity] / self.log.get_nr_of_traces()
                for activity in activity_statistics.index
        ]

        activity_statistics['P(start|a)'] = (
                activity_statistics['P(a|start)'] *
                (self.log.get_nr_of_traces() / activity_statistics['support'].sum()) /
                activity_statistics['frequency']
        )
        activity_statistics['P(end|a)'] = (
                activity_statistics['P(a|end)'] *
                (self.log.get_nr_of_traces() / activity_statistics['support'].sum()) /
                activity_statistics['frequency']
        )

        return activity_statistics

    def compute_variant_statistics_df(self) -> pd.DataFrame:
        """
        computes how often each unique sequence (=variant) occurs in the event log.

        Returns
        -------
        pd.DataFrame
            a dataframe with two columns: Variant (list of activities) | Count
        """
        variant_counter = defaultdict(int)
        for trace in self.log:
            variant_counter[tuple(trace.to_activity_list())] += 1
        return pd.DataFrame([
            [', '.join(variant), count] for variant, count in variant_counter.items()
        ], columns=['Variant', 'Count']).set_index('Variant')

    def compute_trace_statistics(self) -> TraceStatistics:
        """
        computes statistics about traces in the eventlog

        Returns
        -------
        TraceStatistics
            statistics about traces and trace lengths in the log
        """
        return TraceStatistics(self.log)