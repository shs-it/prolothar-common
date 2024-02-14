/*
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
*/

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