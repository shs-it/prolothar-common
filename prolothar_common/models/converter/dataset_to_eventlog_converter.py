# -*- coding: utf-8 -*-

from prolothar_common.models.eventlog import EventLog, Trace, Event
from prolothar_common.models.dataset import TargetSequenceDataset

class DatasetToEventLogConverter():
    """
    converts a Dataset with target sequences and attributes to an EventLog.
    every instance of the dataset is converted to one trace in the log.
    the events of the the trace correspond to the target sequence. the attributes
    of an instance are written to the trace attributes. there will be no event
    attributes.
    """

    def convert(self, dataset: TargetSequenceDataset) -> EventLog:
        """
        converts a Dataset with target sequences and attributes to an Eventlog
        """
        log = EventLog()

        for instance in dataset:
            log.add_trace(Trace(instance.get_id(), [
                Event(symbol) for symbol in instance.get_target_sequence()
            ], attributes = instance.get_features_dict()))

        return log