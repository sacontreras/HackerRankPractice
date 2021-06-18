#!/bin/python3

import math
import os
import random
import re
import sys
import numpy as np
from collections import deque


class Graph():
    def __init__(self, n, edge_weight=6, print_distances=True, debug=False):
        self._d_graph = {lbl_node:{'id':lbl_node,'neighbors':set(),'visited':False} for lbl_node in range(n)}
        self.edge_weight = edge_weight
        self.distances = [-1] * len(self._d_graph)
        self.print_distances = print_distances
        self._debug = debug
        if debug:
            self._adj_mat = [[0 for _ in range(n)] for _ in range(n)]

    def connect(self, from_node, to_node):  # these are zero-based
        self._d_graph[from_node]['neighbors'].add(to_node)
        self._d_graph[to_node]['neighbors'].add(from_node)
        if self._debug:
            self._adj_mat[from_node][to_node] = self._adj_mat[to_node][from_node] = 1

    def __traverse_graph_BFS(self, from_node):
        nodes_pending_queue = deque()
        depth = 0
        nodes_pending_queue.append((from_node,depth))

        while len(nodes_pending_queue) > 0:
            current_node, depth = nodes_pending_queue.popleft()
            d_node = self._d_graph[current_node]

            if not d_node['visited']:
                distance = depth * self.edge_weight
                if self._debug:
                    s_tabs = '\t'*depth
                    print(f"{s_tabs}depth: {depth}, visit: {current_node} --> distance from node {from_node} is: {distance}")
                self.distances[d_node['id']] = distance
                d_node['visited'] = True

                for neighbor_node in d_node['neighbors']:
                    d_node_neighbor = self._d_graph[neighbor_node]
                    if not d_node_neighbor['visited']:
                        nodes_pending_queue.append((neighbor_node,depth+1))

        del self.distances[from_node]


    def find_all_distances(self, from_node):   # BFS
        self.__traverse_graph_BFS(from_node)
        if self.print_distances:
            s_result = ' '.join([str(d) for d in self.distances])
            print(s_result)
    

if __name__ == '__main__':
    debug = False
    output_to_file = False and debug

    s_f_indices = ['00','07','08', '01', '05']

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
            graph = Graph(n, print_distances=False, debug=debug)
            for i in range(m):
                x,y = [int(x) for x in input().split()]
                graph.connect(x-1,y-1) 
            if debug:
                print(f"\t\t--> graph:\n{graph._d_graph}\n")
                print(f"\t\t--> adjacency matrix:\n{np.matrix(graph._adj_mat)}\n")
            s = int(input())
            graph.find_all_distances(s-1)
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
