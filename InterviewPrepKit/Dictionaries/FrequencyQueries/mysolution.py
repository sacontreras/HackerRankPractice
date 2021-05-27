#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the freqQuery function below.
def freqQuery(queries):
    debug = False

    d_by_val = {}
    d_by_counts = {}
    q_3_results = []

    def remove_qval_by_count(q_val, n):
        qvals_set = d_by_counts[n]
        qvals_set.remove(q_val)
        if len(qvals_set) == 0:
            del d_by_counts[n]
        else:
            d_by_counts[n] = qvals_set

    def append_qval_by_count(q_val, n):
        qvals_set = d_by_counts.get(n,set())
        qvals_set.add(q_val)
        d_by_counts[n] = qvals_set

    def update_count(q_val, n_new):
        if q_val in d_by_val:
            n_current = d_by_val[q_val]

            if n_new > 0:
                d_by_val[q_val] = n_new
                if n_new != n_current:
                    remove_qval_by_count(q_val, n_current)
                    append_qval_by_count(q_val, n_new)

            else:   # remove
                del d_by_val[q_val]
                remove_qval_by_count(q_val, n_current)

        else:
            d_by_val[q_val] = 1
            append_qval_by_count(q_val, 1)

    for i, q in enumerate(queries):
        if debug:
            print(f"query {i+1}: {q}")

        q_type = q[0]
        q_val = q[1]

        if q_type == 1: # insert
            """
            Insert x in your data structure
            """
            
            if debug:
                print(f"\tquery type 1: insert {q_val} into datastructure")

            update_count(q_val, d_by_val.get(q_val,0)+1)

            if debug:
                print(f"\t\td_by_val: {d_by_val}")
                print(f"\t\td_by_counts: {d_by_counts}")

        elif q_type == 2: # delete
            """
            Delete one occurence of y from your data structure, if present
            """
            if debug:
                print(f"\tquery type 2: delete one occurrence of {q_val} from datastructure")

            if q_val in d_by_val:
                update_count(q_val, d_by_val[q_val]-1)

                if debug:
                    print(f"\t\td_by_val: {d_by_val}")
                    print(f"\t\td_by_counts: {d_by_counts}")

            else:
                if debug:
                    print(f"\t\t{q_val} is not in datastructure")

        elif q_type == 3: # exists
            """
            Check if any integer is present whose frequency is exactly . If yes, print 1 else 0.
            """
            if debug:
                print(f"\tquery type 3: exists/count of {q_val} in datastructure")

            if q_val in d_by_counts:
                qvals_set_of_n = d_by_counts[q_val]
                if debug:
                    print(f"\t\tvalues in datastructure with exactly {q_val} occurrences: {qvals_set_of_n}")
                q_3_results.append(1)
            else:
                if debug:
                    print(f"\t\tthere are no values in datastructure with exactly {q_val} occurrences")
                q_3_results.append(0)

            if debug:
                print(f"\t\t\tq_3_results index: {len(q_3_results)-1}")

        if debug:
            print()

    return q_3_results


if __name__ == '__main__':
    output_to_file = False
    s_f_index = '08'
    base_path = './InterviewPrepKit/Dictionaries/FrequencyQueries/'
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

    q = int(input().strip())

    queries = []

    for _ in range(q):
        queries.append(list(map(int, input().rstrip().split())))

    ans = freqQuery(queries)

    # fptr.write(str(ans) + '\n')

    # fptr.close()

    result = ans

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
            print(f"failed on q_3_results index: {i}")
        assert(_expect == s_result)
        print()

    fd.close()
    f_expect.close()

    if output_to_file:
        f_debug.close()
        sys.stdout = sys.__stdout__

    sys.stdin = sys.__stdin__    # Reset the stdin to its default value
