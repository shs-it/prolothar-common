# -*- coding: utf-8 -*-

import unittest

import numpy as np

from prolothar_common.experiments.plots.plot_context import PlotContext
from prolothar_common.experiments.plots.density import plot_density

class TestDensity(unittest.TestCase):

    def test_plot_histogram(self):
        with PlotContext(show=False):
            plot_density(np.random.randn(1000), linestyle='solid')
            plot_density(np.random.randn(1000), linestyle='dashed', color='red')

if __name__ == '__main__':
    unittest.main()