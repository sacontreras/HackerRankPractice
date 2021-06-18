#!/bin/python3

from collections import deque
import math
import os
import random
import re
import sys
import numpy as np

# Complete the findShortest function below.

#
# For the weighted graph, <name>:
#
# 1. The number of nodes is <name>_nodes.
# 2. The number of edges is <name>_edges.
# 3. An edge exists between <name>_from[i] to <name>_to[i].
#
#

def build_graph(n, graph_from, graph_to, colors, target_color, debug=False):
    d_graph = {}
    disconnected = set(range(1,n+1))
    if debug:
        print(f"\tbuilding graph...")
        adj_mat = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(len(graph_from)):
        i_from_node = graph_from[i]
        i_to_node = graph_to[i]
        
        from_node = d_graph.get(i_from_node,{'to_nodes':[],'color':colors[i_from_node-1],'visited':False})
        from_node['to_nodes'].append(i_to_node)
        d_graph[i_from_node] = from_node
        disconnected -= set([i_from_node])

        to_node = d_graph.get(i_to_node,{'to_nodes':[],'color':colors[i_to_node-1],'visited':False})
        to_node['to_nodes'].append(i_from_node)
        d_graph[i_to_node] = to_node
        disconnected -= set([i_to_node])

        if debug:
            adj_mat[i_from_node-1][i_to_node-1] = adj_mat[i_to_node-1][i_from_node-1] = 1

    for i in list(disconnected):
        node_i = d_graph.get(i,{'to_nodes':[],'color':colors[i-1],'visited':False})
        d_graph[i] = node_i

    lst_nodes_color_match = [i_node for i_node, _ in filter(lambda t_graph_item: t_graph_item[1]['color']==target_color, d_graph.items())]

    if debug:
        print(f"\t\t--> graph:\n{d_graph}\n")
        print(f"\t\t--> adjacency matrix:\n{np.matrix(adj_mat)}\n")
        print(f"\t\t--> nodes matching color {target_color}: {lst_nodes_color_match}\n")

    return d_graph, lst_nodes_color_match

def visit_handler__print_node(**kwargs):
    d_graph = kwargs['d_graph']
    i_node = kwargs['i_node']
    d_node = d_graph[i_node]
    depth = kwargs['depth']
    c = d_node['color']
    target_color = kwargs['target_color']
    is_color_match = c==target_color
    d_tracking = kwargs['d_tracking']
    debug = kwargs['debug']

    if debug:
        s_tabs = '\t'*depth
        print(f"{s_tabs}depth: {depth}, visit: {i_node} --> d_graph[{i_node}]['color'] == target_color --> {c} == {target_color} --> {is_color_match}")

    if is_color_match:
        if d_tracking['start_node'] is None:
            d_tracking['start_node'] = (i_node, depth)
            if debug:
                print(f"{s_tabs}\t--> start_node is None --> set start_node={d_tracking['start_node']}")

        else:   # start_node already defined
            if d_tracking['end_node'] is None:
                d_tracking['end_node'] = (i_node, depth)
                if debug:
                    print(f"{s_tabs}\t--> end_node is None --> set end_node={d_tracking['end_node']}")
            
            else: 
                current_end_node = d_tracking['end_node']
                if depth < current_end_node[1]: # end_node already defined but reassign if new depth < old depth
                    d_tracking['end_node'] = (i_node, depth)
                    if debug:
                        print(f"{s_tabs}\t--> end_node is {current_end_node} but current depth {depth} is less --> REPLACE end_node={d_tracking['end_node']}")
                else:
                    if debug:
                        print(f"{s_tabs}\t--> end_node is {current_end_node} but current depth {depth} is NOT less --> DO NOT REPLACE end_node")


def traverse_graph_BFS(d_graph, i_node_start, fn_visit_handler, fn_visit_handler__kwargs, debug=False):
    if fn_visit_handler__kwargs is None:
        fn_visit_handler__kwargs = {'full_bfs_path':[]}
    nodes_pending_queue = []
    depth = 0
    nodes_pending_queue.insert(0, (i_node_start,depth))
    while len(nodes_pending_queue) > 0:
        i_node, depth = nodes_pending_queue.pop()
        d_node = d_graph[i_node]

        kwargs = {'d_graph':d_graph,'i_node':i_node,'depth':depth,'debug':debug}
        fn_visit_handler__kwargs.update(kwargs)
        fn_visit_handler(**fn_visit_handler__kwargs)
        d_node['visited'] = True

        for i_node_neighbor in d_node['to_nodes']:
            d_node_neighbor = d_graph[i_node_neighbor]
            if not d_node_neighbor['visited']:
                nodes_pending_queue.insert(0, (i_node_neighbor,depth+1))

def findShortest(graph_nodes, graph_from, graph_to, ids, val, debug=False):
    if debug:
        print(f"graph_nodes: {graph_nodes}\ngraph_from: {graph_from}\ngraph_to: {graph_to}\nids: {ids}\nval: {val}\n")

    d_graph, lst_nodes_color_match = build_graph(graph_nodes, graph_from, graph_to, ids, val, debug=debug)

    if len(lst_nodes_color_match) < 2:
        if debug:
            print(f"short-circuit since len(lst_nodes_color_match)<2 --> start/end path for target color {val} DOES NOT EXIST")
        return -1

    if debug:
        print(f"len(d_graph_color_match)>=2 --> traversing graph BFS to find shortest path for target color {val} ...")
    start_node = lst_nodes_color_match[0]
    d_tracking = {'start_node':None,'end_node':None}
    kwargs = {
        'target_color':val,
        'd_tracking':d_tracking
    }
    traverse_graph_BFS(d_graph, start_node, fn_visit_handler=visit_handler__print_node, fn_visit_handler__kwargs=kwargs, debug=debug)

    start_node = d_tracking['start_node']
    end_node = d_tracking['end_node']
    l_shortest_path = end_node[1]-start_node[1] if (start_node is not None) and (end_node is not None) else -1
    if debug:
        if l_shortest_path != -1:
            print(f"shortest BFS path for target color {val} starts with node {start_node[0]} (at depth {start_node[1]}) and ends with node {end_node[0]} (at depth {end_node[1]})")
        else:
            print(f"but start/end path for target color {val} DOES NOT EXIST")

    return l_shortest_path
    

if __name__ == '__main__':
    debug = True
    output_to_file = False and debug

    s_f_indices = ['00','01','12']

    for s_f_index in s_f_indices:
        base_path = './InterviewPrepKit/Graphs/FindTheNearestClone/'
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
        graph_nodes, graph_edges = map(int, input().split())
        graph_from = [0] * graph_edges
        graph_to = [0] * graph_edges
        for i in range(graph_edges):
            graph_from[i], graph_to[i] = map(int, input().split())
        ids = list(map(int, input().rstrip().split()))
        val = int(input())
        # ans = findShortest(graph_nodes, graph_from, graph_to, ids, val)
        results.append(findShortest(graph_nodes, graph_from, graph_to, ids, val, debug=debug))
        # fptr.write(str(ans) + '\n')
        # fptr.close()




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
