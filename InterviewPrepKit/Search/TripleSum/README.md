[link](https://www.hackerrank.com/challenges/triple-sum/problem?h_l=interview&h_r=next-challenge&h_v=zen&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D=search)


## First Try:

The puzzle itself is straightforward.  It consists of finding the cartesion product of $P \times Q \times R$ where $p \in P, q \in Q, r \in R: p, r \le q$.

The algorithm below does this.  It passed all free test-cases.  However, it failed locked test-case 02 due to timeout.  Upon running this against test-case 02, my algorithm produces the correct result (count) but, indeed, it does take a long time to run.

(see below for my full implementation of this algorithm)

```python
import itertools
def triplets_v1(a, b, c, debug=False):
    """
    Finds all (p, q, r) such that p <= q, q >= r where p is in a, q is in b, and r is in c
    """

    srtd_unq_a = sorted(set(a))
    srtd_unq_b = sorted(set(b))
    srtd_unq_c = sorted(set(c))

    n_a = len(srtd_unq_a)
    n_b = len(srtd_unq_b)
    n_c = len(srtd_unq_c)

    if debug:
        print(f"a: {a}, b: {b}, c: {c}\n\t--> a_sorted: {srtd_unq_a}, b_sorted: {srtd_unq_b}, c_sorted: {srtd_unq_c}")

    n_solutions = 0
    solutions = []

    j = 0
    while j < n_b:
        q_set = set()
        q = srtd_unq_b[j]

        p_sols = []
        i = 0
        while True:
            if i >= n_a:
                break

            p = srtd_unq_a[i]
            if p > q:
                break

            if debug:
                q_set.add(q)
                p_sols.append(p)

            i += 1


        r_sols = []
        k = 0
        while True:
            if k >= n_c:
                break

            r = srtd_unq_c[k]
            if r > q:
                break

            if debug:
                q_set.add(q)
                r_sols.append(r)

            k += 1

        n_size_cartesian_prod = i * k
        if debug and len(p_sols) > 0 and len(r_sols) > 0: # then we want the cartesian product
            cart_prod = list(itertools.product(p_sols,list(q_set),r_sols))
            assert(n_size_cartesian_prod == len(cart_prod))
            solutions.extend(cart_prod)

        n_solutions += n_size_cartesian_prod

        j += 1

    if debug:
        print(f"SOLUTIONS: {solutions}\n")
    
    return n_solutions
```

<p><br>

(Debug) Output for test-case 00:

```
a: [1, 3, 5], b: [2, 3], c: [1, 2, 3]
        --> a_sorted: [1, 3, 5], b_sorted: [2, 3], c_sorted: [1, 2, 3]
SOLUTIONS: [(1, 2, 1), (1, 2, 2), (1, 3, 1), (1, 3, 2), (1, 3, 3), (3, 3, 1), (3, 3, 2), (3, 3, 3)]

result: 8
expect: 8
        --> PASS
```

<p><br>

(Debug) Output for test-case 01:

```
a: [1, 4, 5], b: [2, 3, 3], c: [1, 2, 3]
        --> a_sorted: [1, 4, 5], b_sorted: [2, 3], c_sorted: [1, 2, 3]
SOLUTIONS: [(1, 2, 1), (1, 2, 2), (1, 3, 1), (1, 3, 2), (1, 3, 3)]

result: 5
expect: 5
        --> PASS
```

<p><br>

(Debug) Output for test-case 09:

```
a: [1, 3, 5, 7], b: [5, 7, 9], c: [7, 9, 11, 13]
        --> a_sorted: [1, 3, 5, 7], b_sorted: [5, 7, 9], c_sorted: [7, 9, 11, 13]
SOLUTIONS: [(1, 7, 7), (3, 7, 7), (5, 7, 7), (7, 7, 7), (1, 9, 7), (1, 9, 9), (3, 9, 7), (3, 9, 9), (5, 9, 7), (5, 9, 9), (7, 9, 7), (7, 9, 9)]

result: 12
expect: 12
        --> PASS
```

## Second Try:

I updated the algorithm to focus on counting only, without actually *finding* the tuples.  It is based on the same idea and the algo required only slight modification but, by doing so, I have improved (decreased) complexity significantly.

The modified version below passed all free test-cases, as well as the previously failing test-case 02.  Upon submission, it passed all remaining locked test-cases.

(see below for my full implementation of this algorithm)

```python
def triplets(a, b, c, debug=False):
    """
    Counts all (p, q, r) such that p <= q, q >= r where p is in a, q is in b, and r is in c
    """

    srtd_unq_a = sorted(set(a))
    srtd_unq_b = sorted(set(b))
    srtd_unq_c = sorted(set(c))

    if debug:
        print(f"a: {a}, b: {b}, c: {c}\n\t--> a_sorted: {srtd_unq_a}, b_sorted: {srtd_unq_b}, c_sorted: {srtd_unq_c}")

    n_a = len(srtd_unq_a)
    n_b = len(srtd_unq_b)
    n_c = len(srtd_unq_c)

    n_solutions = 0

    i = k = j = 0
    while j < n_b:
        q = srtd_unq_b[j]

        while True:
            if i >= n_a:
                break
            p = srtd_unq_a[i]
            if p > q:
                break
            if debug:
                print(f"FOUND p=a[i={i}]={p} <= q=b[j={j}]={q}")
            i += 1
        if debug:
            print(f"there are {i} total p in a such that p <= q")


        while True:
            if k >= n_c:
                break
            r = srtd_unq_c[k]
            if r > q:
                break
            if debug:
                print(f"FOUND r=c[k={k}]={r} <= q=b[j={j}]={q}")
            k += 1
        if debug:
            print(f"there are {k} total r in c such that r <= q")

        n_cart_prod = i * k
        if debug:
            print(f"there are {n_cart_prod} total (p,q={q},r) in the cartesian product such that p, r <= q\n")
        n_solutions += n_cart_prod

        j += 1
    
    return n_solutions
```

## POST-MORTEM:

I think the big moral of the story here is to find the most direct path to solving the puzzle and not doing anything extra (which may very increase complexity).  Follow directions!
