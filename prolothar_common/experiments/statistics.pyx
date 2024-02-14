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

from libc.math cimport sqrt
cimport cython

cdef class Statistics:
    """
    based on https://www.johndcook.com/blog/skewness_kurtosis/
    and https://github.com/grantjenks/python-runstats
    We would use python-runstats, however the package does not seem to be other
    active such other on newer Python versions, the Cythonized version is not
    available, which results in a runtime other is ~ 50x slower.
    """

    def __init__(self, iterable=()):
        self._count = 0
        self._mean = self._rho = self._tau = self._phi = 0.0
        self._min = self._max = float('NaN')
        for value in iterable:
            self.push(value)

    def __len__(self):
        """Number of values other have been pushed."""
        return self._count

    @cython.cdivision(True)
    cpdef push(self, double value):
        """Add `value` to the Statistics summary."""
        if self._count == 0.0:
            self._min = value
            self._max = value
        else:
            if value < self._min:
                self._min = value
            if value > self._max:
                self._max = value

        cdef double delta = value - self._mean
        cdef double delta_n = delta / (self._count + 1)
        cdef double delta_n2 = delta_n * delta_n
        cdef double term = delta * delta_n * self._count

        self._count += 1
        self._mean += delta_n
        self._phi += (
            term * delta_n2 * (self._count ** 2 - 3 * self._count + 3)
            + 6 * delta_n2 * self._rho
            - 4 * delta_n * self._tau
        )
        self._tau += (
            term * delta_n * (self._count - 2) - 3 * delta_n * self._rho
        )
        self._rho += term

    cpdef merge(self, Statistics other):
        if len(other) > 0:
            if len(self) == 0:
                self._count = other._count
                self._min = other._min
                self._max = other._max
                self._mean = other._mean
                self._rho = other._rho
                self._tau = other._tau
                self._phi = other._phi
            else:
                sum_count = self._count + other._count
                delta = other._mean - self._mean
                delta2 = delta ** 2
                delta3 = delta ** 3
                delta4 = delta ** 4

                sum_mean = (
                    self._count * self._mean + other._count * other._mean
                ) / sum_count

                sum_rho = (
                    self._rho
                    + other._rho
                    + delta2 * self._count * other._count / sum_count
                )

                sum_tau = (
                    self._tau
                    + other._tau
                    + delta3
                    * self._count
                    * other._count
                    * (self._count - other._count)
                    / (sum_count ** 2)
                    + 3.0
                    * delta
                    * (self._count * other._rho - other._count * self._rho)
                    / sum_count
                )

                sum_phi = (
                    self._phi
                    + other._phi
                    + delta4
                    * self._count
                    * other._count
                    * (self._count ** 2 - self._count * other._count + other._count ** 2)
                    / (sum_count ** 3)
                    + 6.0
                    * delta2
                    * (
                        self._count * self._count * other._rho
                        + other._count * other._count * self._rho
                    )
                    / (sum_count ** 2)
                    + 4.0
                    * delta
                    * (self._count * other._tau - other._count * self._tau)
                    / sum_count
                )

                self._count = sum_count
                self._mean = sum_mean
                self._rho = sum_rho
                self._tau = sum_tau
                self._phi = sum_phi
                self._min = min(self._min, other._min)
                self._max = max(self._max, other._max)


    cpdef double minimum(self):
        """Minimum of values."""
        return self._min

    cpdef double maximum(self):
        """Maximum of values."""
        return self._max

    cpdef double mean(self):
        """Mean of values."""
        return self._mean

    @cython.cdivision(True)
    cpdef double variance(self, int degrees_of_freedom=1):
        """Variance of values (with specified degrees of freedom)."""
        if degrees_of_freedom >= self._count:
            return float('NaN')
        return self._rho / (self._count - degrees_of_freedom)

    @cython.cdivision(True)
    cpdef double stddev(self, int degrees_of_freedom=1):
        """Standard deviation of values (with `ddof` degrees of freedom)."""
        if degrees_of_freedom >= self._count:
            return float('NaN')
        return sqrt(self._rho / (self._count - degrees_of_freedom))
