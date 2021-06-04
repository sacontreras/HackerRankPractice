[link](https://www.hackerrank.com/challenges/angry-children/problem?h_l=interview&h_r%5B%5D%5B%5D%5B%5D=next-challenge&h_r%5B%5D%5B%5D%5B%5D=next-challenge&h_v%5B%5D%5B%5D%5B%5D=zen&h_v%5B%5D%5B%5D%5B%5D=zen&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=greedy-algorithms&h_r=next-challenge&h_v=zen)


## First Try:

This puzzle is very straightforward.  Simply sort the array ($O(n \log n$ complexity), peel off the first $k$ elements, and then take the difference between the last and first elements of those.

This algorithm passed all free test-cases.  Unfortunately, it failed every one of the locked test-cases!

(see below)

```
def maxMin(k, arr, debug=False):
    if debug:
        print(f"k: {k}, arr: {arr}")

    min_unfairness = 0

    arr_sorted = sorted(arr)
    if debug:
        print(f"arr_sorted: {arr_sorted}")
    min_arr = arr_sorted[:k]
    v_max = min_arr[-1]
    v_min = min_arr[0]
    min_unfairness = v_max - v_min
    if debug:
        print(f"min_arr: {min_arr} --> min unfairness = max({min_arr}) - min({min_arr}) = {v_max} - {v_min} = {min_unfairness}")

    return min_unfairness
```

<p><br>

(Debug) Output for test-case 00:

```
k: 3, arr: [10, 100, 300, 200, 1000, 20, 30]
arr_sorted: [10, 20, 30, 100, 200, 300, 1000]
min_arr: [10, 20, 30] --> min unfairness = max([10, 20, 30]) - min([10, 20, 30]) = 30 - 10 = 20
result: 20
expect: 20
```

<p><br>

(Debug) Output for test-case 01:

```
k: 4, arr: [1, 2, 3, 4, 10, 20, 30, 40, 100, 200]
arr_sorted: [1, 2, 3, 4, 10, 20, 30, 40, 100, 200]
min_arr: [1, 2, 3, 4] --> min unfairness = max([1, 2, 3, 4]) - min([1, 2, 3, 4]) = 4 - 1 = 3
result: 3
expect: 3
```

<p><br>

(Debug) Output for test-case 15:

```
k: 2, arr: [1, 2, 1, 2, 1]
arr_sorted: [1, 1, 1, 2, 2]
min_arr: [1, 1] --> min unfairness = max([1, 1]) - min([1, 1]) = 1 - 1 = 0
result: 0
expect: 0
```

## Second Try:

The last algorithm was close but naively neglected to iterate windows of length $k$ from the sorted values.

The new (modified from above) algorithm passed all free test-cases as well as the unlocked test-case 02.  Upon submission, it passed all remaining locked test-cases except for 16.

(see below)

```
def maxMin(k, arr, debug=False):
    if debug:
        print(f"k: {k}, arr: {arr}")

    min_unfairness = 0

    arr_sorted = sorted(arr)
    
    # now we iterate through arr_sorted, taking windows of length k
    if debug:
        print(f"iterating windows of length {k} from arr_sorted: {arr_sorted}")
    min_diff = None
    for i_start in range(len(arr)-k):
        v_max = arr_sorted[i_start+k-1]
        v_min = arr_sorted[i_start]
        diff = v_max - v_min
        if min_diff is None or diff < min_diff:
            min_diff = diff
            if debug:
                print(f"\tnew min diff {min_diff} from window {arr_sorted[i_start:i_start+k]} (from inclusive index bounds [{i_start},{i_start+k-1}])")

    min_unfairness = min_diff

    return min_unfairness
```

<p><br>

(Debug) Output for test-case 00:

```
k: 3, arr: [10, 100, 300, 200, 1000, 20, 30]
iterating windows of length 3 from arr_sorted: [10, 20, 30, 100, 200, 300, 1000]
        new min diff 20 from window [10, 20, 30] (from inclusive index bounds [0,2])
result: 20
expect: 20
```

<p><br>

(Debug) Output for test-case 01:

```
k: 4, arr: [1, 2, 3, 4, 10, 20, 30, 40, 100, 200]
iterating windows of length 4 from arr_sorted: [1, 2, 3, 4, 10, 20, 30, 40, 100, 200]
        new min diff 3 from window [1, 2, 3, 4] (from inclusive index bounds [0,3])
result: 3
expect: 3
```

<p><br>

(Debug) Output for test-case 02:

```
k: 5, arr: [4504, 1520, 5857, 4094, 4157, 3902, 822, 6643, 2422, 7288, 8245, 9948, 2822, 1784, 7802, 3142, 9739, 5629, 5413, 7232]
iterating windows of length 5 from arr_sorted: [822, 1520, 1784, 2422, 2822, 3142, 3902, 4094, 4157, 4504, 5413, 5629, 5857, 6643, 7232, 7288, 7802, 8245, 9739, 9948]
        new min diff 2000 from window [822, 1520, 1784, 2422, 2822] (from inclusive index bounds [0,4])
        new min diff 1622 from window [1520, 1784, 2422, 2822, 3142] (from inclusive index bounds [1,5])
        new min diff 1335 from window [2822, 3142, 3902, 4094, 4157] (from inclusive index bounds [4,8])
result: 1335
expect: 1335
```

<p><br>

(Debug) Output for test-case 15:

```
k: 2, arr: [1, 2, 1, 2, 1]
iterating windows of length 2 from arr_sorted: [1, 1, 1, 2, 2]
        new min diff 0 from window [1, 1] (from inclusive index bounds [0,1])
result: 0
expect: 0
```

## Third Try:

I made a mistake on the upper-bound on the range of starting indices (corresponding to windows of length $k$ in the sorted array).  I was off by 1.

(see below)

```
def maxMin(k, arr, debug=False):
    if debug:
        print(f"k: {k}, arr: {arr}")

    min_unfairness = 0

    arr_sorted = sorted(arr)
    
    # now we iterate through arr_sorted, taking windows of length k
    if debug:
        print(f"iterating windows of length {k} from arr_sorted: {arr_sorted}")
    min_diff = None
    for i_start in range(len(arr)-k+1): # upper-bound was off by 1
        v_max = arr_sorted[i_start+k-1]
        v_min = arr_sorted[i_start]
        diff = v_max - v_min
        if min_diff is None or diff < min_diff:
            min_diff = diff
            if debug:
                print(f"\tnew min diff {min_diff} from window {arr_sorted[i_start:i_start+k]} (from inclusive index bounds [{i_start},{i_start+k-1}])")

    min_unfairness = min_diff

    return min_unfairness
```

<p><br>

(Debug) Output for test-case 00:

```
k: 3, arr: [10, 100, 300, 200, 1000, 20, 30]
iterating windows of length 3 from arr_sorted: [10, 20, 30, 100, 200, 300, 1000]
        new min diff 20 from window [10, 20, 30] (from inclusive index bounds [0,2])
result: 20
expect: 20
```

<p><br>

(Debug) Output for test-case 01:

```
k: 4, arr: [1, 2, 3, 4, 10, 20, 30, 40, 100, 200]
iterating windows of length 4 from arr_sorted: [1, 2, 3, 4, 10, 20, 30, 40, 100, 200]
        new min diff 3 from window [1, 2, 3, 4] (from inclusive index bounds [0,3])
result: 3
expect: 3
```

<p><br>

(Debug) Output for test-case 02:

```
k: 5, arr: [4504, 1520, 5857, 4094, 4157, 3902, 822, 6643, 2422, 7288, 8245, 9948, 2822, 1784, 7802, 3142, 9739, 5629, 5413, 7232]
iterating windows of length 5 from arr_sorted: [822, 1520, 1784, 2422, 2822, 3142, 3902, 4094, 4157, 4504, 5413, 5629, 5857, 6643, 7232, 7288, 7802, 8245, 9739, 9948]
        new min diff 2000 from window [822, 1520, 1784, 2422, 2822] (from inclusive index bounds [0,4])
        new min diff 1622 from window [1520, 1784, 2422, 2822, 3142] (from inclusive index bounds [1,5])
        new min diff 1335 from window [2822, 3142, 3902, 4094, 4157] (from inclusive index bounds [4,8])
result: 1335
expect: 1335
```

<p><br>

(Debug) Output for test-case 15:

```
k: 2, arr: [1, 2, 1, 2, 1]
iterating windows of length 2 from arr_sorted: [1, 1, 1, 2, 2]
        new min diff 0 from window [1, 1] (from inclusive index bounds [0,1])
result: 0
expect: 0
```

<p><br>

(Debug) Output for test-case 16:

```
k: 3, arr: [100, 200, 300, 350, 400, 401, 402]
iterating windows of length 3 from arr_sorted: [100, 200, 300, 350, 400, 401, 402]
        new min diff 200 from window [100, 200, 300] (from inclusive index bounds [0,2])
        new min diff 150 from window [200, 300, 350] (from inclusive index bounds [1,3])
        new min diff 100 from window [300, 350, 400] (from inclusive index bounds [2,4])
        new min diff 51 from window [350, 400, 401] (from inclusive index bounds [3,5])
        new min diff 2 from window [400, 401, 402] (from inclusive index bounds [4,6])
result: 2
expect: 2
```

All remaining locked test-cases are now passing.

## POST-MORTEM:

This was an easy puzzle.  However, it was a great reminder to pay close attention to detail, especially in "off-by-one" considerations.