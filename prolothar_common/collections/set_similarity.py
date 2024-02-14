# -*- coding: utf-8 -*-

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