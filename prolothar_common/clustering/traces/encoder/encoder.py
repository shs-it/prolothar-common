from abc import ABC, abstractmethod

import numpy as np

from prolothar_common.models.eventlog import EventLog

class TraceToVectorEncoder(ABC):
    """
    interface for encoders that transform traces of an EventLog to matrix where
    each row corresponds to a trace in the log
    """

    @abstractmethod
    def encode_log(self, log: EventLog) -> np.ndarray:
        """
        encodes the log into a matrix form where each row corresponds to one
        trace in the log

        Parameters
        ----------
        log : EventLog
            will be encoded as a matrix where each row corresponds to a trace
            in the log

        Returns
        -------
        np.ndarray
            a matrix where each row vector corresponds to a trace in the log
        """

    def __call__(self, log: EventLog) -> np.ndarray:
        return self.encode_log(log)
