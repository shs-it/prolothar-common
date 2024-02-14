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

#include "graph.h"
#include <iostream>

//https://www.tutorialspoint.com/cplusplus-program-to-find-strongly-connected-components-in-graphs

Graph::Graph(int V)
{
    this->V = V;
    adj = new list<int>[V];
}

Graph::Graph(Graph &g)
{
    V = g.V;
    adj = new list<int>[V];
    for (int v = 0; v < V; ++v)
    {
        adj[v] = g.adj[v];
    }
}

int Graph::getNrOfNodes()
{
    return V;
}

list<int>* Graph::getAdjacencyList(int v)
{
    return &this->adj[v];
}

bool Graph::containsEdge(int v, int w)
{
    list<int>::iterator i;
    for (i = adj[v].begin(); i != adj[v].end(); ++i)
    {
        if (*i == w)
        {
            return true;
        }
    }
    return false;
}

// A recursive function to print DFS starting from v
void Graph::DFSUtil(int v, unordered_set<int> &visited, list<int> &component)
{
    // Mark the current node as visited
    visited.insert(v);
    component.push_back(v);

    // Recur for all the vertices adjacent to this vertex
    list<int>::iterator i;
    for (i = adj[v].begin(); i != adj[v].end(); ++i)
        if (visited.find(*i) == visited.end())
            DFSUtil(*i, visited, component);
}

Graph* Graph::getTranspose()
{
    Graph *g = new Graph(V);
    for (int v = 0; v < V; v++)
    {
        // Recur for all the vertices adjacent to this vertex
        list<int>::iterator i;
        for(i = adj[v].begin(); i != adj[v].end(); ++i)
        {
            g->adj[*i].push_back(v);
        }
    }
    return g;
}

void Graph::addEdge(int v, int w)
{
    adj[v].push_back(w); // Add w to v’s list.
}

void Graph::removeEdge(int v, int w)
{
    adj[v].remove(w);
}

void Graph::fillOrder(int v, unordered_set<int> &visited, stack<int> &Stack)
{
    // Mark the current node as visited and print it
    visited.insert(v);

    // Recur for all the vertices adjacent to this vertex
    list<int>::iterator i;
    for(i = adj[v].begin(); i != adj[v].end(); ++i)
        if(visited.find(*i) == visited.end())
            fillOrder(*i, visited, Stack);

    // All vertices reachable from v are processed by now, push v
    Stack.push(v);
}

// The main function that finds and prints all strongly connected
// components
list<list<int>*>* Graph::findStronglyConnectedComponents()
{
    stack<int> Stack;

    // Mark all the vertices as not visited (For first DFS)
    unordered_set<int> visited;

    // Fill vertices in stack according to their finishing times
    for(int i = 0; i < V; i++)
        if(visited.find(i) == visited.end())
            fillOrder(i, visited, Stack);

    // Create a reversed graph
    Graph *gr = getTranspose();

    // Mark all the vertices as not visited (For second DFS)
    visited.clear();

    list<list<int>*> *components = new list<list<int>*>();
    list<int> *component;

    // Now process all vertices in order defined by Stack
    while (!Stack.empty())
    {
        // Pop a vertex from stack
        int v = Stack.top();
        Stack.pop();

        // Print Strongly connected component of the popped vertex
        if (visited.find(v) == visited.end())
        {
            component = new list<int>();
            gr->DFSUtil(v, visited, *component);
            components->push_back(component);
        }
    }

    delete gr;

    return components;
}