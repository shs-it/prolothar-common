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

from abc import ABC, abstractmethod
import os
import math
import pandas as pd
import seaborn as sns
from prolothar_common.experiments.plots.plot_context import PlotContext
from prolothar_common.collections.two_way_dict import TwoWayDict

from prolothar_common.experiments.statistics import Statistics

class _Colors:
    """constants for colors in the result collector plots"""
    GOLD = sns.xkcd_rgb["gold"]
    BLACK = sns.xkcd_rgb["black"]
    GREEN = sns.xkcd_rgb["green"]
    BLUE = sns.xkcd_rgb["blue"]
    RED = sns.xkcd_rgb["red"]
    ORANGE = sns.xkcd_rgb["orange"]
    GREY = sns.xkcd_rgb["grey"]
    OLIVE = sns.xkcd_rgb["olive"]
    CYAN = sns.xkcd_rgb["cyan"]
    BROWN = sns.xkcd_rgb["brown"]
    LIGHT_BROWN = sns.xkcd_rgb["light brown"]
    LIME = sns.xkcd_rgb["lime"]
    PINK = sns.xkcd_rgb["pink"]
    LIGHT_BLUE = sns.xkcd_rgb["light blue"]
    BLUISH_PURPLE = sns.xkcd_rgb["bluish purple"]

class _Markers:
    """constants for markers in the result collector plots"""
    POINT = "."
    PIXEL = ","
    CIRCLE = "o"
    STAR = "*"
    X = "X"
    PLUS = "P"
    TRIANGLE_DOWN = "v"
    TRIANGLE_LEFT = "<"
    TRIANGLE_RIGHT = ">"
    TRIANGLE_UP = "^"
    SQUARE = "s"
    HEXAGON = "H"
    PENTAGON = "p"
    DIAMOND = "D"

