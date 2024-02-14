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

"""
utils for functional programming
"""
from functools import total_ordering

def do_nothing(*args, **kwargs):
    """
    a method that accepts any number of parameters and does nothing
    """

def identity(x):
    """
    just returns x
    """
    return x

@total_ordering
class _MinType(object):
    """
    defines a type that is smaller than everything
    """
    def __le__(self, other):
        return True

    def __eq__(self, other):
        return (self is other)

Min = _MinType()
