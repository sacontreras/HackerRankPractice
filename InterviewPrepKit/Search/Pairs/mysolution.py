#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'pairs' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER k
#  2. INTEGER_ARRAY arr
#

def pairs(k, arr, debug=False):
    n = len(arr)

    arr_sorted = sorted(arr)    # non-decreasing order
    if debug:
        print(f"k: {k}, arr: {arr}\n\t--> arr_sorted: {arr_sorted}")

    solutions = []
    j, i = 1, 0     # the idea here is to keep j >= i
    while j < n:
        a_j = arr_sorted[j]
        a_i = arr_sorted[i]
        d = a_j - a_i

        if debug:
            print(f"a_[j=={j}] - a[i=={i}] == {a_j} - {a_i} = {d} == k (=={k}) ? {d == k}")

        if d == k:
            sol = (j,i)
            solutions.append(sol)
            j += 1
            if debug:
                print(f"\tFOUND A SOLUTION! Incremented j to {j}")

        elif d > k:
            i += 1
            if debug:
                print(f"\td=={d} > k=={k} --> not a solution, DECREASING difference by incrementing i to {i}")

        elif d < k:
            j += 1
            if debug:
                print(f"\td=={d} < k=={k} --> not a solution, INCREASING difference by incrementing j to {j}")
    if debug:
        print(f"SOLUTION indices: {solutions}")
    
    return len(solutions)

    
if __name__ == '__main__':
    debug = True
    output_to_file = False and debug

    s_f_indices = ['15','16','17']

    for s_f_index in s_f_indices:
        base_path = './InterviewPrepKit/Search/Pairs/'
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
        first_multiple_input = input().rstrip().split()
        n = int(first_multiple_input[0])
        k = int(first_multiple_input[1])
        arr = list(map(int, input().rstrip().split()))
        result = pairs(k, arr, debug=debug)
        # fptr.write(str(result) + '\n')
        # fptr.close()




        # single result
        print(f"result: {result}")
        expect = f_expect.readline().strip()
        print(f"expect: {expect}")
        assert(expect == str(result))
        print()

        # multiple
        # expect = f_expect.readlines()
        # for i, l in enumerate(expect):
        #     _expect = l.strip()
        #     print(f"TEST CASE {s_f_index}.{i+1} RESULTS (from query=={queries[i]}):")
        #     s_result = None
        #     if i < len(result):
        #         s_result = ' '.join([str(x) for x in result[i]])
        #         print(f"\tresult: {s_result}")
        #     else:
        #         print(f"\tresult: <non-existence... result only has {len(result)} elements>")
        #     print(f"\texpect: {_expect}")

        #     if s_result != _expect:
        #         print(f"\t\t--> FAILED on result index: {i}")
        #     if not debug:
        #         assert(_expect == s_result)
        #     if _expect == s_result:
        #         print(f"\t\t--> PASS")
        #     print()

        # print("\n\n")

        fd.close()
        f_expect.close()

        if output_to_file:
            f_debug.close()
            sys.stdout = sys.__stdout__

        sys.stdin = sys.__stdin__    # Reset the stdin to its default value
