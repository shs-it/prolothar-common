# -*- coding: utf-8 -*-

import os
import unittest
from unittest.mock import patch
import tempfile
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from prolothar_common.experiments.plots.plot_context import PlotContext
from prolothar_common.experiments.plots.plot_context import GridPlotContext

class TestPlotContext(unittest.TestCase):

    def test_plot_context_show(self):
        with patch('matplotlib.pyplot.show') as mocked_show:
            with PlotContext():
                plt.plot([1,2,3], [1,2,3])
            mocked_show.assert_called_once()

    def test_plot_context_filesave_only(self):
        with patch('matplotlib.pyplot.show') as mocked_show:
            with tempfile.TemporaryDirectory() as directory:
                path_to_plot = os.path.join(directory, 'plot.png')
                with PlotContext(show=False, filepath=path_to_plot):
                    plt.plot([1,2,3], [1,2,3])
                mocked_show.assert_not_called()
                self.assertTrue(os.path.exists(path_to_plot))

    def test_use_tight_layout(self):
        with patch('matplotlib.pyplot.tight_layout') as mock:
            with PlotContext(show=False, use_tight_layout=False):
                plt.plot([1,2,3], [1,2,3])
            mock.assert_not_called()
            with PlotContext(show=False, use_tight_layout=True):
                plt.plot([1,2,3], [1,2,3])
            mock.assert_called_once()

    def test_to_base_64(self):
        with PlotContext(show=False, use_tight_layout=False) as plot_context:
            plt.plot([1,2,3], [1,2,3])
            self.assertIsInstance(plot_context.to_base_64(), str)

    def test_grid_plot_context(self):
        with GridPlotContext(1, 1, show=False) as plot_context:
            self.assertEqual(1, len(plot_context.get_list_of_axes()))
            self.assertIsInstance(plot_context.get_axes(0, 0), Axes)

        with GridPlotContext(1, 3, show=False) as plot_context:
            self.assertEqual(3, len(plot_context.get_list_of_axes()))
            self.assertIsInstance(plot_context.get_axes(0, 0), Axes)
            self.assertIsInstance(plot_context.get_axes(0, 1), Axes)
            self.assertIsInstance(plot_context.get_axes(0, 2), Axes)
            self.assertEqual(1, plot_context.get_nr_rows())
            self.assertEqual(3, plot_context.get_nr_columns())

        with GridPlotContext(3, 1, show=False) as plot_context:
            self.assertEqual(3, len(plot_context.get_list_of_axes()))
            self.assertIsInstance(plot_context.get_axes(0, 0), Axes)
            self.assertIsInstance(plot_context.get_axes(1, 0), Axes)
            self.assertIsInstance(plot_context.get_axes(2, 0), Axes)
            self.assertEqual(3, plot_context.get_nr_rows())
            self.assertEqual(1, plot_context.get_nr_columns())

        with GridPlotContext(2, 2, show=False) as plot_context:
            self.assertEqual(4, len(plot_context.get_list_of_axes()))
            self.assertIsInstance(plot_context.get_axes(0, 0), Axes)
            self.assertIsInstance(plot_context.get_axes(1, 0), Axes)
            self.assertIsInstance(plot_context.get_axes(0, 1), Axes)
            self.assertIsInstance(plot_context.get_axes(1, 1), Axes)

    def test_plot_to_txt_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path_to_log = os.path.join(directory, 'plot.log')
            self.assertFalse(os.path.exists(path_to_log))
            with PlotContext(show=False, use_tight_layout=False, log_filepath=path_to_log):
                plt.plot([1,2,3], [1,2,3])
            self.assertTrue(os.path.exists(path_to_log))
            with open(path_to_log) as f:
                self.assertEqual(f.read().strip(), "plot(([1, 2, 3], [1, 2, 3]),{'scalex': True, 'scaley': True})")

if __name__ == '__main__':
    unittest.main()
