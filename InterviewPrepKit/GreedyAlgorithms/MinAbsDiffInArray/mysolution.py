#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'minimumAbsoluteDifference' function below.
#
# The function is expected to return an INTEGER.
# The function accepts INTEGER_ARRAY arr as parameter.
#

def minimumAbsoluteDifference(arr, debug=False):
    if debug:
        print(f"arr: {arr}")

    min_diff = 0

    n = len(arr)

    if n > 1:
        # sort the array in non-decreasing order
        arr_sorted = sorted(arr)    # O(n log n) worst case
        if debug:
            print(f"arr_sorted: {arr_sorted}")
            print(f"diffs arr_sorted: {[abs(arr_sorted[i]-arr_sorted[i-1]) for i in range(1,n)]}")
        i = 1
        diff = abs(arr_sorted[i] - arr_sorted[i-1])
        min_diff = diff
        if debug:
            print(f"new min diff: abs(arr_sorted[{i}]-arr_sorted[{i-1}])={min_diff}")
        for i in range(2,n):
            diff = abs(arr_sorted[i] - arr_sorted[i-1])
            if diff < min_diff:
                min_diff = diff
                if debug:
                    print(f"new min diff: abs(arr_sorted[{i}]-arr_sorted[{i-1}])={min_diff}")

    return min_diff

    
if __name__ == '__main__':
    debug = True
    output_to_file = False and debug
    s_f_index = '10'
    base_path = './InterviewPrepKit/GreedyAlgorithms/MinAbsDiffInArray/'
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
    arr = list(map(int, input().rstrip().split()))
    result = minimumAbsoluteDifference(arr, debug=debug)
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
