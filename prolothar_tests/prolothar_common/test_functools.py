# -*- coding: utf-8 -*-

import unittest
from prolothar_common.func_tools import identity
from prolothar_common.func_tools import do_nothing

class TestFuncTools(unittest.TestCase):

    def test_identity(self):
        for x in [0, 42, 'abc', None]:
            self.assertEqual(x, identity(x))

    def test_do_nothing(self):
        do_nothing()
        do_nothing(42)
        do_nothing('42')
        do_nothing(x=42)
        do_nothing(42, 43, x=42, y=123)

if __name__ == '__main__':
    unittest.main()