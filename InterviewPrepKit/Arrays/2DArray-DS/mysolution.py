#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'hourglassSum' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY arr as parameter.
#

HOURGLASS_N_ROWS = HOURGLASS_N_COLS = 3

def hourglassSum(arr):
    n_rows = len(arr)
    n_cols = len(arr[0])
    print(f"{n_rows} x {n_cols}\n")
    
    i_hourglass = 0
    sum_hourglass = []
    s_hourglass = []
    for i_row_start in range(0, n_rows-HOURGLASS_N_ROWS+1):
        for i_col_start in range(0, n_cols-HOURGLASS_N_COLS+1):
            
            print(f"hourglass {i_hourglass+1} (with upper-left coords ({i_row_start},{i_col_start})):")
            sum_hourglass.append(0)
            s_hourglass.append("")
            for r in range(i_row_start, i_row_start+HOURGLASS_N_ROWS):
                for c in range(i_col_start, i_col_start+HOURGLASS_N_COLS):
                    v = arr[r][c]
                    
                    if r == i_row_start+1:
                        if c == i_col_start+1:        
                            s_hourglass[i_hourglass] += f"{v} "
                            sum_hourglass[i_hourglass] += v
                        else:
                            s_hourglass[i_hourglass] += f"  "
                    else:
                        s_hourglass[i_hourglass] += f"{v} "
                        sum_hourglass[i_hourglass] += v
                s_hourglass[i_hourglass] += "\n"
            print(f"{s_hourglass[i_hourglass]}\n")
            
            i_hourglass += 1

    i_max_sum = 0
    max_sum = sum_hourglass[i_max_sum]
    for i in range(len(sum_hourglass)):
        sum_i = sum_hourglass[i]
        if sum_i > max_sum:
            i_max_sum = i
            max_sum = sum_i
            
    print(f"hourglass {i_max_sum+1} with max sum of {max_sum} is:\n{s_hourglass[i_max_sum]}")
    
    return max_sum
