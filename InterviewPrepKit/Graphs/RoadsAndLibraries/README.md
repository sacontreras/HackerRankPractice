[link](https://www.hackerrank.com/challenges/torque-and-development/problem?h_l=interview&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=graphs)


## First Try:

This puzzle is not particularly tricky.  It only requires unnderstanding the theory: graphs and DFS.  

There was only really one "gotcha" here, and it was unveiled by failing free test-case 12. In the problem statement we are told that we are given cities (nodes in the graph) labeled $1... n$.  However, when a node does not have any outbound edges - i.e. "roads" - it is not specified in the input... it is absent, since the input consists of an array of $[node_i, node_j]$ where $i$ is the index of the source node and $j$ is the index of the node of the outbound edge, where $i \ne j$.  So, when a node does not have any outbound edges - i.e. it is not connected to any other nodes - it must still be represented (exist) in the graph.

Although it wasn't a "gotcha", per se, it was also important to recognize the algorithm could be further optimized, that DFS traversal - indeed, even building the graph - is unnecessary when `c_road >= c_lib`.  In that case, we know that "case 2" applies for minimum cost (see algorithm).

After considering the above and, of course, implementing the graph datastructure and DFS correctly, all of the free test-cases passed successfully.  Upon submission, all of the remaining locked test-cases passed successfully as well.

(see below for my full implementation of this algorithm)


```python
def build_graph(n, cities, debug=False):
    d_cities_graph = {}
    on_diag = set(range(1,n+1))
    if debug:
        print(f"\tbuilding graph...")
        adj_mat = [[0 for _ in range(n)] for _ in range(n)]
    for road_city_start, road_city_end in cities:
        i = road_city_start
        j = road_city_end
        
        node_i = d_cities_graph.get(i,{'to_nodes':[],'visited':False})
        node_i['to_nodes'].append(j)
        d_cities_graph[i] = node_i
        on_diag -= set([i])

        node_j = d_cities_graph.get(j,{'to_nodes':[],'visited':False})
        node_j['to_nodes'].append(i)
        d_cities_graph[j] = node_j
        on_diag -= set([j])

        if debug:
            adj_mat[i-1][j-1] = adj_mat[j-1][i-1] = 1

    for i in list(on_diag):
        node_i = d_cities_graph.get(i,{'to_nodes':[],'visited':False})
        d_cities_graph[i] = node_i
        if debug:
            adj_mat[i-1][i-1] = 1

    if debug:
        print(f"\t\t--> graph:\n{d_cities_graph}\n")
        print(f"\t\t--> adjacency matrix:\n{np.matrix(adj_mat)}\n")

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
```

<p><br>

(Debug) Output for test-case 00:

```
n: 3, c_lib: 2, c_road: 1, cities: [[1, 2], [3, 1], [2, 3]]
c_road < c_lib --> must build graph and traverse DFS
        building graph...
                --> graph:
{1: {'to_nodes': [2, 3], 'visited': False}, 2: {'to_nodes': [1, 3], 'visited': False}, 3: {'to_nodes': [1, 2], 'visited': False}}

                --> adjacency matrix:
[[0 1 1]
 [1 0 1]
 [1 1 0]]

        traversing graph DFS (building city-paths for each 'county')...
                visit: 1, to_nodes: [2, 3]
                visit: 2, to_nodes: [1, 3]
                        1 has already been visited
                visit: 3, to_nodes: [1, 2]
                        1 has already been visited
                        2 has already been visited
                        3 has already been visited
                        2 has already been visited
                        3 has already been visited
                2 has already been visited
                3 has already been visited
                --> counties: [[1, 2, 3]]

        computing optimal (minimal) cost for each county...
                for county [1, 2, 3]...
                        cost for case 1: 1 library accessible via city path [1, 2, 3]
                                --> (n_roads * c_road) + (1 * c_lib) = (2*1)+(1*2) = 4
                        cost for case 2: 1 library for each of the 3 cities in the county
                                --> n_cities * c_lib = 3*2 = 6
                        MINIMAL COST: CASE 1: 4


n: 6, c_lib: 2, c_road: 5, cities: [[1, 3], [3, 4], [2, 4], [1, 2], [2, 3], [5, 6]]
c_road >= c_lib --> CASE 2 IS OPTIMAL (min cost)
        cost for CASE 2: 1 library for each of the 6
                --> n * c_lib = 6*2 = 12
TEST CASE 00.1:
        result: 4
        expect: 4
                --> PASS

TEST CASE 00.2:
        result: 12
        expect: 12
                --> PASS
```

<p><br>

(Debug) Output for test-case 11:

```
n: 6, c_lib: 2, c_road: 3, cities: [[1, 2], [1, 3], [4, 5], [4, 6]]
c_road >= c_lib --> CASE 2 IS OPTIMAL (min cost)
        cost for CASE 2: 1 library for each of the 6
                --> n * c_lib = 6*2 = 12
TEST CASE 11.1:
        result: 12
        expect: 12
                --> PASS
```

<p><br>

(Debug) Output for test-case 12:

```
n: 5, c_lib: 6, c_road: 1, cities: [[1, 2], [1, 3], [1, 4]]
c_road < c_lib --> must build graph and traverse DFS
        building graph...
                --> graph:
{1: {'to_nodes': [2, 3, 4], 'visited': False}, 2: {'to_nodes': [1], 'visited': False}, 3: {'to_nodes': [1], 'visited': False}, 4: {'to_nodes': [1], 'visited': False}, 5: {'to_nodes': [], 'visited': False}}

                --> adjacency matrix:
[[0 1 1 1 0]
 [1 0 0 0 0]
 [1 0 0 0 0]
 [1 0 0 0 0]
 [0 0 0 0 0]]
                --> disconnected nodes: {5}

        traversing graph DFS (building city-paths for each 'county')...
                visit: 1, to_nodes: [2, 3, 4]
                visit: 2, to_nodes: [1]
                        1 has already been visited
                        2 has already been visited
                visit: 3, to_nodes: [1]
                        1 has already been visited
                        3 has already been visited
                visit: 4, to_nodes: [1]
                        1 has already been visited
                        4 has already been visited
                2 has already been visited
                3 has already been visited
                4 has already been visited
                visit: 5, to_nodes: []
                --> counties: [[1, 2, 3, 4], [5]]

        computing optimal (minimal) cost for each county...
                for county [1, 2, 3, 4]...
                        cost for case 1: 1 library accessible via city path [1, 2, 3, 4]
                                --> (n_roads * c_road) + (1 * c_lib) = (3*1)+(1*6) = 9
                        cost for case 2: 1 library for each of the 4 cities in the county
                                --> n_cities * c_lib = 4*6 = 24
                        MINIMAL COST: CASE 1: 9

                for county [5]...
                        cost for case 1: 1 library accessible via city path [5]
                                --> (n_roads * c_road) + (1 * c_lib) = (0*1)+(1*6) = 6
                        cost for case 2: 1 library for each of the 1 cities in the county
                                --> n_cities * c_lib = 1*6 = 6
                        MINIMAL COST: CASE 1: 6


TEST CASE 12.1:
        result: 15
        expect: 15
                --> PASS
```

## POST-MORTEM:

The high-level moral of the story is: 1.) understand theory, and 2.) make sure all of your free test-cases pass. (Obvious, but worth emphasizing here.)

