# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, TypeVar, Callable

P = TypeVar('P')
E = TypeVar('E')
R = TypeVar('R')

class PartitionableList(ABC):
    """interface for parallelizable operations on lists"""

    def __init__(self, l: List):
        if l is None:
            raise ValueError('list must not be None')
        self._list = l

    @abstractmethod
    def map(self, parameter: P, map_function: Callable[[P, E], R],
            keep_order: bool = True) -> List[R]:
        """
        map operation: each element of the list is mapped to a new element

        Parameters
        ----------
        parameter : P
            parameter that are given to all single map operations
        map_function : Callable[[P, E], R]
            function to map one element in the list
        keep_order : bool, optional
            whether the order in the result list should be the same as in the
            source list, by default True. keeping the order might have a
            negative influence on the computation runtime.

        Returns
        -------
        List[R]
            the transformed list with the mapped elements
        """

    @abstractmethod
    def map_filter(self, parameter: P, map_function: Callable[[P,E],R],
                   filter_function: Callable[[P,R],bool]) -> List[R]:
        """map operation followed by filter operation:
           each element of the list is mapped to a new element and the mapped
           element is only return if it matches the filter
           """

    @abstractmethod
    def map_reduce(self, parameter: P, map_function: Callable[[P,E],R],
                   reduce_function: Callable[[R,R],R]) -> R:
        """map operation followed by reduce operation:
           each element of the list is mapped to a new element and the mapped
           elements are pairwise reduced to a final result
           """
