# -*- coding: utf-8 -*-

from abc import ABC
from typing import Set, Hashable

class Attribute(ABC):
    """abstract definition of an attribute in the data set"""
    def __init__(self, name: str, unique_values: Set[Hashable]):
        """creates a attribute
        Args:
            name:
                name of the attribute
            unique_values:
                values that this attribute has in the given data set
        """
        self.__name = name
        self.__unique_values = unique_values
        
    def get_name(self) -> str:
        return self.__name
    
    def get_nr_of_unique_values(self) -> int:
        """the number of unique values of this attribute in the data set"""
        return len(self.__unique_values)
    
    def get_unique_values(self) -> Set[Hashable]:
        return self.__unique_values
    
    def add_value(self, value: Hashable):
        """adds the value to the set of unique values of this attribute. if the
        value is already in the set of uniques values this method is still
        safe to call
        """
        self.__unique_values.add(value)
    
    def is_categorical(self) -> bool:
        return False
    
    def is_numerical(self) -> bool:
        return False

class CategoricalAttribute(Attribute):
    """a categorical attribute, i.e. an attribute with unordered, discrete 
    values
    """
    def __init__(self, name: str, categories: Set[Hashable]):
        """creates a new categorical attribute
        Args:
            name:
                name of the attribute
            categories:
                values that this attribute can have
        """
        super().__init__(name, categories)

    def is_categorical(self) -> bool:
        return True

class NumericalAttribute(Attribute):
    """a numerical attribute, i.e. an attribute with numerical (int or float)
    values.
    """
    def __init__(self, name: str, unique_values: Set[Hashable]):
        """creates a new numerical attribute
        Args:
            name:
                name of the attribute
            unique_values:
                values that this attribute has in the given data set
        """
        super().__init__(name, unique_values)

    def is_numerical(self) -> bool:
        return True