[link](https://www.hackerrank.com/challenges/ctci-connected-cell-in-a-grid/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=graphs)


## First Try:

This was a tedious but not too difficult puzzle.  Again, as with all graph-theory puzzle, the most important facets are, of course, understanding graph theory itself and then understanding whether BFS or DFS should be used.

From there, one must decide what happens when visting a node.

The problem statement requirements dictate those facets.

The only real "gotchas" were:
- understanding that the graph node labels are the grid coordinates
- understanding that, for a given node, its neighbors are those that it is connected to... this does not necessarily mean that the connection is bi-directional; that is, a given source node may be connected to its neighbors (those adjacent cells containing 1s) but if the source node/cell contains a 0, then of course none of its adjacent cells are connected to it (the source cell)

The last statement implies that the graph, therefore, is directed (not undirected).

I took my time developing this and ensuring all free test-cases passed prior to submission and, upon submission, all remaining locked test-cases passed.

(see below for my full implementation of this algorithm)


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

    def connect_neighbors(r, c):
        from_node = get_node_label(r,c)
        if r-1 >= 0:
            if grid[r-1][c] == 1:
                to_node = get_node_label(r-1,c)
                g.connect(from_node, to_node)
            if c-1 >= 0:
                if grid[r-1][c-1] == 1:
                    to_node = get_node_label(r-1,c-1)
                    g.connect(from_node=from_node, to_node=to_node)
            if c+1 < n:
                if grid[r-1][c+1] == 1:
                    to_node = get_node_label(r-1,c+1)
                    g.connect(from_node, to_node)

        if r+1 < m:
            if grid[r+1][c] == 1:
                to_node = get_node_label(r+1,c)
                g.connect(from_node, to_node)
            if c-1 >= 0:
                if grid[r+1][c-1] == 1:
                    to_node = get_node_label(r+1,c-1)
                    g.connect(from_node, to_node)
            if c+1 < n:
                if grid[r+1][c+1] == 1:
                    to_node = get_node_label(r+1,c+1)
                    g.connect(from_node, to_node)

        if c-1 >= 0:
            if grid[r][c-1] == 1:
                to_node = get_node_label(r,c-1)
                g.connect(from_node, to_node)
            
        if c+1 < n:
            if grid[r][c+1] == 1:
                to_node = get_node_label(r,c+1)
                g.connect(from_node, to_node)

    for r in range(m):
        for c in range(n):
            connect_neighbors(r, c)

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
```

<p><br>

(Debug) Output for test-case 00:

```
grid:
[[1 1 0 0]
 [0 1 1 0]
 [0 0 1 0]
 [1 0 0 0]] is 4 x 4

                --> node labels (grid coordinates): [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (3, 3)]

                --> (directed) graph:
{(0, 0): {'id': (0, 0), 'neighbors': {(0, 1), (1, 1)}}, (0, 1): {'id': (0, 1), 'neighbors': {(1, 1), (1, 2), (0, 0)}}, (0, 2): {'id': (0, 2), 'neighbors': {(0, 1), (1, 1), (1, 2)}}, (0, 3): {'id': (0, 3), 'neighbors': {(1, 2)}}, (1, 0): {'id': (1, 0), 'neighbors': {(0, 1), (1, 1), (0, 0)}}, (1, 1): {'id': (1, 1), 'neighbors': {(0, 1), (1, 2), (2, 2), (0, 0)}}, (1, 2): {'id': (1, 2), 'neighbors': {(0, 1), (1, 1), (2, 2)}}, (1, 3): {'id': (1, 3), 'neighbors': {(1, 2), (2, 2)}}, (2, 0): {'id': (2, 0), 'neighbors': {(1, 1), (3, 0)}}, (2, 1): {'id': (2, 1), 'neighbors': {(1, 1), (1, 2), (2, 2), (3, 0)}}, (2, 2): {'id': (2, 2), 'neighbors': {(1, 1), (1, 2)}}, (2, 3): {'id': (2, 3), 'neighbors': {(1, 2), (2, 2)}}, (3, 0): {'id': (3, 0), 'neighbors': set()}, (3, 1): {'id': (3, 1), 'neighbors': {(3, 0), (2, 2)}}, (3, 2): {'id': (3, 2), 'neighbors': {(2, 2)}}, (3, 3): {'id': (3, 3), 'neighbors': {(2, 2)}}}

                --> corresponding adjacency matrix:
[[0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0]
 [1 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0]
 [0 1 0 0 0 1 1 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0]
 [1 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0]
 [1 1 0 0 0 0 1 0 0 0 1 0 0 0 0 0]
 [0 1 0 0 0 1 0 0 0 0 1 0 0 0 0 0]
 [0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0]
 [0 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0]
 [0 0 0 0 0 1 1 0 0 0 1 0 1 0 0 0]
 [0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0]]

traversing graph DFS starting from node (0, 0)...
        (depth 0) visit: (0, 0), neighbors: {(0, 1), (1, 1)}
                (depth 1) visit: (1, 1), neighbors: {(0, 1), (1, 2), (2, 2), (0, 0)}
                        neighbor node (0, 0) has already been visited
                        (depth 2) visit: (2, 2), neighbors: {(1, 1), (1, 2)}
                                neighbor node (1, 1) has already been visited
                                (depth 3) visit: (1, 2), neighbors: {(0, 1), (1, 1), (2, 2)}
                                        neighbor node (1, 1) has already been visited
                                        neighbor node (2, 2) has already been visited
                                        (depth 4) visit: (0, 1), neighbors: {(1, 1), (1, 2), (0, 0)}
                                                neighbor node (1, 1) has already been visited
                                                neighbor node (1, 2) has already been visited
                                                neighbor node (0, 0) has already been visited

        --> region: [(0, 0), (1, 1), (2, 2), (1, 2), (0, 1)]

traversing graph DFS starting from node (3, 0)...
        (depth 0) visit: (3, 0), neighbors: set()

        --> region: [(3, 0)]

        --> max region (size 5): [(0, 0), (1, 1), (2, 2), (1, 2), (0, 1)]

TEST CASE 00.1:
        result: 5
        expect: 5
                --> PASS
```

<p><br>

(Debug) Output for test-case 01:

```
grid:
[[0 0 1 1]
 [0 0 1 0]
 [0 1 1 0]
 [0 1 0 0]
 [1 1 0 0]] is 5 x 4

                --> node labels (grid coordinates): [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (3, 3), (4, 0), (4, 1), (4, 2), (4, 3)]

                --> (directed) graph:
{(0, 0): {'id': (0, 0), 'neighbors': set()}, (0, 1): {'id': (0, 1), 'neighbors': {(0, 2), (1, 2)}}, (0, 2): {'id': (0, 2), 'neighbors': {(1, 2), (0, 3)}}, (0, 3): {'id': (0, 3), 'neighbors': {(0, 2), (1, 2)}}, (1, 0): {'id': (1, 0), 'neighbors': {(2, 1)}}, (1, 1): {'id': (1, 1), 'neighbors': {(0, 2), (1, 2), (2, 1), (2, 2)}}, (1, 2): {'id': (1, 2), 'neighbors': {(0, 2), (0, 3), (2, 1), (2, 2)}}, (1, 3): {'id': (1, 3), 'neighbors': {(1, 2), (0, 2), (0, 3), (2, 2)}}, (2, 0): {'id': (2, 0), 'neighbors': {(3, 1), (2, 1)}}, (2, 1): {'id': (2, 1), 'neighbors': {(3, 1), (1, 2), (2, 2)}}, (2, 2): {'id': (2, 2), 'neighbors': {(3, 1), (1, 2), (2, 1)}}, (2, 3): {'id': (2, 3), 'neighbors': {(1, 2), (2, 2)}}, (3, 0): {'id': (3, 0), 'neighbors': {(3, 1), (4, 0), (4, 1), (2, 1)}}, (3, 1): {'id': (3, 1), 'neighbors': {(4, 0), (4, 1), (2, 1), (2, 2)}}, (3, 2): {'id': (3, 2), 'neighbors': {(3, 1), (4, 1), (2, 1), (2, 2)}}, (3, 3): {'id': (3, 3), 'neighbors': {(2, 2)}}, (4, 0): {'id': (4, 0), 'neighbors': {(3, 1), (4, 1)}}, (4, 1): {'id': (4, 1), 'neighbors': {(3, 1), (4, 0)}}, (4, 2): {'id': (4, 2), 'neighbors': {(3, 1), (4, 1)}}, (4, 3): {'id': (4, 3), 'neighbors': set()}}

                --> corresponding adjacency matrix:
[[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0]
 [0 0 1 0 0 0 1 0 0 1 1 0 0 0 0 0 0 0 0 0]
 [0 0 1 1 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0]
 [0 0 1 1 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0]
 [0 0 0 0 0 0 1 0 0 0 1 0 0 1 0 0 0 0 0 0]
 [0 0 0 0 0 0 1 0 0 1 0 0 0 1 0 0 0 0 0 0]
 [0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0 1 1 0 0]
 [0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 1 1 0 0]
 [0 0 0 0 0 0 0 0 0 1 1 0 0 1 0 0 0 1 0 0]
 [0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]]

traversing graph DFS starting from node (0, 2)...
        (depth 0) visit: (0, 2), neighbors: {(1, 2), (0, 3)}
                (depth 1) visit: (0, 3), neighbors: {(0, 2), (1, 2)}
                        neighbor node (0, 2) has already been visited
                        (depth 2) visit: (1, 2), neighbors: {(0, 2), (0, 3), (2, 1), (2, 2)}
                                neighbor node (0, 2) has already been visited
                                neighbor node (0, 3) has already been visited
                                (depth 3) visit: (2, 2), neighbors: {(3, 1), (1, 2), (2, 1)}
                                        neighbor node (1, 2) has already been visited
                                        (depth 4) visit: (2, 1), neighbors: {(3, 1), (1, 2), (2, 2)}
                                                neighbor node (1, 2) has already been visited
                                                neighbor node (2, 2) has already been visited
                                                (depth 5) visit: (3, 1), neighbors: {(4, 0), (4, 1), (2, 1), (2, 2)}
                                                        neighbor node (2, 1) has already been visited
                                                        neighbor node (2, 2) has already been visited
                                                        (depth 6) visit: (4, 1), neighbors: {(3, 1), (4, 0)}
                                                                neighbor node (3, 1) has already been visited
                                                                (depth 7) visit: (4, 0), neighbors: {(3, 1), (4, 1)}
                                                                        neighbor node (3, 1) has already been visited
                                                                        neighbor node (4, 1) has already been visited

        --> region: [(0, 2), (0, 3), (1, 2), (2, 2), (2, 1), (3, 1), (4, 1), (4, 0)]

        --> max region (size 8): [(0, 2), (0, 3), (1, 2), (2, 2), (2, 1), (3, 1), (4, 1), (4, 0)]

TEST CASE 01.1:
        result: 8
        expect: 8
                --> PASS
```

<p><br>

(Debug) Output for test-case 07:

```
grid:
[[1 0 1 1 0]
 [1 1 0 0 1]
 [0 1 1 1 0]
 [0 0 0 0 1]
 [1 1 1 0 0]] is 5 x 5

                --> node labels (grid coordinates): [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]

                --> (directed) graph:
{(0, 0): {'id': (0, 0), 'neighbors': {(1, 0), (1, 1)}}, (0, 1): {'id': (0, 1), 'neighbors': {(1, 0), (0, 2), (1, 1), (0, 0)}}, (0, 2): {'id': (0, 2), 'neighbors': {(1, 1), (0, 3)}}, (0, 3): {'id': (0, 3), 'neighbors': {(0, 2), (1, 4)}}, (0, 4): {'id': (0, 4), 'neighbors': {(0, 3), (1, 4)}}, (1, 0): {'id': (1, 0), 'neighbors': {(1, 1), (2, 1), (0, 0)}}, (1, 1): {'id': (1, 1), 'neighbors': {(2, 1), (0, 0), (0, 2), (2, 2), (1, 0)}}, (1, 2): {'id': (1, 2), 'neighbors': {(2, 1), (1, 1), (0, 3), (2, 3), (0, 2), (2, 2)}}, (1, 3): {'id': (1, 3), 'neighbors': {(0, 3), (1, 4), (2, 3), (0, 2), (2, 2)}}, (1, 4): {'id': (1, 4), 'neighbors': {(2, 3), (0, 3)}}, (2, 0): {'id': (2, 0), 'neighbors': {(1, 0), (1, 1), (2, 1)}}, (2, 1): {'id': (2, 1), 'neighbors': {(1, 0), (1, 1), (2, 2)}}, (2, 2): {'id': (2, 2), 'neighbors': {(2, 3), (1, 1), (2, 1)}}, (2, 3): {'id': (2, 3), 'neighbors': {(3, 4), (1, 4), (2, 2)}}, (2, 4): {'id': (2, 4), 'neighbors': {(2, 3), (3, 4), (1, 4)}}, (3, 0): {'id': (3, 0), 'neighbors': {(4, 0), (4, 1), (2, 1)}}, (3, 1): {'id': (3, 1), 'neighbors': {(4, 0), (2, 1), (4, 2), (2, 2), (4, 1)}}, (3, 2): {'id': (3, 2), 'neighbors': {(2, 1), (4, 2), (2, 3), (2, 2), (4, 1)}}, (3, 3): {'id': (3, 3), 'neighbors': {(2, 3), (3, 4), (4, 2), (2, 2)}}, (3, 4): {'id': (3, 4), 'neighbors': {(2, 3)}}, (4, 0): {'id': (4, 0), 'neighbors': {(4, 1)}}, (4, 1): {'id': (4, 1), 'neighbors': {(4, 0), (4, 2)}}, (4, 2): {'id': (4, 2), 'neighbors': {(4, 1)}}, (4, 3): {'id': (4, 3), 'neighbors': {(3, 4), (4, 2)}}, (4, 4): {'id': (4, 4), 'neighbors': {(3, 4)}}}

                --> corresponding adjacency matrix:
[[0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [1 0 1 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [1 0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [1 0 1 0 0 1 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 1 1 0 0 1 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 1 1 0 0 0 0 0 1 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 1 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 1 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 1 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 1 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 1 1 1 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 1 1 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 1 0 0 1 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0]]

traversing graph DFS starting from node (0, 0)...
        (depth 0) visit: (0, 0), neighbors: {(1, 0), (1, 1)}
                (depth 1) visit: (1, 1), neighbors: {(2, 1), (0, 0), (0, 2), (2, 2), (1, 0)}
                        neighbor node (0, 0) has already been visited
                        (depth 2) visit: (1, 0), neighbors: {(1, 1), (2, 1), (0, 0)}
                                neighbor node (1, 1) has already been visited
                                neighbor node (0, 0) has already been visited
                                (depth 3) visit: (2, 1), neighbors: {(1, 0), (1, 1), (2, 2)}
                                        neighbor node (1, 0) has already been visited
                                        neighbor node (1, 1) has already been visited
                                        (depth 4) visit: (2, 2), neighbors: {(2, 3), (1, 1), (2, 1)}
                                                neighbor node (1, 1) has already been visited
                                                neighbor node (2, 1) has already been visited
                                                (depth 5) visit: (2, 3), neighbors: {(3, 4), (1, 4), (2, 2)}
                                                        neighbor node (2, 2) has already been visited
                                                        (depth 6) visit: (1, 4), neighbors: {(2, 3), (0, 3)}
                                                                neighbor node (2, 3) has already been visited
                                                                (depth 7) visit: (0, 3), neighbors: {(0, 2), (1, 4)}
                                                                        neighbor node (1, 4) has already been visited
                                                                        (depth 8) visit: (0, 2), neighbors: {(1, 1), (0, 3)}
                                                                                neighbor node (1, 1) has already been visited
                                                                                neighbor node (0, 3) has already been visited
                                                        (depth 6) visit: (3, 4), neighbors: {(2, 3)}
                                                                neighbor node (2, 3) has already been visited

        --> region: [(0, 0), (1, 1), (1, 0), (2, 1), (2, 2), (2, 3), (1, 4), (0, 3), (0, 2), (3, 4)]

traversing graph DFS starting from node (4, 0)...
        (depth 0) visit: (4, 0), neighbors: {(4, 1)}
                (depth 1) visit: (4, 1), neighbors: {(4, 0), (4, 2)}
                        neighbor node (4, 0) has already been visited
                        (depth 2) visit: (4, 2), neighbors: {(4, 1)}
                                neighbor node (4, 1) has already been visited

        --> region: [(4, 0), (4, 1), (4, 2)]

        --> max region (size 10): [(0, 0), (1, 1), (1, 0), (2, 1), (2, 2), (2, 3), (1, 4), (0, 3), (0, 2), (3, 4)]

TEST CASE 07.1:
        result: 10
        expect: 10
                --> PASS
```

## POST-MORTEM:

(see above commentary)