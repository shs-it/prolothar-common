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
https://stackoverflow.com/questions/492519/timeout-on-a-function-call
"""

import threading
try:
    import thread
except ImportError:
    import _thread as thread

def quit_function():
    # raises KeyboardInterrupt
    thread.interrupt_main()

def timeout(s):
    '''
    use as decorator to exit process if
    function takes longer than s seconds
    '''
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, quit_function)
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer