#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'commonChild' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. STRING s1
#  2. STRING s2
#

def lcs(s1, s2, debug=False):
    """
    Credit/reference:
        https://www.tutorialcup.com/interview/dynamic-programming/longest-common-subsequence.htm
    """

    n_s1 = len(s1)
    n_s2 = len(s2)
  
    # size of the DP table is len(s1)+1 rows x len(s2)+1 columnns
    dp_table__len_common_subseqs = [[None]*(n_s2+1) for r in range(n_s1+1)]
  
    for r in range(n_s1+1):
        for c in range(n_s2+1):
            if r == 0 or c == 0 :
                dp_table__len_common_subseqs[r][c] = 0

            elif s1[r-1] == s2[c-1]:
                dp_table__len_common_subseqs[r][c] = dp_table__len_common_subseqs[r-1][c-1]+1

            else:
                dp_table__len_common_subseqs[r][c] = max(dp_table__len_common_subseqs[r-1][c], dp_table__len_common_subseqs[r][c-1])

    # construct lcs using dp_table__len_common_subseqs
    #   as usual, start from bottom-right cell in dp_table__len_common_subseqs and navigate to the (0,0) cell
    #       this will build the lcs in reverse, therefore we must reverse it upon completion
    r = n_s1
    c = n_s2
    _lcs = ""
    while (r>0 and c>0):
        # if char in s1 associated with row index r and char in s2 associated with col index c are the same
        #   then this char is in the lcs (but recall it is built in reverse)
        if s1[r-1]==s2[c-1]:
            _lcs += s1[r-1]
            r -= 1
            c -= 1
        
        # if current characters do not match
            # then move in the direction, to the cell containing the larger length
            # between cells to the left of, as well as above, the current cell
        elif dp_table__len_common_subseqs[r-1][c] > dp_table__len_common_subseqs[r][c-1]:
            r -= 1

        else:
            c -= 1
      
    # recall that the lcs string was built in reverse so we need to reverse it for the final representation
    _lcs = _lcs[::-1]
    if debug:
        print(f"\tlcs: {_lcs}")
  
    # dp_table__len_common_subseqs contains the lengths of common subsequences of s1[0..n_s2-1] & s2[0..n_s1-1]
    #   but the solution, the max length common subsequence is held in cell dp_table__len_common_subseqs[n_s1][n_s2]
    return dp_table__len_common_subseqs[n_s1][n_s2]

def commonChild(s1, s2, debug=False):
    if debug:
        print(f"s1: {s1}\ns2: {s2}")
    return lcs(s1, s2,debug=debug)
    

if __name__ == '__main__':
    debug = True
    output_to_file = False and debug
    s_f_index = '10'
    base_path = './InterviewPrepKit/StringManipulation/CommonChild/'
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
    s1 = input()
    s2 = input()
    result = commonChild(s1, s2, debug=debug)
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
