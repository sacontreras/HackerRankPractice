[link](https://www.hackerrank.com/challenges/ctci-bubble-sort/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=sorting)


## First Try:
This is a straightforward puzzle.  Simplu carry out the sort using the BubbleSort algo.  Along the way, count n_swaps.  Simple. All free test-cases passed. (see below)

```python
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
```

## POST-MORTEM:

There is nothing magic going on here.  Just follow the directions and win.
