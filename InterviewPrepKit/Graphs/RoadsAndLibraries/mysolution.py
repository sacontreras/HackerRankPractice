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

def build_graph(n, cities, debug=False):
    d_cities_graph = {}
    not_connected = set(range(1,n+1))
    if debug:
        print(f"\tbuilding graph...")
        adj_mat = [[0 for _ in range(n)] for _ in range(n)]
    for road_city_start, road_city_end in cities:
        i = road_city_start
        j = road_city_end
        
        node_i = d_cities_graph.get(i,{'to_nodes':[],'visited':False})
        node_i['to_nodes'].append(j)
        d_cities_graph[i] = node_i
        not_connected -= set([i])

        node_j = d_cities_graph.get(j,{'to_nodes':[],'visited':False})
        node_j['to_nodes'].append(i)
        d_cities_graph[j] = node_j
        not_connected -= set([j])

        if debug:
            adj_mat[i-1][j-1] = adj_mat[j-1][i-1] = 1

    for i in list(not_connected):
        node_i = d_cities_graph.get(i,{'to_nodes':[],'visited':False})
        d_cities_graph[i] = node_i

    if debug:
        print(f"\t\t--> graph:\n{d_cities_graph}\n")
        print(f"\t\t--> adjacency matrix:\n{np.matrix(adj_mat)}")
        if len(not_connected)>0:
            print(f"\t\t--> disconnected nodes: {not_connected}")
        print()

    return d_cities_graph

def traverse_graph_dfs(d_graph, i_node_start, debug=False):
    if debug:
        print(f"\t\tvisit: {i_node_start}, to_nodes: {d_graph[i_node_start]['to_nodes']}")
    path = [i_node_start]
    d_graph[i_node_start]['visited'] = True

    for to_node_i in d_graph[i_node_start]['to_nodes']:
        d_to_node = d_graph[to_node_i]
        if not d_to_node['visited']:
            _path = traverse_graph_dfs(d_graph, to_node_i, debug=debug)
            path.extend(_path)
        if debug:
            print(f"\t\t\t{to_node_i} has already been visited")

    return path

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

    d_cities_graph = build_graph(n, cities, debug=debug)

    counties = []
    if debug:
        print(f"\ttraversing graph DFS (building city-paths for each 'county')...")
    for i_node_start, node_start in d_cities_graph.items():
        if not node_start['visited']:
            counties.append(traverse_graph_dfs(d_cities_graph, i_node_start, debug=debug))
        else:
            if debug:
                print(f"\t\t{i_node_start} has already been visited")
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
