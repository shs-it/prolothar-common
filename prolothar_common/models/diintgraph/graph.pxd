from libcpp.list cimport list as cpplist

cdef extern from 'graph.cpp':
    pass

cdef extern from 'graph.h':
    cdef cppclass Graph:
        Graph(int) except +
        Graph(Graph&) except +
        void addEdge(int, int)
        void removeEdge(int, int)
        bint containsEdge(int, int)
        cpplist[cpplist[int]*]* findStronglyConnectedComponents()
        cpplist[int]* getAdjacencyList(int)
        int getNrOfNodes()