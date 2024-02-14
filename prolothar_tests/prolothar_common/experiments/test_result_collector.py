# -*- coding: utf-8 -*-

import os
import unittest

from tempfile import TemporaryDirectory
from prolothar_common.experiments.result_collector import ResultCollector

class TestResultCollector(unittest.TestCase):

    def test_plot_results_no_markers_and_colors_set(self):
        result_collector = ResultCollector('nr_of_sequences')

        result_collector.add_result('Method A', 'Metric 1', 0, 42)
        result_collector.add_result('Method A', 'Metric 1', 0, 42)
        result_collector.add_result('Method A', 'Metric 1', 1, 43)
        result_collector.add_result('Method A', 'Metric 1', 1, 43)
        result_collector.add_result('Method A', 'Metric 1', 2, 44)
        result_collector.add_result('Method A', 'Metric 1', 2, 44)
        result_collector.add_result('Method A', 'Metric 2', 0, 0.12)
        result_collector.add_result('Method A', 'Metric 2', 0, 0.12)
        result_collector.add_result('Method A', 'Metric 2', 1, 0.43)
        result_collector.add_result('Method A', 'Metric 2', 1, 0.43)
        result_collector.add_result('Method A', 'Metric 2', 2, 0.33)
        result_collector.add_result('Method A', 'Metric 2', 2, 0.33)

        result_collector.add_result('Method B', 'Metric 1', 0, 19)
        result_collector.add_result('Method B', 'Metric 1', 0, 19)
        result_collector.add_result('Method B', 'Metric 1', 1, 25)
        result_collector.add_result('Method B', 'Metric 1', 1, 25)
        result_collector.add_result('Method B', 'Metric 1', 2, 35)
        result_collector.add_result('Method B', 'Metric 1', 2, 35)
        result_collector.add_result('Method B', 'Metric 2', 0, 0.21)
        result_collector.add_result('Method B', 'Metric 2', 0, 0.21)
        result_collector.add_result('Method B', 'Metric 2', 1, 0.34)
        result_collector.add_result('Method B', 'Metric 2', 1, 0.34)
        result_collector.add_result('Method B', 'Metric 2', 2, 0.54)
        result_collector.add_result('Method B', 'Metric 2', 2, 0.54)

        with TemporaryDirectory() as temp_dir:
            result_collector.save_plots(temp_dir)
            self.assertCountEqual(
                ['Metric 1.txt', 'Metric 2.txt',
                 'Metric 1.pdf', 'Metric 1_with_legend.pdf',
                 'Metric 1_with_legend_with_stddev.pdf',
                 'Metric 1_with_legend_with_stderr.pdf',
                 'Metric 1_with_stddev.pdf', 'Metric 1_with_stderr.pdf',
                 'Metric 2.pdf', 'Metric 2_with_legend.pdf',
                 'Metric 2_with_legend_with_stddev.pdf',
                 'Metric 2_with_legend_with_stderr.pdf',
                 'Metric 2_with_stddev.pdf', 'Metric 2_with_stderr.pdf'],
                list(os.listdir(temp_dir))
            )

    def test_plot_results_no_markers_and_colors_set_only_one_value(self):
        result_collector = ResultCollector('nr_of_sequences')

        result_collector.add_result('Method A', 'Metric 1', 0, 42)
        result_collector.add_result('Method A', 'Metric 1', 1, 43)
        result_collector.add_result('Method A', 'Metric 1', 2, 44)
        result_collector.add_result('Method A', 'Metric 2', 0, 0.12)
        result_collector.add_result('Method A', 'Metric 2', 1, 0.43)
        result_collector.add_result('Method A', 'Metric 2', 2, 0.33)

        result_collector.add_result('Method B', 'Metric 1', 0, 19)
        result_collector.add_result('Method B', 'Metric 1', 1, 25)
        result_collector.add_result('Method B', 'Metric 1', 2, 35)
        result_collector.add_result('Method B', 'Metric 2', 0, 0.21)
        result_collector.add_result('Method B', 'Metric 2', 1, 0.34)
        result_collector.add_result('Method B', 'Metric 2', 2, 0.54)

        with TemporaryDirectory() as temp_dir:
            result_collector.save_plots(temp_dir)
            self.assertCountEqual(
                ['Metric 1.txt', 'Metric 2.txt',
                 'Metric 1.pdf', 'Metric 1_with_legend.pdf',
                 'Metric 2.pdf', 'Metric 2_with_legend.pdf'],
                list(os.listdir(temp_dir))
            )

    def test_plot_results_no_markers_and_colors_set_with_multiple_x_values(self):
        result_collector = ResultCollector('nr_of_sequences')

        result_collector.add_result('Method A', 'Metric 1', 0, 42)
        result_collector.add_result('Method A', 'Metric 1', 0, 24)
        result_collector.add_result('Method A', 'Metric 1', 0, 12)
        result_collector.add_result('Method A', 'Metric 1', 1000, 43)
        result_collector.add_result('Method A', 'Metric 1', 1000, 34)
        result_collector.add_result('Method A', 'Metric 1', 1000, 36)
        result_collector.add_result('Method A', 'Metric 1', 2000, 44)
        result_collector.add_result('Method A', 'Metric 1', 2000, 42)
        result_collector.add_result('Method A', 'Metric 1', 2000, 44)
        result_collector.add_result('Method A', 'Metric 1', 2000, 41)
        result_collector.add_result('Method A', 'Metric 2', 0, 0.12)
        result_collector.add_result('Method A', 'Metric 2', 1, 0.43)
        result_collector.add_result('Method A', 'Metric 2', 2, 0.33)

        result_collector.add_result('Method B', 'Metric 1', 0, 19)
        result_collector.add_result('Method B', 'Metric 1', 0, 19)
        result_collector.add_result('Method B', 'Metric 1', 0, 19)
        result_collector.add_result('Method B', 'Metric 1', 1000, 25)
        result_collector.add_result('Method B', 'Metric 1', 1000, 10)
        result_collector.add_result('Method B', 'Metric 1', 1000, 50)
        result_collector.add_result('Method B', 'Metric 1', 2000, 35)
        result_collector.add_result('Method B', 'Metric 1', 2000, 33)
        result_collector.add_result('Method B', 'Metric 1', 2000, 34)
        result_collector.add_result('Method B', 'Metric 2', 0, 0.21)
        result_collector.add_result('Method B', 'Metric 2', 1, 0.34)
        result_collector.add_result('Method B', 'Metric 2', 2, 0.54)

        with TemporaryDirectory() as temp_dir:
            result_collector.save_plots(temp_dir)
            self.assertCountEqual(
                ['Metric 1.txt', 'Metric 2.txt',
                 'Metric 1.pdf', 'Metric 1_with_legend.pdf',
                 'Metric 1_with_legend_with_stddev.pdf',
                 'Metric 1_with_legend_with_stderr.pdf',
                 'Metric 1_with_stddev.pdf', 'Metric 1_with_stderr.pdf',
                 'Metric 2.pdf', 'Metric 2_with_legend.pdf'],
                list(os.listdir(temp_dir))
            )

    def test_plot_results_with_markers_and_colors_set(self):
        result_collector = ResultCollector('nr_of_sequences')

        result_collector.add_result('Method A', 'Metric 1', 0, 42)
        result_collector.add_result('Method A', 'Metric 1', 1, 43)
        result_collector.add_result('Method A', 'Metric 1', 2, 44)
        result_collector.add_result('Method A', 'Metric 2', 0, 0.12)
        result_collector.add_result('Method A', 'Metric 2', 1, 0.43)
        result_collector.add_result('Method A', 'Metric 2', 2, 0.33)

        result_collector.add_result('Method B', 'Metric 1', 0, 19)
        result_collector.add_result('Method B', 'Metric 1', 1, 25)
        result_collector.add_result('Method B', 'Metric 1', 2, 35)
        result_collector.add_result('Method B', 'Metric 2', 0, 0.21)
        result_collector.add_result('Method B', 'Metric 2', 1, 0.34)
        result_collector.add_result('Method B', 'Metric 2', 2, 0.54)

        result_collector.set_color('Method A', ResultCollector.colors.BLUE)
        result_collector.set_color('Method B', ResultCollector.colors.RED)

        result_collector.set_marker('Method A', ResultCollector.markers.PLUS)
        result_collector.set_marker('Method B', ResultCollector.markers.PIXEL)

        with TemporaryDirectory() as temp_dir:
            result_collector.save_plots(temp_dir)
            self.assertCountEqual(
                ['Metric 1.txt', 'Metric 2.txt',
                 'Metric 1.pdf', 'Metric 1_with_legend.pdf',
                 'Metric 2.pdf', 'Metric 2_with_legend.pdf'],
                list(os.listdir(temp_dir))
            )

    def test_plot_results_with_incompatible_x_points(self):
        result_collector = ResultCollector('nr_of_sequences')

        result_collector.add_result('Method A', 'Metric 1', 0, 42)
        result_collector.add_result('Method A', 'Metric 1', 1, 43)
        result_collector.add_result('Method A', 'Metric 1', 2, 44)
        result_collector.add_result('Method A', 'Metric 2', 0, 0.12)
        result_collector.add_result('Method A', 'Metric 2', 1, 0.43)
        result_collector.add_result('Method A', 'Metric 2', 2, 0.33)

        result_collector.add_result('Method B', 'Metric 1', 0, 19)
        result_collector.add_result('Method B', 'Metric 1', 1, 25)
        result_collector.add_result('Method B', 'Metric 1', 2, 35)
        result_collector.add_result('Method B', 'Metric 2', 0, 0.21)
        result_collector.add_result('Method B', 'Metric 2', 2, 0.54)

        with TemporaryDirectory() as temp_dir:
            result_collector.save_plots(temp_dir)
            self.assertCountEqual(
                ['Metric 1.txt', 'Metric 2.txt',
                 'Metric 1.pdf', 'Metric 1_with_legend.pdf',
                 'Metric 2.pdf', 'Metric 2_with_legend.pdf'],
                list(os.listdir(temp_dir))
            )


    def test_plot_results_with_scatter_mode(self):
        result_collector = ResultCollector(
            'nr_of_sequences', mode=ResultCollector.modes.SCATTER)

        result_collector.add_result('Method A', 'Metric 1', 0, 42)
        result_collector.add_result('Method A', 'Metric 1', 0, 24)
        result_collector.add_result('Method A', 'Metric 1', 0, 12)
        result_collector.add_result('Method A', 'Metric 1', 1000, 43)
        result_collector.add_result('Method A', 'Metric 1', 1000, 34)
        result_collector.add_result('Method A', 'Metric 1', 1000, 36)
        result_collector.add_result('Method A', 'Metric 1', 2000, 44)
        result_collector.add_result('Method A', 'Metric 1', 2000, 42)
        result_collector.add_result('Method A', 'Metric 1', 2000, 44)
        result_collector.add_result('Method A', 'Metric 1', 2000, 41)
        result_collector.add_result('Method A', 'Metric 2', 0, 0.12)
        result_collector.add_result('Method A', 'Metric 2', 1, 0.43)
        result_collector.add_result('Method A', 'Metric 2', 2, 0.33)

        result_collector.add_result('Method B', 'Metric 1', 0, 19)
        result_collector.add_result('Method B', 'Metric 1', 0, 19)
        result_collector.add_result('Method B', 'Metric 1', 0, 19)
        result_collector.add_result('Method B', 'Metric 1', 1000, 25)
        result_collector.add_result('Method B', 'Metric 1', 1000, 10)
        result_collector.add_result('Method B', 'Metric 1', 1000, 50)
        result_collector.add_result('Method B', 'Metric 1', 2000, 35)
        result_collector.add_result('Method B', 'Metric 1', 2000, 33)
        result_collector.add_result('Method B', 'Metric 1', 2000, 34)
        result_collector.add_result('Method B', 'Metric 2', 0, 0.21)
        result_collector.add_result('Method B', 'Metric 2', 1, 0.34)
        result_collector.add_result('Method B', 'Metric 2', 2, 0.54)

        result_collector.set_color('Method A', ResultCollector.colors.BLUE)
        result_collector.set_color('Method B', ResultCollector.colors.RED)

        result_collector.set_marker('Method A', ResultCollector.markers.PLUS)
        result_collector.set_marker('Method B', ResultCollector.markers.PIXEL)

        with TemporaryDirectory() as temp_dir:
            result_collector.save_plots(temp_dir)
            self.assertCountEqual(
                ['Metric 1.txt', 'Metric 2.txt',
                 'Metric 1.pdf', 'Metric 1_with_legend.pdf',
                 'Metric 2.pdf', 'Metric 2_with_legend.pdf'],
                list(os.listdir(temp_dir))
            )

    def test_plot_results_with_multiple_x_string_values(self):
        result_collector = ResultCollector('category')

        result_collector.add_result('Method A', 'Metric 1', 'A', 42)
        result_collector.add_result('Method A', 'Metric 1', 'A', 24)
        result_collector.add_result('Method A', 'Metric 1', 'A', 12)
        result_collector.add_result('Method A', 'Metric 1', 'B', 43)
        result_collector.add_result('Method A', 'Metric 1', 'B', 34)
        result_collector.add_result('Method A', 'Metric 1', 'B', 36)
        result_collector.add_result('Method A', 'Metric 1', 'C', 44)
        result_collector.add_result('Method A', 'Metric 1', 'C', 42)
        result_collector.add_result('Method A', 'Metric 1', 'C', 44)
        result_collector.add_result('Method A', 'Metric 1', 'C', 41)
        result_collector.add_result('Method A', 'Metric 2', 'A', 0.12)
        result_collector.add_result('Method A', 'Metric 2', 'B', 0.43)
        result_collector.add_result('Method A', 'Metric 2', 'C', 0.33)

        result_collector.add_result('Method B', 'Metric 1', 'A', 19)
        result_collector.add_result('Method B', 'Metric 1', 'A', 19)
        result_collector.add_result('Method B', 'Metric 1', 'A', 19)
        result_collector.add_result('Method B', 'Metric 1', 'B', 25)
        result_collector.add_result('Method B', 'Metric 1', 'B', 10)
        result_collector.add_result('Method B', 'Metric 1', 'B', 50)
        result_collector.add_result('Method B', 'Metric 1', 'C', 35)
        result_collector.add_result('Method B', 'Metric 1', 'C', 33)
        result_collector.add_result('Method B', 'Metric 1', 'C', 34)
        result_collector.add_result('Method B', 'Metric 2', 'A', 0.21)
        result_collector.add_result('Method B', 'Metric 2', 'B', 0.34)
        result_collector.add_result('Method B', 'Metric 2', 'C', 0.54)

        with TemporaryDirectory() as temp_dir:
            result_collector.save_plots(temp_dir)
            self.assertCountEqual(
                ['Metric 1.txt', 'Metric 2.txt',
                 'Metric 1.pdf', 'Metric 1_with_legend.pdf',
                 'Metric 1_with_legend_with_stddev.pdf',
                 'Metric 1_with_legend_with_stderr.pdf',
                 'Metric 1_with_stddev.pdf', 'Metric 1_with_stderr.pdf',
                 'Metric 2.pdf', 'Metric 2_with_legend.pdf'],
                list(os.listdir(temp_dir))
            )


    def test_plot_results_with_different_number_of_decimals(self):
        result_collector = ResultCollector(
            'x', mode=ResultCollector.modes.create_line_plot_mode(
                nr_of_decimals_in_text_file=4))
        result_collector.add_result('Method A', 'Metric 1', 0, 0.0001)
        result_collector.add_result('Method A', 'Metric 1', 1, 0.001)
        result_collector.add_result('Method A', 'Metric 1', 2, 0.1)
        with TemporaryDirectory() as temp_dir:
            result_collector.save_plots(temp_dir)
            with open(os.path.join(temp_dir, 'Metric 1.txt')) as f:
                text = f.read()
                self.assertIn('0.0001', text)
                self.assertIn('0.001', text)
                self.assertIn('0.1', text)

        result_collector = ResultCollector(
            'x', mode=ResultCollector.modes.create_line_plot_mode(
                nr_of_decimals_in_text_file=1))
        result_collector.add_result('Method A', 'Metric 1', 0, 0.0001)
        result_collector.add_result('Method A', 'Metric 1', 1, 0.001)
        result_collector.add_result('Method A', 'Metric 1', 2, 0.1)
        with TemporaryDirectory() as temp_dir:
            result_collector.save_plots(temp_dir)
            with open(os.path.join(temp_dir, 'Metric 1.txt')) as f:
                text = f.read()
                self.assertNotIn('0.0001', text)
                self.assertNotIn('0.001', text)
                self.assertIn('0.1', text)

if __name__ == '__main__':
    unittest.main()