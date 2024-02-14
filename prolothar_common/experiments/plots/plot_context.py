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
contains a class for "plot context", that means auto showable plots, such that
boilerplate code for plot creation is reduced.
"""

from typing import List
from abc import ABC, abstractmethod

from io import BytesIO
import base64
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes

class _BasePlotContext(ABC):
    """
    template for all PlotContext classes
    """

    def __init__(self, title: str = None, show: bool = True,
                 filepath: str = None, use_tight_layout: bool = False):
        self.__title = title
        self.__show = show
        self.__filepath = filepath
        self.__figure: Figure = None
        self.__use_tight_layout = use_tight_layout

    def get_figure(self) -> Figure:
        return self.__figure

    def __enter__(self):
        self.__figure = self._on_enter()
        self.__figure.suptitle(self.__title)
        return self

    @abstractmethod
    def _on_enter(self) -> Figure:
        """
        called during __enter__. this method should return a Figure object
        created by plot.subplots. The configuration of the figure is done
        by the super class, the configuration of the axes must be done in the
        subclass.
        """

    def __exit__(self, type, value, traceback):
        if self.__use_tight_layout:
            plt.tight_layout()
        if self.__filepath is not None:
            self.__figure.savefig(self.__filepath)
        if self.__show:
            plt.show()
        else:
            plt.close()

    def to_base_64(self, image_format: str = 'png') -> str:
        """
        returns a base64 encoded version of the figure in this plot context
        """
        out_img = BytesIO()
        self.get_figure().savefig(out_img, format=image_format)
        out_img.seek(0)  # rewind file
        return base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")

class PlotContext(_BasePlotContext):
    """
    a class that facilitates plotting and reduced boilerplate code, e.g. by
    automatically calling plt.show() or savefig().
    If you need subfigures, use GridPlotContext()
    """

    def __init__(self, title: str = None, show: bool = True,
                 filepath: str = None, log_filepath: str = None,
                 use_tight_layout: bool = False):
        super().__init__(
            title=title,
            show=show,
            filepath=filepath,
            use_tight_layout=use_tight_layout)
        self.__axes: Axes = None
        if log_filepath is not None:
            self.__log_file = open(log_filepath, 'w')
        else:
            self.__log_file = None

    def _on_enter(self) -> Figure:
        figure, self.__axes = plt.subplots()
        if self.__log_file is not None:
            self.__register_log_plot()
            self.__register_log_legend()
            self.__register_log_hist()
            self.__register_log_bar()
            self.__register_log_scatter()
        return figure

    def __register_log_plot(self):
        def log_plot(*args,**kwargs):
            with np.printoptions(threshold=np.inf):
                self.__log_file.write(f'plot({args},{kwargs})\n')
            return self.__axes.original_plot(*args, **kwargs)
        self.__axes.original_plot = self.__axes.plot
        self.__axes.plot = log_plot

    def __register_log_legend(self):
        def log_legend(*args,**kwargs):
            with np.printoptions(threshold=np.inf):
                self.__log_file.write(f'legend({args},{kwargs})\n')
            return self.__axes.original_legend(*args, **kwargs)
        self.__axes.original_legend = self.__axes.legend
        self.__axes.legend = log_legend

    def __register_log_hist(self):
        def log_hist(*args,**kwargs):
            with np.printoptions(threshold=np.inf):
                self.__log_file.write(f'hist({args},{kwargs})\n')
            return self.__axes.original_hist(*args, **kwargs)
        self.__axes.original_hist = self.__axes.hist
        self.__axes.hist = log_hist

    def __register_log_bar(self):
        def log_bar(*args,**kwargs):
            with np.printoptions(threshold=np.inf):
                self.__log_file.write(f'bar({args},{kwargs})\n')
            return self.__axes.original_bar(*args, **kwargs)
        self.__axes.original_bar = self.__axes.bar
        self.__axes.bar = log_bar

    def __register_log_scatter(self):
        def log_scatter(*args,**kwargs):
            with np.printoptions(threshold=np.inf):
                self.__log_file.write(f'scatter({args},{kwargs})\n')
            return self.__axes.original_scatter(*args, **kwargs)
        self.__axes.original_scatter = self.__axes.scatter
        self.__axes.scatter = log_scatter

    def get_axes(self) -> Axes:
        return self.__axes

    def __exit__(self, type, value, traceback):
        super().__exit__(type, value, traceback)
        if self.__log_file is not None:
            self.__log_file.close()

class GridPlotContext(_BasePlotContext):
    """
    a PlotContext with subfigures in a grid
    """

    def __init__(
            self, nr_of_rows: int, nr_of_columns: int,
            title: str = None, show: bool = True,
            filepath: str = None, use_tight_layout: bool = False,
            sharex: str = 'none',
            sharey: str = 'none'):
        """
        _summary_

        Parameters
        ----------
        nr_of_rows : int
            number of subplot rows
        nr_of_columns : int
            number of subplot columns
        title : str, optional
            title of the figure, by default None
        show : bool, optional
            whether to show the plot (plt.show()), by default True
        filepath : str, optional
            filepath to save the figure, by default None
        use_tight_layout : bool, optional
            whether to use matplotlib tight layouting, by default False
        sharex : str, optional
            one of ['none', 'all', 'row', 'col'], by default 'none'
        sharey : str, optional
            one of ['none', 'all', 'row', 'col'], by default 'none'
        """
        super().__init__(
            title=title,
            show=show,
            filepath=filepath,
            use_tight_layout=use_tight_layout)
        self.__axes: List[List[Axes]] = None
        self.__nr_of_rows = nr_of_rows
        self.__nr_of_columns = nr_of_columns
        self.__sharex = sharex
        self.__sharey = sharey

    def _on_enter(self) -> Figure:
        figure, self.__axes = plt.subplots(
            nrows=self.__nr_of_rows, ncols=self.__nr_of_columns,
            sharex=self.__sharex, sharey=self.__sharey)
        if self.__nr_of_rows == 1 and self.__nr_of_columns == 1:
            self.__axes = np.array([[self.__axes]])
        elif self.__nr_of_rows == 1:
            self.__axes = np.array([self.__axes])
        elif self.__nr_of_columns == 1:
            self.__axes = np.array([self.__axes]).transpose()
        return figure

    def get_nr_columns(self) -> int:
        return self.__nr_of_columns

    def get_nr_rows(self) -> int:
        return self.__nr_of_rows

    def get_axes(self, row_index: int, column_index: int) -> Axes:
        """
        zero-based indexing of rows and columns
        """
        return self.__axes[row_index][column_index]

    def get_list_of_axes(self) -> List[Axes]:
        return self.__axes.flatten().tolist()