## POST-POST-MORTEM:

Similar to other graph-theory puzzle, even though I have already solved this, I thought I would revisit this problem to improve the clarity of my former presentation.  My follow-up centers around the creation of a class in order to better encapsulate most of the graph-theory boiler-plate implementation.

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
```

<p><br>

(Debug) Output for test-case 00:

```
n: 3, c_lib: 2, c_road: 1, cities: [[1, 2], [3, 1], [2, 3]]
c_road < c_lib --> must build graph and traverse DFS
        building graph...
                --> graph:
{1: {'id': 1, 'neighbors': {2, 3}}, 2: {'id': 2, 'neighbors': {1, 3}}, 3: {'id': 3, 'neighbors': {1, 2}}}

                --> adjacency matrix:
[[0 1 1]
 [1 0 1]
 [1 1 0]]

        traversing graph DFS (building city-paths for each 'county')...
        (depth 0) visit: 1, neighbors: {2, 3}
                (depth 1) visit: 3, neighbors: {1, 2}
                        neighbor node 1 has already been visited
                        (depth 2) visit: 2, neighbors: {1, 3}
                                neighbor node 1 has already been visited
                                neighbor node 3 has already been visited
        (start) node 2 has already been visited
        (start) node 3 has already been visited
                --> counties: [[1, 3, 2]]

        computing optimal (minimal) cost for each county...
                for county [1, 3, 2]...
                        cost for case 1: 1 library accessible via city path [1, 3, 2]
                                --> (n_roads * c_road) + (1 * c_lib) = (2*1)+(1*2) = 4
                        cost for case 2: 1 library for each of the 3 cities in the county
                                --> n_cities * c_lib = 3*2 = 6
                        MINIMAL COST: CASE 1: 4


