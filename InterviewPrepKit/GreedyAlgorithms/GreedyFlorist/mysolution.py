#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the getMinimumCost function below.
def getMinimumCost(k, c, debug=False):
    if debug:
        print(f"k: {k}, c: {c}")

    min_cost = 0

    n = len(c)

    if n == k:
        if debug:
            print(f"n == k: {n} == {k} --> final cost list is the original {c}")
        min_cost = sum(c)

    else:
        c_descending = sorted(c, reverse=True)

        cost_lists = [[] for i in range(k)]

        for i, c in enumerate(c_descending):
            i_person = i % k
            cost_list = cost_lists[i_person]
            cost = (len(cost_list)+1) * c
            if debug:
                print(f"for person {i_person}, flower {i} costs {c} --> adjusted flower cost is: ({len(cost_list)}+1)*{c}={cost}")
            cost_list.append(cost)
            if debug:
                print(f"\t--> person {i_person} cost list is now: {cost_list}")
        if debug:
            print(f"\nfinal cost lists: {cost_lists}")

        for cost_list in cost_lists:
            min_cost += sum(cost_list)

    return min_cost

    
if __name__ == '__main__':
    debug = True
    output_to_file = False and debug
    s_f_index = '11'
    base_path = './InterviewPrepKit/GreedyAlgorithms/GreedyFlorist/'
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
    nk = input().split()
    n = int(nk[0])
    k = int(nk[1])
    c = list(map(int, input().rstrip().split()))
    minimumCost = getMinimumCost(k, c, debug=debug)
    # fptr.write(str(minimumCost) + '\n')
    # fptr.close()
    result = minimumCost




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
