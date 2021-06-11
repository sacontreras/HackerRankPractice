[link](https://www.hackerrank.com/challenges/minimum-absolute-difference-in-an-array/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=greedy-algorithms)


## First Try:

This puzzle is fairly straightforward.  If we sort the array in non-decreasing order, then each pair-wise difference (after the sort) will be minimal as well.  We simply take the minimum for our answer.

All free test-cases passed and so did every other test-case upon submission.

(see below)

```python
def minimumAbsoluteDifference(arr, debug=False):
    if debug:
        print(f"arr: {arr}")

    min_diff = 0

    n = len(arr)

    if n > 1:
        # sort the array in non-decreasing order
        arr_sorted = sorted(arr)    # O(n log n) worst case
        if debug:
            print(f"arr_sorted: {arr_sorted}")
            print(f"diffs arr_sorted: {[abs(arr_sorted[i]-arr_sorted[i-1]) for i in range(1,n)]}")
        i = 1
        diff = abs(arr_sorted[i] - arr_sorted[i-1])
        min_diff = diff
        if debug:
            print(f"new min diff: abs(arr_sorted[{i}]-arr_sorted[{i-1}])={min_diff}")
        for i in range(2,n):
            diff = abs(arr_sorted[i] - arr_sorted[i-1])
            if diff < min_diff:
                min_diff = diff
                if debug:
                    print(f"new min diff: abs(arr_sorted[{i}]-arr_sorted[{i-1}])={min_diff}")

    return min_diff
```

<p><br>

(Debug) Output for test-case 00:

```
arr: [3, -7, 0]
arr_sorted: [-7, 0, 3]
diffs arr_sorted: [7, 3]
new min diff: abs(arr_sorted[1]-arr_sorted[0])=7
new min diff: abs(arr_sorted[2]-arr_sorted[1])=3
result: 3
expect: 3
```

<p><br>

(Debug) Output for test-case 01:

```
arr: [-59, -36, -13, 1, -53, -92, -2, -96, -54, 75]
arr_sorted: [-96, -92, -59, -54, -53, -36, -13, -2, 1, 75]
diffs arr_sorted: [4, 33, 5, 1, 17, 23, 11, 3, 74]
new min diff: abs(arr_sorted[1]-arr_sorted[0])=4
new min diff: abs(arr_sorted[4]-arr_sorted[3])=1
result: 1
expect: 1
```

<p><br>

(Debug) Output for test-case 10:

```
arr: [1, -3, 71, 68, 17]
arr_sorted: [-3, 1, 17, 68, 71]
diffs arr_sorted: [4, 16, 51, 3]
new min diff: abs(arr_sorted[1]-arr_sorted[0])=4
new min diff: abs(arr_sorted[4]-arr_sorted[3])=3
result: 3
expect: 3
```

## POST-MORTEM:

See commentary above.