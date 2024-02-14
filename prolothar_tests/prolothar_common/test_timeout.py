# -*- coding: utf-8 -*-

from time import sleep
import unittest
from prolothar_common.timeout import timeout

@timeout(2)
def do_something_timeout_two_seconds(duration_in_s: int) -> bool:
    sleep(duration_in_s)
    return True

class TestTimeout(unittest.TestCase):

    def test_timeout(self):
        self.assertRaises(KeyboardInterrupt, lambda: do_something_timeout_two_seconds(3))

    def test_no_timeout(self):
        self.assertTrue(do_something_timeout_two_seconds(1))

if __name__ == '__main__':
    unittest.main()