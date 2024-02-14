# -*- coding: utf-8 -*-

from prolothar_common.lognoise.lognoise import LogNoise

from prolothar_common.models.eventlog import EventLog, Trace

import random

class RemoveEvents(LogNoise):
    """a LogNoise implementation that randomly removes events"""

    def __init__(self, event_removal_probability: float, random_seed:int=None):
        """creates a new RemvoveEvents LogNoise object
        Args:
           event_removal_probability:
               should be between 0 and 1.0
           random_seed:
               seed to initialize the random generator
        """
        self.__random = random.Random(random_seed)
        self.__random_seed = random_seed

        if event_removal_probability < 0 or event_removal_probability >= 1:
            raise ValueError('event_removal_probability must be in [0,1)')
        self.__event_removal_probability = event_removal_probability

    def apply(self, log: EventLog):
        if self.__event_removal_probability > 0:
            for trace in log.traces:
                self.__apply_on_trace(trace)
            log.traces = [trace for trace in log.traces if len(trace) > 0]

    def __apply_on_trace(self, trace: Trace):
        trace.events = [
            event for event in trace.events \
            if self.__random.uniform(0, 1) >= self.__event_removal_probability]

    def __repr__(self) -> str:
        return "RemoveEvents(%r, seed=%r)" % (
                self.__event_removal_probability, self.__random_seed)