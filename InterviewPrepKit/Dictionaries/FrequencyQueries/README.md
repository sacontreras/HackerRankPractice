[link](https://www.hackerrank.com/challenges/frequency-queries/problem?h_l=interview&h_r=next-challenge&h_v=zen&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=dictionaries-hashmaps)


## First Try:
This puzzle is fairly easy since it is mostly an exercise in tedium and accounting.  Use two dictionaries for O(1) lookup: one to track frequencies of values, keyed by value, and another to track sets of values keyed by count.  All three free test-cases passed but test-cases 5 through 9, as well as 12, failed.

(see below)

```
def freqQuery(queries):
    debug = True

    if debug:
        print(f"queries: {queries}")

    d_by_val = {}
    d_by_counts = {}
    q_3_results = []

    for q in queries:
        q_type = q[0]
        q_val = q[1]

        if q_type == 1: # insert
            """
            Insert x in your data structure
            """
            
            if debug:
                print(f"\tquery type 1: insert {q_val} into datastructure")

            n_q_val = d_by_val.get(q_val,0) + 1
            d_by_val[q_val] = n_q_val
            qvals_set_of_n = d_by_counts.get(n_q_val,set())
            qvals_set_of_n.add(q_val)
            d_by_counts[n_q_val] = qvals_set_of_n

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
                n = d_by_val.get(q_val,0)

                if n > 0:
                    n_new = n - 1

                    d_by_val[q_val] = n_new

                    # now update d_by_counts
                    qvals_set_of_n = d_by_counts.get(n,set())
                    qvals_set_of_n.remove(q_val)

                    if len(qvals_set_of_n) > 0:
                        d_by_counts[n] = qvals_set_of_n
                    else:
                        del d_by_counts[n]

                    if n_new < 1:
                        del d_by_val[q_val]
            else:
                if debug:
                    print(f"\t\t{q_val} is not in datastructure")

            if debug:
                print(f"\t\td_by_val: {d_by_val}")
                print(f"\t\td_by_counts: {d_by_counts}")

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
            print()

    return q_3_results
```

<p><br>

Output for test-case 00:
```
testing against input file ./InterviewPrepKit/Dictionaries/FrequencyQueries/input00.txt...
queries: [[1, 5], [1, 6], [3, 2], [1, 10], [1, 10], [1, 6], [2, 5], [3, 2]]
        query type 1: insert 5 into datastructure
                d_by_val: {5: 1}
                d_by_counts: {1: {5}}

        query type 1: insert 6 into datastructure
                d_by_val: {5: 1, 6: 1}
                d_by_counts: {1: {5, 6}}

        query type 3: exists/count of 2 in datastructure
                there are no values in datastructure with exactly 2 occurrences

        query type 1: insert 10 into datastructure
                d_by_val: {5: 1, 6: 1, 10: 1}
                d_by_counts: {1: {10, 5, 6}}

        query type 1: insert 10 into datastructure
                d_by_val: {5: 1, 6: 1, 10: 2}
                d_by_counts: {1: {10, 5, 6}, 2: {10}}

        query type 1: insert 6 into datastructure
                d_by_val: {5: 1, 6: 2, 10: 2}
                d_by_counts: {1: {10, 5, 6}, 2: {10, 6}}

        query type 2: delete one occurrence of 5 from datastructure
                d_by_val: {6: 2, 10: 2}
                d_by_counts: {1: {10, 6}, 2: {10, 6}}

        query type 3: exists/count of 2 in datastructure
                values in datastructure with exactly 2 occurrences: {10, 6}

expect: 0
result: 0

expect: 1
result: 1
```

<p><br>

Output for test-case 01:
```
testing against input file ./InterviewPrepKit/Dictionaries/FrequencyQueries/input01.txt...
queries: [[3, 4], [2, 1003], [1, 16], [3, 1]]
        query type 3: exists/count of 4 in datastructure
                there are no values in datastructure with exactly 4 occurrences

        query type 2: delete one occurrence of 1003 from datastructure
                1003 is not in datastructure
                d_by_val: {}
                d_by_counts: {}

        query type 1: insert 16 into datastructure
                d_by_val: {16: 1}
                d_by_counts: {1: {16}}

        query type 3: exists/count of 1 in datastructure
                values in datastructure with exactly 1 occurrences: {16}

expect: 0
result: 0

expect: 1
result: 1
```

<p><br>

Output for test-case 02:
```
testing against input file ./InterviewPrepKit/Dictionaries/FrequencyQueries/input02.txt...
queries: [[1, 3], [2, 3], [3, 2], [1, 4], [1, 5], [1, 5], [1, 4], [3, 2], [2, 4], [3, 2]]
        query type 1: insert 3 into datastructure
                d_by_val: {3: 1}
                d_by_counts: {1: {3}}

        query type 2: delete one occurrence of 3 from datastructure
                d_by_val: {}
                d_by_counts: {}

        query type 3: exists/count of 2 in datastructure
                there are no values in datastructure with exactly 2 occurrences

        query type 1: insert 4 into datastructure
                d_by_val: {4: 1}
                d_by_counts: {1: {4}}

        query type 1: insert 5 into datastructure
                d_by_val: {4: 1, 5: 1}
                d_by_counts: {1: {4, 5}}

        query type 1: insert 5 into datastructure
                d_by_val: {4: 1, 5: 2}
                d_by_counts: {1: {4, 5}, 2: {5}}

        query type 1: insert 4 into datastructure
                d_by_val: {4: 2, 5: 2}
                d_by_counts: {1: {4, 5}, 2: {4, 5}}

        query type 3: exists/count of 2 in datastructure
                values in datastructure with exactly 2 occurrences: {4, 5}

        query type 2: delete one occurrence of 4 from datastructure
                d_by_val: {4: 1, 5: 2}
                d_by_counts: {1: {4, 5}, 2: {5}}

        query type 3: exists/count of 2 in datastructure
                values in datastructure with exactly 2 occurrences: {5}

expect: 0
result: 0

expect: 1
result: 1

expect: 1
result: 1
```

## Second Try:

In the first try, I failed to update `d_by_counts` on insert. (see below)

But still failing on test cases 8,9, and 12.

```
def freqQuery(queries):
    debug = False

    d_by_val = {}
    d_by_counts = {}
    q_3_results = []

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

            # update count in d_by_val first
            n_q_val = d_by_val.get(q_val,0)
            n_new_q_val = n_q_val + 1
            d_by_val[q_val] = n_new_q_val

            # now update d_by_counts by removing q_val from set keyed by n_q_val
            qvals_set_of_n = d_by_counts.get(n_q_val,set())
            if q_val in qvals_set_of_n:
                qvals_set_of_n.remove(q_val)
                if len(qvals_set_of_n) > 0:
                    d_by_counts[n_q_val] = qvals_set_of_n
                else:
                    del d_by_counts[n_q_val]

            # finally update d_by_counts by adding q_val to set keyed by n_new_q_val
            qvals_set_of_n = d_by_counts.get(n_new_q_val,set())
            qvals_set_of_n.add(q_val)
            d_by_counts[n_new_q_val] = qvals_set_of_n

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
                n = d_by_val.get(q_val,0)

                if n > 0:
                    n_new = n - 1

                    d_by_val[q_val] = n_new

                    # now update d_by_counts
                    qvals_set_of_n = d_by_counts.get(n,set())
                    if q_val in qvals_set_of_n:
                        qvals_set_of_n.remove(q_val)

                    if len(qvals_set_of_n) > 0:
                        d_by_counts[n] = qvals_set_of_n
                    else:
                        del d_by_counts[n]

                    if n_new < 1:
                        del d_by_val[q_val]

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
```

## Third Try

This iteration consisted merely of consolidation functionality into a common `update_count` function.  ALL TEST CASES NOW PASSING! (see below)

```
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
```


## POST-MORTEM:

The main "take-aways" here are to always keep in mind complexity and to mind your "spaghetti code".  Dictionaries were vital to a nice time complexity in this case.  In the first two iterations, I neglected to consolidate code into common operations, reasulting in different behavior in different instances.  That is a big fat NO-NO!