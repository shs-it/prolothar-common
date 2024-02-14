# -*- coding: utf-8 -*-

import unittest
from prolothar_common.console_utils import nullify_output

class TestConsoleUtils(unittest.TestCase):

    def test_nullify_output(self):
        with nullify_output(suppress_stdout=True):
            print('abc')

if __name__ == '__main__':
    unittest.main()