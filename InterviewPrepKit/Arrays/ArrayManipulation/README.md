[link](https://www.hackerrank.com/challenges/crush/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=arrays)

The explanation of the puzzle is not exactly clear and REQUIRES inspecting the example in order to sort out the correct logic.


## First Try:

In theory, again, this puzzle is fairly straightforward.  My initial attempt is brute force and is logically correct.  However, it is sub-optimal with O(n^2) complexity and thus fails half of the test cases due to timeout.  Downloading test-cases shows the logic is correct.  (see below)

```
def arrayManipulation(n, queries):
    arr = [0 for _ in range(n)]
    # print(f"initialized array of length {n}: {arr}")

    # print("queries:")
    for lb_1, ub_1, k in queries:
        for i in range(lb_1-1, ub_1):
            arr[i] += k
        # print(f"\t{lb_1}\t{ub_1}\t{k}\t--> arr: {arr}")

    max_v = arr[0]
    for v in arr:
        if v > max_v:
            max_v = v
    
    return max_v
```


# Second Try:

I analyzed the patterns produced from several of the free test cases.  Upon inspection of the output from the brute force approach above, it looks as if the pattern shows that the only entries that contribute to the max calc involve only indices lb_1-1 and ub_1 (inclusive).  If we track the cumulative sum and update max_v based on that, in that case we substract the val at ub_1 (inclusive).  This will result in linear complexity.  (see below)

ALL TEST CASES PASSED!
```
def arrayManipulation(n, queries):
    arr_debug = None
    arr = [0 for _ in range(n+1)]
    
    debug = n <= 10

    if debug:
        arr_debug = [0 for _ in range(n)]
    else:
        print(f"debug output suppressed for large n")

    if debug:
        print("queries:")
    max_v_debug = 0

    for lb_1, ub_1, k in queries:   # indices are for 1-based array

        # brute force investigation
        if debug:
            for i in range(lb_1-1, ub_1):   # since array is 1-based
                arr_debug[i] += k
                if arr_debug[i] > max_v_debug:
                    max_v_debug = arr_debug[i]
            print(f"\t{lb_1}\t{ub_1}\t{k}\t--> arr_debug:\t{arr_debug}")

        # upon inspection of the above, it looks as if the pattern
        #   shows that the only entries that contribute to the max calc
        #   involve only indices lb_1-1 and ub_1 (inclusive)
        #   if we track the cumulative sum and update max_v based on that
        #       in that case we substract the val at ub_1 (inclusive)
        #   this will result in linear complexity
        arr[lb_1-1] += k
        arr[ub_1] -= k
        if debug:
            print(f"\t{lb_1}\t{ub_1}\t{k}\t--> arr:\t{arr}")
        if debug:
            print()

    if debug:
        print(f"max_v_debug is {max_v_debug}")

    max_v = arr[0]
    s = 0
    for v in arr:
        s += v
        if s > max_v:
            max_v = s

    if debug:
        print(f"max_v == max_v_debug --> {max_v} == {max_v_debug} ? {max_v == max_v_debug}")
        assert(max_v == max_v_debug)
    
    return max_v
```


## POST-MORTEM:

The trick in this case was testing, testing, testing and then analyzing the resulting patterns.