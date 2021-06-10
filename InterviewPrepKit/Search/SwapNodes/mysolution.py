#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'swapNodes' function below.
#
# The function is expected to return a 2D_INTEGER_ARRAY.
# The function accepts following parameters:
#  1. 2D_INTEGER_ARRAY indexes
#  2. INTEGER_ARRAY queries
#

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

    
if __name__ == '__main__':
    debug = True
    output_to_file = False and debug

    s_f_indices = ['00','99','03', '02']

    for s_f_index in s_f_indices:
        base_path = './InterviewPrepKit/Search/SwapNodes/'
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
        n = int(input().strip())
        indexes = []
        for _ in range(n):
            indexes.append(list(map(int, input().rstrip().split())))
        queries_count = int(input().strip())
        queries = []
        for _ in range(queries_count):
            queries_item = int(input().strip())
            queries.append(queries_item)
        result = swapNodes(indexes, queries, debug=debug)
        # fptr.write('\n'.join([' '.join(map(str, x)) for x in result]))
        # fptr.write('\n')
        # fptr.close()




        # # single result
        # print(f"result: {result}")
        # expect = f_expect.readline().strip()
        # print(f"expect: {expect}")
        # assert(expect == str(result))
        # print()

        # multiple
        expect = f_expect.readlines()
        for i, l in enumerate(expect):
            _expect = l.strip()
            print(f"TEST CASE {s_f_index}.{i+1} RESULTS (from query=={queries[i]}):")
            s_result = None
            if i < len(result):
                s_result = ' '.join([str(x) for x in result[i]])
                print(f"\tresult: {s_result}")
            else:
                print(f"\tresult: <non-existence... result only has {len(result)} elements>")
            print(f"\texpect: {_expect}")

            if s_result != _expect:
                print(f"\t\t--> FAILED on result index: {i}")
            if not debug:
                assert(_expect == s_result)
            if _expect == s_result:
                print(f"\t\t--> PASS")
            print()

        print("\n\n")

        fd.close()
        f_expect.close()

        if output_to_file:
            f_debug.close()
            sys.stdout = sys.__stdout__

        sys.stdin = sys.__stdin__    # Reset the stdin to its default value
