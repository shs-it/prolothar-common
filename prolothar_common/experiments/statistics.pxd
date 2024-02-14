cdef class Statistics:

    cdef unsigned long _count
    cdef double _mean, _rho, _tau, _phi, _min, _max

    cpdef push(self, double value)
    cpdef merge(self, Statistics other)
    cpdef double minimum(self)
    cpdef double maximum(self)
    cpdef double mean(self)
    cpdef double variance(self, int degrees_of_freedom = ?)
    cpdef double stddev(self, int degrees_of_freedom = ?)
