#ifndef RECTANGLE_H
#define RECTANGLE_H

#include <list>
#include <stack>
#include <unordered_set>
using namespace std;

class Graph
{
    int V;    // No. of vertices
    list<int> *adj;    // An array of adjacency lists

    // Fills Stack with vertices (in increasing order of finishing
    // times). The top element of stack has the maximum finishing
    // time
    void fillOrder(int v, unordered_set<int> &visited, stack<int> &Stack);

    // A recursive function to print DFS starting from v
    void DFSUtil(int v, unordered_set<int> &visited, list<int> &component);

public:
    Graph(int V);
    Graph(Graph &g);
    ~Graph () { delete[] adj; }

    int getNrOfNodes();

    void addEdge(int v, int w);
    void removeEdge(int v, int w);
    bool containsEdge(int v, int w);

    list<int>* getAdjacencyList(int v);

    // The main function that finds and prints strongly connected
    // components
    list<list<int>*>* findStronglyConnectedComponents();

    // Function that returns reverse (or transpose) of this graph
    Graph* getTranspose();
};

#endif