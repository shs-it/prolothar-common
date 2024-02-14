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

from typing import List, Tuple, Set, Union

cimport cython
from libc.math cimport log2 as clog2
from libc.math cimport log as cln
from libc.math cimport log10 as clog10
from libc.math cimport ceil as cceil
from math import log as ln
from scipy.special.cython_special cimport betaln # type: ignore
from scipy.special import gammaln as lgamma # type: ignore

from lru import LRU

_PRECOMPUTED_LN: List[float] = []
_PRECOMPUTED_SUM_LOG_I_FROM_1_TO_N: List[float] = []
_LGAMMA_CACHE = LRU(1000)

cpdef double L_N(int n) except 0.0:
    """returns the length of the code length of encoding a positive integer n
    with optimal prefix codes.
    https://www.researchgate.net/publication/38358970_A_Universal_Prior_for_Integers_and_Estimation_by_Minimum_Description_Length

    L_N(n) = log(n) + loglog(n) + logloglog(n) + ... + log(c_0)
    """
    cdef double code_length
    cdef double summand
    if n < 1:
        raise ValueError('n must be a positive integer, but is %r' % n)
    try:
        return _PRECOMPUTED_LN[n-1]
    except IndexError:
        # intialize code length to c_0 of the paper
        # c_0 is a constant based on kraft inequalitiy and ensures that the probabilites
        # of all numbers sums up to 1
        code_length = clog2(2.8565064)
        summand = clog2(n)
        while summand > 0:
            code_length += summand
            summand = clog2(summand)
        return code_length

@cython.cdivision(True)
cpdef double log2binom(int n, int k):
    """computes and returns log2(binom(n,k))
    """
    #https://stackoverflow.com/questions/21767690/python-log-n-choose-k
    #divided by ln(2) to transform to log_2
    if k == 0:
        return 0.0
    elif k == 1:
        return clog2(n)
    else:
        return (-betaln(1 + n - k, 1 + k) - cln(n + 1)) / cln(2)

def log2multinom(n: int, ks: Union[List[int],Tuple[int],Set[int]]) -> float:
    """computes the logarithm of a multinomial"""
    if n != sum(ks):
        raise ValueError('n (%d) must be the sum of all ks %r' % (n, ks))
    result = lgamma(n+1) #ln(n!)
    for k in ks:
        result -= lgamma(k+1)
    return result / ln(2)

cpdef double L_U(int m, int n):
    """computes log2binom(m-1,n-1), i.e.
    the encoded length for the number of combinations summing to m with n
    non-zero terms. L_U(0,0) := 0.
    """
    if m == 0 and n == 0:
        return 0.0
    return log2binom(m-1, n-1)

@cython.cdivision(True)
cpdef double prequential_coding_length(
        dict counts, double epsilon = 0.5):
    """computes the length in bits that is needed to encode a discrete sequence
    using prequential codes.

    Args:
        counts:
            a dictionary of the alphabet of the sequence. every symbol in the
            alphabet is assigned to its usage in the sequence.
            Dict[Hashable,int]
        epsilon:
            the initial usage (epsilon in literature) of all symbols.
            default is 0.5
    """
    cdef size_t nr_of_symbols = len(counts)
    cdef int length_of_sequence = 0
    cdef int i
    for i in counts.values():
        length_of_sequence += i

    if nr_of_symbols <= 1 or length_of_sequence == 0:
        return 0

    cdef double total_length = cached_lgamma(epsilon * nr_of_symbols + length_of_sequence)
    total_length -= cached_lgamma(epsilon * nr_of_symbols)
    cdef double symbol_usage
    for symbol_usage in counts.values():
        total_length -= (cached_lgamma(epsilon + symbol_usage) - cached_lgamma(epsilon))
    total_length = total_length / cln(2)

    return total_length

cpdef double cached_lgamma(double x):
    """
    computes the lgamma function and caches the result in a LRU cache
    """
    try:
        return _LGAMMA_CACHE[x]
    except KeyError:
        y = lgamma(x)
        _LGAMMA_CACHE[x] = y
        return y

def sum_log_i_from_1_to_n(n: int) -> float:
    """
    computes log(1) + log(2) + log(3) + ... + log(n)

    Parameters
    ----------
    n : int
        must be > 0, otherwise a ValueError is raised

    Returns
    -------
    float
        log(1) + log(2) + log(3) + ... + log(n)
    """
    if n < 1:
        raise ValueError('n must not be < 1 but was %d' % n)
    try:
        return _PRECOMPUTED_SUM_LOG_I_FROM_1_TO_N[n-1]
    except IndexError:
        return lgamma(n+1) / ln(2)

cpdef double L_R(double real_number, int precision = 5):
    """
    computes the encoded length of a real number up to a given precision
    """
    #encode sign +,-,0
    cdef double encoded_length = clog2(3)
    if real_number == 0:
        return encoded_length
    if real_number < 0:
        real_number = -real_number
    cdef int shift = int(cceil(precision - clog10(real_number)))
    #sign of shift +,-0
    encoded_length *= 2
    if shift > 0:
        encoded_length += L_N(shift) + L_N(max(<int>cceil(real_number * 10**shift), 1))
    elif shift < 0:
        encoded_length += L_N(-shift) + L_N(max(1, <int>cceil(real_number)))
    else:
        encoded_length += L_N(<int>cceil(real_number))
    return encoded_length

_PRECOMPUTED_LN = [L_N(n) for n in range(1, 101)]
_PRECOMPUTED_SUM_LOG_I_FROM_1_TO_N = [
    sum_log_i_from_1_to_n(n) for n in range(1, 101)
]