[link](https://www.hackerrank.com/challenges/greedy-florist/problem?h_l=interview&h_r%5B%5D=next-challenge&h_r%5B%5D=next-challenge&h_v%5B%5D=zen&h_v%5B%5D=zen&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D=greedy-algorithms)


## First Try:

The most difficult aspect of this puzzle is understanding the puzzle itself and its requirements.  First, from the top, this is a problem of optimization.  Here, we don't mean optimization in the sense of optimizing the runtime complexity of the algorithm.  Instead, "optimization" here literally means that this algorithm should be written such that the cost to each of the $k$ people purchasing flowers should be minimized, and we see that in the wording of the puzzle itself: "determine the minimum cost to purchase all of the flowers".  Therefore, in order to minimize cost to each person, we must apply the least "multipliers" to the greatest costs.  So, we obviously must sort the cost list in descending order.  From there, we assign costs to each person in a "daisy-chain" fashion, which implies assignment by the index of the flower mod $k$.

The algorithm below passed all of the free test-cases and upon submissions passed all of the remaining locked test-cases.

(see below)

```python
def getMinimumCost(k, c, debug=False):
    if debug:
        print(f"k: {k}, c: {c}")

    min_cost = 0

    n = len(c)

    if n == k:
        if debug:
            print(f"n == k: {n} == {k} --> final cost list is the original {c}")
        min_cost = sum(c)

    else:
        c_descending = sorted(c, reverse=True)

        cost_lists = [[] for i in range(k)]

        for i, c in enumerate(c_descending):
            i_person = i % k
            cost_list = cost_lists[i_person]
            cost = (len(cost_list)+1) * c
            if debug:
                print(f"for person {i_person}, flower {i} costs {c} --> adjusted flower cost is: ({len(cost_list)}+1)*{c}={cost}")
            cost_list.append(cost)
            if debug:
                print(f"\t--> person {i_person} cost list is now: {cost_list}")
        if debug:
            print(f"\nfinal cost lists: {cost_lists}")

        for cost_list in cost_lists:
            min_cost += sum(cost_list)

    return min_cost
```

<p><br>

(Debug) Output for test-case 00:

```
k: 3, c: [2, 5, 6]
n == k: 3 == 3 --> final cost list is the original [2, 5, 6]
result: 13
expect: 13
```

<p><br>

(Debug) Output for test-case 10:

```
k: 2, c: [2, 5, 6]
for person 0, flower 0 costs 6 --> adjusted flower cost is: (0+1)*6=6
        --> person 0 cost list is now: [6]
for person 1, flower 1 costs 5 --> adjusted flower cost is: (0+1)*5=5
        --> person 1 cost list is now: [5]
for person 0, flower 2 costs 2 --> adjusted flower cost is: (1+1)*2=4
        --> person 0 cost list is now: [6, 4]

final cost lists: [[6, 4], [5]]
result: 15
expect: 15
```

<p><br>

(Debug) Output for test-case 11:

```
k: 3, c: [1, 3, 5, 7, 9]
for person 0, flower 0 costs 9 --> adjusted flower cost is: (0+1)*9=9
        --> person 0 cost list is now: [9]
for person 1, flower 1 costs 7 --> adjusted flower cost is: (0+1)*7=7
        --> person 1 cost list is now: [7]
for person 2, flower 2 costs 5 --> adjusted flower cost is: (0+1)*5=5
        --> person 2 cost list is now: [5]
for person 0, flower 3 costs 3 --> adjusted flower cost is: (1+1)*3=6
        --> person 0 cost list is now: [9, 6]
for person 1, flower 4 costs 1 --> adjusted flower cost is: (1+1)*1=2
        --> person 1 cost list is now: [7, 2]

final cost lists: [[9, 6], [7, 2], [5]]
result: 29
expect: 29
```

## POST-MORTEM:

See commentary above.