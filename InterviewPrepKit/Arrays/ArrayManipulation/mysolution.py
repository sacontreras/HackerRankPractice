#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'arrayManipulation' function below.
#
# The function is expected to return a LONG_INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. 2D_INTEGER_ARRAY queries
#

def arrayManipulation(n, queries):
    arr_debug = None
    arr = [0 for _ in range(n+1)]
    
    debug = n <= 10

    if debug:
        arr_debug = [0 for _ in range(n)]
    else:
        print(f"debug output suppressed for large n")

    if debug:
        print("queries:")
    max_v_debug = 0

    for lb_1, ub_1, k in queries:   # indices are for 1-based array

        # brute force investigation
        if debug:
            for i in range(lb_1-1, ub_1):   # since array is 1-based
                arr_debug[i] += k
                if arr_debug[i] > max_v_debug:
                    max_v_debug = arr_debug[i]
            print(f"\t{lb_1}\t{ub_1}\t{k}\t--> arr_debug:\t{arr_debug}")

        # upon inspection of the above, it looks as if the pattern
        #   shows that the only entries that contribute to the max calc
        #   involve only indices lb_1-1 and ub_1 (inclusive)
        #   if we track the cumulative sum and update max_v based on that
        #       in that case we substract the val at ub_1 (inclusive)
        #   this will result in linear complexity
        arr[lb_1-1] += k
        arr[ub_1] -= k
        if debug:
            print(f"\t{lb_1}\t{ub_1}\t{k}\t--> arr:\t{arr}")
        if debug:
            print()

    if debug:
        print(f"max_v_debug is {max_v_debug}")

    max_v = arr[0]
    s = 0
    for v in arr:
        s += v
        if s > max_v:
            max_v = s

    if debug:
        print(f"max_v == max_v_debug --> {max_v} == {max_v_debug} ? {max_v == max_v_debug}")
        assert(max_v == max_v_debug)
    
    return max_v


if __name__ == '__main__':
    fd = open('./InterviewPrepKit/Arrays/ArrayManipulation/input15.txt')
    sys.stdin = fd

    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    print(f"n is {n}")

    m = int(first_multiple_input[1])

    queries = []

    for _ in range(m):
        queries.append(list(map(int, input().rstrip().split())))

    result = arrayManipulation(n, queries)

    # fptr.write(str(result) + '\n')

    # fptr.close()

    print(result)

    sys.stdin = sys.__stdin__    # Reset the stdin to its default value
