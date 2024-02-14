import numpy as np
import pandas as pd

from sgt import SGT

from prolothar_common.models.eventlog import EventLog

from prolothar_common.clustering.traces.encoder.encoder import TraceToVectorEncoder

class ActivitySgt(TraceToVectorEncoder):
    """
    encodes the activities in a Trace with SGT (Sequence Graph Transform)
    https://pypi.org/project/sgt/
    """
    def __init__(self, drop_all_zeros_columns: bool = True):
        self.__drop_all_zeros_columns = drop_all_zeros_columns

    def encode_log(self, log: EventLog) -> np.ndarray:
        data = [
            [i, trace.to_activity_list()]
            for i, trace in enumerate(log)
        ]
        sgt_df = SGT().fit_transform(pd.DataFrame(data=data, columns=['id', 'sequence']))
        sgt_df.drop(['id'], inplace=True, axis=1)
        if self.__drop_all_zeros_columns:
            sgt_df = sgt_df.loc[:, (sgt_df != 0).any(axis=0)]
        return sgt_df.to_numpy()
