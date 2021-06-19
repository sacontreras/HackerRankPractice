[link](https://www.hackerrank.com/challenges/find-the-nearest-clone/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=graphs)


## First Try:

Like all graph-theory puzzles, this puzzle is not super tricky.  But it definitely requires a full understanding of graphs and their corresponding traversals, BFS in particular.

Of course, a full understanding of the requirements was essential (as always).  This naturally leads one to understanding that BFS (instead of DFS) is required in this case.

The remainder of the puzzle required designing an effective means to track auxiliary information.  Specifically, both start and end nodes must be tracked and, more importantly, the corresponding depths.

This algorithm constructs the BFS traversal and sets both the start end and nodes with the corresponding color match.  If not both are set, then return -1.  Otherwise, slice the path from the starting node to the end node with minimal depth.

With this approach, all free test-cases passed.  Upon submission, all remaining locked test-cases passed.

(see below for my full implementation of this algorithm)


```python
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
```

<p><br>

(Debug) Output for test-case 00:

```
graph_nodes: 4
graph_from: [1, 1, 4]
graph_to: [2, 3, 2]
ids: [1, 2, 1, 1]
val: 1

        building graph...
                --> graph:
{1: {'to_nodes': [2, 3], 'color': 1, 'visited': False}, 2: {'to_nodes': [1, 4], 'color': 2, 'visited': False}, 3: {'to_nodes': [1], 'color': 1, 'visited': False}, 4: {'to_nodes': [2], 'color': 1, 'visited': False}}

                --> adjacency matrix:
[[0 1 1 0]
 [1 0 0 1]
 [1 0 0 0]
 [0 1 0 0]]

                --> nodes matching color 1: [1, 3, 4]

len(d_graph_color_match)>=2 --> traversing graph BFS to find shortest path for target color 1 ...
depth: 0, visit: 1 --> d_graph[1]['color'] == target_color --> 1 == 1 --> True
        --> start_node is None --> set start_node=(1, 0)
        depth: 1, visit: 2 --> d_graph[2]['color'] == target_color --> 2 == 1 --> False
        depth: 1, visit: 3 --> d_graph[3]['color'] == target_color --> 1 == 1 --> True
                --> end_node is None --> set end_node=(3, 1)
                depth: 2, visit: 4 --> d_graph[4]['color'] == target_color --> 1 == 1 --> True
                        --> end_node is (3, 1) but current depth 2 is NOT less --> DO NOT REPLACE end_node
shortest BFS path for target color 1 starts with node 1 (at depth 0) and ends with node 3 (at depth 1)
TEST CASE 00.1:
        result: 1
        expect: 1
                --> PASS
```

<p><br>

(Debug) Output for test-case 01:

```
graph_nodes: 4
graph_from: [1, 1, 4]
graph_to: [2, 3, 2]
ids: [1, 2, 3, 4]
val: 2

        building graph...
                --> graph:
{1: {'to_nodes': [2, 3], 'color': 1, 'visited': False}, 2: {'to_nodes': [1, 4], 'color': 2, 'visited': False}, 3: {'to_nodes': [1], 'color': 3, 'visited': False}, 4: {'to_nodes': [2], 'color': 4, 'visited': False}}

                --> adjacency matrix:
[[0 1 1 0]
 [1 0 0 1]
 [1 0 0 0]
 [0 1 0 0]]

                --> nodes matching color 2: [2]

short-circuit since len(lst_nodes_color_match)<2 --> start/end path for target color 2 DOES NOT EXIST
TEST CASE 01.1:
        result: -1
        expect: -1
                --> PASS
```

<p><br>

(Debug) Output for test-case 12:

```
graph_nodes: 5
graph_from: [1, 1, 2, 3]
graph_to: [2, 3, 4, 5]
ids: [1, 2, 3, 3, 2]
val: 2

        building graph...
                --> graph:
{1: {'to_nodes': [2, 3], 'color': 1, 'visited': False}, 2: {'to_nodes': [1, 4], 'color': 2, 'visited': False}, 3: {'to_nodes': [1, 5], 'color': 3, 'visited': False}, 4: {'to_nodes': [2], 'color': 3, 'visited': False}, 5: {'to_nodes': [3], 'color': 2, 'visited': False}}

                --> adjacency matrix:
[[0 1 1 0 0]
 [1 0 0 1 0]
 [1 0 0 0 1]
 [0 1 0 0 0]
 [0 0 1 0 0]]

                --> nodes matching color 2: [2, 5]

len(d_graph_color_match)>=2 --> traversing graph BFS to find shortest path for target color 2 ...
depth: 0, visit: 2 --> d_graph[2]['color'] == target_color --> 2 == 2 --> True
        --> start_node is None --> set start_node=(2, 0)
        depth: 1, visit: 1 --> d_graph[1]['color'] == target_color --> 1 == 2 --> False
        depth: 1, visit: 4 --> d_graph[4]['color'] == target_color --> 3 == 2 --> False
                depth: 2, visit: 3 --> d_graph[3]['color'] == target_color --> 3 == 2 --> False
                        depth: 3, visit: 5 --> d_graph[5]['color'] == target_color --> 2 == 2 --> True
                                --> end_node is None --> set end_node=(5, 3)
shortest BFS path for target color 2 starts with node 2 (at depth 0) and ends with node 5 (at depth 3)
TEST CASE 12.1:
        result: 3
        expect: 3
                --> PASS
```

## POST-MORTEM:

Even though I have already solved this, I thought I would revisit this problem to improve the clarity of my former presentation.  My follow-up centers around the creation of a class in order to better encapsulate most of the graph-theory boiler-plate implementation.

```python
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

    def traverse_BFS(self, start_from_node, fn_visit_handler, fn_visit_handler__kwargs):
        nodes_pending_queue = deque()
        depth = 0
        nodes_pending_queue.append((start_from_node,depth))

        if fn_visit_handler__kwargs is None:
            fn_visit_handler__kwargs = {}
        fn_visit_handler__kwargs.update({'g':self})

        while len(nodes_pending_queue) > 0:
            current_node, depth = nodes_pending_queue.popleft() # O(1)
            d_node = self._d_graph[current_node]

            if current_node not in self.visited:
                kwargs = {'current_node':current_node,'depth':depth}
                fn_visit_handler__kwargs.update(kwargs)
                fn_visit_handler(**fn_visit_handler__kwargs)
                self.visited.add(current_node)

                for neighbor_node in d_node['neighbors']:
                    if neighbor_node not in self.visited:
                        nodes_pending_queue.append((neighbor_node,depth+1))


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
        print(f"{s_tabs}depth: {depth}, visit: {current_node} --> d_graph[{current_node}]['color'] == target_color --> {c} == {target_color} --> {is_color_match}")

    if is_color_match:
        if d_tracking['start_node'] is None:
            d_tracking['start_node'] = (current_node, depth)
            if debug:
                print(f"{s_tabs}\t--> start_node is None --> set start_node={d_tracking['start_node']}")

        else:   # start_node already defined
            if d_tracking['end_node'] is None:
                d_tracking['end_node'] = (current_node, depth)
                if debug:
                    print(f"{s_tabs}\t--> end_node is None --> set end_node={d_tracking['end_node']}")
            
            else: 
                current_end_node = d_tracking['end_node']
                if depth < current_end_node[1]: # end_node already defined but reassign if new depth < old depth
                    d_tracking['end_node'] = (current_node, depth)
                    if debug:
                        print(f"{s_tabs}\t--> end_node is {current_end_node} but current depth {depth} is less --> REPLACE end_node={d_tracking['end_node']}")
                else:
                    if debug:
                        print(f"{s_tabs}\t--> end_node is {current_end_node} but current depth {depth} is NOT less --> DO NOT REPLACE end_node")

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
    g.traverse_BFS(start_node, fn_visit_handler=visit_handler__print_node, fn_visit_handler__kwargs=kwargs)

    start_node = d_tracking['start_node']
    end_node = d_tracking['end_node']
    l_shortest_path = end_node[1]-start_node[1] if (start_node is not None) and (end_node is not None) else -1
    if debug:
        if l_shortest_path != -1:
            print(f"shortest BFS path for target color {val} starts with node {start_node[0]} (at depth {start_node[1]}) and ends with node {end_node[0]} (at depth {end_node[1]})")
        else:
            print(f"but start/end path for target color {val} DOES NOT EXIST")

    return l_shortest_path
```

<p><br>

(Debug) Output for test-case 00:

```
graph_nodes: 4
graph_from: [1, 1, 4]
graph_to: [2, 3, 2]
ids: [1, 2, 1, 1]
val: 1

        building graph...
                --> graph:
{1: {'id': 1, 'neighbors': {2, 3}, 'color': 1}, 2: {'id': 2, 'neighbors': {1, 4}, 'color': 2}, 3: {'id': 3, 'neighbors': {1}, 'color': 1}, 4: {'id': 4, 'neighbors': {2}, 'color': 1}}

                --> adjacency matrix:
[[0 1 1 0]
 [1 0 0 1]
 [1 0 0 0]
 [0 1 0 0]]

                --> nodes matching color 1: [1, 3, 4]

len(d_graph_color_match)>=2 --> traversing graph BFS to find shortest path for target color 1 ...
depth: 0, visit: 1 --> d_graph[1]['color'] == target_color --> 1 == 1 --> True
        --> start_node is None --> set start_node=(1, 0)
        depth: 1, visit: 2 --> d_graph[2]['color'] == target_color --> 2 == 1 --> False
        depth: 1, visit: 3 --> d_graph[3]['color'] == target_color --> 1 == 1 --> True
                --> end_node is None --> set end_node=(3, 1)
                depth: 2, visit: 4 --> d_graph[4]['color'] == target_color --> 1 == 1 --> True
                        --> end_node is (3, 1) but current depth 2 is NOT less --> DO NOT REPLACE end_node
shortest BFS path for target color 1 starts with node 1 (at depth 0) and ends with node 3 (at depth 1)
TEST CASE 00.1:
        result: 1
        expect: 1
                --> PASS
```

<p><br>

(Debug) Output for test-case 01:

```
graph_nodes: 4
graph_from: [1, 1, 4]
graph_to: [2, 3, 2]
ids: [1, 2, 3, 4]
val: 2

        building graph...
                --> graph:
{1: {'id': 1, 'neighbors': {2, 3}, 'color': 1}, 2: {'id': 2, 'neighbors': {1, 4}, 'color': 2}, 3: {'id': 3, 'neighbors': {1}, 'color': 3}, 4: {'id': 4, 'neighbors': {2}, 'color': 4}}

                --> adjacency matrix:
[[0 1 1 0]
 [1 0 0 1]
 [1 0 0 0]
 [0 1 0 0]]

                --> nodes matching color 2: [2]

short-circuit since len(lst_nodes_color_match)<2 --> start/end path for target color 2 DOES NOT EXIST
TEST CASE 01.1:
        result: -1
        expect: -1
                --> PASS
```

<p><br>

(Debug) Output for test-case 12:

```
graph_nodes: 5
graph_from: [1, 1, 2, 3]
graph_to: [2, 3, 4, 5]
ids: [1, 2, 3, 3, 2]
val: 2

        building graph...
                --> graph:
{1: {'id': 1, 'neighbors': {2, 3}, 'color': 1}, 2: {'id': 2, 'neighbors': {1, 4}, 'color': 2}, 3: {'id': 3, 'neighbors': {1, 5}, 'color': 3}, 4: {'id': 4, 'neighbors': {2}, 'color': 3}, 5: {'id': 5, 'neighbors': {3}, 'color': 2}}

                --> adjacency matrix:
[[0 1 1 0 0]
 [1 0 0 1 0]
 [1 0 0 0 1]
 [0 1 0 0 0]
 [0 0 1 0 0]]

                --> nodes matching color 2: [2, 5]

len(d_graph_color_match)>=2 --> traversing graph BFS to find shortest path for target color 2 ...
depth: 0, visit: 2 --> d_graph[2]['color'] == target_color --> 2 == 2 --> True
        --> start_node is None --> set start_node=(2, 0)
        depth: 1, visit: 1 --> d_graph[1]['color'] == target_color --> 1 == 2 --> False
        depth: 1, visit: 4 --> d_graph[4]['color'] == target_color --> 3 == 2 --> False
                depth: 2, visit: 3 --> d_graph[3]['color'] == target_color --> 3 == 2 --> False
                        depth: 3, visit: 5 --> d_graph[5]['color'] == target_color --> 2 == 2 --> True
                                --> end_node is None --> set end_node=(5, 3)
shortest BFS path for target color 2 starts with node 2 (at depth 0) and ends with node 5 (at depth 3)
TEST CASE 12.1:
        result: 3
        expect: 3
                --> PASS
```