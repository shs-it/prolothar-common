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

from typing import Set

def sorensen_dice_coefficient(a: Set, b: Set) -> float:
   """https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient"""
   if len(a) == 0 and len(b) == 0:
       return 1.0
   else:
       return 2 * len(a.intersection(b)) / (len(a) + len(b))

def jaccard_index(a: Set, b: Set) -> float:
    """
    https://en.wikipedia.org/wiki/Jaccard_index
    """
    if len(a) == 0 and len(b) == 0:
        return 1.0
    else:
        intersection = a.intersection(b)
        return len(intersection) / (len(a) + len(b) - len(intersection))

def overlap_coefficient(a: Set, b: Set) -> float:
    """
    https://en.wikipedia.org/wiki/Overlap_coefficient
    """
    if len(a) == 0 and len(b) == 0:
        return 1.0
    else:
        intersection = a.intersection(b)
        return len(intersection) / min(len(a), len(b))