n: 6, c_lib: 2, c_road: 5, cities: [[1, 3], [3, 4], [2, 4], [1, 2], [2, 3], [5, 6]]
c_road >= c_lib --> CASE 2 IS OPTIMAL (min cost)
        cost for CASE 2: 1 library for each of the 6
                --> n * c_lib = 6*2 = 12
TEST CASE 00.1:
        result: 4
        expect: 4
                --> PASS

TEST CASE 00.2:
        result: 12
        expect: 12
                --> PASS
```

<p><br>

(Debug) Output for test-case 11:

```
n: 6, c_lib: 2, c_road: 3, cities: [[1, 2], [1, 3], [4, 5], [4, 6]]
c_road >= c_lib --> CASE 2 IS OPTIMAL (min cost)
        cost for CASE 2: 1 library for each of the 6
                --> n * c_lib = 6*2 = 12
TEST CASE 11.1:
        result: 12
        expect: 12
                --> PASS
```

<p><br>

(Debug) Output for test-case 12:

```
n: 5, c_lib: 6, c_road: 1, cities: [[1, 2], [1, 3], [1, 4]]
c_road < c_lib --> must build graph and traverse DFS
        building graph...
                --> graph:
{1: {'id': 1, 'neighbors': {2, 3, 4}}, 2: {'id': 2, 'neighbors': {1}}, 3: {'id': 3, 'neighbors': {1}}, 4: {'id': 4, 'neighbors': {1}}, 5: {'id': 5, 'neighbors': set()}}

                --> adjacency matrix:
[[0 1 1 1 0]
 [1 0 0 0 0]
 [1 0 0 0 0]
 [1 0 0 0 0]
 [0 0 0 0 0]]

        traversing graph DFS (building city-paths for each 'county')...
        (depth 0) visit: 1, neighbors: {2, 3, 4}
                (depth 1) visit: 4, neighbors: {1}
                        neighbor node 1 has already been visited
                (depth 1) visit: 3, neighbors: {1}
                        neighbor node 1 has already been visited
                (depth 1) visit: 2, neighbors: {1}
                        neighbor node 1 has already been visited
        (start) node 2 has already been visited
        (start) node 3 has already been visited
        (start) node 4 has already been visited
        (depth 0) visit: 5, neighbors: set()
                --> counties: [[1, 4, 3, 2], [5]]

        computing optimal (minimal) cost for each county...
                for county [1, 4, 3, 2]...
                        cost for case 1: 1 library accessible via city path [1, 4, 3, 2]
                                --> (n_roads * c_road) + (1 * c_lib) = (3*1)+(1*6) = 9
                        cost for case 2: 1 library for each of the 4 cities in the county
                                --> n_cities * c_lib = 4*6 = 24
                        MINIMAL COST: CASE 1: 9

                for county [5]...
                        cost for case 1: 1 library accessible via city path [5]
                                --> (n_roads * c_road) + (1 * c_lib) = (0*1)+(1*6) = 6
                        cost for case 2: 1 library for each of the 1 cities in the county
                                --> n_cities * c_lib = 1*6 = 6
                        MINIMAL COST: CASE 1: 6


TEST CASE 12.1:
        result: 15
        expect: 15
                --> PASS
```