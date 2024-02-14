# -*- coding: utf-8 -*-

def prime_factors(n):
    """computes the primefactors of a number
    https://stackoverflow.com/questions/16996217/prime-factorization-list
    """
    f, fs = 3, []
    while n % 2 == 0:
        fs.append(2)
        n /= 2
    while f * f <= n:
        while n % f == 0:
            fs.append(int(f))
            n /= f
        f += 2
    if n > 1: fs.append(int(n))
    return fs