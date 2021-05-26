#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the minimumSwaps function below.
def minimumSwaps(arr):
    d_arr = {v:i for i,v in enumerate(arr)} # for O(1) lookup

    n_swaps = 0
    
    for i0 in range(len(arr)):
        e = arr[i0]
        e0 = i0+1
        if e != e0:    # then we need to swap with what it should be
            # locate index of e0 in arr
            # i = arr.index(e0)   # but this takes a looong time, so use O(1) lookup of dict
            i = d_arr[e0]

            # swap in array and update the dict
            arr[i0] = e0
            d_arr[e0] = i0
            arr[i] = e
            d_arr[e] = i

            n_swaps += 1

    return n_swaps


if __name__ == '__main__':
    fd = open('./InterviewPrepKit/Arrays/MinimumSwaps2/input09.txt')
    sys.stdin = fd

    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input())

    arr = list(map(int, input().rstrip().split()))

    res = minimumSwaps(arr)

    # fptr.write(str(res) + '\n')

    # fptr.close()

    print(res)

    sys.stdin = sys.__stdin__    # Reset the stdin to its default value
