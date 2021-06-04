#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'maxMin' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER k
#  2. INTEGER_ARRAY arr
#

def maxMin(k, arr, debug=False):
    if debug:
        print(f"k: {k}, arr: {arr}")

    min_unfairness = 0

    arr_sorted = sorted(arr)
    
    # now we iterate through arr_sorted, taking windows of length k
    if debug:
        print(f"iterating windows of length {k} from arr_sorted: {arr_sorted}")
    min_diff = None
    for i_start in range(len(arr)-k+1):
        v_max = arr_sorted[i_start+k-1]
        v_min = arr_sorted[i_start]
        diff = v_max - v_min
        if min_diff is None or diff < min_diff:
            min_diff = diff
            if debug:
                print(f"\tnew min diff {min_diff} from window {arr_sorted[i_start:i_start+k]} (from inclusive index bounds [{i_start},{i_start+k-1}])")

    min_unfairness = min_diff

    return min_unfairness

    
if __name__ == '__main__':
    debug = True
    output_to_file = False and debug

    s_f_indices = ['00','01','02','15','16']

    for s_f_index in s_f_indices:
        base_path = './InterviewPrepKit/GreedyAlgorithms/MaxMin/'
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
        k = int(input().strip())
        arr = []
        for _ in range(n):
            arr_item = int(input().strip())
            arr.append(arr_item)
        result = maxMin(k, arr, debug=debug)
        # fptr.write(str(result) + '\n')
        # fptr.close()




        # single result
        print(f"result: {result}")
        expect = f_expect.readline().strip()
        print(f"expect: {expect}")
        assert(expect == str(result))
        print()

        # # multiple
        # expect = f_expect.readlines()
        # for i, l in enumerate(expect):
        #     _expect = l.strip()
        #     print(f"expect: {_expect}")
        #     s_result = None
        #     if i < len(result):
        #         s_result = str(result[i])
        #         print(f"result: {s_result}")
        #     else:
        #         print(f"result: <non-existence... result only has {len(result)} elements>")
        #     if _expect != s_result:
        #         print(f"failed on result index: {i}")
        #     assert(_expect == s_result)
        #     print()

        fd.close()
        f_expect.close()

        if output_to_file:
            f_debug.close()
            sys.stdout = sys.__stdout__

        sys.stdin = sys.__stdin__    # Reset the stdin to its default value
