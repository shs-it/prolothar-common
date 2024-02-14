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

from collections import deque
from tqdm import tqdm

from prolothar_common.parallel.abstract.partitionable.partitionable_list import PartitionableList
from prolothar_common.parallel.abstract.partitionable.partitionable_list import P,E,R
from prolothar_common.collections import list_utils

from multiprocessing import Process, Queue

from functools import reduce

class MultiprocessPartitionableList(PartitionableList):
    """partitionable list implementation for the multiprocess module"""

    def __init__(self, l: List, nr_of_workers: int, show_progressbar: bool = False):
        super().__init__(l)
        self.__nr_of_workers = nr_of_workers
        self.__show_progressbar = show_progressbar

    def map(self, parameter: P, map_function: Callable[[P,E],R],
            keep_order: bool = True) -> List[R]:
        if keep_order:
            return self.__map_with_order_guarantee(parameter, map_function)
        else:
            return self.__map_without_order_guarantee(parameter, map_function)

    def __map_without_order_guarantee(
            self, parameter: P, map_function: Callable[[P,E],R]) -> List[R]:
        result_queue = Queue()

        workers = []
        for partition in list_utils.view_of_n_partitions(
                self._list, self.__nr_of_workers):
            worker = MapWorker(partition, parameter, map_function, result_queue)
            worker.start()
            workers.append(worker)

        return self.__collect_worker_results(workers, result_queue)

    def __map_with_order_guarantee(
            self, parameter: P, map_function: Callable[[P,E],R]) -> List[R]:
        workers = []
        for partition in list_utils.view_of_n_partitions(
                self._list, self.__nr_of_workers):
            worker = MapWorker(partition, parameter, map_function, Queue())
            worker.start()
            workers.append(worker)

        return self.__collect_worker_results_with_order_guarantee(workers)

    def map_filter(self, parameter: P, map_function: Callable[[P,E],R],
                   filter_function: Callable[[P,R],bool]) -> List[R]:
        result_queue = Queue()

        workers = []
        for partition in list_utils.view_of_n_partitions(
                self._list, self.__nr_of_workers):
            worker = MapFilterWorker(partition, parameter, map_function,
                                     filter_function, result_queue)
            worker.start()
            workers.append(worker)

        return self.__collect_worker_results(workers, result_queue)

    def map_reduce(self, parameter: P, map_function: Callable[[P,E],R],
                   reduce_function: Callable[[R,R],R]) -> R:
        result_queue = Queue()

        workers = []
        for partition in list_utils.view_of_n_partitions(
                self._list, self.__nr_of_workers):
            worker = MapReduceWorker(partition, parameter, map_function,
                                     reduce_function, result_queue)
            worker.start()
            workers.append(worker)

        return reduce(
                reduce_function,
                self.__collect_worker_results(workers, result_queue))

    def __collect_worker_results(self, workers, result_queue):
        mapped_list = []

        nr_of_finished_workers = 0
        with tqdm(total=len(self._list), disable=not self.__show_progressbar) as progressbar:
            while nr_of_finished_workers < len(workers):
                result = result_queue.get()
                if isinstance(result, StopIteration):
                    nr_of_finished_workers += 1
                elif isinstance(result, Exception):
                    [worker.terminate() for worker in workers]
                    raise result
                else:
                    mapped_list.append(result)
                    progressbar.update(1)

        [worker.join() for worker in workers]
        return mapped_list

    def __collect_worker_results_with_order_guarantee(self, workers):
        mapped_list_dict = { id(worker): [] for worker in workers }

        open_workers = deque(workers)

        with tqdm(total=len(self._list), disable=not self.__show_progressbar) as progressbar:
            while open_workers:
                current_worker = open_workers.pop()
                result = current_worker.result_queue.get()
                if not isinstance(result, StopIteration):
                    if isinstance(result, Exception):
                        [worker.terminate() for worker in workers]
                        raise result
                    mapped_list_dict[id(current_worker)].append(result)
                    open_workers.appendleft(current_worker)
                    progressbar.update(1)

        [worker.join() for worker in workers]

        result_list = mapped_list_dict[id(workers[0])]
        for worker in workers[1:]:
            result_list.extend(mapped_list_dict[id(worker)])
        return result_list

class MapWorker(Process):

    def __init__(self, l: List, parameter: P, map_function: Callable[[P,E],R],
                 result_queue: Queue):
        super().__init__()
        self.list = l
        self.parameter = parameter
        self.map_function = map_function
        self.result_queue = result_queue

    def run(self):
        for element in self.list:
            try:
                self.result_queue.put(self.map_function(self.parameter, element))
            except Exception as e:
                self.result_queue.put(e)
        self.result_queue.put(StopIteration())

class MapFilterWorker(Process):

    def __init__(self, l: List, parameter: P, map_function: Callable[[P,E],R],
                 filter_function: Callable[[P,R],bool], result_queue: Queue):
        super().__init__()
        self.list = l
        self.parameter = parameter
        self.map_function = map_function
        self.filter_function = filter_function
        self.result_queue = result_queue

    def run(self):
        for element in self.list:
            try:
                mapped_element = self.map_function(self.parameter, element)
                if self.filter_function(self.parameter, mapped_element):
                    self.result_queue.put(mapped_element)
            except Exception as e:
                self.result_queue.put(e)
        self.result_queue.put(StopIteration())

class MapReduceWorker(Process):

    def __init__(self, l: List, parameter: P, map_function: Callable[[P,E],R],
                 reduce_function: Callable[[P,R],bool], result_queue: Queue):
        super().__init__()
        self.list = l
        self.parameter = parameter
        self.map_function = map_function
        self.reduce_function = reduce_function
        self.result_queue = result_queue

    def run(self):
        try:
            self.result_queue.put(reduce(
                self.reduce_function,
                (self.map_function(self.parameter, element)
                 for element in self.list)))
        except Exception as e:
            self.result_queue.put(e)
        self.result_queue.put(StopIteration())
