"""
https://stackoverflow.com/questions/492519/timeout-on-a-function-call
"""

import sys
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