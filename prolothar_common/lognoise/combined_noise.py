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