from typing import List, Dict

import numpy as np

from prolothar_common.models.eventlog import EventLog

from prolothar_common.clustering.traces.encoder.encoder import TraceToVectorEncoder

class ActivityOneHotEncoding(TraceToVectorEncoder):
    """
    encodes the activities in a Trace as a one-hot-encoded vector.
    returns a numpy array. each line corresponds to one trace, each column
    corresponds to one activity. the value is 1 if the activity occurs in this
    trace and 0 otherwise.
    """

    def encode_log(self, log: EventLog) -> np.ndarray:
        encoder_dict = {a: i for i,a in enumerate(log.compute_activity_set())}
        return np.array([self._encode_trace(trace, encoder_dict) \
                        for trace in log.to_simple_activity_log()])

    def _encode_trace(self, trace: List[str], encoder_dict: Dict[str, int]):
        encoded_trace = [0] * len(encoder_dict)
        for activity in trace:
            encoded_trace[encoder_dict[activity]] = 1
        return encoded_trace
