# -*- coding: utf-8 -*-

import unittest
import numpy as np
from prolothar_common.experiments.plots.heatmap import plot_heatmap
from prolothar_common.experiments.plots.heatmap import annotate_heatmap

class TestHeatmap(unittest.TestCase):

    def test_plot_heatmap_wrong_number_of_dimensions(self):
        with self.assertRaises(ValueError):
            plot_heatmap(
                np.array([[[1,2], [4,0]], [[0,1], [0,1]]]),
                ['row_1', 'row_2'],
                ['col_1', 'col_2']
            )

    def test_plot_heatmap_not_enough_row_labels(self):
        with self.assertRaises(ValueError):
            plot_heatmap(
                np.array([[1,2], [4,0]]),
                ['row_1'],
                ['col_1', 'col_2']
            )

    def test_plot_heatmap_not_enough_column_labels(self):
        with self.assertRaises(ValueError):
            plot_heatmap(
                np.array([[1,2], [4,0]]),
                ['row_1', 'row_2'],
                ['col_1']
            )

    def test_plot_heatmap_with_colorbar(self):
        heatmap, colorbar = plot_heatmap(
            np.array([[1,2,3], [4,0,2]]),
            ['row_1', 'row_2'],
            ['col_1', 'col_2', 'col_3'],
            cmap='YlGn'
        )
        self.assertIsNotNone(heatmap)
        self.assertIsNotNone(colorbar)

    def test_plot_heatmap_without_colorbar(self):
        data = np.array([[1,2,3], [4,0,2]])
        heatmap, colorbar = plot_heatmap(
            data,
            ['row_1', 'row_2'],
            ['col_1', 'col_2', 'col_3'],
            show_colorbar=False
        )
        self.assertIsNotNone(heatmap)
        np.testing.assert_array_equal(data, heatmap.get_array())
        self.assertIsNone(colorbar)

    def test_plot_heatmap_large_values(self):
        data = np.array([[1000,2000,3000], [4000,0,2001]])
        heatmap, colorbar = plot_heatmap(
            data,
            ['row_1', 'row_2'],
            ['col_1', 'col_2', 'col_3'],
            show_colorbar=False
        )
        self.assertIsNotNone(heatmap)
        np.testing.assert_array_equal(data, heatmap.get_array())
        self.assertIsNone(colorbar)

    def test_annotate_heatmap(self):
        heatmap, _ = plot_heatmap(
            np.array([[1,2,3], [4,0,2]]),
            ['row_1', 'row_2'],
            ['col_1', 'col_2', 'col_3'],
            show_colorbar=False
        )
        texts = annotate_heatmap(heatmap, valfmt="{x:.1f} t")
        self.assertListEqual(
            ['1.0 t', '2.0 t', '3.0 t', '4.0 t', '0.0 t', '2.0 t'],
            [text.get_text() for text in texts]
        )

if __name__ == '__main__':
    unittest.main()