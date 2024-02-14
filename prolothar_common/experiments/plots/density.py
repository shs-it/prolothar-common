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

from typing import Collection, Union

import pandas as pd
from matplotlib.axes import Axes

def plot_density(
    values: Collection[Union[float, int]],
    ax: Axes = None, linestyle='solid', **kwargs):
    """
    plots a kernel density estimation of the given values

    Parameters
    ----------
    values : Collection[Union[float, int]]
        a collection of numbers for which you want to plot the estimated density
    ax : Axes, optional
        matplotlib axes for plotting, by default None, i.e. plt.gca()
    linestyle : str, optional
        e.g. 'solid' or 'dashed' or 'dotted', by default 'solid'
    """
    pd.Series(values).plot(kind='density', linestyle=linestyle, ax=ax, **kwargs)