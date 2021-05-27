import math
import os
import random
import re
import sys

#
# Complete the 'countSwaps' function below.
#
# The function accepts INTEGER_ARRAY a as parameter.
#

def countSwaps(a):
    debug = False
    
    n_swaps = 0
    elt_first = None
    elt_last = None

    for i in range(len(a)):
        for j in range(len(a)-1):
            # Swap adjacent elements if they are in decreasing order
            a_j = a[j]
            a_j_plus_1 = a[j+1]
            if a_j > a_j_plus_1:
                a[j+1] = a_j
                a[j] = a_j_plus_1
                n_swaps += 1

    elt_first = a[0]
    elt_last = a[-1]
    
    print(f"Array is sorted in {n_swaps} swaps.")
    print(f"First Element: {elt_first}")
    print(f"Last Element: {elt_last}")


if __name__ == '__main__':
    output_to_file = False
    s_f_index = '03'
    base_path = './InterviewPrepKit/Sorting/BubbleSort/'
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




    n = int(input().strip())
    a = list(map(int, input().rstrip().split()))
    countSwaps(a)




    expect = f_expect.readlines()
    for i, l in enumerate(expect):
        _expect = l.strip()
        print(f"expect: {_expect}")

    fd.close()
    f_expect.close()

    if output_to_file:
        f_debug.close()
        sys.stdout = sys.__stdout__

    sys.stdin = sys.__stdin__    # Reset the stdin to its default value
