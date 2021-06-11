#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the triplets function below.
import itertools
def triplets_v1(a, b, c, debug=False):
    """
    Finds all (p, q, r) such that p <= q, q >= r where p is in a, q is in b, and r is in c
    """

    srtd_unq_a = sorted(set(a))
    srtd_unq_b = sorted(set(b))
    srtd_unq_c = sorted(set(c))

    n_a = len(srtd_unq_a)
    n_b = len(srtd_unq_b)
    n_c = len(srtd_unq_c)

    if debug:
        print(f"a: {a}, b: {b}, c: {c}\n\t--> a_sorted: {srtd_unq_a}, b_sorted: {srtd_unq_b}, c_sorted: {srtd_unq_c}")

    n_solutions = 0
    solutions = []

    j = 0
    while j < n_b:
        q_set = set()
        q = srtd_unq_b[j]

        p_sols = []
        i = 0
        while True:
            if i >= n_a:
                break

            p = srtd_unq_a[i]
            if p > q:
                break

            if debug:
                q_set.add(q)
                p_sols.append(p)

            i += 1


        r_sols = []
        k = 0
        while True:
            if k >= n_c:
                break

            r = srtd_unq_c[k]
            if r > q:
                break

            if debug:
                q_set.add(q)
                r_sols.append(r)

            k += 1

        n_size_cartesian_prod = i * k
        if debug and len(p_sols) > 0 and len(r_sols) > 0: # then we want the cartesian product
            cart_prod = list(itertools.product(p_sols,list(q_set),r_sols))
            assert(n_size_cartesian_prod == len(cart_prod))
            solutions.extend(cart_prod)

        n_solutions += n_size_cartesian_prod

        j += 1

    if debug:
        print(f"SOLUTIONS: {solutions}\n")
    
    return n_solutions

def triplets(a, b, c, debug=False):
    """
    Counts all (p, q, r) such that p <= q, q >= r where p is in a, q is in b, and r is in c
    """

    srtd_unq_a = sorted(set(a))
    srtd_unq_b = sorted(set(b))
    srtd_unq_c = sorted(set(c))

    if debug:
        print(f"a: {a}, b: {b}, c: {c}\n\t--> a_sorted: {srtd_unq_a}, b_sorted: {srtd_unq_b}, c_sorted: {srtd_unq_c}")

    n_a = len(srtd_unq_a)
    n_b = len(srtd_unq_b)
    n_c = len(srtd_unq_c)

    n_solutions = 0

    i = k = j = 0
    while j < n_b:
        q = srtd_unq_b[j]

        while True:
            if i >= n_a:
                break
            p = srtd_unq_a[i]
            if p > q:
                break
            if debug:
                print(f"FOUND p=a[i={i}]={p} <= q=b[j={j}]={q}")
            i += 1
        if debug:
            print(f"there are {i} total p in a such that p <= q")


        while True:
            if k >= n_c:
                break
            r = srtd_unq_c[k]
            if r > q:
                break
            if debug:
                print(f"FOUND r=c[k={k}]={r} <= q=b[j={j}]={q}")
            k += 1
        if debug:
            print(f"there are {k} total r in c such that r <= q")

        n_cart_prod = i * k
        if debug:
            print(f"there are {n_cart_prod} total (p,q={q},r) in the cartesian product such that p, r <= q\n")
        n_solutions += n_cart_prod

        j += 1
    
    return n_solutions

    
if __name__ == '__main__':
    debug = True
    output_to_file = False and debug

    # s_f_indices = ['00','01','09','02']
    s_f_indices = ['00','01','09']

    for s_f_index in s_f_indices:
        base_path = './InterviewPrepKit/Search/TripleSum/'
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
        lenaLenbLenc = input().split()
        lena = int(lenaLenbLenc[0])
        lenb = int(lenaLenbLenc[1])
        lenc = int(lenaLenbLenc[2])
        arra = list(map(int, input().rstrip().split()))
        arrb = list(map(int, input().rstrip().split()))
        arrc = list(map(int, input().rstrip().split()))
        result = triplets_v1(arra, arrb, arrc, debug=debug)
        # fptr.write(str(ans) + '\n')
        # fptr.close()




        # single result
        print(f"result: {result}")
        expect = f_expect.readline().strip()
        print(f"expect: {expect}")
        if str(result) != expect:
            print(f"\t--> FAIL")
        if not debug:
            assert(str(result) == expect)
        if str(result) == expect:
            print(f"\t--> PASS")
        print()

        # multiple
        # expect = f_expect.readlines()
        # for i, l in enumerate(expect):
        #     _expect = l.strip()
        #     print(f"TEST CASE {s_f_index}.{i+1} RESULTS (from query=={queries[i]}):")
        #     s_result = None
        #     if i < len(result):
        #         s_result = ' '.join([str(x) for x in result[i]])
        #         print(f"\tresult: {s_result}")
        #     else:
        #         print(f"\tresult: <non-existence... result only has {len(result)} elements>")
        #     print(f"\texpect: {_expect}")

        #     if s_result != _expect:
        #         print(f"\t\t--> FAILED on result index: {i}")
        #     if not debug:
        #         assert(_expect == s_result)
        #     if _expect == s_result:
        #         print(f"\t\t--> PASS")
        #     print()

        # print("\n\n")

        fd.close()
        f_expect.close()

        if output_to_file:
            f_debug.close()
            sys.stdout = sys.__stdout__

        sys.stdin = sys.__stdin__    # Reset the stdin to its default value
