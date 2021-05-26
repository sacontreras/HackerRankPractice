#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the countTriplets function below.
def countTriplets_1(arr, r):
    """
    This implementation is not only wrong some of the time, but when it is right it is O(n^3) complexity!  AWFUL!
    """

    debug = True

    if debug:
        print(f"arr: {arr}, r: {r}")

    n_geom_series = 0

    lst_series = []

    l_arr = len(arr)

    for ub in range(l_arr-1,-1,-1):

        for lb in range(ub,-1,-1):
            i_start = None
            series = arr[lb:ub+1]

            if len(series) > 1:
                if debug:
                    print(f"inspecting series: {series}")

                for i in range(ub,lb,-1):
                    a_i = arr[i]
                    a_i_minus_1 = arr[i-1]
                    is_ratio = a_i//a_i_minus_1 == r
                    if debug:
                        print(f"inspect elements at i,i-1: {i},{i-1} --> ({a_i}/{a_i_minus_1})=={r} ? {is_ratio}")
                    if not is_ratio:
                        break
                    i_start = i
                
                if i_start is not None and i_start-1 == lb:
                    geom_series = series
                    lst_series.append(geom_series)
                    if debug:
                        print(f"{geom_series} is geometric with ratio {r}")
                    n_geom_series += 1
                else:
                    if debug:
                        print(f"{series} is not geometric")

                if debug:
                    print()

    return n_geom_series

def countTriplets(arr, r):
    debug = True

    if debug:
        print(f"arr: {arr}, r: {r}")

    n_geom_series = 0

    # store the frequency of all the elements
    d_right = {}
    for a_j in arr:
        d_right[a_j] = d_right.get(a_j,0) + 1

    if debug:
        print(f"right map: {d_right}")

    d_left = {}

    # traverse the array elements from left side
    for a_j in arr:
        a_i = a_j / r
        a_k = a_j * r
        
        # first decrement it's count from d_right by 1
        d_right[a_j] -= 1

        # check the count of a_k in d_right
        n_a_k = d_right.get(a_k,0)

        # check the count of a_i in d_left
        n_a_i = d_left.get(a_i,0)

        # increment n_geom_series by product of the above
        n_geom_series += n_a_k * n_a_i

        # increment could of a_j in d_left by 1
        d_left[a_j] = d_left.get(a_j,0) + 1

        """
        intuition:
            d_left holds elements with indices < j
            d_right holds elements with indices > j
        """

    if debug:
        print(f"left map: {d_left}")
        print(f"right map: {d_right}")

    return n_geom_series


if __name__ == '__main__':
    s_f_index = '12'
    base_path = './InterviewPrepKit/Dictionaries/CountTriplets/'
    fname_input = base_path + f'input{s_f_index}.txt'
    fname_expect = base_path + f'output{s_f_index}.txt'

    print(f"\ntesting against input file {fname_input}...")

    fd = open(fname_input)
    sys.stdin = fd

    f_expect = open(fname_expect)

    
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    nr = input().rstrip().split()

    n = int(nr[0])

    r = int(nr[1])

    arr = list(map(int, input().rstrip().split()))

    ans = countTriplets(arr, r)

    # fptr.write(str(ans) + '\n')

    # fptr.close()


    print(f"result: {ans}")
    expect = f_expect.readline().strip()
    print(f"expect: {expect}")
    assert(expect == str(ans))
    print()
    

    fd.close()
    f_expect.close()

    sys.stdin = sys.__stdin__    # Reset the stdin to its default value
