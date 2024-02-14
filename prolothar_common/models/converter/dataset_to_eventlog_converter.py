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