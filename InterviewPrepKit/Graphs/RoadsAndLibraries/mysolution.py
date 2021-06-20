#!/bin/python3

import math
import os
import random
import re
import sys
import numpy as np

#
# Complete the 'roadsAndLibraries' function below.
#
# The function is expected to return a LONG_INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. INTEGER c_lib
#  3. INTEGER c_road
#  4. 2D_INTEGER_ARRAY cities
#

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

def build_graph(n, cities, debug=False):
    g = Graph(n, debug=debug)   # undirected by default
    if debug:
        print(f"\tbuilding graph...")
    for road_city_start, road_city_end in cities:
        g.connect(road_city_start, road_city_end)   # undirected by default
    if debug:
        print(f"\t\t--> graph:\n{g._d_graph}\n")
        print(f"\t\t--> adjacency matrix:\n{np.matrix(g._adj_mat)}")
        print()

    return g

def node_visit_handler__append_path(**kwargs):
    g = kwargs['g']
    d_graph = g._d_graph
    current_node = kwargs['current_node']
    d_node = d_graph[current_node]
    depth = kwargs['depth']
    path = kwargs['path']
    debug = g._debug
    path.append(current_node)

def roadsAndLibraries(n, c_lib, c_road, cities, debug=False):
    if debug:
        print(f"n: {n}, c_lib: {c_lib}, c_road: {c_road}, cities: {cities}")

    min_cost = 0

    if c_road >= c_lib:
        min_cost = n * c_lib
        if debug:
            print(f"c_road >= c_lib --> CASE 2 IS OPTIMAL (min cost)")
            print(f"\tcost for CASE 2: 1 library for each of the {n}")
            print(f"\t\t--> n * c_lib = {n}*{c_lib} = {min_cost}")
        return min_cost
    
    if debug:
        print(f"c_road < c_lib --> must build graph and traverse DFS")

    g = build_graph(n, cities, debug=debug)

    counties = []
    if debug:
        print(f"\ttraversing graph DFS (building city-paths for each 'county')...")
    for i_node_start, node_start in g._d_graph.items():
        if i_node_start not in g.visited:
            path=[]
            g.traverse(i_node_start, fn_visit_handler=node_visit_handler__append_path, fn_visit_handler__kwargs={'path':path}, traversal_mode='DFS')
            counties.append(path)
        else:
            if debug:
                print(f"\t(start) node {i_node_start} has already been visited")
    if debug:
        print(f"\t\t--> counties: {counties}\n")

    if debug:
        print(f"\tcomputing optimal (minimal) cost for each county...")
    for path_between_cities in counties:
        n_cities = len(path_between_cities)
        n_roads = n_cities-1

        cost_case_1 = n_roads*c_road + c_lib
        cost_case_2 = n_cities * c_lib
        min_c1_c2 = min(cost_case_1, cost_case_2)
        if debug:
            print(f"\t\tfor county {path_between_cities}...")
            print(f"\t\t\tcost for case 1: 1 library accessible via city path {path_between_cities}")
            print(f"\t\t\t\t--> (n_roads * c_road) + (1 * c_lib) = ({n_roads}*{c_road})+(1*{c_lib}) = {cost_case_1}")
            print(f"\t\t\tcost for case 2: 1 library for each of the {n_cities} cities in the county")
            print(f"\t\t\t\t--> n_cities * c_lib = {n_cities}*{c_lib} = {cost_case_2}")
            print(f"\t\t\tMINIMAL COST: CASE {'2' if cost_case_2<cost_case_1 else '1'}: {min_c1_c2}\n")

        min_cost += min_c1_c2

    if debug:
        print()

    return min_cost

    
if __name__ == '__main__':
    debug = True
    output_to_file = False and debug

    s_f_indices = ['00','11','12']

    for s_f_index in s_f_indices:
        base_path = './InterviewPrepKit/Graphs/RoadsAndLibraries/'
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




        # fptr = open(os.environ['OUTPUT_PATH'], 'w')
        results = []
        q = int(input().strip())
        for q_itr in range(q):
            first_multiple_input = input().rstrip().split()
            n = int(first_multiple_input[0])
            m = int(first_multiple_input[1])
            c_lib = int(first_multiple_input[2])
            c_road = int(first_multiple_input[3])
            cities = []
            for _ in range(m):
                cities.append(list(map(int, input().rstrip().split())))
            # result = roadsAndLibraries(n, c_lib, c_road, cities)
            results.append(roadsAndLibraries(n, c_lib, c_road, cities, debug=debug))
            # fptr.write(str(result) + '\n')
        # fptr.close()




        # # single result
        # print(f"result: {result}")
        # expect = f_expect.readline().strip()
        # print(f"expect: {expect}")
        # if str(result) != expect:
        #     print(f"\t--> FAIL")
        # if not debug:
        #     assert(str(result) == expect)
        # if str(result) == expect:
        #     print(f"\t--> PASS")
        # print()

        # multiple
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
