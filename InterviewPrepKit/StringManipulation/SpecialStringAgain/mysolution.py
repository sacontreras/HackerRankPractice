#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the substrCount function below.
def substrCount_v1(n, s, debug=False):
    if debug:
        print(f"n: {n}, s: {s}")

    n_special_strings = 0

    set_chars = set(list(s))
    if len(set_chars) == 1:
        n_special_strings = n*(n+1)//2
        if debug:
            print(f"short circuit to n(n+1)/2 since there is only one unique char")

    else:
        if debug:
            n_subs = 0
            print("ALL substrings:", end=" ")
            for i_start in range(n):
                for l in range(n-i_start,0,-1):
                    subs = s[i_start:i_start+l]
                    print(subs, end=" ")
                    n_subs += 1
            print(f"\n\t{n_subs} total")

            n_subs = 0
            print("odd-length substrings:", end=" ")
            for i_start in range(n):
                for l in range(n-i_start,0,-1):
                    subs = s[i_start:i_start+l]
                    if len(subs)%2 == 1:
                        print(subs, end=" ")
                        n_subs += 1
            print(f"\n\t{n_subs} total\n")

        mid = n // 2

        if debug:
            n_subs = 0

        for i_mid in range(n):
            max_r = mid
            if i_mid < mid:
                max_r = i_mid
            elif i_mid > mid:
                max_r = (n-1) - i_mid

            for r in range(0,max_r+1):
                i_start = i_mid-r
                i_end = i_mid+r
                subs = s[i_mid] if r == 0 else s[i_start:i_end+1]
                if debug:
                    print(f"odd-length substring '{subs}' at indices {list(range(i_start,i_end+1))}")

                if len(subs) > 1:
                    l_sub = s[i_start:i_mid]
                    l_sub_first_dup = l_sub[0]*len(l_sub)
                    is_special = l_sub_first_dup==l_sub
                    r_sub = s[i_mid+1:i_end+1]
                    r_sub_first_dup = r_sub[0]*len(r_sub)
                    is_special = is_special and r_sub_first_dup==l_sub_first_dup
                    if debug:
                        print(f"\thas: mid({i_mid})='{s[i_mid]}', radius={r} --> left-half='{l_sub}' ({list(range(i_start,i_mid))}), right-half='{r_sub}' ({list(range(i_mid+1,i_end+1))}) --> {'SPECIAL' if is_special else 'NOT special'}")
                    n_special_strings += 1 if is_special else 0
                else:
                    if debug:
                        print(f"\tSPECIAL since length is 1")
                    n_special_strings += 1
                
                if debug:
                    n_subs += 1

        if debug:
            print(f"{n_subs} odd-length substrings total")
        
    return n_special_strings


def vectorize_char_counts(n, s):
    char_count_tuples = []
    i = 0

    while (i < n):
        c = s[i]
        n_c = 1

        while (i+1 < n and s[i+1]==c):   # adjacent chars, left-to-right, are the same
            i += 1
            n_c += 1

        char_count_tuples.append((c,n_c))
        i += 1

    return char_count_tuples

def vectorize_case2_special_substrings(n, s):
    case2_special_substrings = []

    for i_mid in range(1, n):
        char_radius = 1

        while True:
            i_start = i_mid - char_radius
            i_end = i_mid + char_radius

            if 0 <= i_start < i_end < n:
                is_mid_char_different = s[i_mid] != s[i_mid-1]  # unique middle char differentiates from case 1 (same-character substrings)
                is_same_surrounding_char = s[i_start] == s[i_end]
                is_contiguous_same_char_left = s[i_mid-1] == s[i_start]

                if is_mid_char_different and is_same_surrounding_char and is_contiguous_same_char_left:
                    case2_special_substrings.append(s[i_start:i_end+1])
                    char_radius += 1

                else:
                    break

            else:
                break

    return case2_special_substrings

def substrCount(n, s, debug=False):
    if debug:
        print(f"n: {n}, s: {s}\n")

    n_special_strings = 0

    # case 1: all same-character substrings: given any string of length n, it will have n(n+1)/2 substrings
    #   and we count all of them since the base string is based on a single char
    n_case1_subs = 0
    char_count_tuples = vectorize_char_counts(n, s)
    if debug:
        i = 0
        print(f"counting same-character (case-1) substrings...")
    for c, n_c in char_count_tuples:
        n_substrings = n_c*(n_c+1)//2
        if debug:
            print(f"\tsubstring '{c*n_c}' ({[_i for _i in range(i,i+n_c)]}) has {n_substrings} sub-substrings")
            i += n_c
        n_case1_subs += n_substrings
    if debug:
        print(f"\t\t{n_case1_subs} total same-character special substrings")

    # case 2
    n_case2_subs = 0
    case2_special_substrings = vectorize_case2_special_substrings(n, s)
    if debug:
        print(f"\ncounting case-2 substrings...")
        for c2subs in case2_special_substrings:
            print(f"\t{c2subs}")
    n_case2_subs = len(case2_special_substrings)
    if debug:
        print(f"\t\t{n_case2_subs} total case-2 special substrings\n")

    n_special_strings = n_case1_subs + n_case2_subs

    return n_special_strings
    

if __name__ == '__main__':
    debug = False
    output_to_file = False and debug
    s_f_index = '02'
    base_path = './InterviewPrepKit/StringManipulation/SpecialStringAgain/'
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
    n = int(input())
    s = input()
    result = substrCount(n, s, debug)
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
