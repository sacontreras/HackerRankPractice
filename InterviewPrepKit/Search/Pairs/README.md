[link](https://www.hackerrank.com/challenges/pairs/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=search)


## First Try:

This puzzle was very straightforward, even easy.  The trick, of course, is to solve it with optimal complexity.  Iterating over two indices with a loop within a loop is sub-optimal.  Therefore, the scheme upfront is to first sort the array in non-decreasing order.  We can then iterate over two indices using a single loop.  

The logic goes like this.  Set $j=1$ and $i=0$ initially, where $0 \le i \le j < n$.  At each iteration, consider $\Delta = a_j - a_i$.  If $\Delta == k$ we have found a solution: move to the next $j = j + 1$.  If $\Delta > k$, we need to decrease $\Delta$ by moving to the next $i = i + 1$.  If $\Delta < k$, we need to increase $\Delta$ by moving to the next $j = j + 1$.

In the end, we simply tally the number of solutions for our result.

The algorithm below passed all free test-cases and upon submission passed all remaining locked test-cases.


(see below for my full implementation of this algorithm)

```
def pairs(k, arr, debug=False):
    n = len(arr)

    arr_sorted = sorted(arr)    # non-decreasing order
    if debug:
        print(f"k: {k}, arr: {arr}\n\t--> arr_sorted: {arr_sorted}")

    solutions = []
    j, i = 1, 0     # the idea here is to keep j >= i
    while j < n:
        a_j = arr_sorted[j]
        a_i = arr_sorted[i]
        d = a_j - a_i

        if debug:
            print(f"a_[j=={j}] - a[i=={i}] == {a_j} - {a_i} = {d} == k (=={k}) ? {d == k}")

        if d == k:
            sol = (j,i)
            solutions.append(sol)
            j += 1
            if debug:
                print(f"\tFOUND A SOLUTION! Incremented j to {j}")

        elif d > k:
            i += 1
            if debug:
                print(f"\td=={d} > k=={k} --> not a solution, DECREASING difference by incrementing i to {i}")

        elif d < k:
            j += 1
            if debug:
                print(f"\td=={d} < k=={k} --> not a solution, INCREASING difference by incrementing j to {j}")
    if debug:
        print(f"SOLUTION indices: {solutions}")
    
    return len(solutions)
```

<p><br>

(Debug) Output for test-case 15:

```
k: 2, arr: [1, 5, 3, 4, 2]
        --> arr_sorted: [1, 2, 3, 4, 5]
a_[j==1] - a[i==0] == 2 - 1 = 1 == k (==2) ? False
        d==1 < k==2 --> not a solution, INCREASING difference by incrementing j to 2
a_[j==2] - a[i==0] == 3 - 1 = 2 == k (==2) ? True
        FOUND A SOLUTION! Incremented j to 3
a_[j==3] - a[i==0] == 4 - 1 = 3 == k (==2) ? False
        d==3 > k==2 --> not a solution, DECREASING difference by incrementing i to 1
a_[j==3] - a[i==1] == 4 - 2 = 2 == k (==2) ? True
        FOUND A SOLUTION! Incremented j to 4
a_[j==4] - a[i==1] == 5 - 2 = 3 == k (==2) ? False
        d==3 > k==2 --> not a solution, DECREASING difference by incrementing i to 2
a_[j==4] - a[i==2] == 5 - 3 = 2 == k (==2) ? True
        FOUND A SOLUTION! Incremented j to 5
SOLUTION indices: [(2, 0), (3, 1), (4, 2)]
result: 3
expect: 3
```

<p><br>

(Debug) Output for test-case 16:

```
k: 1, arr: [363374326, 364147530, 61825163, 1073065718, 1281246024, 1399469912, 428047635, 491595254, 879792181, 1069262793]
        --> arr_sorted: [61825163, 363374326, 364147530, 428047635, 491595254, 879792181, 1069262793, 1073065718, 1281246024, 1399469912]
a_[j==1] - a[i==0] == 363374326 - 61825163 = 301549163 == k (==1) ? False
        d==301549163 > k==1 --> not a solution, DECREASING difference by incrementing i to 1
a_[j==1] - a[i==1] == 363374326 - 363374326 = 0 == k (==1) ? False
        d==0 < k==1 --> not a solution, INCREASING difference by incrementing j to 2
a_[j==2] - a[i==1] == 364147530 - 363374326 = 773204 == k (==1) ? False
        d==773204 > k==1 --> not a solution, DECREASING difference by incrementing i to 2
a_[j==2] - a[i==2] == 364147530 - 364147530 = 0 == k (==1) ? False
        d==0 < k==1 --> not a solution, INCREASING difference by incrementing j to 3
a_[j==3] - a[i==2] == 428047635 - 364147530 = 63900105 == k (==1) ? False
        d==63900105 > k==1 --> not a solution, DECREASING difference by incrementing i to 3
a_[j==3] - a[i==3] == 428047635 - 428047635 = 0 == k (==1) ? False
        d==0 < k==1 --> not a solution, INCREASING difference by incrementing j to 4
a_[j==4] - a[i==3] == 491595254 - 428047635 = 63547619 == k (==1) ? False
        d==63547619 > k==1 --> not a solution, DECREASING difference by incrementing i to 4
a_[j==4] - a[i==4] == 491595254 - 491595254 = 0 == k (==1) ? False
        d==0 < k==1 --> not a solution, INCREASING difference by incrementing j to 5
a_[j==5] - a[i==4] == 879792181 - 491595254 = 388196927 == k (==1) ? False
        d==388196927 > k==1 --> not a solution, DECREASING difference by incrementing i to 5
a_[j==5] - a[i==5] == 879792181 - 879792181 = 0 == k (==1) ? False
        d==0 < k==1 --> not a solution, INCREASING difference by incrementing j to 6
a_[j==6] - a[i==5] == 1069262793 - 879792181 = 189470612 == k (==1) ? False
        d==189470612 > k==1 --> not a solution, DECREASING difference by incrementing i to 6
a_[j==6] - a[i==6] == 1069262793 - 1069262793 = 0 == k (==1) ? False
        d==0 < k==1 --> not a solution, INCREASING difference by incrementing j to 7
a_[j==7] - a[i==6] == 1073065718 - 1069262793 = 3802925 == k (==1) ? False
        d==3802925 > k==1 --> not a solution, DECREASING difference by incrementing i to 7
a_[j==7] - a[i==7] == 1073065718 - 1073065718 = 0 == k (==1) ? False
        d==0 < k==1 --> not a solution, INCREASING difference by incrementing j to 8
a_[j==8] - a[i==7] == 1281246024 - 1073065718 = 208180306 == k (==1) ? False
        d==208180306 > k==1 --> not a solution, DECREASING difference by incrementing i to 8
a_[j==8] - a[i==8] == 1281246024 - 1281246024 = 0 == k (==1) ? False
        d==0 < k==1 --> not a solution, INCREASING difference by incrementing j to 9
a_[j==9] - a[i==8] == 1399469912 - 1281246024 = 118223888 == k (==1) ? False
        d==118223888 > k==1 --> not a solution, DECREASING difference by incrementing i to 9
a_[j==9] - a[i==9] == 1399469912 - 1399469912 = 0 == k (==1) ? False
        d==0 < k==1 --> not a solution, INCREASING difference by incrementing j to 10
SOLUTION indices: []
result: 0
expect: 0
```

<p><br>

(Debug) Output for test-case 17:

```
k: 2, arr: [1, 3, 5, 8, 6, 4, 2]
        --> arr_sorted: [1, 2, 3, 4, 5, 6, 8]
a_[j==1] - a[i==0] == 2 - 1 = 1 == k (==2) ? False
        d==1 < k==2 --> not a solution, INCREASING difference by incrementing j to 2
a_[j==2] - a[i==0] == 3 - 1 = 2 == k (==2) ? True
        FOUND A SOLUTION! Incremented j to 3
a_[j==3] - a[i==0] == 4 - 1 = 3 == k (==2) ? False
        d==3 > k==2 --> not a solution, DECREASING difference by incrementing i to 1
a_[j==3] - a[i==1] == 4 - 2 = 2 == k (==2) ? True
        FOUND A SOLUTION! Incremented j to 4
a_[j==4] - a[i==1] == 5 - 2 = 3 == k (==2) ? False
        d==3 > k==2 --> not a solution, DECREASING difference by incrementing i to 2
a_[j==4] - a[i==2] == 5 - 3 = 2 == k (==2) ? True
        FOUND A SOLUTION! Incremented j to 5
a_[j==5] - a[i==2] == 6 - 3 = 3 == k (==2) ? False
        d==3 > k==2 --> not a solution, DECREASING difference by incrementing i to 3
a_[j==5] - a[i==3] == 6 - 4 = 2 == k (==2) ? True
        FOUND A SOLUTION! Incremented j to 6
a_[j==6] - a[i==3] == 8 - 4 = 4 == k (==2) ? False
        d==4 > k==2 --> not a solution, DECREASING difference by incrementing i to 4
a_[j==6] - a[i==4] == 8 - 5 = 3 == k (==2) ? False
        d==3 > k==2 --> not a solution, DECREASING difference by incrementing i to 5
a_[j==6] - a[i==5] == 8 - 6 = 2 == k (==2) ? True
        FOUND A SOLUTION! Incremented j to 7
SOLUTION indices: [(2, 0), (3, 1), (4, 2), (5, 3), (6, 5)]
result: 5
expect: 5
```

## POST-MORTEM:

See commentary above.
