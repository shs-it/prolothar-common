# -*- coding: utf-8 -*-

from prolothar_common.models.eventlog import EventLog

from abc import ABC, abstractmethod

class LogNoise(ABC):
    """interface for methods that add artificial noise to an event log"""

    @abstractmethod
    def apply(self, log: EventLog):
        """applies noise to the given log"""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass