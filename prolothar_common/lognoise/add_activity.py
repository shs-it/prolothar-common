# -*- coding: utf-8 -*-

from prolothar_common.lognoise.lognoise import LogNoise

from prolothar_common.models.eventlog import EventLog, Trace, Event

import random

class AddActivity(LogNoise):
    """a LogNoise implementation that randomly adds a given activity"""

    def __init__(self, activity: str, add_probability: float,
                 random_seed:int=None):
        """creates a new AddActivity LogNoise object
        Args:
           activity:
               the activity that should be added as noise
           add_probability:
               should be between 0 and 1.0
           random_seed:
               seed to initialize the random generator
        """
        self.__random = random.Random(random_seed)
        self.__random_seed = random_seed
        self.__activity = activity

        if add_probability < 0 or add_probability >= 1:
            raise ValueError('event_removal_probability must be in [0,1)')
        self.__add_probability = add_probability

    def apply(self, log: EventLog):
        if self.__add_probability > 0:
            for trace in log.traces:
                self.__apply_on_trace(trace)

    def __apply_on_trace(self, trace: Trace):
        new_event_list = []
        for true_event, random_number in zip(
                trace.events,
                [self.__random.uniform(0, 1) for _ in range(len(trace))]):
            new_event_list.append(true_event)
            if random_number < self.__add_probability:
                new_event_list.append(Event(self.__activity))
        trace.events = new_event_list

    def __repr__(self) -> str:
        return "AddActivity(%s, %r, seed=%r)" % (
                self.__activity, self.__add_probability, self.__random_seed)