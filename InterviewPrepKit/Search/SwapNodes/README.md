[link](https://www.hackerrank.com/challenges/swap-nodes-algo/problem?h_l=interview&h_r=next-challenge&h_v=zen&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=search)


## First Try:

The first thing I have to say is that I had to re-read the problem statement several times before understanding the problem in its totality.  The difficult part is not the theory required which is, of course, Binary Trees and their respective traversals.  That part is straightforward.  

What wasn't immediately straightforward was that swaps should occur when:
- traversing in *preorder*
- given the definition of *depth* as stated in the problem statement - i.e. depth of the root is 1 (not 0, as is the usual fashion), then child nodes of all nodes with $depth\ \%\ k == 0$ should be swapped.  

NOTE that at first I thought only child nodes of all nodes with $depth\ == k$ should be swapped.  Additionally, I initially traversed *inorder* to conduct the swap.

Then, of course, after the swaps are complete the tree should be traversed *inorder*.  This part was straightforward from the start - the problem statement makes this clear.

But my initial mistakes noted above initially resulted in the free test-cases failing.

Upon addressing those mistakes, all free test-cases passed and upon submission, all remaining locked test-cases passed.

I should also note that it was important to adjust the recursion limit via
```
import sys
sys.setrecursionlimit(2000)
```
as well.

(see below for my full implementation of this algorithm)

```
import sys
sys.setrecursionlimit(2000)

class BinaryTree():
    def __init__(self, val, depth=0, orientation=0, parent=None, debug=False):
        self.val = val
        self.depth = depth
        self.orientation = orientation
        self.parent = parent
        self.left = None
        self.right = None
        self.debug = debug

        if debug:
            print("\t"*depth, end="")
            if orientation == 0:
                print(f"--> new ROOT ", end="")
            elif orientation == -1:
                print(f"parent (val:{parent.val},depth:{parent.depth}) --> new LEFT child ", end="")
            else:
                print(f"parent (val:{parent.val},depth:{parent.depth}) --> new RIGHT child ", end="")
            print(f"(val:{val},depth:{depth})")

    def new_left_child(self, val):
        self.left = BinaryTree(val=val, depth=self.depth+1, orientation=-1, parent=self, debug=self.debug)
        return self.left

    def new_right_child(self, val):
        self.right = BinaryTree(val=val, depth=self.depth+1, orientation=1, parent=self, debug=self.debug)
        return self.right


def print_tree(root, val="val", left="left", right="right"):
    """
    https://stackoverflow.com/a/65865825/11761918
    """
    def display(root, val=val, left=left, right=right):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if getattr(root, right) is None and getattr(root, left) is None:
            line = '%s' % getattr(root, val)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if getattr(root, right) is None:
            lines, n, p, x = display(getattr(root, left))
            s = '%s' % getattr(root, val)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if getattr(root, left) is None:
            lines, n, p, x = display(getattr(root, right))
            s = '%s' % getattr(root, val)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = display(getattr(root, left))
        right, m, q, y = display(getattr(root, right))
        s = '%s' % getattr(root, val)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

    lines, *_ = display(root, val, left, right)
    for line in lines:
        print(line)


def build_tree(indexes, debug=False):
    """
    level-order iteration using double-ended queue
    """
    n_index_pairs = len(indexes)
    if debug:
        print(f"\t--> tree has {n_index_pairs} child-index pairs --> MAX of {2*n_index_pairs + 1} nodes possible (including ROOT)")
        print(f"BUILDING TREE...")

    root = None
    if n_index_pairs > 0:
        nodes_pending_queue = []
        root = BinaryTree(val=1, debug=debug)
        nodes_pending_queue.insert(0, root)
        while len(indexes) > 0:
            p = nodes_pending_queue.pop()
            v_l, v_r = indexes.pop(0)
            if v_l != -1:
                nodes_pending_queue.insert(0, p.new_left_child(v_l))
            if v_r != -1:
                nodes_pending_queue.insert(0, p.new_right_child(v_r))

    if debug:
        print(f"BUILT TREE:")
        print_tree(root)
        print()

    return root


def swap_children(kargs):
    p = kargs['p']
    d = kargs['d']
    debug = kargs['debug']

    q = kargs['query']

    left_child = p.left
    right_child = p.right

    if (left_child is not None or right_child is not None) and (p.depth+1) % q == 0:
        if debug:
            if p.orientation == 0:
                print(f"ROOT ", end="")
            print(f"node (val:{p.val},depth:{p.depth}) ", end="")
            print(f"MATCHES query: child-depth {p.depth+1} % {q} == 0:")
            print(f"\tSWAP LEFT: ({'None' if left_child is None else 'val:'+str(left_child.val)+',depth:'+str(left_child.depth)}), ", end="")
            print(f"RIGHT: ({'None' if right_child is None else 'val:'+str(right_child.val)+',depth:'+str(right_child.depth)}) ")

        p.left = right_child
        p.right = left_child

        if debug:
            print(f"\t\t--> LEFT: ({'None' if p.left is None else 'val:'+str(p.left.val)+',depth:'+str(p.left.depth)}), ", end="")
            print(f"RIGHT: ({'None' if p.right is None else 'val:'+str(p.right.val)+',depth:'+str(p.right.depth)})")


def traverse_preorder(p, d=0, fn_visit_handler=swap_children, fn_visit_handler__kargs=None, debug=False):
    if p is None:
        return

    if fn_visit_handler__kargs is None:
        fn_visit_handler__kargs = {}
    kargs = {'p':p,'d':d,'debug':debug}
    fn_visit_handler__kargs.update(kargs)
    fn_visit_handler(fn_visit_handler__kargs)

    traverse_preorder(
        p.left, 
        d=d+1, 
        fn_visit_handler=fn_visit_handler, 
        fn_visit_handler__kargs=fn_visit_handler__kargs, 
        debug=debug)

    traverse_preorder(
        p.right, 
        d=d+1, 
        fn_visit_handler=fn_visit_handler, 
        fn_visit_handler__kargs=fn_visit_handler__kargs, 
        debug=debug)


def append_list(kargs):
    p = kargs['p']
    d = kargs['d']
    debug = kargs['debug']

    lst = kargs['list']
    lst.append(p.val)
    if debug:
        print(f"\tappended value {p.val} to list --> {lst}")
    kargs['list'] = lst


def traverse_inorder(p, d=0, fn_visit_handler=append_list, fn_visit_handler__kargs=None, debug=False):
    if p is None:
        return

    traverse_inorder(
        p.left, 
        d=d+1, 
        fn_visit_handler=fn_visit_handler, 
        fn_visit_handler__kargs=fn_visit_handler__kargs, 
        debug=debug)

    if fn_visit_handler__kargs is None:
        fn_visit_handler__kargs = {}
    kargs = {'p':p,'d':d,'debug':debug}
    fn_visit_handler__kargs.update(kargs)
    fn_visit_handler(fn_visit_handler__kargs)

    traverse_inorder(
        p.right, 
        d=d+1, 
        fn_visit_handler=fn_visit_handler, 
        fn_visit_handler__kargs=fn_visit_handler__kargs, 
        debug=debug)


def swapNodes(indexes, queries, debug=False):
    if debug:
        print(f"indexes: {indexes}, queries: {queries}")

    result = []

    root = build_tree(indexes, debug=debug)

    for i, q in enumerate(queries):
        if debug:
            print(f"QUERY {i+1}: SWAP CHILD NODES WITH DEPTH % {q} == 0, CURRENT tree (before query):")
            print_tree(root)
            print()
            print(f"RUNNING query {i+1} (k={q}) ...")
        traverse_preorder(
            root, 
            fn_visit_handler=swap_children, 
            fn_visit_handler__kargs={'query':q}, 
            debug=debug)
        if debug:
            print()
            print(f"AFTER running query {i+1}: SWAP CHILD NODES WITH DEPTH % {q} == 0, RESULTING tree IS:")
            print_tree(root)
            print()

        if debug:
            print(f"BUILDING inorder traversal of RESULTING tree...")
        list_inorder_traversal = []
        traverse_inorder(
            root, 
            fn_visit_handler=append_list, 
            fn_visit_handler__kargs={'list':list_inorder_traversal}, 
            debug=debug)
        if debug:
            print(f"RESULTING inorder traversal: {list_inorder_traversal}\n\n")

        result.append(list_inorder_traversal)

    return result
```

<p><br>

(Debug) Output for test-case 00:

```
indexes: [[2, 3], [-1, -1], [-1, -1]], queries: [1, 1]
        --> tree has 3 child-index pairs --> MAX of 7 nodes possible (including ROOT)
BUILDING TREE...
--> new ROOT (val:1,depth:0)
        parent (val:1,depth:0) --> new LEFT child (val:2,depth:1)
        parent (val:1,depth:0) --> new RIGHT child (val:3,depth:1)
BUILT TREE:
 1 
/ \
2 3

QUERY 1: SWAP CHILD NODES WITH DEPTH % 1 == 0, CURRENT tree (before query):
 1 
/ \
2 3

RUNNING query 1 (k=1) ...
ROOT node (val:1,depth:0) MATCHES query: child-depth 1 % 1 == 0:
        SWAP LEFT: (val:2,depth:1), RIGHT: (val:3,depth:1) 
                --> LEFT: (val:3,depth:1), RIGHT: (val:2,depth:1)

AFTER running query 1: SWAP CHILD NODES WITH DEPTH % 1 == 0, RESULTING tree IS:
 1 
/ \
3 2

BUILDING inorder traversal of RESULTING tree...
        appended value 3 to list --> [3]
        appended value 1 to list --> [3, 1]
        appended value 2 to list --> [3, 1, 2]
RESULTING inorder traversal: [3, 1, 2]


QUERY 2: SWAP CHILD NODES WITH DEPTH % 1 == 0, CURRENT tree (before query):
 1 
/ \
3 2

RUNNING query 2 (k=1) ...
ROOT node (val:1,depth:0) MATCHES query: child-depth 1 % 1 == 0:
        SWAP LEFT: (val:3,depth:1), RIGHT: (val:2,depth:1) 
                --> LEFT: (val:2,depth:1), RIGHT: (val:3,depth:1)

AFTER running query 2: SWAP CHILD NODES WITH DEPTH % 1 == 0, RESULTING tree IS:
 1 
/ \
2 3

BUILDING inorder traversal of RESULTING tree...
        appended value 2 to list --> [2]
        appended value 1 to list --> [2, 1]
        appended value 3 to list --> [2, 1, 3]
RESULTING inorder traversal: [2, 1, 3]


TEST CASE 00.1 RESULTS (from query==1):
        result: 3 1 2
        expect: 3 1 2
                --> PASS

TEST CASE 00.2 RESULTS (from query==1):
        result: 2 1 3
        expect: 2 1 3
                --> PASS
```

<p><br>

(Debug) Output for test-case 99 (custom test case I wrote to match the second example):

```
indexes: [[2, 3], [-1, 4], [-1, 5], [-1, -1], [-1, -1]], queries: [2]
        --> tree has 5 child-index pairs --> MAX of 11 nodes possible (including ROOT)
BUILDING TREE...
--> new ROOT (val:1,depth:0)
        parent (val:1,depth:0) --> new LEFT child (val:2,depth:1)
        parent (val:1,depth:0) --> new RIGHT child (val:3,depth:1)
                parent (val:2,depth:1) --> new RIGHT child (val:4,depth:2)
                parent (val:3,depth:1) --> new RIGHT child (val:5,depth:2)
BUILT TREE:
 _1  
/  \ 
2  3 
 \  \
 4  5

QUERY 1: SWAP CHILD NODES WITH DEPTH % 2 == 0, CURRENT tree (before query):
 _1  
/  \ 
2  3 
 \  \
 4  5

RUNNING query 1 (k=2) ...
node (val:2,depth:1) MATCHES query: child-depth 2 % 2 == 0:
        SWAP LEFT: (None), RIGHT: (val:4,depth:2) 
                --> LEFT: (val:4,depth:2), RIGHT: (None)
node (val:3,depth:1) MATCHES query: child-depth 2 % 2 == 0:
        SWAP LEFT: (None), RIGHT: (val:5,depth:2) 
                --> LEFT: (val:5,depth:2), RIGHT: (None)

AFTER running query 1: SWAP CHILD NODES WITH DEPTH % 2 == 0, RESULTING tree IS:
  1_ 
 /  \
 2  3
/  / 
4  5 

BUILDING inorder traversal of RESULTING tree...
        appended value 4 to list --> [4]
        appended value 2 to list --> [4, 2]
        appended value 1 to list --> [4, 2, 1]
        appended value 5 to list --> [4, 2, 1, 5]
        appended value 3 to list --> [4, 2, 1, 5, 3]
RESULTING inorder traversal: [4, 2, 1, 5, 3]


TEST CASE 99.1 RESULTS (from query==2):
        result: 4 2 1 5 3
        expect: 4 2 1 5 3
                --> PASS
```

<p><br>

(Debug) Output for test-case 03:

```
indexes: [[2, 3], [4, -1], [5, -1], [6, -1], [7, 8], [-1, 9], [-1, -1], [10, 11], [-1, -1], [-1, -1], [-1, -1]], queries: [2, 4]
        --> tree has 11 child-index pairs --> MAX of 23 nodes possible (including ROOT)
BUILDING TREE...
--> new ROOT (val:1,depth:0)
        parent (val:1,depth:0) --> new LEFT child (val:2,depth:1)
        parent (val:1,depth:0) --> new RIGHT child (val:3,depth:1)
                parent (val:2,depth:1) --> new LEFT child (val:4,depth:2)
                parent (val:3,depth:1) --> new LEFT child (val:5,depth:2)
                        parent (val:4,depth:2) --> new LEFT child (val:6,depth:3)
                        parent (val:5,depth:2) --> new LEFT child (val:7,depth:3)
                        parent (val:5,depth:2) --> new RIGHT child (val:8,depth:3)
                                parent (val:6,depth:3) --> new RIGHT child (val:9,depth:4)
                                parent (val:8,depth:3) --> new LEFT child (val:10,depth:4)
                                parent (val:8,depth:3) --> new RIGHT child (val:11,depth:4)
BUILT TREE:
    1_______ 
   /        \
   2   _____3
  /   /      
 _4   5__    
/    /   \   
6    7   8_  
 \      /  \ 
 9     10 11 

QUERY 1: SWAP CHILD NODES WITH DEPTH % 2 == 0, CURRENT tree (before query):
    1_______ 
   /        \
   2   _____3
  /   /      
 _4   5__    
/    /   \   
6    7   8_  
 \      /  \ 
 9     10 11 

RUNNING query 1 (k=2) ...
node (val:2,depth:1) MATCHES query: child-depth 2 % 2 == 0:
        SWAP LEFT: (val:4,depth:2), RIGHT: (None) 
                --> LEFT: (None), RIGHT: (val:4,depth:2)
node (val:6,depth:3) MATCHES query: child-depth 4 % 2 == 0:
        SWAP LEFT: (None), RIGHT: (val:9,depth:4) 
                --> LEFT: (val:9,depth:4), RIGHT: (None)
node (val:3,depth:1) MATCHES query: child-depth 2 % 2 == 0:
        SWAP LEFT: (val:5,depth:2), RIGHT: (None) 
                --> LEFT: (None), RIGHT: (val:5,depth:2)
node (val:8,depth:3) MATCHES query: child-depth 4 % 2 == 0:
        SWAP LEFT: (val:10,depth:4), RIGHT: (val:11,depth:4) 
                --> LEFT: (val:11,depth:4), RIGHT: (val:10,depth:4)

AFTER running query 1: SWAP CHILD NODES WITH DEPTH % 2 == 0, RESULTING tree IS:
 ___1        
/    \       
2__  3_      
   \   \     
   4   5__   
  /   /   \  
  6   7   8_ 
 /       /  \
 9      11 10

BUILDING inorder traversal of RESULTING tree...
        appended value 2 to list --> [2]
        appended value 9 to list --> [2, 9]
        appended value 6 to list --> [2, 9, 6]
        appended value 4 to list --> [2, 9, 6, 4]
        appended value 1 to list --> [2, 9, 6, 4, 1]
        appended value 3 to list --> [2, 9, 6, 4, 1, 3]
        appended value 7 to list --> [2, 9, 6, 4, 1, 3, 7]
        appended value 5 to list --> [2, 9, 6, 4, 1, 3, 7, 5]
        appended value 11 to list --> [2, 9, 6, 4, 1, 3, 7, 5, 11]
        appended value 8 to list --> [2, 9, 6, 4, 1, 3, 7, 5, 11, 8]
        appended value 10 to list --> [2, 9, 6, 4, 1, 3, 7, 5, 11, 8, 10]
RESULTING inorder traversal: [2, 9, 6, 4, 1, 3, 7, 5, 11, 8, 10]


QUERY 2: SWAP CHILD NODES WITH DEPTH % 4 == 0, CURRENT tree (before query):
 ___1        
/    \       
2__  3_      
   \   \     
   4   5__   
  /   /   \  
  6   7   8_ 
 /       /  \
 9      11 10

RUNNING query 2 (k=4) ...
node (val:6,depth:3) MATCHES query: child-depth 4 % 4 == 0:
        SWAP LEFT: (val:9,depth:4), RIGHT: (None) 
                --> LEFT: (None), RIGHT: (val:9,depth:4)
node (val:8,depth:3) MATCHES query: child-depth 4 % 4 == 0:
        SWAP LEFT: (val:11,depth:4), RIGHT: (val:10,depth:4) 
                --> LEFT: (val:10,depth:4), RIGHT: (val:11,depth:4)

AFTER running query 2: SWAP CHILD NODES WITH DEPTH % 4 == 0, RESULTING tree IS:
 ___1        
/    \       
2__  3_      
   \   \     
  _4   5__   
 /    /   \  
 6    7   8_ 
  \      /  \
  9     10 11

BUILDING inorder traversal of RESULTING tree...
        appended value 2 to list --> [2]
        appended value 6 to list --> [2, 6]
        appended value 9 to list --> [2, 6, 9]
        appended value 4 to list --> [2, 6, 9, 4]
        appended value 1 to list --> [2, 6, 9, 4, 1]
        appended value 3 to list --> [2, 6, 9, 4, 1, 3]
        appended value 7 to list --> [2, 6, 9, 4, 1, 3, 7]
        appended value 5 to list --> [2, 6, 9, 4, 1, 3, 7, 5]
        appended value 10 to list --> [2, 6, 9, 4, 1, 3, 7, 5, 10]
        appended value 8 to list --> [2, 6, 9, 4, 1, 3, 7, 5, 10, 8]
        appended value 11 to list --> [2, 6, 9, 4, 1, 3, 7, 5, 10, 8, 11]
RESULTING inorder traversal: [2, 6, 9, 4, 1, 3, 7, 5, 10, 8, 11]


TEST CASE 03.1 RESULTS (from query==2):
        result: 2 9 6 4 1 3 7 5 11 8 10
        expect: 2 9 6 4 1 3 7 5 11 8 10
                --> PASS

TEST CASE 03.2 RESULTS (from query==4):
        result: 2 6 9 4 1 3 7 5 10 8 11
        expect: 2 6 9 4 1 3 7 5 10 8 11
                --> PASS
```

<p><br>

(Debug) Output for test-case 02:

```
indexes: [[2, 3], [4, 5], [6, -1], [-1, 7], [8, 9], [10, 11], [12, 13], [-1, 14], [-1, -1], [15, -1], [16, 17], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1]], queries: [2, 3]
        --> tree has 17 child-index pairs --> MAX of 35 nodes possible (including ROOT)
BUILDING TREE...
--> new ROOT (val:1,depth:0)
        parent (val:1,depth:0) --> new LEFT child (val:2,depth:1)
        parent (val:1,depth:0) --> new RIGHT child (val:3,depth:1)
                parent (val:2,depth:1) --> new LEFT child (val:4,depth:2)
                parent (val:2,depth:1) --> new RIGHT child (val:5,depth:2)
                parent (val:3,depth:1) --> new LEFT child (val:6,depth:2)
                        parent (val:4,depth:2) --> new RIGHT child (val:7,depth:3)
                        parent (val:5,depth:2) --> new LEFT child (val:8,depth:3)
                        parent (val:5,depth:2) --> new RIGHT child (val:9,depth:3)
                        parent (val:6,depth:2) --> new LEFT child (val:10,depth:3)
                        parent (val:6,depth:2) --> new RIGHT child (val:11,depth:3)
                                parent (val:7,depth:3) --> new LEFT child (val:12,depth:4)
                                parent (val:7,depth:3) --> new RIGHT child (val:13,depth:4)
                                parent (val:8,depth:3) --> new RIGHT child (val:14,depth:4)
                                parent (val:10,depth:3) --> new LEFT child (val:15,depth:4)
                                parent (val:11,depth:3) --> new LEFT child (val:16,depth:4)
                                parent (val:11,depth:3) --> new RIGHT child (val:17,depth:4)
BUILT TREE:
       _____1___________ 
      /                 \
 _____2___        ______3
/         \      /       
4__     __5      6___    
   \   /   \    /    \   
   7_  8_  9   10   11_  
  /  \   \    /    /   \ 
 12 13  14   15   16  17 

QUERY 1: SWAP CHILD NODES WITH DEPTH % 2 == 0, CURRENT tree (before query):
       _____1___________ 
      /                 \
 _____2___        ______3
/         \      /       
4__     __5      6___    
   \   /   \    /    \   
   7_  8_  9   10   11_  
  /  \   \    /    /   \ 
 12 13  14   15   16  17 

RUNNING query 1 (k=2) ...
node (val:2,depth:1) MATCHES query: child-depth 2 % 2 == 0:
        SWAP LEFT: (val:4,depth:2), RIGHT: (val:5,depth:2) 
                --> LEFT: (val:5,depth:2), RIGHT: (val:4,depth:2)
node (val:8,depth:3) MATCHES query: child-depth 4 % 2 == 0:
        SWAP LEFT: (None), RIGHT: (val:14,depth:4) 
                --> LEFT: (val:14,depth:4), RIGHT: (None)
node (val:7,depth:3) MATCHES query: child-depth 4 % 2 == 0:
        SWAP LEFT: (val:12,depth:4), RIGHT: (val:13,depth:4) 
                --> LEFT: (val:13,depth:4), RIGHT: (val:12,depth:4)
node (val:3,depth:1) MATCHES query: child-depth 2 % 2 == 0:
        SWAP LEFT: (val:6,depth:2), RIGHT: (None) 
                --> LEFT: (None), RIGHT: (val:6,depth:2)
node (val:10,depth:3) MATCHES query: child-depth 4 % 2 == 0:
        SWAP LEFT: (val:15,depth:4), RIGHT: (None) 
                --> LEFT: (None), RIGHT: (val:15,depth:4)
node (val:11,depth:3) MATCHES query: child-depth 4 % 2 == 0:
        SWAP LEFT: (val:16,depth:4), RIGHT: (val:17,depth:4) 
                --> LEFT: (val:17,depth:4), RIGHT: (val:16,depth:4)

AFTER running query 1: SWAP CHILD NODES WITH DEPTH % 2 == 0, RESULTING tree IS:
      ______1            
     /       \           
    _2       3____       
   /  \           \      
   5  4__       __6___   
  / \    \     /      \  
  8 9    7_   10_    11_ 
 /      /  \     \  /   \
14     13 12    15 17  16

BUILDING inorder traversal of RESULTING tree...
        appended value 14 to list --> [14]
        appended value 8 to list --> [14, 8]
        appended value 5 to list --> [14, 8, 5]
        appended value 9 to list --> [14, 8, 5, 9]
        appended value 2 to list --> [14, 8, 5, 9, 2]
        appended value 4 to list --> [14, 8, 5, 9, 2, 4]
        appended value 13 to list --> [14, 8, 5, 9, 2, 4, 13]
        appended value 7 to list --> [14, 8, 5, 9, 2, 4, 13, 7]
        appended value 12 to list --> [14, 8, 5, 9, 2, 4, 13, 7, 12]
        appended value 1 to list --> [14, 8, 5, 9, 2, 4, 13, 7, 12, 1]
        appended value 3 to list --> [14, 8, 5, 9, 2, 4, 13, 7, 12, 1, 3]
        appended value 10 to list --> [14, 8, 5, 9, 2, 4, 13, 7, 12, 1, 3, 10]
        appended value 15 to list --> [14, 8, 5, 9, 2, 4, 13, 7, 12, 1, 3, 10, 15]
        appended value 6 to list --> [14, 8, 5, 9, 2, 4, 13, 7, 12, 1, 3, 10, 15, 6]
        appended value 17 to list --> [14, 8, 5, 9, 2, 4, 13, 7, 12, 1, 3, 10, 15, 6, 17]
        appended value 11 to list --> [14, 8, 5, 9, 2, 4, 13, 7, 12, 1, 3, 10, 15, 6, 17, 11]
        appended value 16 to list --> [14, 8, 5, 9, 2, 4, 13, 7, 12, 1, 3, 10, 15, 6, 17, 11, 16]
RESULTING inorder traversal: [14, 8, 5, 9, 2, 4, 13, 7, 12, 1, 3, 10, 15, 6, 17, 11, 16]


QUERY 2: SWAP CHILD NODES WITH DEPTH % 3 == 0, CURRENT tree (before query):
      ______1            
     /       \           
    _2       3____       
   /  \           \      
   5  4__       __6___   
  / \    \     /      \  
  8 9    7_   10_    11_ 
 /      /  \     \  /   \
14     13 12    15 17  16

RUNNING query 2 (k=3) ...
node (val:5,depth:2) MATCHES query: child-depth 3 % 3 == 0:
        SWAP LEFT: (val:8,depth:3), RIGHT: (val:9,depth:3) 
                --> LEFT: (val:9,depth:3), RIGHT: (val:8,depth:3)
node (val:4,depth:2) MATCHES query: child-depth 3 % 3 == 0:
        SWAP LEFT: (None), RIGHT: (val:7,depth:3) 
                --> LEFT: (val:7,depth:3), RIGHT: (None)
node (val:6,depth:2) MATCHES query: child-depth 3 % 3 == 0:
        SWAP LEFT: (val:10,depth:3), RIGHT: (val:11,depth:3) 
                --> LEFT: (val:11,depth:3), RIGHT: (val:10,depth:3)

AFTER running query 2: SWAP CHILD NODES WITH DEPTH % 3 == 0, RESULTING tree IS:
      ______1            
     /       \           
  ___2_____  3______     
 /         \        \    
 5__     __4      __6_   
/   \   /        /    \  
9   8   7_      11_  10_ 
   /   /  \    /   \    \
  14  13 12   17  16   15

BUILDING inorder traversal of RESULTING tree...
        appended value 9 to list --> [9]
        appended value 5 to list --> [9, 5]
        appended value 14 to list --> [9, 5, 14]
        appended value 8 to list --> [9, 5, 14, 8]
        appended value 2 to list --> [9, 5, 14, 8, 2]
        appended value 13 to list --> [9, 5, 14, 8, 2, 13]
        appended value 7 to list --> [9, 5, 14, 8, 2, 13, 7]
        appended value 12 to list --> [9, 5, 14, 8, 2, 13, 7, 12]
        appended value 4 to list --> [9, 5, 14, 8, 2, 13, 7, 12, 4]
        appended value 1 to list --> [9, 5, 14, 8, 2, 13, 7, 12, 4, 1]
        appended value 3 to list --> [9, 5, 14, 8, 2, 13, 7, 12, 4, 1, 3]
        appended value 17 to list --> [9, 5, 14, 8, 2, 13, 7, 12, 4, 1, 3, 17]
        appended value 11 to list --> [9, 5, 14, 8, 2, 13, 7, 12, 4, 1, 3, 17, 11]
        appended value 16 to list --> [9, 5, 14, 8, 2, 13, 7, 12, 4, 1, 3, 17, 11, 16]
        appended value 6 to list --> [9, 5, 14, 8, 2, 13, 7, 12, 4, 1, 3, 17, 11, 16, 6]
        appended value 10 to list --> [9, 5, 14, 8, 2, 13, 7, 12, 4, 1, 3, 17, 11, 16, 6, 10]
        appended value 15 to list --> [9, 5, 14, 8, 2, 13, 7, 12, 4, 1, 3, 17, 11, 16, 6, 10, 15]
RESULTING inorder traversal: [9, 5, 14, 8, 2, 13, 7, 12, 4, 1, 3, 17, 11, 16, 6, 10, 15]


TEST CASE 02.1 RESULTS (from query==2):
        result: 14 8 5 9 2 4 13 7 12 1 3 10 15 6 17 11 16
        expect: 14 8 5 9 2 4 13 7 12 1 3 10 15 6 17 11 16
                --> PASS

TEST CASE 02.2 RESULTS (from query==3):
        result: 9 5 14 8 2 13 7 12 4 1 3 17 11 16 6 10 15
        expect: 9 5 14 8 2 13 7 12 4 1 3 17 11 16 6 10 15
                --> PASS
```

## POST-MORTEM:

See commentary above.
