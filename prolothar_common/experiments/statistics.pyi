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

from typing import Iterable

class Statistics:

    def __init__(self, iterable: Iterable[float]=()): ...

    def push(self, value: float): ...
    def merge(self, other: 'Statistics'): ...
    def minimum(self) -> float: ...
    def maximum(self) -> float: ...
    def mean(self) -> float: ...
    def variance(self, degrees_of_freedom: int = 1) -> float: ...
    def stddev(self, degrees_of_freedom: int = 1) -> float: ...
