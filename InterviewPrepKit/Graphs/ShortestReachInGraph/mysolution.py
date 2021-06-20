#!/bin/python3

import math
import os
import random
import re
import sys
import numpy as np


from collections import deque
class Graph():
    def __init__(self, n, is_directed=False, node_labels=None, debug=False):
        self.is_directed = is_directed
        if node_labels is None:
            node_labels = list(range(1,n+1))
        self.node_labels = node_labels
        self._d_graph = {lbl_node:{'id':lbl_node,'neighbors':set()} for lbl_node in node_labels}
        self.visited = set()
        self._debug = debug
        if debug:
            self._adj_mat = [[0 for _ in range(n)] for _ in range(n)]

    def connect(self, from_node, to_node):
        self._d_graph[from_node]['neighbors'].add(to_node)
        if not self.is_directed:
            self._d_graph[to_node]['neighbors'].add(from_node)
        if self._debug:
            self._adj_mat[self.node_labels.index(from_node)][self.node_labels.index(to_node)] = 1
            if not self.is_directed:
                self._adj_mat[self.node_labels.index(to_node)][self.node_labels.index(from_node)] = 1

    def reset_visited(self):
        self.visited = set()

    def traverse(self, start_from_node, fn_visit_handler, fn_visit_handler__kwargs, traversal_mode='BFS'):
        nodes_pending_queue = deque()
        depth = 0
        nodes_pending_queue.append((start_from_node,depth))

        if fn_visit_handler__kwargs is None:
            fn_visit_handler__kwargs = {}
        fn_visit_handler__kwargs.update({'g':self})

        while len(nodes_pending_queue) > 0:
            current_node, depth = nodes_pending_queue.popleft() if traversal_mode=='BFS' else nodes_pending_queue.pop()     # O(1)
            d_node = self._d_graph[current_node]

            if current_node not in self.visited:
                if self._debug:
                    s_tabs = "\t"*depth
                    print(f"\t{s_tabs}(depth {depth}) visit: {current_node}, neighbors: {self._d_graph[current_node]['neighbors']}")
                kwargs = {'current_node':current_node,'depth':depth}
                fn_visit_handler__kwargs.update(kwargs)
                if fn_visit_handler:
                    fn_visit_handler(**fn_visit_handler__kwargs)
                self.visited.add(current_node)

                for neighbor_node in d_node['neighbors']:
                    if neighbor_node not in self.visited:
                        nodes_pending_queue.append((neighbor_node,depth+1))
                    else:
                        if self._debug:
                            print(f"\t\t{s_tabs}neighbor node {neighbor_node} has already been visited")


def node_visit_handler__append_path(**kwargs):
    g = kwargs['g']
    d_graph = g._d_graph
    current_node = kwargs['current_node']
    d_node = d_graph[current_node]
    depth = kwargs['depth']
    
    distance = depth * g.edge_weight
    if g._debug:
        s_tabs = '\t'*depth
        print(f"{s_tabs}\t\t--> distance from start node is: depth * edge_weight = {depth} * {g.edge_weight} = {distance}")
    g.distances[d_node['id']] = distance

def find_all_distances(g, start_from_node):   # BFS
    g.traverse(start_from_node, fn_visit_handler=node_visit_handler__append_path, fn_visit_handler__kwargs=None, traversal_mode='BFS')
    del g.distances[start_from_node]
    if g.print_distances:
        s_result = ' '.join([str(d) for d in g.distances])
        print(s_result)
    else:
        if g._debug:
            print(f"\nfind_all_distances (from start node {start_from_node}) result: {g.distances}\n")
    

if __name__ == '__main__':
    debug = True
    output_to_file = False and debug

    # s_f_indices = ['00','07','08', '01', '05']
    s_f_indices = ['00','07','08']

    for s_f_index in s_f_indices:
        base_path = './InterviewPrepKit/Graphs/ShortestReachInGraph/'
        fname_input = base_path + f'input{s_f_index}.txt'
        fname_expect = base_path + f'output{s_f_index}.txt'

        print(f"\ntesting against input file {fname_input}...")

        fd = open(fname_input)
        sys.stdin = fd

        f_expect = open(fname_expect)
        f_debug = None
        if output_to_file:
            f_debug = open(base_path+f'debug-output{s_f_index}.txt', 'w')
            sys.stdout = f_debug




        results = []
        t = int(input())
        for i in range(t):
            n,m = [int(value) for value in input().split()]
            graph = Graph(n, node_labels = list(range(n)), debug=debug)

            graph.edge_weight = 6
            graph.distances = [-1] * len(graph._d_graph)
            graph.print_distances = not debug
            graph.find_all_distances = find_all_distances

            for i in range(m):
                x,y = [int(x) for x in input().split()]
                graph.connect(x-1,y-1) 
            if debug:
                print(f"\t\t--> graph:\n{graph._d_graph}\n")
                print(f"\t\t--> adjacency matrix:\n{np.matrix(graph._adj_mat)}\n")
            s = int(input())
            graph.find_all_distances(graph, s-1)
            results.append(graph.distances)




        expect = f_expect.readlines()
        for i, l in enumerate(expect):
            _expect = l.strip()
            print(f"TEST CASE {s_f_index}.{i+1}:")
            s_result = None
            if i < len(results):
                s_result = ' '.join([str(x) for x in results[i]])
                # s_result = str(results[i])
                print(f"\tresult: {s_result}")
            else:
                print(f"\tresult: <non-existence... results only has {len(results)} elements>")
            print(f"\texpect: {_expect}")

            if s_result != _expect:
                print(f"\t\t--> FAILED on result index: {i}")
            if not debug:
                assert(_expect == s_result)
            if _expect == s_result:
                print(f"\t\t--> PASS")
            print()

        # print("\n\n")

        fd.close()
        f_expect.close()

        if output_to_file:
            f_debug.close()
            sys.stdout = sys.__stdout__

        sys.stdin = sys.__stdin__    # Reset the stdin to its default value
