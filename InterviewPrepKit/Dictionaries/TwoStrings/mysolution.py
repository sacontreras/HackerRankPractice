#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'twoStrings' function below.
#
# The function is expected to return a STRING.
# The function accepts following parameters:
#  1. STRING s1
#  2. STRING s2
#

def twoStrings(s1, s2):
    d_s1_subs = {}
    d_s2_subs = {}

    # to have any substring in common, both strings must have at least one char in common
    for c in s1:
        d_s1_subs[c] = d_s1_subs.get(c,0) + 1
    for c in s2:
        try:
            n_sub_s2_in_s1 = d_s1_subs[c]
            if n_sub_s2_in_s1 > 0:
                return "YES"
        except:
            pass 
        d_s2_subs[c] = d_s1_subs.get(c,0) + 1

    return "NO"


if __name__ == '__main__':
    s_f_index = '03'
    base_path = './InterviewPrepKit/Dictionaries/TwoStrings/'
    fname_input = base_path + f'input{s_f_index}.txt'
    fname_expect = base_path + f'output{s_f_index}.txt'
    print(f"testing against input file {fname_input}")

    fd = open(fname_input)
    sys.stdin = fd

    f_expect = open(fname_expect)

    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input().strip())

    for q_itr in range(q):
        s1 = input()

        s2 = input()

        result = twoStrings(s1, s2)

        # fptr.write(result + '\n')

        print(f"result: {result}")
        expect = f_expect.readline().strip()
        print(f"expect: {expect}")
        assert(expect == result)
        print()

    # fptr.close()

    fd.close()
    f_expect.close()

    sys.stdin = sys.__stdin__    # Reset the stdin to its default value
