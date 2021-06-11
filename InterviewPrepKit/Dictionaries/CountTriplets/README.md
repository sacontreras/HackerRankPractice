[link](https://www.hackerrank.com/challenges/count-triplets-1/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=dictionaries-hashmaps)


## First Try:

Mathematically speaking, this puzzle is straightforward.  Algorithmically speaking, the approach is not too difficult.  I inspected the free test-cases to arrive at the following implementation.  All three free test-cases passed successfully.

HOWEVER, this has woeful O(n^3) complexity and does not match the spec entirely, failing test-case 02 outright and timing out on test-cases 3 through 11. 

(see below)

```python
def countTriplets(arr, r):
    debug = True

    if debug:
        print(f"arr: {arr}, r: {r}")

    n_geom_series = 0

    lst_series = []

    l_arr = len(arr)

    for ub in range(l_arr-1,-1,-1):
        
        for lb in range(ub,-1,-1):
            i_start = None
            series = arr[lb:ub+1]

            if len(series) > 1:
                if debug:
                    print(f"inspecting series: {series}")

                for i in range(ub,lb,-1):
                    a_i = arr[i]
                    a_i_minus_1 = arr[i-1]
                    is_ratio = a_i//a_i_minus_1 == r
                    if debug:
                        print(f"inspect elements at i,i-1: {i},{i-1} --> ({a_i}/{a_i_minus_1})=={r} ? {is_ratio}")
                    if not is_ratio:
                        break
                    i_start = i
                
                if i_start is not None and i_start-1 == lb:
                    geom_series = series
                    lst_series.append(geom_series)
                    if debug:
                        print(f"{geom_series} is geometric with ratio {r}")
                    n_geom_series += 1
                else:
                    if debug:
                        print(f"{series} is not geometric")

                if debug:
                    print()

    return n_geom_series
```

<p><br>

Output for test-case 00:
```
testing against input file ./InterviewPrepKit/Dictionaries/CountTriplets/input00.txt...
arr: [1, 2, 2, 4], r: 2
inspecting series: [2, 4]
inspect elements at i,i-1: 3,2 --> (4/2)==2 ? True
[2, 4] is geometric with ratio 2

inspecting series: [2, 2, 4]
inspect elements at i,i-1: 3,2 --> (4/2)==2 ? True
inspect elements at i,i-1: 2,1 --> (2/2)==2 ? False
[2, 2, 4] is not geometric

inspecting series: [1, 2, 2, 4]
inspect elements at i,i-1: 3,2 --> (4/2)==2 ? True
inspect elements at i,i-1: 2,1 --> (2/2)==2 ? False
[1, 2, 2, 4] is not geometric

inspecting series: [2, 2]
inspect elements at i,i-1: 2,1 --> (2/2)==2 ? False
[2, 2] is not geometric

inspecting series: [1, 2, 2]
inspect elements at i,i-1: 2,1 --> (2/2)==2 ? False
[1, 2, 2] is not geometric

inspecting series: [1, 2]
inspect elements at i,i-1: 1,0 --> (2/1)==2 ? True
[1, 2] is geometric with ratio 2

result: 2
expect: 2
```

<p><br>

Output for test-case 01:
```
testing against input file ./InterviewPrepKit/Dictionaries/CountTriplets/input01.txt...
arr: [1, 3, 9, 9, 27, 81], r: 3
inspecting series: [27, 81]
inspect elements at i,i-1: 5,4 --> (81/27)==3 ? True
[27, 81] is geometric with ratio 3

inspecting series: [9, 27, 81]
inspect elements at i,i-1: 5,4 --> (81/27)==3 ? True
inspect elements at i,i-1: 4,3 --> (27/9)==3 ? True
[9, 27, 81] is geometric with ratio 3

inspecting series: [9, 9, 27, 81]
inspect elements at i,i-1: 5,4 --> (81/27)==3 ? True
inspect elements at i,i-1: 4,3 --> (27/9)==3 ? True
inspect elements at i,i-1: 3,2 --> (9/9)==3 ? False
[9, 9, 27, 81] is not geometric

inspecting series: [3, 9, 9, 27, 81]
inspect elements at i,i-1: 5,4 --> (81/27)==3 ? True
inspect elements at i,i-1: 4,3 --> (27/9)==3 ? True
inspect elements at i,i-1: 3,2 --> (9/9)==3 ? False
[3, 9, 9, 27, 81] is not geometric

inspecting series: [1, 3, 9, 9, 27, 81]
inspect elements at i,i-1: 5,4 --> (81/27)==3 ? True
inspect elements at i,i-1: 4,3 --> (27/9)==3 ? True
inspect elements at i,i-1: 3,2 --> (9/9)==3 ? False
[1, 3, 9, 9, 27, 81] is not geometric

inspecting series: [9, 27]
inspect elements at i,i-1: 4,3 --> (27/9)==3 ? True
[9, 27] is geometric with ratio 3

inspecting series: [9, 9, 27]
inspect elements at i,i-1: 4,3 --> (27/9)==3 ? True
inspect elements at i,i-1: 3,2 --> (9/9)==3 ? False
[9, 9, 27] is not geometric

inspecting series: [3, 9, 9, 27]
inspect elements at i,i-1: 4,3 --> (27/9)==3 ? True
inspect elements at i,i-1: 3,2 --> (9/9)==3 ? False
[3, 9, 9, 27] is not geometric

inspecting series: [1, 3, 9, 9, 27]
inspect elements at i,i-1: 4,3 --> (27/9)==3 ? True
inspect elements at i,i-1: 3,2 --> (9/9)==3 ? False
[1, 3, 9, 9, 27] is not geometric

inspecting series: [9, 9]
inspect elements at i,i-1: 3,2 --> (9/9)==3 ? False
[9, 9] is not geometric

inspecting series: [3, 9, 9]
inspect elements at i,i-1: 3,2 --> (9/9)==3 ? False
[3, 9, 9] is not geometric

inspecting series: [1, 3, 9, 9]
inspect elements at i,i-1: 3,2 --> (9/9)==3 ? False
[1, 3, 9, 9] is not geometric

inspecting series: [3, 9]
inspect elements at i,i-1: 2,1 --> (9/3)==3 ? True
[3, 9] is geometric with ratio 3

inspecting series: [1, 3, 9]
inspect elements at i,i-1: 2,1 --> (9/3)==3 ? True
inspect elements at i,i-1: 1,0 --> (3/1)==3 ? True
[1, 3, 9] is geometric with ratio 3

inspecting series: [1, 3]
inspect elements at i,i-1: 1,0 --> (3/1)==3 ? True
[1, 3] is geometric with ratio 3

result: 6
expect: 6
```

<p><br>

Output for test-case 12:
```
testing against input file ./InterviewPrepKit/Dictionaries/CountTriplets/input12.txt...
arr: [1, 5, 5, 25, 125], r: 5
inspecting series: [25, 125]
inspect elements at i,i-1: 4,3 --> (125/25)==5 ? True
[25, 125] is geometric with ratio 5

inspecting series: [5, 25, 125]
inspect elements at i,i-1: 4,3 --> (125/25)==5 ? True
inspect elements at i,i-1: 3,2 --> (25/5)==5 ? True
[5, 25, 125] is geometric with ratio 5

inspecting series: [5, 5, 25, 125]
inspect elements at i,i-1: 4,3 --> (125/25)==5 ? True
inspect elements at i,i-1: 3,2 --> (25/5)==5 ? True
inspect elements at i,i-1: 2,1 --> (5/5)==5 ? False
[5, 5, 25, 125] is not geometric

inspecting series: [1, 5, 5, 25, 125]
inspect elements at i,i-1: 4,3 --> (125/25)==5 ? True
inspect elements at i,i-1: 3,2 --> (25/5)==5 ? True
inspect elements at i,i-1: 2,1 --> (5/5)==5 ? False
[1, 5, 5, 25, 125] is not geometric

inspecting series: [5, 25]
inspect elements at i,i-1: 3,2 --> (25/5)==5 ? True
[5, 25] is geometric with ratio 5

inspecting series: [5, 5, 25]
inspect elements at i,i-1: 3,2 --> (25/5)==5 ? True
inspect elements at i,i-1: 2,1 --> (5/5)==5 ? False
[5, 5, 25] is not geometric

inspecting series: [1, 5, 5, 25]
inspect elements at i,i-1: 3,2 --> (25/5)==5 ? True
inspect elements at i,i-1: 2,1 --> (5/5)==5 ? False
[1, 5, 5, 25] is not geometric

inspecting series: [5, 5]
inspect elements at i,i-1: 2,1 --> (5/5)==5 ? False
[5, 5] is not geometric

inspecting series: [1, 5, 5]
inspect elements at i,i-1: 2,1 --> (5/5)==5 ? False
[1, 5, 5] is not geometric

inspecting series: [1, 5]
inspect elements at i,i-1: 1,0 --> (5/1)==5 ? True
[1, 5] is geometric with ratio 5

result: 4
expect: 4
```

## Second Try:

First thing to note here is that I did not use the HUGE tell right from the get-go!  This puzzle in the "Dictionaries" section, yet I did not use any dictionaries in my first implementation!  Obviously, I will want to use dictionaries in order to leverage O(1) lookup.

Additionally, admittedly, I unlocked the "Editorial".  (see below)

```python
def countTriplets(arr, r):
    debug = True

    if debug:
        print(f"arr: {arr}, r: {r}")

    n_geom_series = 0

    # store the frequency of all the elements
    d_right = {}
    for a_j in arr:
        d_right[a_j] = d_right.get(a_j,0) + 1

    if debug:
        print(f"right map: {d_right}")

    d_left = {}

    # traverse the array elements from left side
    for a_j in arr:
        a_i = a_j / r
        a_k = a_j * r
        
        # first decrement it's count from d_right by 1
        d_right[a_j] -= 1

        # check the count of a_k in d_right
        n_a_k = d_right.get(a_k,0)

        # check the count of a_i in d_left
        n_a_i = d_left.get(a_i,0)

        # increment n_geom_series by product of the above
        n_geom_series += n_a_k * n_a_i

        # increment could of a_j in d_left by 1
        d_left[a_j] = d_left.get(a_j,0) + 1

        """
        intuition:
            d_left holds elements with indices < j
            d_right holds elements with indices > j
        """

    if debug:
        print(f"left map: {d_left}")
        print(f"right map: {d_right}")

    return n_geom_series
```


## POST-MORTEM:

The First Try was good to get a feel for the math.  But it had horrible complexity.  Complexity >= O(n^2) is almost always the wrong answer!  Also, when math is involved, understand it intimately!