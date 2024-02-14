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
This experiment compares our current longest_common_subsequence cython
implementation with the naive python version
"""

from typing import List, Tuple

from random import Random
import string
import numpy as np

from prolothar_common.experiments.stopwatch import Stopwatch
from prolothar_common.longest_common_subsequence import lcs_with_backtrace

def py_lcs_with_backtrace(x_list: List, y_list: List) -> Tuple[int, List[Tuple[int,int]]]:
    C = np.zeros((len(x_list) + 1, len(y_list) + 1), dtype=int)

    for i, x in enumerate(x_list):
        for j, y in enumerate(y_list):
            if x == y:
                C[i+1,j+1] = C[i,j] + 1
            else:
                C[i+1,j+1] = max(C[i+1,j],C[i,j+1])

    #Backtrace
    i = len(x_list)
    j = len(y_list)
    backtrace: List[Tuple[int, int]] = []
    while i != 0 and j != 0:
        if x_list[i-1] == y_list[j-1]:
            i -= 1
            j -= 1
            backtrace.append((i,j))
        elif C[i-1,j] > C[i,j-1]:
            i -= 1
        else:
            j -= 1
    return C[-1,-1], backtrace[::-1]

def py_lcs_with_backtrace2(x_list: List, y_list: List) -> Tuple[int, List[Tuple[int,int]]]:
    C = [[0] * (len(y_list) + 1) for _ in range(len(x_list) + 1)]
    for i, ca in enumerate(x_list, 1):
        for j, cb in enumerate(y_list, 1):
            C[i][j] = (
                C[i - 1][j - 1] + 1 if ca == cb else
                max(C[i][j - 1], C[i - 1][j]))

    #Backtrace
    i = len(x_list)
    j = len(y_list)
    backtrace: List[Tuple[int, int]] = []
    while i != 0 and j != 0:
        if x_list[i-1] == y_list[j-1]:
            i -= 1
            j -= 1
            backtrace.append((i,j))
        elif C[i-1][j] > C[i][j-1]:
            i -= 1
        else:
            j -= 1
    return C[-1][-1], backtrace[::-1]

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

benchmark(py_lcs_with_backtrace, 'pure python version using numpy')
benchmark(py_lcs_with_backtrace2, 'pure python version using a 2-d list')
benchmark(lcs_with_backtrace, 'cython version')
