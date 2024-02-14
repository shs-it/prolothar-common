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