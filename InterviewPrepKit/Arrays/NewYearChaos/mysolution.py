#!/bin/python3

import math
import os
import random
import re
import sys
import path
import mergesort

#
# Complete the 'minimumBribes' function below.
#
# The function accepts INTEGER_ARRAY q as parameter.
#

def minimumBribes(q):
    # credit where credit is due:
    #   referenced article https://www.tutorialspoint.com/program-to-count-number-of-swaps-required-to-change-one-list-to-another-in-python

    # e.g.
    #   q   = [2,1,5,3,4]   (if and only if)
    #   q0  = [1,2,3,4,5]
    #
    #   iterating through q, we have:
    #       p = 2   <-->    q0.index(p) == 1    (moved forward 1 spot from q0)
    #           (increment n_bribes by spots moved from q0 for p==2)                                n_bribed += q0.index(p) --> n_bribed = 1
    #           (now pop this index, q0.index(p)==1, from q0 since we are done handling p == 2)     q0.pop(q0.index(p))     --> q0 = [1,3,4,5]
    #       p = 1   <-->    q0.index(p) == 0    (did not move forward from q0)
    #           (increment n_bribes by spots moved from q0 for p==1)                                n_bribed += q0.index(p) --> n_bribed = 1
    #           (now pop this index, q0.index(p)==0, from q0 since we are done handling p == 1)     q0.pop(q0.index(p))     --> q0 = [3,4,5]
    #       p = 5   <-->    q0.index(p) == 2    (moved forward 2 spots from q0)
    #           (increment n_bribes by spots moved from q0 for p==5)                                n_bribed += q0.index(p) --> n_bribed = 3
    #           (now pop this index, q0.index(p)==2, from q0 since we are done handling p == 5)     q0.pop(q0.index(p))     --> q0 = [3,4]
    #       p = 3   <-->    q0.index(p) == 0    (did not move forward from q0)
    #           (increment n_bribes by spots moved from q0 for p==3)                                n_bribed += q0.index(p) --> n_bribed = 3
    #           (now pop this index, q0.index(p)==0, from q0 since we are done handling p == 3)     q0.pop(q0.index(p))     --> q0 = [4]
    #       p = 4   <-->    q0.index(p) == 0    (did not move forward from q0)
    #           (increment n_bribes by spots moved from q0 for p==4)                                n_bribed += q0.index(p) --> n_bribed = 3
    #           (now pop this index, q0.index(p)==0, from q0 since we are done handling p == 4)     q0.pop(q0.index(p))     --> q0 = []

    # get q0 (prior to bribes), so that we can compare it to q (after bribes have occurred)
    q0 = [p0 for p0 in range(1,len(q)+1)]

    n_bribes = 0

    for p in q:        
        i0 = pos_forward_from_q0 = q0.index(p)

        if pos_forward_from_q0 > 2:
            print("Too chaotic")
            return

        # now pop value at this index, q0.index(p), from q0 since we are done handling this p
        q0.pop(i0)

        n_bribes += pos_forward_from_q0

    print(n_bribes)
        

if __name__ == '__main__':
    fd = open('./InterviewPrepKit/Arrays/NewYearChaos/input06.txt')
    sys.stdin = fd

    t = int(input().strip())

    for t_itr in range(t):
        n = int(input().strip())

        q = list(map(int, input().rstrip().split()))

        minimumBribes(q)

    sys.stdin = sys.__stdin__    # Reset the stdin to its default value