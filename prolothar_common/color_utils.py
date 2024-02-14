# -*- coding: utf-8 -*-

from typing import Tuple
import math

def is_light_or_dark_rgb(rgb: Tuple[int, int, int]) -> str:
    """
    determines wheter a given rgb color is light or dark
    https://stackoverflow.com/questions/22603510/is-this-possible-to-detect-a-colour-is-a-light-or-dark-colour

    Parameters
    ----------
    rgb : Tuple[int, int, int]
        rgb vector (0..255, 0..255, 0..255)

    Returns
    -------
    str
        'light' or 'dark'
    """
    [r,g,b] = rgb
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    if hsp > 127.5:
        return 'light'
    else:
        return 'dark'