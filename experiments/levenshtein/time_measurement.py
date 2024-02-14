"""
This experiments compares our current longest_common_subsequence cython
implementation with the naive python version
"""

from random import Random
import string

from prolothar_common.experiments.stopwatch import Stopwatch
from prolothar_common.levenshtein import levenshtein_with_backtrace

stopwatch = Stopwatch()

random = Random(42)
strings = [
    ''.join(random.choices(string.ascii_uppercase, k=random.randint(1,50))) for _ in range(1000)
]
candidate_pairs = [
    (random.choice(strings), random.choice(strings)) for _ in range(100000)
]

def benchmark(method, name):
    stopwatch.start()
    for x,y in candidate_pairs:
        lcs, b = method(x,y)
        assert lcs == len(b)
    print('%s: %r' % (name, stopwatch.get_elapsed_time()))

benchmark(levenshtein_with_backtrace, 'levenshtein_with_backtrace')
