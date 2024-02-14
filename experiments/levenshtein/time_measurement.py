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
This experiment benchmarks our current levenstein
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
