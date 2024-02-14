# -*- coding: utf-8 -*-

class TwoWayDict():
    """
    A dictionary with inverse/reverse look up. Keys are handled uniquely, values
    can be assigned to multiple keys. During reverse look up, one key (value)
    will return a list of values (keys).
    """
    
    def __init__(self):
        self.dict = dict()
        self.__inverse_dict = dict()
    
    def __setitem__(self, key, value):
        self.dict[key] = value
        if value not in self.__inverse_dict:
            self.__inverse_dict[value] = set()
        self.__inverse_dict[value].add(key)
        
    def __getitem__(self, key):
        return self.dict[key]    
    
    def __contains__(self, key):
        return key in self.dict
    
    def inverse(self, key):
        return self.__inverse_dict[key]