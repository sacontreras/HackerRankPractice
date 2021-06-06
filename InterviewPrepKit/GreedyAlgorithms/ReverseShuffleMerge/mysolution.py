#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'reverseShuffleMerge' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#
def reverseShuffleMerge(s, debug=False):
    if debug:
        s_reversed = s[::-1]
        i_mid = len(s)//2
        s_l = s[:i_mid]
        s_r = s[i_mid:]
        print(f"s: '{s}'\n\ts_reversed: {s_reversed}\n\tsplit is s_l:'{s_l}', s_r:'{s_r}'\n")

    d_s_c_freq = {}
    for c in s:
        d_s_c_freq[c] = d_s_c_freq.get(c,0) + 1
    d_A_c_freq_required = {c:n_c//2 for c, n_c in d_s_c_freq.items()}
    if debug:
        print(f"char freqs required of final version of string A: {d_A_c_freq_required}")
    d_A_shuff_c_freq_required = d_A_c_freq_required.copy()
    
    A_arr = []
		
    s_rev = s[::-1]
    if debug:
        print(f"processing s in reverse: {s_rev}...")
    for c in s_rev:
        n_c_A_req = d_A_c_freq_required[c]

        if n_c_A_req > 0:
            if debug:
                print(f"\tstring A still requires {n_c_A_req} '{c}' chars")

            while True:
                l_A = len(A_arr)

                if l_A > 0:
                    c_last_of_A = A_arr[-1]
                    n_c_A_shuff_req = d_A_shuff_c_freq_required[c_last_of_A]

                    violates_lexicographical_req = c_last_of_A > c
                    shuff_A_needs_chars = n_c_A_shuff_req > 0
                    if debug:
                        if violates_lexicographical_req:
                            print(f"\t\tlexicographical violation: last char of string A: '{c_last_of_A}' > '{c}", end=" ")
                            if shuff_A_needs_chars:
                                print(f"and shuffle(A) needs {n_c_A_shuff_req} chars")
                            else:
                                print(f"but shuffle(A) does not need anymore chars")

                    if violates_lexicographical_req and shuff_A_needs_chars:
                        A_arr.pop()
                        if debug:
                            print(f"\t\t\tremoving last char of string A: '{c_last_of_A}' --> A is now: '{''.join(A_arr)}'")
                        d_A_c_freq_required[c_last_of_A] += 1
                        if debug:
                            print(f"\t\t\tincrementing count of '{c_last_of_A}' required in A to {d_A_c_freq_required[c_last_of_A]}")
                        d_A_shuff_c_freq_required[c_last_of_A] -= 1
                        if debug:
                            print(f"\t\t\tdecrementing count of '{c_last_of_A}' required in shuffle(A) to {d_A_shuff_c_freq_required[c_last_of_A]}")

                    else:
                        break

                else:
                    break
            
            A_arr.append(c)
            if debug:
                print(f"\t\tafter appending '{c}', string A is: '{''.join(A_arr)}'")
            d_A_c_freq_required[c] -= 1

        else:
            d_A_shuff_c_freq_required[c] -= 1

    return ''.join(A_arr)

    
if __name__ == '__main__':
    debug = True
    output_to_file = False and debug

    s_f_indices = ['00','15','16']

    for s_f_index in s_f_indices:
        base_path = './InterviewPrepKit/GreedyAlgorithms/ReverseShuffleMerge/'
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
        result = reverseShuffleMerge(s, debug=debug)
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
