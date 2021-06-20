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
        traversal_mode = traversal_mode.upper()
        if traversal_mode != 'BFS':
            traversal_mode = 'DFS'

        if self._debug:
            print(f"traversing graph {traversal_mode} starting from node {start_from_node}...")

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

#
# Complete the 'maxRegion' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY grid as parameter.
#

def build_graph(grid, debug=False):
    m = len(grid)
    n = len(grid[0])

    node_labels = []
    for r in range(m):
        for c in range(n):
            node_labels.append((r,c))
    n_node_label_map = len(node_labels)
    g = Graph(n_node_label_map, node_labels=node_labels, is_directed=True, debug=debug)

    # def get_node_label(r,c, mode='index'):
    def get_node_label(r,c, mode='tuple'):
        return node_labels.index((r,c)) if mode=='index' else (r,c)

    for r in range(m):
        for c in range(n):
            from_node = get_node_label(r,c)
            if r-1 >= 0:
                if grid[r-1][c] == 1:
                    to_node = get_node_label(r-1,c)
                    g.connect(from_node, to_node)
                if c-1 >= 0:
                    if grid[r-1][c-1] == 1:
                        to_node = get_node_label(r-1,c-1)
                        g.connect(from_node=from_node, to_node=to_node)
                if c+1 < len(grid[r]):
                    if grid[r-1][c+1] == 1:
                        to_node = get_node_label(r-1,c+1)
                        g.connect(from_node, to_node)

            if r+1 < len(grid):
                if grid[r+1][c] == 1:
                    to_node = get_node_label(r+1,c)
                    g.connect(from_node, to_node)
                if c-1 >= 0:
                    if grid[r+1][c-1] == 1:
                        to_node = get_node_label(r+1,c-1)
                        g.connect(from_node, to_node)
                if c+1 < len(grid[r]):
                    if grid[r+1][c+1] == 1:
                        to_node = get_node_label(r+1,c+1)
                        g.connect(from_node, to_node)

            if c-1 >= 0:
                if grid[r][c-1] == 1:
                    to_node = get_node_label(r,c-1)
                    g.connect(from_node, to_node)
                
            if c+1 < len(grid[r]):
                if grid[r][c+1] == 1:
                    to_node = get_node_label(r,c+1)
                    g.connect(from_node, to_node)

    if debug:
        print(f"\t\t--> node labels (grid coordinates): {g.node_labels}\n")
        print(f"\t\t--> ({'un' if not g.is_directed else ''}directed) graph:\n{g._d_graph}\n")
        print(f"\t\t--> corresponding adjacency matrix:\n{np.matrix(g._adj_mat)}\n")

    return g


def node_visit_handler__append_region(**kwargs):
    g = kwargs['g']
    d_graph = g._d_graph
    current_node = kwargs['current_node']
    d_node = d_graph[current_node]
    depth = kwargs['depth']
    region = kwargs['region']
    debug = g._debug
    region.append(current_node)

def maxRegion(grid, debug=False):
    max_region = 0

    if debug:
        grid_mat = np.matrix(grid)
        print(f"grid:\n{grid_mat} is {grid_mat.shape[0]} x {grid_mat.shape[1]}\n")

    g = build_graph(grid, debug=debug)

    regions = []
    max_region = None
    max_region_index = None
    for i, start_node in enumerate(g.node_labels):
        region = []
        if grid[start_node[0]][start_node[1]]==1 and start_node not in g.visited:
            g.traverse(start_node, fn_visit_handler=node_visit_handler__append_region, fn_visit_handler__kwargs={'region':region}, traversal_mode='DFS')
            if debug:
                print(f"\n\t--> region: {region}\n")
            region_size = len(region)
            if max_region is None or region_size>max_region:
                max_region_index = len(regions)
                max_region = region_size
            regions.append(region)
        # else:
        #     if debug:
        #         print(f"\n\t\t--> start node {start_node} is not in a region or has already been visited\n")
    if debug:
        print(f"\t--> max region (size {max_region}): {regions[max_region_index]}\n")

    return max_region
    

if __name__ == '__main__':
    debug = True
    output_to_file = False and debug

    s_f_indices = ['00','01','07']

    for s_f_index in s_f_indices:
        base_path = './InterviewPrepKit/Graphs/ConnectedCellInGrid/'
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
        # fptr = open(os.environ['OUTPUT_PATH'], 'w')
        n = int(input().strip())
        m = int(input().strip())
        grid = []
        for _ in range(n):
            grid.append(list(map(int, input().rstrip().split())))
        res = maxRegion(grid, debug=debug)
        # fptr.write(str(res) + '\n')
        # fptr.close()
        results.append(res)




        expect = f_expect.readlines()
        for i, l in enumerate(expect):
            _expect = l.strip()
            print(f"TEST CASE {s_f_index}.{i+1}:")
            s_result = None
            if i < len(results):
                # s_result = ' '.join([str(x) for x in results[i]])
                s_result = str(results[i])
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
