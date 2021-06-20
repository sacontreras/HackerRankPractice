[link](https://www.hackerrank.com/challenges/ctci-bfs-shortest-reach/problem?h_l=interview&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D=graphs&h_r=next-challenge&h_v=zen)


## First Try:

Again, most of the difficulty in graph puzzles is, well, graphs and the little bit of graph theory understanding required.  We are given that the graph needs to be traversed BFS.  There doesn't seem to be much more to it than that.

The implementation passed all free test-cases.  

But, upon submission, failed locked test-cases 1 and 6 due to "wrong answer" and 2 and 5 due to timeout.

(see below for my full implementation of this algorithm)


```python
class Graph():
    def __init__(self, n, edge_weight=6, print_distances=True, debug=False):
        self._d_graph = {lbl_node:{'id':lbl_node,'neighbors':[],'visited':False} for lbl_node in range(n)}
        self.edge_weight = edge_weight
        self.print_distances = print_distances
        self._debug = debug
        if debug:
            self._adj_mat = [[0 for _ in range(n)] for _ in range(n)]

    def connect(self, from_node, to_node):  # these are zero-based
        self._d_graph[from_node]['neighbors'].append(to_node)
        self._d_graph[to_node]['neighbors'].append(from_node)
        if self._debug:
            self._adj_mat[from_node][to_node] = self._adj_mat[to_node][from_node] = 1

    def __traverse_graph_BFS(self, from_node):
        distances = [-1] * len(self._d_graph)
        nodes_pending_queue = []
        depth = 0
        nodes_pending_queue.insert(0, (from_node,depth))
        while len(nodes_pending_queue) > 0:
            current_node, depth = nodes_pending_queue.pop()
            d_node = self._d_graph[current_node]

            distance = depth * self.edge_weight
            if self._debug:
                s_tabs = '\t'*depth
                print(f"{s_tabs}depth: {depth}, visit: {current_node} --> distance from node {from_node} is: {distance}")
            distances[d_node['id']] = distance
            d_node['visited'] = True

            for neighbor_node in d_node['neighbors']:
                d_node_neighbor = self._d_graph[neighbor_node]
                if not d_node_neighbor['visited']:
                    nodes_pending_queue.insert(0, (neighbor_node,depth+1))

        del distances[from_node]

        return distances

    def find_all_distances(self, from_node):   # BFS
        distances = self.__traverse_graph_BFS(from_node)
        if self.print_distances:
            s_result = ' '.join([str(d) for d in distances])
            print(s_result)
        else:
            return distances
```

<p><br>

(Debug) Output for test-case 00:

```
                --> graph:
{0: {'id': 0, 'neighbors': [1, 2], 'visited': False}, 1: {'id': 1, 'neighbors': [0], 'visited': False}, 2: {'id': 2, 'neighbors': [0], 'visited': False}, 3: {'id': 3, 'neighbors': [], 'visited': False}}

                --> adjacency matrix:
[[0 1 1 0]
 [1 0 0 0]
 [1 0 0 0]
 [0 0 0 0]]

depth: 0, visit: 0 --> distance from node 0 is: 0
        depth: 1, visit: 1 --> distance from node 0 is: 6
        depth: 1, visit: 2 --> distance from node 0 is: 6
                --> graph:
{0: {'id': 0, 'neighbors': [], 'visited': False}, 1: {'id': 1, 'neighbors': [2], 'visited': False}, 2: {'id': 2, 'neighbors': [1], 'visited': False}}

                --> adjacency matrix:
[[0 0 0]
 [0 0 1]
 [0 1 0]]

depth: 0, visit: 1 --> distance from node 1 is: 0
        depth: 1, visit: 2 --> distance from node 1 is: 6
TEST CASE 00.1:
        result: 6 6 -1
        expect: 6 6 -1
                --> PASS

TEST CASE 00.2:
        result: -1 6
        expect: -1 6
                --> PASS
```

<p><br>

(Debug) Output for test-case 07:

```
                --> graph:
{0: {'id': 0, 'neighbors': [1, 4], 'visited': False}, 1: {'id': 1, 'neighbors': [0, 2], 'visited': False}, 2: {'id': 2, 'neighbors': [1, 3], 'visited': False}, 3: {'id': 3, 'neighbors': [2], 'visited': False}, 4: {'id': 4, 'neighbors': [0], 'visited': False}, 5: {'id': 5, 'neighbors': [], 'visited': False}}

                --> adjacency matrix:
[[0 1 0 0 1 0]
 [1 0 1 0 0 0]
 [0 1 0 1 0 0]
 [0 0 1 0 0 0]
 [1 0 0 0 0 0]
 [0 0 0 0 0 0]]

depth: 0, visit: 0 --> distance from node 0 is: 0
        depth: 1, visit: 1 --> distance from node 0 is: 6
        depth: 1, visit: 4 --> distance from node 0 is: 6
                depth: 2, visit: 2 --> distance from node 0 is: 12
                        depth: 3, visit: 3 --> distance from node 0 is: 18
TEST CASE 07.1:
        result: 6 12 18 6 -1
        expect: 6 12 18 6 -1
                --> PASS
```

<p><br>

(Debug) Output for test-case 08:

```
                --> graph:
{0: {'id': 0, 'neighbors': [1, 2], 'visited': False}, 1: {'id': 1, 'neighbors': [0, 4], 'visited': False}, 2: {'id': 2, 'neighbors': [0, 3], 'visited': False}, 3: {'id': 3, 'neighbors': [2], 'visited': False}, 4: {'id': 4, 'neighbors': [1], 'visited': False}, 5: {'id': 5, 'neighbors': [], 'visited': False}, 6: {'id': 6, 'neighbors': [], 'visited': False}}

                --> adjacency matrix:
[[0 1 1 0 0 0 0]
 [1 0 0 0 1 0 0]
 [1 0 0 1 0 0 0]
 [0 0 1 0 0 0 0]
 [0 1 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]]

depth: 0, visit: 1 --> distance from node 1 is: 0
        depth: 1, visit: 0 --> distance from node 1 is: 6
        depth: 1, visit: 4 --> distance from node 1 is: 6
                depth: 2, visit: 2 --> distance from node 1 is: 12
                        depth: 3, visit: 3 --> distance from node 1 is: 18
TEST CASE 08.1:
        result: 6 12 18 6 -1 -1
        expect: 6 12 18 6 -1 -1
                --> PASS
```

## Second Try:

I unlocked test-case 1.  I forget to do a pre-check to make sure the source node has not already been visited.

After this change, the locked test-case (1) passed.

Upon submission, all remaining locked test-cases passed except for locked test-case 5.  This one is still failing due to timeout.

Running this test-case locally passes.  It doesn't take very long but obviously is still too long for the HackerRank interpreter.

(see below for my full implementation of this algorithm)

```python
class Graph():
    def __init__(self, n, edge_weight=6, print_distances=True, debug=False):
        self._d_graph = {lbl_node:{'id':lbl_node,'neighbors':[],'visited':False} for lbl_node in range(n)}
        self.edge_weight = edge_weight
        self.print_distances = print_distances
        self._debug = debug
        if debug:
            self._adj_mat = [[0 for _ in range(n)] for _ in range(n)]

    def connect(self, from_node, to_node):  # these are zero-based
        self._d_graph[from_node]['neighbors'].append(to_node)
        self._d_graph[to_node]['neighbors'].append(from_node)
        if self._debug:
            self._adj_mat[from_node][to_node] = self._adj_mat[to_node][from_node] = 1

    def __traverse_graph_BFS(self, from_node):
        distances = [-1] * len(self._d_graph)
        nodes_pending_queue = []
        depth = 0
        nodes_pending_queue.insert(0, (from_node,depth))
        while len(nodes_pending_queue) > 0:
            current_node, depth = nodes_pending_queue.pop()
            d_node = self._d_graph[current_node]

            if not d_node['visited']:
                distance = depth * self.edge_weight
                if self._debug:
                    s_tabs = '\t'*depth
                    print(f"{s_tabs}depth: {depth}, visit: {current_node} --> distance from node {from_node} is: {distance}")
                distances[d_node['id']] = distance
                d_node['visited'] = True

                for neighbor_node in d_node['neighbors']:
                    d_node_neighbor = self._d_graph[neighbor_node]
                    if not d_node_neighbor['visited']:
                        nodes_pending_queue.insert(0, (neighbor_node,depth+1))

        del distances[from_node]

        return distances

    def find_all_distances(self, from_node):   # BFS
        distances = self.__traverse_graph_BFS(from_node)
        if self.print_distances:
            s_result = ' '.join([str(d) for d in distances])
            print(s_result)
        else:
            return distances
```

<p><br>

(Debug) Output for test-case 01:

```
                --> graph:
{0: {'id': 0, 'neighbors': [20, 15, 63, 48, 45, 63, 7, 2, 31, 27, 69, 56, 16, 42, 40, 62, 20, 44, 51, 11, 27, 20, 8, 25, 37, 14, 18, 30, 68, 63, 3, 9, 31, 37, 20, 66, 3, 14, 6, 39, 43, 15, 37, 44, 44, 15, 46, 37, 22, 32, 33, 34, 33, 11, 55, 1, 66, 47, 18, 29, 9, 69, 47, 43, 53, 40, 67, 15, 20, 15, 40, 21, 59, 12, 10, 35, 69, 31, 32, 18, 26, 51, 10, 60, 23, 48, 7, 11, 36, 47, 27, 6, 51, 1, 51, 8, 69, 21, 50, 14, 3, 54, 14, 11, 18, 7, 59, 63, 15, 26, 46, 7, 52], 'visited': False}, 1: {'id': 1, 'neighbors': [29, 15, 49, 12, 2, 47, 22, 25, 62, 4, 46, 9, 67, 67, 11, 11, 21, 21, 7, 64, 68, 15, 51, 14, 32, 5, 0, 32, 35, 58, 59, 10, 27, 28, 22, 61, 11, 44, 14, 34, 21, 30, 55, 0, 60, 10, 24, 31, 42, 2, 65, 46], 'visited': False}, 2: {'id': 2, 'neighbors': [65, 29, 12, 26, 1, 58, 20, 0, 59, 64, 56, 18, 33, 5, 67, 18, 12, 44, 45, 46, 19, 32, 32, 23, 54, 5, 32, 68, 24, 69, 37, 25, 64, 37, 30, 65, 44, 10, 49, 46, 3, 15, 3, 48, 13, 37, 62, 12, 45, 43, 8, 15, 18, 1, 3, 30], 'visited': False}, 3: {'id': 3, 'neighbors': [10, 9, 45, 27, 5, 43, 64, 23, 0, 62, 47, 59, 0, 13, 47, 32, 58, 6, 31, 40, 30, 34, 8, 15, 21, 26, 48, 4, 36, 49, 10, 60, 40, 5, 40, 2, 68, 50, 55, 2, 68, 30, 20, 32, 20, 0, 32, 46, 63, 67, 31, 4, 2, 31, 35, 25], 'visited': False}, 4: {'id': 4, 'neighbors': [54, 34, 21, 14, 9, 22, 45, 30, 1, 47, 64, 21, 10, 44, 23, 67, 62, 47, 10, 62, 58, 28, 17, 65, 36, 59, 63, 17, 23, 61, 17, 69, 26, 58, 3, 24, 24, 7, 12, 9, 14, 57, 43, 9, 20, 11, 28, 9, 65, 61, 30, 39, 43, 9, 3, 7], 'visited': False}, 5: {'id': 5, 'neighbors': [62, 39, 13, 31, 3, 2, 40, 64, 7, 15, 62, 33, 8, 2, 15, 60, 36, 29, 60, 32, 56, 44, 29, 1, 59, 65, 36, 3, 63, 56, 23, 32, 33, 39, 47, 36, 11, 38, 60, 36, 26, 54, 45, 68], 'visited': False}, 6: {'id': 6, 'neighbors': [57, 9, 42, 30, 23, 8, 30, 68, 57, 63, 34, 26, 56, 61, 12, 18, 61, 39, 36, 0, 19, 3, 19, 30, 13, 55, 44, 56, 11, 9, 63, 18, 23, 26, 67, 31, 62, 59, 35, 35, 34, 68, 44, 64, 8, 31, 0, 47, 14, 47, 50, 64, 10, 11, 54, 26, 22, 56, 61, 29, 27], 'visited': False}, 7: {'id': 7, 'neighbors': [18, 67, 0, 18, 27, 59, 17, 69, 45, 35, 30, 35, 43, 44, 23, 38, 5, 64, 45, 51, 1, 26, 56, 67, 15, 52, 4, 16, 64, 49, 40, 62, 69, 31, 24, 64, 43, 15, 39, 0, 36, 67, 13, 25, 54, 29, 35, 0, 4, 59, 50, 36, 0], 'visited': False}, 8: {'id': 8, 'neighbors': [49, 65, 6, 54, 45, 69, 39, 0, 63, 58, 46, 32, 60, 61, 51, 5, 16, 30, 31, 19, 28, 50, 9, 49, 3, 62, 12, 17, 51, 21, 60, 54, 44, 37, 16, 34, 34, 43, 13, 6, 53, 19, 0, 52, 47, 39, 12, 2, 47, 51, 60, 22, 23, 54, 18, 44], 'visited': False}, 9: {'id': 9, 'neighbors': [6, 10, 68, 3, 45, 21, 4, 30, 39, 64, 17, 41, 11, 20, 1, 42, 34, 68, 17, 50, 0, 61, 59, 63, 45, 42, 57, 8, 64, 57, 49, 6, 0, 56, 29, 28, 52, 4, 41, 56, 33, 4, 65, 23, 41, 17, 52, 51, 4, 66, 66, 52, 20, 27, 24, 25, 30, 4, 27, 45, 25, 61], 'visited': False}, 10: {'id': 10, 'neighbors': [9, 34, 69, 3, 63, 38, 50, 30, 50, 4, 52, 16, 28, 22, 4, 38, 60, 67, 29, 35, 16, 39, 59, 21, 69, 33, 36, 11, 30, 3, 37, 2, 12, 23, 1, 44, 0, 39, 25, 22, 0, 29, 47, 65, 27, 55, 23, 22, 67, 26, 28, 1, 6, 15, 39, 68], 'visited': False}, 11: {'id': 11, 'neighbors': [18, 18, 36, 17, 27, 9, 0, 22, 15, 50, 17, 1, 67, 67, 38, 33, 61, 54, 1, 60, 21, 60, 35, 63, 0, 30, 61, 31, 6, 10, 46, 48, 50, 43, 1, 4, 0, 47, 50, 63, 25, 18, 49, 5, 6, 49, 0, 47, 51, 20, 33, 19, 41, 50, 64, 63, 36], 'visited': False}, 12: {'id': 12, 'neighbors': [37, 21, 2, 1, 34, 52, 45, 15, 64, 50, 21, 6, 22, 47, 15, 69, 2, 24, 29, 58, 19, 21, 33, 20, 69, 56, 8, 55, 69, 55, 4, 37, 46, 10, 34, 0, 35, 32, 16, 27, 16, 38, 20, 2, 19, 58, 8, 68, 64, 13, 50, 45], 'visited': False}, 13: {'id': 13, 'neighbors': [45, 25, 61, 34, 53, 5, 37, 50, 68, 63, 14, 53, 36, 39, 3, 27, 27, 67, 55, 61, 19, 25, 69, 53, 6, 26, 16, 34, 47, 41, 34, 44, 58, 19, 61, 29, 25, 2, 8, 56, 7, 37, 61, 45, 60, 15, 53, 67, 25, 57, 12, 24, 48, 53], 'visited': False}, 14: {'id': 14, 'neighbors': [43, 4, 31, 54, 16, 68, 46, 60, 66, 63, 0, 56, 13, 23, 62, 33, 29, 43, 30, 64, 0, 18, 65, 31, 46, 49, 60, 31, 56, 1, 38, 15, 68, 18, 15, 67, 4, 43, 46, 54, 43, 38, 30, 1, 19, 49, 42, 6, 30, 53, 43, 0, 0, 25, 54, 15, 30, 50, 40, 63], 'visited': False}, 15: {'id': 15, 'neighbors': [0, 69, 1, 45, 35, 12, 68, 19, 11, 32, 68, 61, 12, 40, 38, 68, 5, 40, 5, 0, 56, 0, 25, 21, 48, 3, 1, 18, 14, 7, 51, 40, 50, 14, 23, 60, 0, 0, 49, 58, 42, 69, 2, 7, 61, 23, 46, 13, 48, 10, 56, 56, 14, 2, 27, 45, 0, 57, 27, 20], 'visited': False}, 16: {'id': 16, 'neighbors': [55, 49, 14, 68, 0, 49, 50, 39, 37, 10, 64, 25, 65, 53, 18, 29, 8, 21, 10, 31, 63, 24, 18, 49, 13, 57, 7, 58, 66, 12, 8, 23, 30, 12, 45, 35, 50, 65, 23, 28, 17, 21, 27, 40, 20, 40, 69, 27], 'visited': False}, 17: {'id': 17, 'neighbors': [19, 11, 9, 54, 55, 66, 7, 9, 62, 56, 22, 32, 11, 31, 32, 66, 46, 55, 4, 51, 51, 4, 66, 41, 62, 68, 4, 43, 25, 21, 44, 23, 8, 48, 41, 54, 9, 54, 24, 24, 44, 65, 21, 30, 50, 16, 51, 23, 62, 62, 65, 30, 54, 31, 65], 'visited': False}, 18: {'id': 18, 'neighbors': [11, 48, 7, 53, 11, 7, 40, 23, 63, 67, 45, 22, 2, 36, 0, 6, 2, 44, 60, 16, 34, 54, 14, 68, 56, 21, 37, 41, 30, 16, 31, 64, 27, 27, 15, 0, 14, 20, 69, 68, 49, 68, 6, 43, 20, 36, 27, 19, 0, 21, 37, 60, 30, 41, 54, 11, 47, 66, 2, 0, 8], 'visited': False}, 19: {'id': 19, 'neighbors': [17, 38, 48, 62, 24, 39, 25, 15, 59, 27, 63, 20, 2, 21, 53, 35, 6, 27, 12, 8, 6, 56, 13, 55, 58, 48, 52, 48, 33, 30, 18, 46, 13, 26, 41, 14, 36, 8, 50, 12, 26, 63, 40, 11, 31, 55], 'visited': False}, 20: {'id': 20, 'neighbors': [0, 40, 42, 2, 27, 0, 9, 0, 35, 30, 47, 19, 54, 39, 65, 0, 43, 34, 56, 28, 42, 27, 57, 12, 67, 27, 65, 68, 51, 57, 21, 24, 33, 67, 18, 0, 65, 18, 27, 46, 32, 36, 59, 31, 30, 4, 3, 55, 28, 57, 61, 26, 12, 41, 52, 3, 34, 56, 9, 24, 69, 57, 11, 16, 49, 15], 'visited': False}, 21: {'id': 21, 'neighbors': [12, 4, 9, 41, 22, 4, 44, 54, 33, 45, 65, 12, 38, 67, 46, 40, 41, 38, 19, 16, 18, 31, 49, 1, 1, 12, 10, 11, 47, 37, 15, 45, 29, 3, 53, 17, 20, 47, 47, 25, 8, 66, 0, 37, 26, 62, 18, 17, 24, 54, 1, 0, 68, 16, 51, 42, 44, 69, 44], 'visited': False}, 22: {'id': 22, 'neighbors': [29, 1, 42, 65, 60, 34, 4, 52, 56, 18, 11, 21, 62, 35, 12, 17, 10, 67, 44, 0, 52, 25, 52, 58, 36, 1, 58, 33, 55, 68, 38, 10, 33, 32, 10, 38, 45, 6, 8, 45], 'visited': False}, 23: {'id': 23, 'neighbors': [6, 38, 68, 44, 28, 69, 18, 54, 31, 61, 4, 3, 52, 14, 7, 2, 33, 46, 51, 51, 35, 51, 59, 29, 48, 50, 4, 17, 15, 58, 10, 6, 49, 64, 24, 16, 5, 9, 47, 0, 57, 35, 10, 15, 56, 16, 31, 54, 38, 24, 17, 27, 28, 52, 67, 65, 66, 43, 61, 8], 'visited': False}, 24: {'id': 24, 'neighbors': [65, 19, 42, 40, 69, 52, 12, 63, 16, 2, 62, 39, 49, 46, 4, 4, 43, 46, 30, 39, 32, 20, 25, 7, 59, 49, 66, 23, 52, 17, 17, 41, 21, 57, 1, 23, 38, 20, 34, 67, 48, 9, 34, 13, 50], 'visited': False}, 25: {'id': 25, 'neighbors': [13, 68, 48, 19, 52, 1, 65, 52, 0, 57, 28, 58, 16, 65, 50, 40, 48, 13, 15, 67, 53, 68, 61, 2, 42, 54, 17, 60, 22, 21, 62, 24, 33, 10, 47, 58, 29, 30, 52, 34, 43, 13, 11, 7, 48, 35, 14, 13, 68, 41, 9, 61, 38, 9, 51, 3], 'visited': False}, 26: {'id': 26, 'neighbors': [49, 59, 2, 31, 27, 32, 6, 27, 29, 36, 37, 65, 30, 39, 64, 49, 39, 43, 35, 7, 29, 13, 45, 63, 3, 45, 33, 48, 68, 4, 29, 48, 35, 47, 6, 36, 28, 51, 64, 21, 19, 0, 31, 47, 20, 10, 58, 19, 40, 28, 6, 35, 43, 5, 59, 27, 53, 43, 0, 66, 27, 39], 'visited': False}, 27: {'id': 27, 'neighbors': [63, 53, 54, 0, 11, 20, 68, 3, 26, 52, 46, 7, 41, 33, 43, 0, 26, 37, 19, 57, 59, 67, 64, 13, 55, 45, 47, 13, 19, 55, 20, 18, 18, 20, 55, 57, 1, 20, 18, 37, 49, 12, 33, 0, 10, 35, 55, 60, 52, 23, 41, 63, 16, 9, 56, 15, 26, 9, 49, 43, 38, 15, 16, 58, 26, 6], 'visited': False}, 28: {'id': 28, 'neighbors': [44, 33, 56, 23, 43, 25, 46, 47, 37, 10, 64, 64, 55, 45, 4, 20, 8, 54, 36, 53, 66, 68, 9, 62, 68, 1, 26, 52, 38, 4, 20, 41, 45, 68, 10, 16, 63, 59, 39, 23, 26, 34, 36, 49], 'visited': False}, 29: {'id': 29, 'neighbors': [31, 1, 22, 2, 53, 48, 42, 58, 45, 26, 14, 16, 12, 42, 32, 10, 47, 40, 5, 57, 61, 26, 23, 21, 5, 58, 56, 50, 60, 44, 0, 58, 26, 9, 33, 68, 43, 25, 53, 13, 45, 31, 61, 10, 50, 7, 45, 64, 54, 66, 46, 44, 6, 67], 'visited': False}, 30: {'id': 30, 'neighbors': [66, 6, 55, 9, 6, 4, 10, 59, 20, 7, 0, 48, 60, 32, 14, 26, 33, 8, 68, 43, 50, 57, 65, 18, 6, 3, 66, 11, 58, 51, 35, 57, 59, 10, 68, 58, 2, 24, 32, 61, 19, 14, 51, 16, 25, 20, 3, 47, 17, 14, 53, 18, 1, 33, 4, 14, 68, 56, 9, 55, 17, 37, 2], 'visited': False}, 31: {'id': 31, 'neighbors': [29, 45, 69, 14, 0, 26, 5, 67, 23, 55, 43, 67, 68, 34, 0, 17, 21, 14, 8, 16, 3, 14, 34, 18, 53, 40, 11, 67, 59, 51, 34, 59, 7, 36, 6, 66, 0, 48, 42, 63, 20, 29, 26, 35, 54, 47, 6, 33, 47, 23, 54, 60, 55, 1, 61, 54, 55, 3, 19, 17, 3, 64], 'visited': False}, 32: {'id': 32, 'neighbors': [67, 44, 50, 26, 59, 56, 53, 15, 8, 44, 17, 40, 45, 30, 2, 17, 2, 43, 29, 3, 53, 54, 2, 5, 40, 59, 0, 1, 67, 1, 47, 51, 68, 24, 30, 47, 47, 12, 20, 0, 5, 62, 55, 22, 57, 3, 68, 3, 62, 44, 53, 48, 65], 'visited': False}, 33: {'id': 33, 'neighbors': [53, 57, 28, 48, 69, 55, 57, 27, 69, 53, 43, 21, 69, 2, 65, 14, 34, 59, 23, 11, 5, 30, 38, 44, 44, 12, 0, 50, 0, 10, 26, 58, 20, 29, 47, 19, 25, 60, 22, 61, 62, 9, 22, 5, 65, 27, 61, 63, 31, 51, 69, 30, 68, 11, 62, 46, 56], 'visited': False}, 34: {'id': 34, 'neighbors': [10, 4, 42, 12, 13, 47, 22, 6, 9, 41, 63, 31, 67, 66, 33, 56, 18, 67, 64, 20, 68, 44, 31, 54, 3, 46, 0, 13, 67, 31, 37, 12, 54, 61, 13, 62, 55, 6, 8, 8, 25, 42, 1, 45, 46, 41, 20, 24, 48, 28, 56, 24], 'visited': False}, 35: {'id': 35, 'neighbors': [58, 56, 15, 49, 57, 49, 64, 45, 20, 7, 22, 7, 54, 36, 61, 47, 65, 19, 10, 23, 26, 11, 53, 64, 44, 30, 38, 53, 1, 48, 26, 12, 0, 64, 6, 69, 6, 16, 66, 53, 31, 23, 61, 27, 45, 25, 53, 26, 38, 7, 41, 69, 48, 65, 69, 48, 3], 'visited': False}, 36: {'id': 36, 'neighbors': [37, 11, 68, 68, 63, 53, 18, 59, 63, 46, 13, 46, 26, 35, 6, 42, 56, 37, 4, 5, 28, 10, 61, 60, 3, 5, 22, 26, 31, 18, 41, 20, 39, 54, 0, 7, 58, 19, 5, 69, 57, 61, 5, 40, 46, 28, 7, 44, 11], 'visited': False}, 37: {'id': 37, 'neighbors': [12, 36, 47, 56, 45, 63, 13, 49, 53, 0, 16, 27, 41, 58, 51, 38, 28, 0, 26, 47, 0, 36, 67, 0, 18, 21, 2, 69, 2, 61, 56, 10, 12, 34, 45, 60, 38, 8, 27, 55, 21, 52, 46, 58, 45, 46, 2, 61, 18, 56, 13, 64, 60, 39, 51, 50, 66, 30, 51, 54], 'visited': False}, 38: {'id': 38, 'neighbors': [19, 23, 62, 47, 10, 58, 50, 61, 57, 51, 21, 45, 37, 21, 7, 15, 10, 59, 11, 33, 52, 41, 69, 14, 35, 39, 68, 37, 41, 14, 22, 28, 39, 52, 50, 12, 22, 45, 39, 23, 24, 5, 57, 35, 66, 25, 56, 53, 27, 69], 'visited': False}, 39: {'id': 39, 'neighbors': [19, 9, 5, 49, 43, 8, 48, 16, 20, 13, 6, 61, 0, 26, 67, 10, 40, 26, 42, 69, 68, 68, 24, 38, 24, 10, 56, 36, 38, 48, 5, 7, 46, 52, 55, 8, 38, 64, 28, 4, 10, 37, 58, 49, 59, 69, 26], 'visited': False}, 40: {'id': 40, 'neighbors': [58, 20, 43, 18, 0, 24, 42, 21, 5, 32, 15, 66, 25, 57, 15, 57, 29, 3, 39, 32, 53, 31, 59, 15, 66, 0, 3, 7, 0, 3, 50, 47, 43, 62, 49, 46, 55, 69, 26, 64, 14, 19, 64, 16, 36, 54, 16, 60, 64], 'visited': False}, 41: {'id': 41, 'neighbors': [54, 50, 21, 9, 65, 27, 46, 42, 37, 34, 21, 69, 43, 43, 43, 56, 54, 64, 61, 18, 51, 38, 64, 17, 62, 13, 17, 9, 38, 36, 55, 46, 9, 46, 19, 58, 24, 28, 18, 20, 34, 25, 27, 35, 11, 65], 'visited': False}, 42: {'id': 42, 'neighbors': [61, 58, 6, 34, 20, 43, 22, 51, 0, 24, 59, 62, 41, 9, 40, 29, 63, 65, 36, 9, 29, 65, 20, 66, 59, 53, 39, 61, 25, 53, 48, 15, 50, 31, 48, 34, 50, 44, 58, 14, 62, 53, 1, 64, 21, 60, 60, 64, 50, 52], 'visited': False}, 43: {'id': 43, 'neighbors': [69, 14, 40, 42, 28, 65, 39, 3, 27, 61, 33, 53, 64, 31, 46, 57, 7, 14, 20, 32, 68, 41, 0, 50, 41, 41, 57, 30, 47, 26, 63, 51, 57, 17, 0, 24, 55, 51, 18, 11, 14, 66, 4, 63, 14, 29, 7, 40, 58, 66, 25, 8, 65, 67, 14, 2, 47, 4, 26, 51, 23, 26, 27, 50], 'visited': False}, 44: {'id': 44, 'neighbors': [28, 45, 66, 32, 23, 69, 0, 61, 21, 4, 32, 18, 7, 2, 68, 22, 33, 53, 0, 51, 45, 0, 34, 5, 33, 6, 35, 64, 29, 17, 65, 46, 2, 10, 8, 51, 13, 1, 53, 17, 6, 42, 68, 56, 56, 64, 32, 21, 68, 29, 45, 36, 59, 21, 8], 'visited': False}, 45: {'id': 45, 'neighbors': [13, 31, 44, 9, 0, 15, 69, 37, 3, 69, 12, 4, 69, 8, 59, 18, 49, 35, 7, 21, 38, 29, 54, 32, 2, 9, 67, 7, 28, 27, 44, 57, 21, 69, 26, 26, 59, 50, 66, 37, 29, 16, 49, 37, 48, 28, 34, 54, 2, 38, 13, 22, 35, 59, 68, 55, 64, 29, 68, 15, 9, 22, 44, 64, 50, 5, 46, 12], 'visited': False}, 46: {'id': 46, 'neighbors': [52, 65, 27, 14, 1, 41, 8, 65, 43, 21, 28, 48, 36, 2, 36, 23, 47, 17, 47, 14, 0, 54, 52, 34, 24, 11, 59, 24, 44, 12, 60, 47, 62, 2, 14, 20, 41, 19, 40, 41, 51, 37, 65, 37, 39, 34, 15, 63, 47, 3, 29, 36, 60, 1, 33, 0, 55, 45], 'visited': False}, 47: {'id': 47, 'neighbors': [1, 37, 48, 38, 34, 4, 63, 12, 48, 65, 28, 20, 67, 58, 53, 4, 3, 35, 46, 37, 56, 27, 3, 29, 46, 56, 43, 56, 69, 62, 21, 52, 0, 62, 0, 32, 21, 13, 21, 63, 32, 33, 46, 26, 32, 25, 40, 64, 23, 30, 10, 31, 0, 11, 63, 26, 6, 6, 8, 56, 31, 69, 49, 18, 5, 46, 43, 11, 8], 'visited': False}, 48: {'id': 48, 'neighbors': [62, 62, 18, 19, 0, 47, 25, 61, 33, 60, 39, 29, 47, 46, 64, 30, 25, 61, 69, 15, 23, 19, 3, 49, 26, 54, 42, 11, 26, 19, 35, 17, 68, 52, 31, 42, 39, 62, 2, 50, 0, 45, 68, 56, 58, 25, 15, 24, 34, 32, 35, 13, 35], 'visited': False}, 49: {'id': 49, 'neighbors': [8, 65, 26, 16, 1, 67, 60, 35, 39, 35, 37, 45, 16, 57, 50, 60, 60, 55, 21, 61, 56, 26, 14, 8, 9, 50, 16, 24, 48, 3, 7, 18, 15, 2, 64, 23, 54, 24, 27, 40, 45, 14, 58, 58, 47, 11, 11, 50, 69, 39, 27, 20, 28], 'visited': False}, 50: {'id': 50, 'neighbors': [67, 41, 32, 66, 10, 10, 13, 12, 38, 49, 16, 9, 65, 11, 25, 66, 66, 53, 43, 52, 8, 30, 57, 33, 56, 49, 23, 29, 52, 15, 45, 11, 59, 64, 42, 40, 57, 3, 42, 48, 16, 38, 57, 11, 17, 19, 6, 0, 29, 51, 49, 14, 61, 37, 7, 43, 11, 12, 42, 45, 24], 'visited': False}, 51: {'id': 51, 'neighbors': [58, 58, 62, 42, 0, 38, 53, 37, 8, 23, 23, 7, 44, 17, 23, 17, 41, 1, 43, 30, 20, 15, 31, 32, 8, 68, 66, 43, 44, 26, 30, 46, 0, 56, 67, 9, 61, 0, 0, 33, 17, 21, 50, 64, 59, 43, 11, 37, 8, 57, 37, 61, 25], 'visited': False}, 52: {'id': 52, 'neighbors': [46, 12, 25, 27, 22, 62, 25, 66, 10, 24, 23, 67, 50, 38, 64, 46, 47, 63, 22, 7, 65, 50, 19, 22, 9, 54, 28, 48, 61, 37, 24, 25, 9, 39, 38, 8, 20, 9, 56, 27, 23, 67, 42, 0], 'visited': False}, 53: {'id': 53, 'neighbors': [33, 27, 56, 18, 29, 61, 13, 54, 33, 37, 43, 32, 36, 51, 47, 13, 59, 58, 16, 19, 50, 44, 32, 42, 25, 63, 13, 31, 40, 35, 64, 59, 35, 21, 28, 42, 0, 60, 55, 54, 29, 68, 59, 55, 57, 44, 35, 30, 8, 69, 66, 14, 42, 13, 63, 54, 35, 32, 26, 54, 56, 38, 13], 'visited': False}, 54: {'id': 54, 'neighbors': [4, 66, 41, 65, 14, 27, 58, 67, 8, 23, 53, 69, 17, 21, 45, 35, 20, 67, 18, 2, 58, 11, 64, 41, 32, 65, 28, 34, 46, 62, 60, 25, 48, 60, 34, 58, 8, 67, 14, 52, 17, 53, 49, 60, 36, 17, 31, 66, 21, 45, 18, 31, 23, 7, 0, 53, 6, 14, 31, 61, 29, 40, 62, 17, 53, 37, 55, 5, 8], 'visited': False}, 55: {'id': 55, 'neighbors': [16, 30, 33, 17, 31, 49, 28, 27, 17, 27, 13, 19, 6, 0, 12, 12, 27, 43, 68, 53, 22, 41, 37, 34, 3, 53, 40, 32, 20, 10, 1, 39, 31, 27, 65, 45, 31, 30, 19, 67, 46, 54], 'visited': False}, 56: {'id': 56, 'neighbors': [35, 53, 59, 37, 28, 0, 60, 22, 2, 32, 62, 6, 14, 17, 64, 34, 65, 36, 47, 18, 41, 20, 15, 47, 49, 47, 19, 5, 69, 7, 14, 50, 6, 29, 12, 9, 37, 9, 39, 5, 51, 13, 37, 23, 47, 48, 44, 20, 52, 44, 15, 15, 6, 27, 30, 34, 66, 38, 53, 33, 57], 'visited': False}, 57: {'id': 57, 'neighbors': [6, 33, 66, 6, 35, 33, 38, 49, 69, 25, 43, 59, 60, 27, 40, 68, 40, 43, 9, 30, 50, 20, 45, 29, 9, 30, 43, 58, 20, 16, 64, 27, 64, 65, 4, 50, 60, 53, 23, 32, 20, 50, 62, 63, 24, 36, 38, 20, 65, 51, 13, 15, 56], 'visited': False}, 58: {'id': 58, 'neighbors': [40, 42, 35, 2, 51, 51, 54, 38, 66, 62, 60, 8, 62, 25, 37, 29, 47, 53, 66, 61, 4, 54, 3, 12, 63, 29, 30, 19, 60, 57, 29, 4, 30, 33, 23, 1, 16, 54, 59, 22, 15, 22, 59, 25, 13, 43, 37, 41, 36, 42, 66, 49, 26, 49, 12, 48, 39, 61, 27], 'visited': False}, 59: {'id': 59, 'neighbors': [26, 56, 2, 45, 32, 7, 42, 19, 30, 36, 53, 57, 3, 33, 38, 9, 27, 63, 67, 10, 42, 60, 4, 32, 23, 40, 53, 31, 30, 46, 45, 5, 1, 31, 50, 58, 0, 58, 68, 24, 6, 20, 53, 45, 28, 51, 69, 26, 0, 7, 39, 44], 'visited': False}, 60: {'id': 60, 'neighbors': [49, 22, 56, 48, 14, 58, 49, 49, 30, 64, 18, 57, 8, 66, 10, 61, 5, 11, 14, 61, 5, 59, 11, 54, 58, 29, 36, 25, 3, 54, 15, 8, 46, 33, 37, 53, 63, 57, 54, 0, 65, 18, 1, 13, 31, 27, 37, 5, 66, 66, 8, 42, 66, 46, 42, 40], 'visited': False}, 61: {'id': 61, 'neighbors': [42, 13, 53, 48, 38, 44, 43, 23, 66, 6, 15, 6, 68, 35, 9, 58, 65, 8, 39, 11, 60, 49, 13, 41, 60, 48, 29, 25, 42, 11, 36, 4, 66, 37, 30, 66, 67, 34, 69, 1, 33, 66, 63, 52, 13, 64, 62, 29, 15, 37, 66, 35, 33, 51, 20, 13, 4, 31, 36, 54, 50, 6, 25, 23, 51, 9, 58], 'visited': False}, 62: {'id': 62, 'neighbors': [48, 48, 19, 68, 38, 5, 63, 51, 1, 63, 0, 42, 52, 58, 56, 58, 22, 17, 4, 14, 3, 5, 4, 69, 47, 54, 17, 24, 8, 47, 41, 7, 28, 25, 46, 6, 33, 34, 40, 21, 32, 48, 61, 63, 42, 2, 57, 69, 68, 32, 17, 17, 69, 54, 33, 68], 'visited': False}, 63: {'id': 63, 'neighbors': [64, 0, 27, 0, 10, 62, 6, 37, 18, 62, 8, 36, 13, 47, 14, 0, 42, 19, 34, 36, 9, 24, 59, 16, 58, 53, 4, 11, 26, 43, 52, 66, 47, 69, 69, 64, 6, 5, 43, 61, 60, 31, 69, 62, 47, 33, 11, 57, 46, 28, 53, 3, 19, 27, 0, 14, 11], 'visited': False}, 64: {'id': 64, 'neighbors': [63, 9, 12, 2, 4, 3, 35, 43, 16, 48, 60, 28, 56, 28, 14, 5, 27, 7, 34, 54, 26, 41, 52, 1, 9, 41, 53, 18, 35, 2, 44, 7, 57, 63, 49, 50, 57, 35, 23, 7, 26, 47, 61, 6, 37, 6, 65, 39, 40, 45, 44, 42, 12, 29, 51, 40, 42, 11, 45, 31, 40], 'visited': False}, 65: {'id': 65, 'neighbors': [49, 24, 2, 8, 54, 46, 22, 41, 43, 25, 21, 33, 46, 47, 50, 25, 20, 16, 42, 61, 26, 56, 35, 14, 42, 4, 67, 54, 30, 20, 52, 44, 2, 5, 20, 57, 9, 46, 33, 60, 17, 16, 10, 43, 4, 69, 64, 55, 57, 17, 23, 1, 35, 41, 32, 17], 'visited': False}, 66: {'id': 66, 'neighbors': [30, 57, 54, 44, 50, 58, 17, 61, 52, 14, 40, 34, 0, 50, 50, 58, 60, 17, 42, 67, 30, 17, 67, 0, 28, 63, 61, 40, 45, 51, 61, 21, 43, 16, 31, 61, 24, 43, 67, 35, 61, 58, 54, 9, 9, 53, 18, 60, 29, 60, 37, 38, 23, 56, 60, 26], 'visited': False}, 67: {'id': 67, 'neighbors': [32, 49, 7, 50, 54, 18, 31, 1, 1, 21, 4, 31, 2, 47, 34, 68, 11, 52, 22, 11, 54, 27, 34, 45, 10, 39, 37, 13, 65, 59, 25, 66, 66, 32, 20, 7, 31, 0, 20, 34, 61, 14, 6, 54, 66, 51, 7, 10, 43, 13, 24, 3, 23, 52, 29, 55], 'visited': False}, 68: {'id': 68, 'neighbors': [9, 25, 62, 23, 6, 36, 36, 16, 27, 14, 15, 13, 15, 9, 0, 61, 31, 67, 15, 43, 57, 44, 18, 30, 34, 2, 1, 25, 17, 39, 39, 20, 26, 30, 14, 28, 32, 51, 18, 38, 18, 28, 29, 48, 55, 59, 22, 3, 53, 3, 6, 28, 48, 44, 62, 45, 21, 32, 12, 25, 33, 45, 30, 44, 10, 62, 5], 'visited': False}, 69: {'id': 69, 'neighbors': [15, 10, 43, 31, 45, 45, 44, 0, 33, 23, 45, 54, 8, 33, 7, 57, 33, 24, 12, 41, 62, 47, 13, 2, 48, 37, 56, 45, 38, 10, 12, 39, 4, 0, 12, 63, 18, 7, 63, 61, 0, 35, 15, 63, 40, 53, 62, 65, 0, 47, 33, 36, 20, 62, 49, 59, 21, 35, 16, 39, 35, 38], 'visited': False}}

                --> adjacency matrix:
[[0 1 1 ... 1 1 1]
 [1 0 1 ... 1 1 0]
 [1 1 0 ... 1 1 1]
 ...
 [1 1 1 ... 0 1 0]
 [1 1 1 ... 1 0 0]
 [1 0 1 ... 0 0 0]]

depth: 0, visit: 15 --> distance from node 15 is: 0
        depth: 1, visit: 0 --> distance from node 15 is: 6
        depth: 1, visit: 69 --> distance from node 15 is: 6
        depth: 1, visit: 1 --> distance from node 15 is: 6
        depth: 1, visit: 45 --> distance from node 15 is: 6
        depth: 1, visit: 35 --> distance from node 15 is: 6
        depth: 1, visit: 12 --> distance from node 15 is: 6
        depth: 1, visit: 68 --> distance from node 15 is: 6
        depth: 1, visit: 19 --> distance from node 15 is: 6
        depth: 1, visit: 11 --> distance from node 15 is: 6
        depth: 1, visit: 32 --> distance from node 15 is: 6
        depth: 1, visit: 61 --> distance from node 15 is: 6
        depth: 1, visit: 40 --> distance from node 15 is: 6
        depth: 1, visit: 38 --> distance from node 15 is: 6
        depth: 1, visit: 5 --> distance from node 15 is: 6
        depth: 1, visit: 56 --> distance from node 15 is: 6
        depth: 1, visit: 25 --> distance from node 15 is: 6
        depth: 1, visit: 21 --> distance from node 15 is: 6
        depth: 1, visit: 48 --> distance from node 15 is: 6
        depth: 1, visit: 3 --> distance from node 15 is: 6
        depth: 1, visit: 18 --> distance from node 15 is: 6
        depth: 1, visit: 14 --> distance from node 15 is: 6
        depth: 1, visit: 7 --> distance from node 15 is: 6
        depth: 1, visit: 51 --> distance from node 15 is: 6
        depth: 1, visit: 50 --> distance from node 15 is: 6
        depth: 1, visit: 23 --> distance from node 15 is: 6
        depth: 1, visit: 60 --> distance from node 15 is: 6
        depth: 1, visit: 49 --> distance from node 15 is: 6
        depth: 1, visit: 58 --> distance from node 15 is: 6
        depth: 1, visit: 42 --> distance from node 15 is: 6
        depth: 1, visit: 2 --> distance from node 15 is: 6
        depth: 1, visit: 46 --> distance from node 15 is: 6
        depth: 1, visit: 13 --> distance from node 15 is: 6
        depth: 1, visit: 10 --> distance from node 15 is: 6
        depth: 1, visit: 27 --> distance from node 15 is: 6
        depth: 1, visit: 57 --> distance from node 15 is: 6
        depth: 1, visit: 20 --> distance from node 15 is: 6
                depth: 2, visit: 63 --> distance from node 15 is: 12
                depth: 2, visit: 31 --> distance from node 15 is: 12
                depth: 2, visit: 16 --> distance from node 15 is: 12
                depth: 2, visit: 62 --> distance from node 15 is: 12
                depth: 2, visit: 44 --> distance from node 15 is: 12
                depth: 2, visit: 8 --> distance from node 15 is: 12
                depth: 2, visit: 37 --> distance from node 15 is: 12
                depth: 2, visit: 30 --> distance from node 15 is: 12
                depth: 2, visit: 9 --> distance from node 15 is: 12
                depth: 2, visit: 66 --> distance from node 15 is: 12
                depth: 2, visit: 6 --> distance from node 15 is: 12
                depth: 2, visit: 39 --> distance from node 15 is: 12
                depth: 2, visit: 43 --> distance from node 15 is: 12
                depth: 2, visit: 22 --> distance from node 15 is: 12
                depth: 2, visit: 33 --> distance from node 15 is: 12
                depth: 2, visit: 34 --> distance from node 15 is: 12
                depth: 2, visit: 55 --> distance from node 15 is: 12
                depth: 2, visit: 47 --> distance from node 15 is: 12
                depth: 2, visit: 29 --> distance from node 15 is: 12
                depth: 2, visit: 53 --> distance from node 15 is: 12
                depth: 2, visit: 67 --> distance from node 15 is: 12
                depth: 2, visit: 59 --> distance from node 15 is: 12
                depth: 2, visit: 26 --> distance from node 15 is: 12
                depth: 2, visit: 36 --> distance from node 15 is: 12
                depth: 2, visit: 54 --> distance from node 15 is: 12
                depth: 2, visit: 52 --> distance from node 15 is: 12
                depth: 2, visit: 24 --> distance from node 15 is: 12
                depth: 2, visit: 41 --> distance from node 15 is: 12
                depth: 2, visit: 4 --> distance from node 15 is: 12
                depth: 2, visit: 65 --> distance from node 15 is: 12
                depth: 2, visit: 64 --> distance from node 15 is: 12
                depth: 2, visit: 28 --> distance from node 15 is: 12
                depth: 2, visit: 17 --> distance from node 15 is: 12
TEST CASE 01.1:
        result: 6 6 6 6 12 6 12 6 12 12 6 6 6 6 6 12 12 6 6 6 6 12 6 12 6 12 6 12 12 12 12 6 12 12 6 12 12 6 12 6 12 6 12 12 6 6 12 6 6 6 6 12 12 12 12 6 6 6 12 6 6 12 12 12 12 12 12 6 6
        expect: 6 6 6 6 12 6 12 6 12 12 6 6 6 6 6 12 12 6 6 6 6 12 6 12 6 12 6 12 12 12 12 6 12 12 6 12 12 6 12 6 12 6 12 12 6 6 12 6 6 6 6 12 12 12 12 6 6 6 12 6 6 12 12 12 12 12 12 6 6
                --> PASS
```

## Third Try:

The logic implemented previously is sound.  This changes made in this iteration consisted only of optimization.  

Specifically:
- change `neighbors` collection from `list` to `set`
- changed `nodes_pending_queue` from `list` to `deque`, which probably had the biggest impact... `pop()` occurs in O(1) time

After making the above changes, the final failing test-case 05 passed.

(see below for my full implementation of this algorithm)

```python
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
```


## POST-MORTEM:

Once again, the puzzle itself is very straightforward, even easy, but of course requires knowing a little bit of graph theory.  The pitfalls I encountered here centered around using optimal auxiliary data structures.  (see above commentary)

## POST-POST-MORTEM:

Similar to other graph-theory puzzles, even though I have already solved this, I thought I would revisit this problem to improve the clarity of my former presentation.  My follow-up centers around the creation of a class in order to better encapsulate most of the graph-theory boiler-plate implementation.

The refactoring also improved performance (runtime complexity) further, even though all test-cases were already passing.

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
```

Note that in addition to the above code, usage works as follows:

First, instantiate:
```python
graph = Graph(n, node_labels = list(range(n)))
```

Then:
```python
graph.edge_weight = 6
graph.distances = [-1] * len(graph._d_graph)
graph.print_distances = not debug
graph.find_all_distances = find_all_distances
```

Finally, call:
```python
graph.find_all_distances(graph, s-1)
```

<p><br>

(Debug) Output for test-case 00:

```
                --> graph:
{0: {'id': 0, 'neighbors': {1, 2}}, 1: {'id': 1, 'neighbors': {0}}, 2: {'id': 2, 'neighbors': {0}}, 3: {'id': 3, 'neighbors': set()}}

                --> adjacency matrix:
[[0 1 1 0]
 [1 0 0 0]
 [1 0 0 0]
 [0 0 0 0]]

        (depth 0) visit: 0, neighbors: {1, 2}
                --> distance from start node is: depth * edge_weight = 0 * 6 = 0
                (depth 1) visit: 1, neighbors: {0}
                        --> distance from start node is: depth * edge_weight = 1 * 6 = 6
                        neighbor node 0 has already been visited
                (depth 1) visit: 2, neighbors: {0}
                        --> distance from start node is: depth * edge_weight = 1 * 6 = 6
                        neighbor node 0 has already been visited

find_all_distances (from start node 0) result: [6, 6, -1]

                --> graph:
{0: {'id': 0, 'neighbors': set()}, 1: {'id': 1, 'neighbors': {2}}, 2: {'id': 2, 'neighbors': {1}}}

                --> adjacency matrix:
[[0 0 0]
 [0 0 1]
 [0 1 0]]

        (depth 0) visit: 1, neighbors: {2}
                --> distance from start node is: depth * edge_weight = 0 * 6 = 0
                (depth 1) visit: 2, neighbors: {1}
                        --> distance from start node is: depth * edge_weight = 1 * 6 = 6
                        neighbor node 1 has already been visited

find_all_distances (from start node 1) result: [-1, 6]

TEST CASE 00.1:
        result: 6 6 -1
        expect: 6 6 -1
                --> PASS

TEST CASE 00.2:
        result: -1 6
        expect: -1 6
                --> PASS
```

<p><br>

(Debug) Output for test-case 07:

```
                --> graph:
{0: {'id': 0, 'neighbors': {1, 4}}, 1: {'id': 1, 'neighbors': {0, 2}}, 2: {'id': 2, 'neighbors': {1, 3}}, 3: {'id': 3, 'neighbors': {2}}, 4: {'id': 4, 'neighbors': {0}}, 5: {'id': 5, 'neighbors': set()}}

                --> adjacency matrix:
[[0 1 0 0 1 0]
 [1 0 1 0 0 0]
 [0 1 0 1 0 0]
 [0 0 1 0 0 0]
 [1 0 0 0 0 0]
 [0 0 0 0 0 0]]

        (depth 0) visit: 0, neighbors: {1, 4}
                --> distance from start node is: depth * edge_weight = 0 * 6 = 0
                (depth 1) visit: 1, neighbors: {0, 2}
                        --> distance from start node is: depth * edge_weight = 1 * 6 = 6
                        neighbor node 0 has already been visited
                (depth 1) visit: 4, neighbors: {0}
                        --> distance from start node is: depth * edge_weight = 1 * 6 = 6
                        neighbor node 0 has already been visited
                        (depth 2) visit: 2, neighbors: {1, 3}
                                --> distance from start node is: depth * edge_weight = 2 * 6 = 12
                                neighbor node 1 has already been visited
                                (depth 3) visit: 3, neighbors: {2}
                                        --> distance from start node is: depth * edge_weight = 3 * 6 = 18
                                        neighbor node 2 has already been visited

find_all_distances (from start node 0) result: [6, 12, 18, 6, -1]

TEST CASE 07.1:
        result: 6 12 18 6 -1
        expect: 6 12 18 6 -1
                --> PASS
```

<p><br>

(Debug) Output for test-case 08:

```
                --> graph:
{0: {'id': 0, 'neighbors': {1, 2}}, 1: {'id': 1, 'neighbors': {0, 4}}, 2: {'id': 2, 'neighbors': {0, 3}}, 3: {'id': 3, 'neighbors': {2}}, 4: {'id': 4, 'neighbors': {1}}, 5: {'id': 5, 'neighbors': set()}, 6: {'id': 6, 'neighbors': set()}}

                --> adjacency matrix:
[[0 1 1 0 0 0 0]
 [1 0 0 0 1 0 0]
 [1 0 0 1 0 0 0]
 [0 0 1 0 0 0 0]
 [0 1 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]]

        (depth 0) visit: 1, neighbors: {0, 4}
                --> distance from start node is: depth * edge_weight = 0 * 6 = 0
                (depth 1) visit: 0, neighbors: {1, 2}
                        --> distance from start node is: depth * edge_weight = 1 * 6 = 6
                        neighbor node 1 has already been visited
                (depth 1) visit: 4, neighbors: {1}
                        --> distance from start node is: depth * edge_weight = 1 * 6 = 6
                        neighbor node 1 has already been visited
                        (depth 2) visit: 2, neighbors: {0, 3}
                                --> distance from start node is: depth * edge_weight = 2 * 6 = 12
                                neighbor node 0 has already been visited
                                (depth 3) visit: 3, neighbors: {2}
                                        --> distance from start node is: depth * edge_weight = 3 * 6 = 18
                                        neighbor node 2 has already been visited

find_all_distances (from start node 1) result: [6, 12, 18, 6, -1, -1]

TEST CASE 08.1:
        result: 6 12 18 6 -1 -1
        expect: 6 12 18 6 -1 -1
                --> PASS
```