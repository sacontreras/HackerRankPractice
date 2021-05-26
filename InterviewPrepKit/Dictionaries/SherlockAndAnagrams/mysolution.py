#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'sherlockAndAnagrams' function below.
#
# The function is expected to return an INTEGER.
# The function accepts STRING s as parameter.
#


# def perms(lst):
#     """
#     credit: https://stackoverflow.com/a/18230722/11761918
#     """

#     stack = list(lst)
#     results = [stack.pop()]
#     while len(stack) != 0:
#         c = stack.pop()
#         new_results = []
#         for w in results:
#             for i in range(len(w)+1):
#                 new_results.append(w[:i] + c + w[i:])
#         results = new_results
#     return results


def sherlockAndAnagrams(s):
    debug = False

    n_anagram_basis = 0

    l_s = len(s)

    if debug:
        print(f"string '{s}'")

    d_s_sub_anagrams_basis = {}
    for i_start in range(l_s):
        for i_end in range(i_start, l_s):
            sub_s = s[i_start:i_end+1]
            sub_s_arr_sorted = sorted(list(sub_s))
            sub_s_sorted = "".join(sub_s_arr_sorted)
            indices = list(range(i_start,i_end+1))
            if sub_s_sorted in d_s_sub_anagrams_basis:
                n_anagram_basis += len(d_s_sub_anagrams_basis[sub_s_sorted])
                lst = d_s_sub_anagrams_basis[sub_s_sorted]
                lst.append(indices)
                d_s_sub_anagrams_basis[sub_s_sorted] = lst
            else:
                d_s_sub_anagrams_basis[sub_s_sorted] = [indices]

    if debug:
        print(d_s_sub_anagrams_basis)
        
    return n_anagram_basis


if __name__ == '__main__':
    s_f_index = '01'
    base_path = './InterviewPrepKit/Dictionaries/SherlockAndAnagrams/'
    fname_input = base_path + f'input{s_f_index}.txt'
    fname_expect = base_path + f'output{s_f_index}.txt'

    print(f"\ntesting against input file {fname_input}")

    fd = open(fname_input)
    sys.stdin = fd

    f_expect = open(fname_expect)

    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input().strip())

    for q_itr in range(q):
        s = input()

        result = sherlockAndAnagrams(s)

        # fptr.write(str(result) + '\n')

        print(f"result: {result}")
        expect = f_expect.readline().strip()
        print(f"expect: {expect}")
        assert(expect == str(result))
        print()

    # fptr.close()

    fd.close()
    f_expect.close()

    sys.stdin = sys.__stdin__    # Reset the stdin to its default value
