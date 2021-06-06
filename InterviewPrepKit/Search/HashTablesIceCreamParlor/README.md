[link](https://www.hackerrank.com/challenges/ctci-ice-cream-parlor/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=search)


## First Try:

This puzzle if fairly straightforward.  Essentially, it can be distilled down to: given target sum $k$ and a list of integers $a_i: 1 \le i \le n, a_i > 0$, find $i \ne j$ such that $a_i + a_j = k$.

We construct a single dictionary (hash table) keyed by each $a_i$, with associated value consisting of the list (array) of indices $1 \le i \le n$ incident with each occurrence of $a_i$.

We then iterate the keys, each $a_i$, and check for existence of key $a_j = k - a_i$.  If it exists, we simply return $i, j$.

This algorithm passed all free test-cases and, upon submission, all locked test-cases.

(see below)

```
def whatFlavors(cost, money, debug=False):
    if debug:
        print(f"cost: {cost}, money: {money}")

    i_f_2 = i_f_1 = 0

    d_costs = {}
    for i, c in enumerate(cost):
        indices = d_costs.get(c,[])
        indices.append(i)
        d_costs[c] = indices
    if debug:
        print(f"d_costs: {d_costs}")

    for c, indices in d_costs.items():
        if len(indices) > 0:
            need = money - c
            i_c = indices.pop(0)
            if debug:
                print(f"\tcost {c} (at index {i_c+1}) requires complement cost {need}")
            if need in d_costs:
                need_indices = d_costs[need]
                if len(need_indices) > 0:
                    i_need = need_indices.pop(0)
                    i_f_1 = i_c+1
                    i_f_2 = i_need+1
                    if debug:
                        print(f"\t\titem found at index {i_need+1}")
                    break
            if debug:
                print(f"\t\tbut no item at need cost {need} is available")
        
    result = f"{i_f_1} {i_f_2}"
    print(result)

    if debug:
        return result
```

<p><br>

(Debug) Output for test-case 14:

```
cost: [1, 4, 5, 3, 2], money: 4
d_costs: {1: [0], 4: [1], 5: [2], 3: [3], 2: [4]}
        cost 1 (at index 1) requires complement cost 3
                item found at index 4
1 4
cost: [2, 2, 4, 3], money: 4
d_costs: {2: [0, 1], 4: [2], 3: [3]}
        cost 2 (at index 1) requires complement cost 2
                item found at index 2
1 2
expect: 1 4
result: 1 4

expect: 1 2
result: 1 2
```

<p><br>

(Debug) Output for test-case 15:

```
cost: [1, 2, 3, 5, 6], money: 5
d_costs: {1: [0], 2: [1], 3: [2], 5: [3], 6: [4]}
        cost 1 (at index 1) requires complement cost 4
                but no item at need cost 4 is available
        cost 2 (at index 2) requires complement cost 3
                item found at index 3
2 3
expect: 2 3
result: 2 3
```

<p><br>

(Debug) Output for test-case 16:

```
cost: [4, 3, 2, 5, 7], money: 8
d_costs: {4: [0], 3: [1], 2: [2], 5: [3], 7: [4]}
        cost 4 (at index 1) requires complement cost 4
                but no item at need cost 4 is available
        cost 3 (at index 2) requires complement cost 5
                item found at index 4
2 4
cost: [7, 2, 5, 4, 11], money: 12
d_costs: {7: [0], 2: [1], 5: [2], 4: [3], 11: [4]}
        cost 7 (at index 1) requires complement cost 5
                item found at index 3
1 3
expect: 2 4
result: 2 4

expect: 1 3
result: 1 3
```

## POST-MORTEM:

There were no real "gotchas" with this puzzle.  Successfully solving on the first try simply required reading the specification closely and then recognizing it could be solved easiest with a hash table.