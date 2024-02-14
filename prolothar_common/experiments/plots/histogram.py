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
This module contains methods to plot histograms of discrete or continuous values
"""
from typing import Iterable, Collection, Union
from collections import Counter
from math import sqrt

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

def plot_counts(values: Iterable, ax: Axes = None, order_by: str = 'value', bar_width: int = 1):
    """
    plots the frequency of discrete values

    Parameters
    ----------
    values : Iterable
        a container of discete values whose frequency will be plotted
    ax : Axes
        matplotlib axis to plot. must only be set if multiple plots are supposed
        to be combined in one plot by using subplots.
    order_by : str
        can be 'value', 'frequency_asc' or 'frequency_desc'. determines the order
        on the x axis
    bar_width : int
        bar width measured in units on x-axis.
        default is 1.
    """
    if not ax:
        ax = plt.gca()

    counter = Counter()
    for v in values:
        counter[v] += 1

    if order_by == 'value':
        x, y = zip(*sorted(counter.items()))
    elif order_by == 'frequency_asc':
        x, y = zip(*sorted(counter.items(), key=lambda x: x[1]))
    elif order_by == 'frequency_desc':
        x, y = zip(*sorted(counter.items(), key=lambda x: -x[1]))
    else:
        raise ValueError('unknown value for order_by: "%s"' % order_by)
    ax.bar(x, y, bar_width)

def plot_histogram(
    values: Collection[Union[float, int]], nr_of_bins: int = None,
    ax: Axes = None, histtype: str = 'bar', linestyle='solid', density: bool = False,
    alpha: float=1):
    """
    plots the histogram of a collection of numbers

    Parameters
    ----------
    values : Collection[Union[float, int]]
        a collection of numbers for which you want to plot the histogram
    nr_of_bins : int, optional
        number of histogram bins, by default None, i.e. int(sqrt(len(values)))
    ax : Axes, optional
        matplotlib axes for plotting, by default None, i.e. plt.gca()
    histtype : str, optional
        one of bar ['bar', 'step'], by default 'bar'
    linestyle : str, optional
        e.g. 'solid' or 'dashed' or 'dotted', by default 'solid'
    density : bool, optional
        if True, the counts are normalized, such that the integral sums up to 1,
        by default False
    """
    if not ax:
        ax = plt.gca()
    if not nr_of_bins:
        nr_of_bins = int(sqrt(len(values)))

    ax.hist(values, bins=nr_of_bins, histtype=histtype, ls=linestyle, density=density, alpha=alpha)
