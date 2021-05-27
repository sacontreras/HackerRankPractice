#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'maximumToys' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY prices
#  2. INTEGER k
#

def maximumToys(prices, k):
    debug = True

    if debug:
        print(f"prices: {prices}, k: {k}")

    max_toys = 0

    prices.sort()

    sum_prices = 0
    for p in prices:
        sum_prices += p
        if sum_prices >= k:
            break
        max_toys += 1

    return max_toys


if __name__ == '__main__':
    output_to_file = False
    s_f_index = '17'
    base_path = './InterviewPrepKit/Sorting/MarkAndToys/'
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




    first_multiple_input = input().rstrip().split()
    n = int(first_multiple_input[0])
    k = int(first_multiple_input[1])
    prices = list(map(int, input().rstrip().split()))
    result = maximumToys(prices, k)




    print(f"result: {result}")
    expect = f_expect.readline().strip()
    print(f"expect: {expect}")
    assert(expect == str(result))
    print()

    fd.close()
    f_expect.close()

    if output_to_file:
        f_debug.close()
        sys.stdout = sys.__stdout__

    sys.stdin = sys.__stdin__    # Reset the stdin to its default value
