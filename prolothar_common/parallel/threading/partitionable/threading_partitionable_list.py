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

from typing import List,Callable

from prolothar_common.parallel.abstract.partitionable.partitionable_list import PartitionableList
from prolothar_common.parallel.abstract.partitionable.partitionable_list import P,E,R
from prolothar_common.collections import list_utils

from threading import Thread

from functools import reduce

class ThreadingPartitionableList(PartitionableList):
    """partitionable list implementation for the threading module"""

    def __init__(self, l: List, nr_of_workers: int):
        super().__init__(l)
        self.__nr_of_workers = nr_of_workers

    def __join_workers(self, workers: List):
        for worker in workers:
            worker.join()
            if worker.exception is not None:
                raise worker.exception

    def map(self, parameter: P, map_function: Callable[[P,E],R],
            keep_order: bool = True) -> List[R]:
        if keep_order:
            return self.__map_with_order_guarantee(parameter, map_function)
        else:
            return self.__map_without_order_guarantee(parameter, map_function)

    def __map_without_order_guarantee(
            self, parameter: P, map_function: Callable[[P,E],R]) -> List[R]:
        result_list = []

        workers = []
        for partition in list_utils.view_of_n_partitions(
                self._list, self.__nr_of_workers):
            worker = MapWorker(partition, parameter, map_function, result_list)
            worker.start()
            workers.append(worker)

        self.__join_workers(workers)

        return result_list

    def __map_with_order_guarantee(
            self, parameter: P, map_function: Callable[[P,E],R]) -> List[R]:
        workers = []
        result_lists = []
        for partition in list_utils.view_of_n_partitions(
                self._list, self.__nr_of_workers):
            result_lists.append([])
            worker = MapWorker(partition, parameter, map_function, result_lists[-1])
            worker.start()
            workers.append(worker)

        self.__join_workers(workers)

        def combine_lists(x,y):
            x.extend(y)
            return x
        return reduce(combine_lists, result_lists)

    def map_filter(self, parameter: P, map_function: Callable[[P,E],R],
                   filter_function: Callable[[P,R],bool]) -> List[R]:
        result_list = []

        workers = []
        for partition in list_utils.view_of_n_partitions(
                self._list, self.__nr_of_workers):
            worker = MapFilterWorker(partition, parameter, map_function,
                                     filter_function, result_list)
            worker.start()
            workers.append(worker)

        self.__join_workers(workers)

        return result_list

    def map_reduce(self, parameter: P, map_function: Callable[[P,E],R],
                   reduce_function: Callable[[R,R],R]) -> R:
        result_list = []

        workers = []
        for partition in list_utils.view_of_n_partitions(
                self._list, self.__nr_of_workers):
            worker = MapReduceWorker(partition, parameter, map_function,
                                     reduce_function, result_list)
            worker.start()
            workers.append(worker)

        self.__join_workers(workers)

        return reduce(reduce_function, result_list)

class AbstractWorker(Thread):
    def __init__(self):
        super().__init__()
        self.exception: Exception|None = None

    def run(self):
        try:
            self._run()
        except Exception as e:
            self.exception = e

class MapWorker(AbstractWorker):

    def __init__(self, l: List, parameter: P, map_function: Callable[[P,E],R],
                 result_list: List):
        super().__init__()
        self.list = l
        self.parameter = parameter
        self.map_function = map_function
        self.result_list = result_list

    def _run(self):
        for element in self.list:
            self.result_list.append(self.map_function(self.parameter, element))

class MapFilterWorker(AbstractWorker):

    def __init__(self, l: List, parameter: P, map_function: Callable[[P,E],R],
                 filter_function: Callable[[P,R],bool], result_list: List):
        super().__init__()
        self.list = l
        self.parameter = parameter
        self.map_function = map_function
        self.filter_function = filter_function
        self.result_list = result_list

    def _run(self):
        for element in self.list:
            mapped_element = self.map_function(self.parameter, element)
            if self.filter_function(self.parameter, mapped_element):
                self.result_list.append(mapped_element)

class MapReduceWorker(AbstractWorker):

    def __init__(self, l: List, parameter: P, map_function: Callable[[P,E],R],
                 reduce_function: Callable[[P,R],bool], result_list: List):
        super().__init__()
        self.list = l
        self.parameter = parameter
        self.map_function = map_function
        self.reduce_function = reduce_function
        self.result_list = result_list

    def _run(self):
        self.result_list.append(reduce(
            self.reduce_function,
            (self.map_function(self.parameter, element)
                for element in self.list)))
