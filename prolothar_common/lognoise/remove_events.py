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