class PlotMode(ABC):

    def __init__(
            self, nr_of_decimals_in_text_file: int = 2,
            legend_anchor: int|str = 'upper left',
            legend_position: tuple[float,float] = (1.05, 1),
            legend_nr_of_columns: int = 1):
        self.__text_file_float_format = f'%.{nr_of_decimals_in_text_file}f'
        self.__legend_position = legend_position
        self.__legend_anchor = legend_anchor
        self.__legend_nr_of_columns = legend_nr_of_columns

    @abstractmethod
    def save_plots_for_result_type(
            self, result_type: str, x_labels: dict[int, str],
            miner_dict: dict[str, dict[object, Statistics]],
            plot_data: pd.DataFrame, markers: list, colors: list, dashes: list,
            directory: str, show_legend: bool):
        pass

    @abstractmethod
    def create_value_collector(self):
        pass

    @abstractmethod
    def add_to_value_collector(self, value, value_collector):
        pass

    @abstractmethod
    def get_x_y(self, x_dict):
        pass

    def __configure_legend(self, plot_context: PlotContext, show_legend: bool):
        if show_legend:
            plot_context.get_axes().legend(
                bbox_to_anchor=self.__legend_position,
                loc=self.__legend_anchor, borderaxespad=0.,
                ncol=self.__legend_nr_of_columns)
        else:
            plot_context.get_axes().legend().set_visible(False)

    def __configure_y_axis(self, plot_context: PlotContext, min_value: float, max_value: float):
        #make sure that plots with values between 0 and 1 always have the
        #same scale for better comparison between different plots
        if min_value >= 0 and max_value <= 1:
            plot_context.get_axes().set_ylim(0, 1)

    def __configure_x_axis(self, plot_context: PlotContext, x_labels: dict[int, str]):
        if x_labels:
            x_ticks = sorted(x_labels.keys())
            plot_context.get_axes().set_xticks(x_ticks)
            plot_context.get_axes().set_xticklabels([x_labels[x] for x in x_ticks])

    def _plot_values_for_miners(
            self, x_name: str, x_labels: dict[int, str], miner_dict,
            show_stddev: bool, show_stderr: bool,
            show_legend: bool, plot_context: PlotContext,
            directory: str, result_type: str, colors: list,
            miner_order: list[str]):
        i = 0
        min_value = float('inf')
        max_value = float('-inf')
        for miner_name in miner_order:
            x_dict = miner_dict[miner_name]
            stddevs_for_miner = []
            stderrors_for_miner = []
            mins_for_miner = []
            maxs_for_miner = []
            nr_of_values_for_miner = []
            for x, statistics in sorted(x_dict.items()):
                if show_stddev and len(statistics) > 1:
                    self.__plot_stddev_bar(
                        plot_context, colors[i], i, len(miner_dict), x, statistics)
                if show_stderr and len(statistics) > 1:
                    self.__plot_stderr_bar(
                        plot_context, colors[i], i, len(miner_dict), x, statistics)
                if len(statistics) > 1 and isinstance(statistics, Statistics):
                    stddevs_for_miner.append(statistics.stddev())
                    stderrors_for_miner.append(statistics.stddev() /
                                            math.sqrt(len(statistics)))
                if isinstance(statistics, Statistics):
                    mins_for_miner.append(statistics.minimum())
                    maxs_for_miner.append(statistics.maximum())
                    nr_of_values_for_miner.append(len(statistics))
            x_list, values_of_miner = self.get_x_y(x_dict)
            min_value = min(min_value, min(values_of_miner))
            max_value = max(max_value, max(values_of_miner))
            if not (show_stddev or show_legend or show_stderr):
                self.__save_values_to_text_file(
                    x_name, miner_name, directory, result_type, x_list, values_of_miner,
                    stddevs_for_miner, stderrors_for_miner, mins_for_miner,
                    maxs_for_miner, nr_of_values_for_miner)
            i += 1
        self.__configure_x_axis(plot_context, x_labels)
        self.__configure_y_axis(plot_context, min_value, max_value)
        plot_context.get_axes().set(xlabel=x_name, ylabel=result_type)
        self.__configure_legend(plot_context, show_legend)

    def __plot_stddev_bar(
            self, plot_context: PlotContext, color: str, miner_index: int, nr_of_miners: int,
            x, statistics_at_x: Statistics):
        plot_context.get_axes().vlines(
                x=self.__get_x_of_bar(plot_context, x, miner_index, nr_of_miners),
                ymin=(statistics_at_x.mean() - abs(statistics_at_x.stddev())),
                ymax=(statistics_at_x.mean() + abs(statistics_at_x.stddev())),
                color=color)

    def __plot_stderr_bar(
            self, plot_context: PlotContext, color: str, miner_index: int, nr_of_miners: int,
            x, statistics_at_x: Statistics):
        stderr = statistics_at_x.stddev() / math.sqrt(len(statistics_at_x))
        plot_context.get_axes().vlines(
                x=self.__get_x_of_bar(plot_context, x, miner_index, nr_of_miners),
                ymin=(statistics_at_x.mean() - abs(stderr)),
                ymax=(statistics_at_x.mean() + abs(stderr)),
                color=color)

    def __get_x_of_bar(self, plot_context: PlotContext, x, miner_index: int, nr_of_miners: int):
        dodge_index = (miner_index - nr_of_miners // 2)
        #if the number of miners is even, then there is no center index
        #=> shift right half (including center 0) of indices to the right
        if dodge_index >= 0 and nr_of_miners % 2 == 0:
            dodge_index += 1
        pixel_to_coordinate = plot_context.get_axes().transData.inverted().transform
        bar_distance = pixel_to_coordinate((4,0))[0] - pixel_to_coordinate((0,0))[0]
        return x + dodge_index * bar_distance

    def __save_values_to_text_file(
            self, x_name: str, miner_name: str, directory: str, result_type: str, x_list,
            values_of_miner, stddevs_for_miner, stderrors_for_miner, mins_for_miner,
            maxs_for_miner, nr_of_values_for_miner):
        with open(os.path.join(directory, result_type + '.txt'), 'a') as f:
            f.write('%s: %r\n' % (x_name, x_list))
            f.write('values for %s: %s\n' % (
                    miner_name, ', '.join(
                            self.__text_file_float_format % x for x in values_of_miner)))
            if stddevs_for_miner:
                f.write('stddevs for %s: %s\n' % (
                        miner_name, ', '.join(
                                self.__text_file_float_format % x for x in stddevs_for_miner)))
            if stderrors_for_miner:
                f.write('stderrs for %s: %s\n' % (
                        miner_name, ', '.join(
                                self.__text_file_float_format % x for x in stderrors_for_miner)))
            if mins_for_miner:
                f.write('min for %s: %s\n' % (
                        miner_name, ', '.join(
                                self.__text_file_float_format % x for x in mins_for_miner)))
            if maxs_for_miner:
                f.write('max for %s: %s\n' % (
                        miner_name, ', '.join(
                                self.__text_file_float_format % x for x in maxs_for_miner)))
            if nr_of_values_for_miner:
                f.write('nr of values for %s: %s\n' % (
                        miner_name, ', '.join(
                                self.__text_file_float_format % x for x in nr_of_values_for_miner)))

class _LinePlotMode(PlotMode):

    def create_value_collector(self):
        return Statistics()

    def add_to_value_collector(self, value, value_collector):
        value_collector.push(value)

    def get_x_y(self, x_dict):
        return zip(*sorted([
            (x, statistics.mean())
            for x, statistics in x_dict.items()
        ]))

    def save_plots_for_result_type(
            self, x_name: str, x_labels: dict[int, str], result_type: str,
            miner_dict: dict[str, dict[object, Statistics]],
            plot_data: pd.DataFrame, markers: list, colors: list, dashes: list,
            directory: str, show_legend: bool):
        for show_stddev, show_stderr in [(True, False), (False, True), (False, False)]:
            #skip stddev/stderr plot if no miner has more than one y-value per x-value
            if (show_stddev or show_stderr) and not any(
                    any(len(value_list) > 1 for value_list in statistics_dict.values())
                    for statistics_dict in miner_dict.values()):
                continue
            plot_filepath = self.__determine_plot_filepath(
                directory, result_type, show_legend, show_stddev, show_stderr)

            try:
                with PlotContext(show=False, use_tight_layout=True,
                                filepath=plot_filepath) as plot_context:
                    sns.lineplot(
                        data=plot_data, markers=markers, dashes=dashes,
                        palette=colors, ax=plot_context.get_axes())
                    self._plot_values_for_miners(
                        x_name, x_labels, miner_dict,
                        show_stddev, show_stderr, show_legend, plot_context,
                        directory, result_type, colors, plot_data.columns)
            except TypeError as e:
                print(f'could not create plot for {result_type} due to {e}')
                print(plot_data.to_string())

    def __determine_plot_filepath(
            self, directory, result_type, show_legend, show_stddev, show_stderr):
        plot_name = result_type
        if show_legend:
            plot_name += '_with_legend'
        if show_stddev:
            plot_name += '_with_stddev'
        if show_stderr:
            plot_name += '_with_stderr'
        plot_name += '.pdf'
        return os.path.join(directory, plot_name)

class _ScatterPlotMode(PlotMode):
    def create_value_collector(self):
        return []

    def add_to_value_collector(self, value, value_collector):
        value_collector.append(value)

    def get_x_y(self, x_dict):
        x_list = []
        y_list = []
        for x, ys in x_dict.items():
            x_list.extend([x] * len(ys))
            y_list.extend(ys)
        return x_list, y_list

    def save_plots_for_result_type(
            self, x_name: str, x_labels: dict[int, str], result_type: str,
            miner_dict: dict[str, dict[object, Statistics]],
            plot_data: pd.DataFrame, markers: list, colors: list, dashes: list,
            directory: str, show_legend: bool):
        plot_filepath = self.__determine_plot_filepath(directory, result_type, show_legend)

        with PlotContext(show=False, use_tight_layout=True,
                        filepath=plot_filepath) as plot_context:
            sns.scatterplot(data=plot_data, markers=markers,
                            palette=colors, ax=plot_context.get_axes())

            self._plot_values_for_miners(
                x_name, x_labels, miner_dict, False, False, show_legend, plot_context,
                directory, result_type, colors, plot_data.columns)

    def __determine_plot_filepath(
            self, directory, result_type, show_legend):
        plot_name = result_type
        if show_legend:
            plot_name += '_with_legend'
        plot_name += '.pdf'
        return os.path.join(directory, plot_name)


class _Modes:
    SCATTER = _ScatterPlotMode()
    LINE = _LinePlotMode()
    create_line_plot_mode = _LinePlotMode
    create_scatter_plot_mode = _ScatterPlotMode

class ResultCollector():

    colors = _Colors
    markers = _Markers
    modes = _Modes

    def __init__(self, x_name: str, mode: PlotMode = _Modes.LINE):
        self.__result_type_dict = {}
        self.__color_dict = {}
        self.__marker_dict = {}
        self.__x_name = x_name
        self.__x_labels = TwoWayDict()
        self.__mode = mode

    def add_result(self, miner_name: str, result_type: str,
                   x: int|str, value: float):
        if result_type not in self.__result_type_dict:
            self.__result_type_dict[result_type] = {}
        miner_dict = self.__result_type_dict[result_type]
        if miner_name not in miner_dict:
            miner_dict[miner_name] = {}
        x_dict = miner_dict[miner_name]
        if isinstance(x, str):
            try:
                x = next(iter(self.__x_labels.inverse(x)))
            except KeyError:
                self.__x_labels[len(self.__x_labels.dict)] = x
                x = len(self.__x_labels.dict) - 1
        if x not in x_dict:
            x_dict[x] = self.__mode.create_value_collector()
        self.__mode.add_to_value_collector(value, x_dict[x])

    def save_plots(self, directory: str):
        for result_type, miner_dict in self.__result_type_dict.items():
            plot_data, markers, colors, dashes = self.__get_plot_data(miner_dict)
            for show_legend in [True, False]:
                self.__mode.save_plots_for_result_type(
                    self.__x_name, self.__x_labels.dict, result_type, miner_dict, plot_data,
                    markers, colors, dashes,
                    directory, show_legend)
            # for show_legend, show_stddev, show_stderr in itertools.product([True, False], repeat=3):
                # if not (show_stderr and show_stddev):

    def __get_plot_data(self, miner_dict):
        plot_data = {}
        colors = []
        markers = []
        max_length_x_list = []
        for miner_name, x_dict in miner_dict.items():
            x_list, values = self.__mode.get_x_y(x_dict)
            plot_data[miner_name] = values
            colors.append(self.__color_dict.get(miner_name, _Colors.BLACK))
            markers.append(self.__marker_dict.get(miner_name, _Markers.X))
            if len(x_list) > len(max_length_x_list):
                max_length_x_list = x_list
        try:
            plot_data = pd.DataFrame.from_dict(plot_data)
        except ValueError:
            #ValueError is thrown if the miners have for this key a different
            #number of values. this usually happens if one of the miners
            #crashes during the experiments and delivers no outputs.
            #to prevent loss of the other values, we remove the deffective
            #miners for this plot.
            max_nr_of_values = max(len(v) for v in plot_data.values())
            plot_data = pd.DataFrame.from_dict({
                k: v for k,v in plot_data.items() if len(v) == max_nr_of_values
            })
            colors.remove(self.__color_dict.get(miner_name, _Colors.BLACK))
            markers.remove(self.__marker_dict.get(miner_name, _Markers.X))

        plot_data.index = max_length_x_list
        dashes = [
            "",
            (4, 1.5),
            (1, 1),
            (3, 1, 1.5, 1),
            (5, 1, 1, 1),
            (5, 1, 2, 1, 2, 1),
            (2, 2, 3, 1.5),
            (1, 2.5, 3, 1.2),
            (2, 0.3, 0.7, 0.5),
            "",
            (4, 1.5),
            (1, 1),
            (3, 1, 1.5, 1),
            (5, 1, 1, 1),
            (5, 1, 2, 1, 2, 1),
            (2, 2, 3, 1.5),
            (1, 2.5, 3, 1.2),
            (2, 0.3, 0.7, 0.5)
        ][:len(markers)]
        return plot_data, markers, colors, dashes

    def set_color(self, miner_name: str, color: str):
        self.__color_dict[miner_name] = color

    def set_marker(self, miner_name: str, marker: str):
        self.__marker_dict[miner_name] = marker