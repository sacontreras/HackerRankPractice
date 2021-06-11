[link](https://www.hackerrank.com/challenges/luck-balance/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=greedy-algorithms&h_r=next-challenge&h_v=zen)


## First Try:

This puzzle is fairly straightforward.  Basically, it requires inspection of all of the examples to extract the pattern.  We first partition the contests array into important and unimportant contests.  From there, we sort the important contests and lose the top $k$ (by luck).  Doing so will maximize luck balances according to the forumula: `sum(<luck of top k sorted important contests>) + sum(<luck of each unimportant contest>) - sum(<luck of bottom remaining important contests>)`.  

This passed all free test-cases and upon submission, pass all test-cases except for test-case 08.

(see below)

```python
def luckBalance(k, contests, debug=False):
    if debug:
        print(f"k: {k}, {len(contests)} contests: {contests}\n")

    max_luck_balance = 0

    unimportant_losses = list(filter(lambda c: c[1]==0, contests))
    if debug:
        print(f"{len(unimportant_losses)} unimportant_losses: {unimportant_losses}\n")

    important_losses = sorted(filter(lambda c: c[1]==1, contests), key=lambda c: c[0])
    if debug:
        print(f"{len(important_losses)} important_losses: {important_losses}")
    max_luck_important_losses = important_losses[len(important_losses)-k:]
    if debug:
        print(f"\ttop {k} important losses by luck: {max_luck_important_losses}")
    min_luck_important_losses = important_losses[:len(important_losses)-k]
    if debug:
        print(f"\tbottom {len(important_losses)-k} important losses by luck: {min_luck_important_losses}")

    s_max_luck_important_losses = sum([c[0] for c in max_luck_important_losses])
    s_unimportant_losses = sum([c[0] for c in unimportant_losses])
    s_min_luck_important_losses = sum([c[0] for c in min_luck_important_losses])
    max_luck_balance = s_max_luck_important_losses + s_unimportant_losses - s_min_luck_important_losses
    if debug:
        print(f"max luck: max_luck_important_losses + unimportant_losses - min_luck_important_losses = {s_max_luck_important_losses} + {s_unimportant_losses} - {s_min_luck_important_losses} = {max_luck_balance}")

    return max_luck_balance
```

<p><br>

(Debug) Output for test-case 00:

```
k: 3, 6 contests: [[5, 1], [2, 1], [1, 1], [8, 1], [10, 0], [5, 0]]

2 unimportant_losses: [[10, 0], [5, 0]]

4 important_losses: [[1, 1], [2, 1], [5, 1], [8, 1]]
        top 3 important losses by luck: [[2, 1], [5, 1], [8, 1]]
        bottom 1 important losses by luck: [[1, 1]]
max luck: max_luck_important_losses + unimportant_losses - min_luck_important_losses = 15 + 15 - 1 = 29
result: 29
expect: 29
```

<p><br>

(Debug) Output for test-case 03:

```
k: 5, 8 contests: [[13, 1], [10, 1], [9, 1], [8, 1], [13, 1], [12, 1], [18, 1], [13, 1]]

0 unimportant_losses: []

8 important_losses: [[8, 1], [9, 1], [10, 1], [12, 1], [13, 1], [13, 1], [13, 1], [18, 1]]
        top 5 important losses by luck: [[12, 1], [13, 1], [13, 1], [13, 1], [18, 1]]
        bottom 3 important losses by luck: [[8, 1], [9, 1], [10, 1]]
max luck: max_luck_important_losses + unimportant_losses - min_luck_important_losses = 69 + 0 - 27 = 42
result: 42
expect: 42
```

<p><br>

(Debug) Output for test-case 12:

```
k: 2, 5 contests: [[5, 1], [4, 0], [6, 1], [2, 1], [8, 0]]

2 unimportant_losses: [[4, 0], [8, 0]]

3 important_losses: [[2, 1], [5, 1], [6, 1]]
        top 2 important losses by luck: [[5, 1], [6, 1]]
        bottom 1 important losses by luck: [[2, 1]]
max luck: max_luck_important_losses + unimportant_losses - min_luck_important_losses = 11 + 12 - 2 = 21
result: 21
expect: 21
```

## Second Try:

The only modification to get this to pass on the failed test-case (08) was to set k to `min(k, len(important_losses))`  

This passed all free test-cases and upon submission, passed ALL test-cases including the previously failing test-case (08).

(see below)

```python
def luckBalance(k, contests, debug=False):
    if debug:
        print(f"k: {k}, {len(contests)} contests: {contests}\n")

    max_luck_balance = 0

    unimportant_losses = list(filter(lambda c: c[1]==0, contests))
    if debug:
        print(f"{len(unimportant_losses)} unimportant_losses: {unimportant_losses}\n")

    important_losses = sorted(filter(lambda c: c[1]==1, contests), key=lambda c: c[0])
    if debug:
        print(f"{len(important_losses)} important_losses: {important_losses}")
    k = min(k, len(important_losses))
    max_luck_important_losses = important_losses[len(important_losses)-k:]
    if debug:
        print(f"\ttop {k} important losses by luck: {max_luck_important_losses}")
    min_luck_important_losses = important_losses[:len(important_losses)-k]
    if debug:
        print(f"\tbottom {len(important_losses)-k} important losses by luck: {min_luck_important_losses}")

    s_max_luck_important_losses = sum([c[0] for c in max_luck_important_losses])
    s_unimportant_losses = sum([c[0] for c in unimportant_losses])
    s_min_luck_important_losses = sum([c[0] for c in min_luck_important_losses])
    max_luck_balance = s_max_luck_important_losses + s_unimportant_losses - s_min_luck_important_losses
    if debug:
        print(f"max luck: max_luck_important_losses + unimportant_losses - min_luck_important_losses = {s_max_luck_important_losses} + {s_unimportant_losses} - {s_min_luck_important_losses} = {max_luck_balance}")

    return max_luck_balance
```

<p><br>

(Debug) Output for test-case 08:

```
k: 58, 97 contests: [[105, 0], [103, 0], [106, 1], [106, 1], [103, 0], [103, 1], [105, 1], [106, 1], [105, 0], [104, 0], [103, 0], [102, 0], [104, 0], [105, 0], [104, 0], [102, 1], [104, 0], [106, 1], [104, 1], [101, 1], [105, 0], [103, 0], [104, 0], [106, 0], [102, 1], [103, 0], [102, 0], [103, 1], [106, 0], [104, 1], [101, 1], [101, 1], [106, 0], [103, 1], [103, 0], [104, 1], [101, 0], [105, 1], [105, 0], [104, 1], [105, 0], [106, 0], [104, 0], [105, 0], [101, 1], [106, 1], [105, 0], [103, 0], [104, 1], [101, 1], [106, 1], [104, 0], [106, 1], [105, 0], [103, 1], [101, 0], [103, 0], [101, 0], [105, 1], [104, 1], [104, 1], [105, 1], [105, 1], [103, 0], [101, 0], [104, 1], [106, 1], [105, 1], [105, 0], [106, 1], [104, 1], [105, 1], [103, 1], [102, 1], [106, 0], [101, 0], [105, 1], [104, 1], [103, 1], [106, 1], [101, 0], [106, 1], [103, 0], [106, 1], [102, 1], [103, 0], [101, 1], [102, 1], [101, 1], [104, 0], [106, 0], [102, 0], [104, 0], [105, 0], [105, 0], [102, 1], [103, 1]]

47 unimportant_losses: [[105, 0], [103, 0], [103, 0], [105, 0], [104, 0], [103, 0], [102, 0], [104, 0], [105, 0], [104, 0], [104, 0], [105, 0], [103, 0], [104, 0], [106, 0], [103, 0], [102, 0], [106, 0], [106, 0], [103, 0], [101, 0], [105, 0], [105, 0], [106, 0], [104, 0], [105, 0], [105, 0], [103, 0], [104, 0], [105, 0], [101, 0], [103, 0], [101, 0], [103, 0], [101, 0], [105, 0], [106, 0], [101, 0], [101, 0], [103, 0], [103, 0], [104, 0], [106, 0], [102, 0], [104, 0], [105, 0], [105, 0]]

50 important_losses: [[101, 1], [101, 1], [101, 1], [101, 1], [101, 1], [101, 1], [101, 1], [102, 1], [102, 1], [102, 1], [102, 1], [102, 1], [102, 1], [103, 1], [103, 1], [103, 1], [103, 1], [103, 1], [103, 1], [103, 1], [104, 1], [104, 1], [104, 1], [104, 1], [104, 1], [104, 1], [104, 1], [104, 1], [104, 1], [104, 1], [105, 1], [105, 1], [105, 1], [105, 1], [105, 1], [105, 1], [105, 1], [105, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1]]
        top 50 important losses by luck: [[101, 1], [101, 1], [101, 1], [101, 1], [101, 1], [101, 1], [101, 1], [102, 1], [102, 1], [102, 1], [102, 1], [102, 1], [102, 1], [103, 1], [103, 1], [103, 1], [103, 1], [103, 1], [103, 1], [103, 1], [104, 1], [104, 1], [104, 1], [104, 1], [104, 1], [104, 1], [104, 1], [104, 1], [104, 1], [104, 1], [105, 1], [105, 1], [105, 1], [105, 1], [105, 1], [105, 1], [105, 1], [105, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1], [106, 1]]
        bottom 0 important losses by luck: []
max luck: max_luck_important_losses + unimportant_losses - min_luck_important_losses = 5192 + 4877 - 0 = 10069
result: 10069
expect: 10069
```

## POST-MORTEM:

See commentary above.