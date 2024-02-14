# -*- coding: utf-8 -*-

from prolothar_common.lognoise.lognoise import LogNoise

from prolothar_common.models.eventlog import EventLog, Trace

import random

class SwapEvents(LogNoise):
    """a LogNoise implementation that randomly swaps neighbored events"""

    def __init__(self, event_swap_probability: float, random_seed:int=None):
        """creates a new SwapEvents LogNoise object
        Args:
           event_swap_probability:
               should be between 0 and 1.0
           random_seed:
               seed to initialize the random generator
        """
        self.__random = random.Random(random_seed)
        self.__random_seed = random_seed

        if event_swap_probability < 0 or event_swap_probability >= 1:
            raise ValueError('event_swap_probability must be in [0,1)')
        self.__event_swap_probability = event_swap_probability

    def apply(self, log: EventLog):
        if self.__event_swap_probability > 0:
            for trace in log.traces:
                self.__apply_on_trace(trace)

    def __apply_on_trace(self, trace: Trace):
        for i in range(len(trace.events) - 1):
            if self.__random.uniform(0, 1) < self.__event_swap_probability:
                trace.events[i], trace.events[i+1] = trace.events[i+1], trace.events[i]

    def __repr__(self) -> str:
        return "SwapEvents(%r, seed=%r)" % (
                self.__event_swap_probability, self.__random_seed)