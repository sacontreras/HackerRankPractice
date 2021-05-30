#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'makeAnagram' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. STRING a
#  2. STRING b
#

def makeAnagram(a, b, debug=False):
    if debug:
        print(f"a: {a}, b: {b}")
    
    n_del_req = 0

    d_a_freq = {}
    for c in a:
        d_a_freq[c] = d_a_freq.get(c,0) + 1
    d_b_freq = {}
    for c in b:
        d_b_freq[c] = d_b_freq.get(c,0) + 1
    if debug:
        print(f"d_a_freq: {d_a_freq}")
        print(f"d_b_freq: {d_b_freq}")

    chars_in_common = set(d_a_freq.keys()) & set(d_b_freq.keys())
    if debug:
        print(f"chars_in_common: {chars_in_common}")

    for c in (set(d_a_freq.keys()) - chars_in_common):
        n_c = d_a_freq[c]
        if debug:
            print(f"{n_c} instances of '{c}' must be deleted from a")
        n_del_req += n_c
    for c in (set(d_b_freq.keys()) - chars_in_common):
        n_c = d_b_freq[c]
        if debug:
            print(f"{n_c} instances of '{c}' must be deleted from b")
        n_del_req += n_c
    for c in chars_in_common:
        n_c_a = d_a_freq[c]
        n_c_b = d_b_freq[c]
        n_c_diff = max(n_c_a,n_c_b) - min(n_c_a,n_c_b)
        if debug and n_c_diff > 0:
            print(f"{n_c} disjoint instances of '{c}' must be deleted")
        n_del_req += n_c_diff
    
    return n_del_req
    

if __name__ == '__main__':
    debug = True
    output_to_file = False and debug
    s_f_index = '15'
    base_path = './InterviewPrepKit/StringManipulation/MakingAnagrams/'
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
    a = input()
    b = input()
    result = makeAnagram(a, b, debug)
    # fptr.write(str(res) + '\n')
    # fptr.close()




    # single result
    print(f"result: {result}")
    expect = f_expect.readline().strip()
    print(f"expect: {expect}")
    assert(expect == str(result))
    print()

    # multiple
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
