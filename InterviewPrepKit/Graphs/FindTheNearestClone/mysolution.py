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
                if debug:
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
                        if debug:
                            print(f"\t\t{s_tabs}neighbor node {neighbor_node} has already been visited")


def build_graph(n, graph_from, graph_to, colors, target_color, debug=False):
    g = Graph(n, debug=debug)
    for i_node in range(1,n+1):
        g._d_graph[i_node].update({'color':colors[i_node-1]})

    if debug:
        print(f"\tbuilding graph...")
    for i in range(len(graph_from)):
        g.connect(graph_from[i], graph_to[i])
    lst_nodes_color_match = [i_node for i_node, _ in filter(lambda t_graph_item: t_graph_item[1]['color']==target_color, g._d_graph.items())]
    if debug:
        print(f"\t\t--> graph:\n{g._d_graph}\n")
        print(f"\t\t--> adjacency matrix:\n{np.matrix(g._adj_mat)}\n")
        print(f"\t\t--> nodes matching color {target_color}: {lst_nodes_color_match}\n")

    return g, lst_nodes_color_match

def visit_handler__print_node(**kwargs):
    g = kwargs['g']
    d_graph = g._d_graph
    current_node = kwargs['current_node']
    d_node = d_graph[current_node]
    depth = kwargs['depth']
    c = d_node['color']
    target_color = kwargs['target_color']
    is_color_match = c==target_color
    d_tracking = kwargs['d_tracking']
    debug = g._debug

    if debug:
        s_tabs = '\t'*depth
        print(f"{s_tabs}\t\t--> d_graph[{current_node}]['color'] == target_color --> {c} == {target_color} --> {is_color_match}")

    if is_color_match:
        if d_tracking['start_node'] is None:
            d_tracking['start_node'] = (current_node, depth)
            if debug:
                print(f"{s_tabs}\t\t\t--> start_node is None --> set start_node={d_tracking['start_node']}")

        else:   # start_node already defined
            if d_tracking['end_node'] is None:
                d_tracking['end_node'] = (current_node, depth)
                if debug:
                    print(f"{s_tabs}\t\t\t--> end_node is None --> set end_node={d_tracking['end_node']}")
            
            else: 
                current_end_node = d_tracking['end_node']
                if depth < current_end_node[1]: # end_node already defined but reassign if new depth < old depth
                    d_tracking['end_node'] = (current_node, depth)
                    if debug:
                        print(f"{s_tabs}\t\t\t--> end_node is {current_end_node} but current depth {depth} is less --> REPLACE end_node={d_tracking['end_node']}")
                else:
                    if debug:
                        print(f"{s_tabs}\t\t\t--> end_node is {current_end_node} but current depth {depth} is NOT less --> DO NOT REPLACE end_node")

def findShortest(graph_nodes, graph_from, graph_to, ids, val, debug=False):
    if debug:
        print(f"graph_nodes: {graph_nodes}\ngraph_from: {graph_from}\ngraph_to: {graph_to}\nids: {ids}\nval: {val}\n")

    g, lst_nodes_color_match = build_graph(graph_nodes, graph_from, graph_to, ids, val, debug=debug)

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
    g.traverse(start_node, fn_visit_handler=visit_handler__print_node, fn_visit_handler__kwargs=kwargs, traversal_mode='BFS')

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
