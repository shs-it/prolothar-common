# -*- coding: utf-8 -*-

import unittest

import numpy as np

from prolothar_common.experiments.plots.plot_context import PlotContext
from prolothar_common.experiments.plots.histogram import plot_counts
from prolothar_common.experiments.plots.histogram import plot_histogram

class TestHistogram(unittest.TestCase):

    def test_plot_counts(self):
        with PlotContext(show=False):
            plot_counts(['a', 'b', 'b', 'a', 'a', 'c', 'b', 'b', 'b', 'b'])
        with PlotContext(show=False):
            plot_counts(['a', 'b', 'b', 'a', 'a', 'c', 'b', 'b', 'b', 'b'],
                        order_by='frequency_asc')
        with PlotContext(show=False):
            plot_counts(['a', 'b', 'b', 'a', 'a', 'c', 'b', 'b', 'b', 'b'],
                        order_by='frequency_desc')

    def test_plot_histogram(self):
        with PlotContext(show=False):
            plot_histogram(np.random.randn(1000), nr_of_bins=10)

    def test_plot_two_histograms(self):
        with PlotContext(show=False):
            plot_histogram(
                np.random.randn(1000), nr_of_bins=10,
                histtype='step', linestyle='dashed', density=True)
            plot_histogram(
                np.random.randn(1000), nr_of_bins=10,
                histtype='step', linestyle='dotted', density=True)
        with PlotContext(show=False) as plot_context:
            plot_histogram(
                np.random.randn(1000), nr_of_bins=10,
                alpha=0.5, density=True)
            plot_histogram(
                np.random.randn(1000), nr_of_bins=10,
                alpha=0.5, density=True)
            plot_context.get_axes().legend(['1', '2'])

if __name__ == '__main__':
    unittest.main()