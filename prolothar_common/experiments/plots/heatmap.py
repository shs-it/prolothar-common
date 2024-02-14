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
methods for creating heatmap plots
"""

from typing import List, Tuple
import numpy as np
from matplotlib.axes import Axes
from matplotlib.image import AxesImage
from matplotlib.colorbar import Colorbar
from matplotlib.ticker import StrMethodFormatter
from matplotlib.text import Text
import matplotlib.pyplot as plt

def plot_heatmap(
    data: np.ndarray, row_labels: List[str], col_labels: List[str],
    ax: Axes = None, show_colorbar: bool = True, colorbar_kw = {},
    colorbar_label: str = "", **kwargs) -> Tuple[AxesImage,Colorbar]:
    """
    creates a heatmap
    https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html

    Parameters
    ----------
    data : np.ndarray
        a 2-dimension matrix of shape (N,M) to be plotted as a heatmap
    row_labels : List[str]
        a list or array of length N with the labels for the rows
    col_labels : List[str]
        a list or array of length M with the labels for the columns
    ax : Axes, optional
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted. If
        not provided, use current axes or create a new one
    show_colorbar : bool, optional
        if True, a colorbar as legend of the heatmap values is plotted next to the
        heatmap itself, by default True
    colorbar_kw : dict, optional
        A dictionary with arguments to `matplotlib.Figure.colorbar`, by default {}
    colorbar_label : str, optional
        The label for the colorbar, by default ""
    cmap: optional
        The colormap for the heatmap. default is from purple to yellow.
        See https://matplotlib.org/3.3.3/tutorials/colors/colormaps.html
        for more details.
    **kwargs
        All other arguments are forwarded to `imshow`.

    Returns
    -------
    Tuple[AxesImage,Colorbar]
        a tuple consisting of the heatmap and the colorbar. in case of
        "show_colorbar" is False, the second entry of the tuple will be None.
    """
    if data.ndim != 2:
        raise ValueError('data must have exactly 2 dimensions but has %d' % data.ndim)
    if data.shape[0] != len(row_labels):
        raise ValueError('wrong number of row labels. expected %d but was %d' % (
            data.shape[0], len(row_labels)))
    if data.shape[1] != len(col_labels):
        raise ValueError('wrong number of column labels. expected %d but was %d' % (
            data.shape[1], len(col_labels)))

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    heatmap = ax.imshow(data, **kwargs)

    # Create colorbar
    colorbar = None
    if show_colorbar:
        colorbar = ax.figure.colorbar(heatmap, ax=ax, **colorbar_kw)
        colorbar.ax.set_ylabel(colorbar_label, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return heatmap, colorbar

def annotate_heatmap(im: AxesImage, data: np.ndarray=None, valfmt="{x:.2f}",
                     textcolors=["white", "black"],
                     threshold=None, **textkw) -> List[Text]:
    """
    https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)
    return texts
