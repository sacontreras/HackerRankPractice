#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'countInversions' function below.
#
# The function is expected to return a LONG_INTEGER.
# The function accepts INTEGER_ARRAY arr as parameter.
#

import mergesort
def countInversions(arr, debug=False):
    if debug:
        print(f"arr: {arr}")
    n_inversions = mergesort.mergesort(arr)[0]
    if debug:
        print(f"arr (after mergesort): {arr}")
        print(f"mergesort swapped {n_inversions} (number of inversions)\n")

    return n_inversions


if __name__ == '__main__':
    debug = False
    output_to_file = False and debug
    s_f_index = '15'
    base_path = './InterviewPrepKit/Sorting/MergesortCountingInversions/'
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



    result = []
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')
    t = int(input().strip())
    for t_itr in range(t):
        n = int(input().strip())
        arr = list(map(int, input().rstrip().split()))
        # result = countInversions(arr)
        result.append(countInversions(arr, debug))
    #     fptr.write(str(result) + '\n')
    # fptr.close()




    expect = f_expect.readlines()
    for i, l in enumerate(expect):
        _expect = l.strip()
        print(f"expect: {_expect}")
        s_result = None
        if i < len(result):
            s_result = str(result[i])
            print(f"result: {s_result}")
        else:
            print(f"result: <non-existence... result only has {len(result)} elements>")
        if _expect != s_result:
            print(f"failed on result index: {i}")
        assert(_expect == s_result)
        print()

    fd.close()
    f_expect.close()

    if output_to_file:
        f_debug.close()
        sys.stdout = sys.__stdout__

    sys.stdin = sys.__stdin__    # Reset the stdin to its default value
