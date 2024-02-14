# -*- coding: utf-8 -*-

from prolothar_common.lognoise.lognoise import LogNoise

from prolothar_common.models.eventlog import EventLog

from typing import List

class CombinedNoise(LogNoise):
    """a LogNoise enabling a mixture of different noise models"""

    def __init__(self, noise_model_list: List[LogNoise]):
        """creates a new CombinedNoise LogNoise object
        Args:
           noise_model_list:
               submodels that will be applied all together on the data.
               the submodels will be applied in the given order, i.e. if
               add noise comes first and remove noise comes last, the remove
               noise can remove the added activities.
        """
        if not noise_model_list:
            raise ValueError('noise_model_list must not be empty')
        self.__noise_model_list = noise_model_list

    def apply(self, log: EventLog):
        for noise_model in self.__noise_model_list:
            noise_model.apply(log)

    def __repr__(self) -> str:
        return "CombinedNoise(%r)" % (self.__noise_model_list)