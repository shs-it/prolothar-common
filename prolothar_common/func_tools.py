"""
utils for functional programming
"""
from functools import total_ordering

def do_nothing(*args, **kwargs):
    """
    a method that accepts any number of parameters and does nothing
    """

def identity(x):
    """
    just returns x
    """
    return x

@total_ordering
class _MinType(object):
    """
    defines a type that is smaller than everything
    """
    def __le__(self, other):
        return True

    def __eq__(self, other):
        return (self is other)

Min = _MinType()
