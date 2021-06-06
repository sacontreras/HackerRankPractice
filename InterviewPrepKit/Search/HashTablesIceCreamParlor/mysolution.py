#!/bin/python3

import math
import os
import random
import re
import sys
from typing import Counter

#
# Complete the 'whatFlavors' function below.
#
# The function accepts following parameters:
#  1. INTEGER_ARRAY cost
#  2. INTEGER money
#

def whatFlavors(cost, money, debug=False):
    if debug:
        print(f"cost: {cost}, money: {money}")

    i_f_2 = i_f_1 = 0

    d_costs = {}
    for i, c in enumerate(cost):
        indices = d_costs.get(c,[])
        indices.append(i)
        d_costs[c] = indices
    if debug:
        print(f"d_costs: {d_costs}")

    for c, indices in d_costs.items():
        if len(indices) > 0:
            need = money - c
            i_c = indices.pop(0)
            if debug:
                print(f"\tcost {c} (at index {i_c+1}) requires complement cost {need}")
            if need in d_costs:
                need_indices = d_costs[need]
                if len(need_indices) > 0:
                    i_need = need_indices.pop(0)
                    i_f_1 = i_c+1
                    i_f_2 = i_need+1
                    if debug:
                        print(f"\t\titem found at index {i_need+1}")
                    break
            if debug:
                print(f"\t\tbut no item at need cost {need} is available")
        
    result = f"{i_f_1} {i_f_2}"
    print(result)

    if debug:
        return result

    
if __name__ == '__main__':
    debug = True
    output_to_file = False and debug

    s_f_indices = ['14','15','16']

    for s_f_index in s_f_indices:
        base_path = './InterviewPrepKit/Search/HashTablesIceCreamParlor/'
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
        t = int(input().strip())
        for t_itr in range(t):
            money = int(input().strip())
            n = int(input().strip())
            cost = list(map(int, input().rstrip().split()))
            result.append(whatFlavors(cost, money, debug=debug))




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
