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