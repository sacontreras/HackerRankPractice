#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'alternatingCharacters' function below.
#
# The function is expected to return an INTEGER.
# The function accepts STRING s as parameter.
#

def alternatingCharacters(s, debug=False):
    if debug:
        print(f"s: {s}")

    n_del_req = 0

    d_s_char_incidence = {}
    d_s_char_remove = {}
    for i,c in enumerate(s):
        lst_incidence = d_s_char_incidence.get(c,[])

        if len(lst_incidence) > 0:
            last_index = lst_incidence[-1]
            if last_index == i-1:
                lst_remove_at = d_s_char_remove.get(c,[])
                lst_remove_at.append(last_index)
                d_s_char_remove[c] = lst_remove_at

        lst_incidence.append(i)
        d_s_char_incidence[c] = lst_incidence

    if debug:
        print(f"d_s_char_incidence: {d_s_char_incidence}")
        print(f"d_s_char_remove: {d_s_char_remove}\n")

    for c, lst_remove_at in d_s_char_remove.items():
        n_del_req += len(lst_remove_at)

    return n_del_req
    

if __name__ == '__main__':
    debug = True
    output_to_file = False and debug
    s_f_index = '14'
    base_path = './InterviewPrepKit/StringManipulation/AlternatingCharacters/'
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
    result = []
    q = int(input().strip())
    for q_itr in range(q):
        s = input()
        # result = alternatingCharacters(s)
        result.append(alternatingCharacters(s,debug))
        # fptr.write(str(result) + '\n')
    # fptr.close()




    # single result
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
