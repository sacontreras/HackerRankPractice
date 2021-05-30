#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'isValid' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#

def isValid(s, debug=False):
    if debug:
        print(f"s: {s}")

    d_c_freq = {}
    for c in s:
        d_c_freq[c] = d_c_freq.get(c,0) + 1
    d_freq_c = {}
    for c,n_c in d_c_freq.items():
        set_c = d_freq_c.get(n_c,set())
        set_c.add(c)
        d_freq_c[n_c] = set_c

    if debug:
        print(f"d_c_freq: {d_c_freq} (len={len(d_c_freq)})")
        print(f"d_freq_c: {d_freq_c} (len={len(d_freq_c)})")

    distinct_counts = len(d_freq_c)
    if distinct_counts <= 1:
        return "YES"

    elif distinct_counts > 2:
        return "NO"
    
    else:   # distinct_counts == 2
        # get set with minimum cardinality (and its key)
        set_min = None
        set_min_key = None
        all_keys = set(d_freq_c.keys())
        for n_c, set_c in d_freq_c.items():
            if set_min is None:
                set_min = set_c
                set_min_key = n_c
            else:
                if len(set_c) < len(set_min):
                    set_min = set_c
                    set_min_key = n_c

        if len(set_min) == 1:
            all_keys.remove(set_min_key)
            set_max_key = list(all_keys)[0]
            if debug:
                print(f"set_max_key = all_keys - set_min_key: {set_max_key}")
            n_set_min_key_post_redux = set_min_key-1
            if n_set_min_key_post_redux<=0 or n_set_min_key_post_redux==set_max_key:
                return "YES"
            else:
                return "NO"
        else:
            return "NO"
    

if __name__ == '__main__':
    debug = True
    output_to_file = False and debug
    s_f_index = '04'
    base_path = './InterviewPrepKit/StringManipulation/SherlockValidString/'
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
    s = input()
    result = isValid(s, debug)
    # fptr.write(result + '\n')
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
