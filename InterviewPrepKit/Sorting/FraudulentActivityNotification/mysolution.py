#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'activityNotifications' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY expenditure
#  2. INTEGER d
#

from bisect import bisect_left, insort_left
def activityNotifications(expenditure, d):
    debug = False

    n_notify = 0

    n = len(expenditure)
    
    if debug:
        print(f"expenditure: {expenditure}, d: {d}")

    # new for v. 2: 
    #   pre-sorting this the first time yields a nearly sorted list for all subsequent iterations
    #   and then we can find the index of the one new expenditure to be replaced
    #   via bisect_left() and then replace it with insort_left with O(n) complexity
    prev_exp_sorted = sorted(expenditure[0:d])

    for i_end in range(d,n):
        i_start = i_end-d

        if debug:
            prev_expenditures = expenditure[i_start:i_end]  # # new for v. 2: only need this when debugging
        # prev_exp_sorted = sorted(prev_expenditures) # bottleneck in v. 1
        
        med = None
        i_med_offset = d // 2
        if debug:
            print(f"\texpenditure indices: [{i_start},{i_end-1}] --> i_med_offset: {i_start+i_med_offset}")
        if d % 2 == 1:
            med = prev_exp_sorted[i_med_offset]
        else:
            med = (prev_exp_sorted[i_med_offset-1]+prev_exp_sorted[i_med_offset]) / 2

        exp_thresh = 2*med

        exp_today = expenditure[i_end]

        thresh_reached = exp_today >= exp_thresh

        if debug:
            print(f"\ton day {i_end+1}, prior {d} expenditures: {prev_expenditures} (sorted: {prev_exp_sorted})")
            print(f"\t\t--> median: {med} --> expenditure threshold: {exp_thresh}")
            print(f"\t\t\texpenditure today (day {i_end+1}) is {exp_today} --> notify (exp >= thresh)? {exp_today} >= {exp_thresh}? {thresh_reached}")
    
        n_notify += 1 if thresh_reached else 0

        # new for v. 2
        remove_at = bisect_left(prev_exp_sorted, expenditure[i_end-d])
        prev_exp_sorted.pop(remove_at)
        insort_left(prev_exp_sorted, expenditure[i_end])
    
    return n_notify


if __name__ == '__main__':
    output_to_file = False
    s_f_index = '02'
    base_path = './InterviewPrepKit/Sorting/FraudulentActivityNotification/'
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
    first_multiple_input = input().rstrip().split()
    n = int(first_multiple_input[0])
    d = int(first_multiple_input[1])
    expenditure = list(map(int, input().rstrip().split()))
    result = activityNotifications(expenditure, d)
    # fptr.write(str(result) + '\n')
    # fptr.close()




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
