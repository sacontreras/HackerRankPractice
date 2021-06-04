#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'luckBalance' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER k
#  2. 2D_INTEGER_ARRAY contests
#

def luckBalance(k, contests, debug=False):
    if debug:
        print(f"k: {k}, {len(contests)} contests: {contests}\n")

    max_luck_balance = 0

    unimportant_losses = list(filter(lambda c: c[1]==0, contests))
    if debug:
        print(f"{len(unimportant_losses)} unimportant_losses: {unimportant_losses}\n")

    important_losses = sorted(filter(lambda c: c[1]==1, contests), key=lambda c: c[0])
    if debug:
        print(f"{len(important_losses)} important_losses: {important_losses}")
    k = min(k, len(important_losses))
    max_luck_important_losses = important_losses[len(important_losses)-k:]
    if debug:
        print(f"\ttop {k} important losses by luck: {max_luck_important_losses}")
    min_luck_important_losses = important_losses[:len(important_losses)-k]
    if debug:
        print(f"\tbottom {len(important_losses)-k} important losses by luck: {min_luck_important_losses}")

    s_max_luck_important_losses = sum([c[0] for c in max_luck_important_losses])
    s_unimportant_losses = sum([c[0] for c in unimportant_losses])
    s_min_luck_important_losses = sum([c[0] for c in min_luck_important_losses])
    max_luck_balance = s_max_luck_important_losses + s_unimportant_losses - s_min_luck_important_losses
    if debug:
        print(f"max luck: max_luck_important_losses + unimportant_losses - min_luck_important_losses = {s_max_luck_important_losses} + {s_unimportant_losses} - {s_min_luck_important_losses} = {max_luck_balance}")

    return max_luck_balance

    
if __name__ == '__main__':
    debug = True
    output_to_file = False and debug
    s_f_index = '08'
    base_path = './InterviewPrepKit/GreedyAlgorithms/LuckBalance/'
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
    contests = []
    for _ in range(n):
        contests.append(list(map(int, input().rstrip().split())))
    result = luckBalance(k, contests, debug=debug)
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
