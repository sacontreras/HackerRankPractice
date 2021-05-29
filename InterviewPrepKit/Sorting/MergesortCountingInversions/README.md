[link](https://www.hackerrank.com/challenges/ctci-merge-sort/problem?h_l=interview&h_r=next-challenge&h_v=zen&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=sorting&h_r=next-challenge&h_v=zen)


## First Try:

This is based on a version of mergesort that I previously implemented in Java.  It has been modified to aditionally count inversions encountered during the sort.  The only catch here is, of course, properly understanding how to implement in-place mergesort.  The modification to count inversions is straightforward.  This implementation passed all three free test-cases.

However, upon submission, it failed test-cases 1, 4 through 9, and 11 through 13.

(see below)

```
def sort(ary, lb, mid, ub, debug_depth=-1):
    # pivot on left partition first
    i_inspect = lb
    i_right_partition = mid + 1 # note that i_right_partition will advance

    debug_header = None
    if debug_depth > -1:
        debug_header = f"depth {debug_depth}:"+"\t"*debug_depth
        print(f"{debug_header}lb={lb}, mid={mid}, ub={ub} --> left: {ary[lb:i_right_partition]}, right: {ary[i_right_partition:ub+1]}")

    inv_count = 0
    
    while i_inspect < mid+1:
        if debug_depth > -1:
            print(f"{debug_header}\t(left) ary[{i_inspect}]={ary[i_inspect]} > (right) ary[{i_right_partition}]={ary[i_right_partition]} ?", end=" ")
        if ary[i_inspect] > ary[i_right_partition]:	# then item in left partition is greater than item in right partition
            # there has been an inversion
            inv_count += 1
            if debug_depth > -1:
                print(f"True --> INVERTED, incremented inv_count to {inv_count}")

            # so swap the value we are inspecting in the left partition with value we are comparing it to in the right partition
            val_left_partition = ary[i_inspect]
            val_right_partition = ary[i_right_partition]
            ary[i_inspect] = val_right_partition
            ary[i_right_partition] = val_left_partition
            if debug_depth > -1:
                print(f"{debug_header}\t\tswapped (left) ary[{i_inspect}]={val_left_partition} <--> (right) ary[{i_right_partition}]={val_right_partition}")
                print(f"{debug_header}\t\t\tleft: {ary[lb:i_right_partition]}, right: {ary[i_right_partition:ub+1]}")

        else:	
            if debug_depth > -1:
                print(f"False --> NOT inverted")
        
        if i_right_partition < ub:
            i_right_partition += 1 # advance the right-comparison index to the next element
        else:   # then we have compared the pivot ("inspection") element in the left partition to every element in the right partition
            i_inspect += 1  # so we can now advance to the next pivot ("inspection") element in the left partition
            i_right_partition = mid + 1 # now we need to reset the right-position "pointer" back to the beginning (of the right partition)
        

    # now reconcile (sort) right partition
    i_inspect = mid + 1 # obviously we start inspection at first elt in right partition
    i_compare = mid + 2 # and we begin with the second element in the right partition (since it is pointless to compared the inspection element to itself)
    if debug_depth > -1:
        if i_inspect < ub: 
            print(f"{debug_header}\t(right) sort {ary[i_inspect:ub+1]}")
    while i_inspect < ub:
        if debug_depth > -1:
            print(f"{debug_header}\t\t(inspect) ary[{i_inspect}]={ary[i_inspect]} > (compare) ary[{i_compare}]={ary[i_compare]} ?", end=" ")
        if ary[i_inspect] > ary[i_compare]:
            inv_count += 1
            if debug_depth > -1:
                print(f"True --> INVERTED, incremented inv_count to {inv_count}")

            # so swap the value we are inspecting in the right partition with value we are comparing it to (also in the right partition)
            val_inspect = ary[i_inspect]
            val_compare = ary[i_compare]
            ary[i_inspect] = val_compare
            ary[i_compare] = val_inspect
            if debug_depth > -1:
                print(f"{debug_header}\t\t\tswapped ary[{i_inspect}]={val_inspect} <--> ary[{i_compare}]={val_compare}")
                print(f"{debug_header}\t\t\t\tright: {ary[i_right_partition:ub+1]}")

        else:
            if debug_depth > -1:
                print(f"False --> NOT inverted")	
            
        if i_compare < ub:
            i_compare += 1
        else:
            i_inspect += 1
            i_compare = i_inspect+1

    return inv_count
			
		
# merge_sort uses the concept known as Divide and Conquer
def merge_sort(ary, lb, ub, debug_depth=-1):
    # this is a recursive function, so we need a base case
    if lb == ub:	# then we have sub-divided ary until the point that the current sub-array contains only a single element
        return 0

    inv_count = 0
        
    # otherwise, sub-divide ary,	
    # e.g. {74, 4, -12, 8, 9, 7, 2, 0}		should produce the following logical subdivisions
    # 		  |				 |
    # {-74, 4, -12, 8}	{9, 7, 2, 0}
    # 	  |   	   |	  |		  |
    # {-74, 4} {-12, 8}	 {9, 7}   {2, 0}
    #   |    |   |    |   |   |    |  |
    # {-74} {4} {-12} {8} {9} {7} {2} {0}
    
    # first step is to find the index that will sub-divide ary into two logical partitions
    mid = (lb + ub) // 2	# note that since this is integer division, we will implicitly round down
    
    # now recursively partition ary into left and right sub-arrays
    # left partition will consist of elements from ary ranging from indexes lb to mid
    inv_count += merge_sort(ary, lb, mid, debug_depth)
    # right partition will consist of elements from ary ranging from indexes mid+1 to ub
    inv_count += merge_sort(ary, mid+1, ub, debug_depth)
    
    # now we need to sort/merge the left and right partitions
    inv_count += sort(ary, lb, mid, ub, debug_depth)

    return inv_count


def mergesort(ary, debug=False):
    return merge_sort(ary, 0, len(ary)-1, debug_depth=0 if debug else -1)

def countInversions(arr):
    debug = True

    if debug:
        print(f"arr: {arr}")
    n_inversions = mergesort.mergesort(arr, debug)
    if debug:
        print(f"arr (after mergesort): {arr}")
        print(f"mergesort swapped {n_inversions} (number of inversions)\n")

    return n_inversions
```

<p><br>

(Debug) Output for test-case 00:

```
testing against input file ./InterviewPrepKit/Sorting/MergesortCountingInversions/input00.txt...
arr: [1, 1, 1, 2, 2]
depth 0:lb=0, mid=0, ub=1 --> left: [1], right: [1]
depth 0:        (left) ary[0]=1 > (right) ary[1]=1 ? False --> NOT inverted
depth 0:lb=0, mid=1, ub=2 --> left: [1, 1], right: [1]
depth 0:        (left) ary[0]=1 > (right) ary[2]=1 ? False --> NOT inverted
depth 0:        (left) ary[1]=1 > (right) ary[2]=1 ? False --> NOT inverted
depth 0:lb=3, mid=3, ub=4 --> left: [2], right: [2]
depth 0:        (left) ary[3]=2 > (right) ary[4]=2 ? False --> NOT inverted
depth 0:lb=0, mid=2, ub=4 --> left: [1, 1, 1], right: [2, 2]
depth 0:        (left) ary[0]=1 > (right) ary[3]=2 ? False --> NOT inverted
depth 0:        (left) ary[0]=1 > (right) ary[4]=2 ? False --> NOT inverted
depth 0:        (left) ary[1]=1 > (right) ary[3]=2 ? False --> NOT inverted
depth 0:        (left) ary[1]=1 > (right) ary[4]=2 ? False --> NOT inverted
depth 0:        (left) ary[2]=1 > (right) ary[3]=2 ? False --> NOT inverted
depth 0:        (left) ary[2]=1 > (right) ary[4]=2 ? False --> NOT inverted
depth 0:        (right) sort [2, 2]
depth 0:                (inspect) ary[3]=2 > (compare) ary[4]=2 ? False --> NOT inverted
arr (after mergesort): [1, 1, 1, 2, 2]
mergesort swapped 0 (number of inversions)

arr: [2, 1, 3, 1, 2]
depth 0:lb=0, mid=0, ub=1 --> left: [2], right: [1]
depth 0:        (left) ary[0]=2 > (right) ary[1]=1 ? True --> INVERTED, incremented inv_count to 1
depth 0:                swapped (left) ary[0]=2 <--> (right) ary[1]=1
depth 0:                        left: [1], right: [2]
depth 0:lb=0, mid=1, ub=2 --> left: [1, 2], right: [3]
depth 0:        (left) ary[0]=1 > (right) ary[2]=3 ? False --> NOT inverted
depth 0:        (left) ary[1]=2 > (right) ary[2]=3 ? False --> NOT inverted
depth 0:lb=3, mid=3, ub=4 --> left: [1], right: [2]
depth 0:        (left) ary[3]=1 > (right) ary[4]=2 ? False --> NOT inverted
depth 0:lb=0, mid=2, ub=4 --> left: [1, 2, 3], right: [1, 2]
depth 0:        (left) ary[0]=1 > (right) ary[3]=1 ? False --> NOT inverted
depth 0:        (left) ary[0]=1 > (right) ary[4]=2 ? False --> NOT inverted
depth 0:        (left) ary[1]=2 > (right) ary[3]=1 ? True --> INVERTED, incremented inv_count to 1
depth 0:                swapped (left) ary[1]=2 <--> (right) ary[3]=1
depth 0:                        left: [1, 1, 3], right: [2, 2]
depth 0:        (left) ary[1]=1 > (right) ary[4]=2 ? False --> NOT inverted
depth 0:        (left) ary[2]=3 > (right) ary[3]=2 ? True --> INVERTED, incremented inv_count to 2
depth 0:                swapped (left) ary[2]=3 <--> (right) ary[3]=2
depth 0:                        left: [1, 1, 2], right: [3, 2]
depth 0:        (left) ary[2]=2 > (right) ary[4]=2 ? False --> NOT inverted
depth 0:        (right) sort [3, 2]
depth 0:                (inspect) ary[3]=3 > (compare) ary[4]=2 ? True --> INVERTED, incremented inv_count to 3
depth 0:                        swapped ary[3]=3 <--> ary[4]=2
depth 0:                                right: [2, 3]
arr (after mergesort): [1, 1, 2, 2, 3]
mergesort swapped 4 (number of inversions)

expect: 0
result: 0

expect: 4
result: 4
```

<p><br>

(Debug) Output for test-case 14:
```
testing against input file ./InterviewPrepKit/Sorting/MergesortCountingInversions/input14.txt...
arr: [1, 5, 3, 7]
depth 0:lb=0, mid=0, ub=1 --> left: [1], right: [5]
depth 0:        (left) ary[0]=1 > (right) ary[1]=5 ? False --> NOT inverted
depth 0:lb=2, mid=2, ub=3 --> left: [3], right: [7]
depth 0:        (left) ary[2]=3 > (right) ary[3]=7 ? False --> NOT inverted
depth 0:lb=0, mid=1, ub=3 --> left: [1, 5], right: [3, 7]
depth 0:        (left) ary[0]=1 > (right) ary[2]=3 ? False --> NOT inverted
depth 0:        (left) ary[0]=1 > (right) ary[3]=7 ? False --> NOT inverted
depth 0:        (left) ary[1]=5 > (right) ary[2]=3 ? True --> INVERTED, incremented inv_count to 1
depth 0:                swapped (left) ary[1]=5 <--> (right) ary[2]=3
depth 0:                        left: [1, 3], right: [5, 7]
depth 0:        (left) ary[1]=3 > (right) ary[3]=7 ? False --> NOT inverted
depth 0:        (right) sort [5, 7]
depth 0:                (inspect) ary[2]=5 > (compare) ary[3]=7 ? False --> NOT inverted
arr (after mergesort): [1, 3, 5, 7]
mergesort swapped 1 (number of inversions)

arr: [7, 5, 3, 1]
depth 0:lb=0, mid=0, ub=1 --> left: [7], right: [5]
depth 0:        (left) ary[0]=7 > (right) ary[1]=5 ? True --> INVERTED, incremented inv_count to 1
depth 0:                swapped (left) ary[0]=7 <--> (right) ary[1]=5
depth 0:                        left: [5], right: [7]
depth 0:lb=2, mid=2, ub=3 --> left: [3], right: [1]
depth 0:        (left) ary[2]=3 > (right) ary[3]=1 ? True --> INVERTED, incremented inv_count to 1
depth 0:                swapped (left) ary[2]=3 <--> (right) ary[3]=1
depth 0:                        left: [1], right: [3]
depth 0:lb=0, mid=1, ub=3 --> left: [5, 7], right: [1, 3]
depth 0:        (left) ary[0]=5 > (right) ary[2]=1 ? True --> INVERTED, incremented inv_count to 1
depth 0:                swapped (left) ary[0]=5 <--> (right) ary[2]=1
depth 0:                        left: [1, 7], right: [5, 3]
depth 0:        (left) ary[0]=1 > (right) ary[3]=3 ? False --> NOT inverted
depth 0:        (left) ary[1]=7 > (right) ary[2]=5 ? True --> INVERTED, incremented inv_count to 2
depth 0:                swapped (left) ary[1]=7 <--> (right) ary[2]=5
depth 0:                        left: [1, 5], right: [7, 3]
depth 0:        (left) ary[1]=5 > (right) ary[3]=3 ? True --> INVERTED, incremented inv_count to 3
depth 0:                swapped (left) ary[1]=5 <--> (right) ary[3]=3
depth 0:                        left: [1, 3, 7], right: [5]
depth 0:        (right) sort [7, 5]
depth 0:                (inspect) ary[2]=7 > (compare) ary[3]=5 ? True --> INVERTED, incremented inv_count to 4
depth 0:                        swapped ary[2]=7 <--> ary[3]=5
depth 0:                                right: [5, 7]
arr (after mergesort): [1, 3, 5, 7]
mergesort swapped 6 (number of inversions)

expect: 1
result: 1

expect: 6
result: 6
```

<p><br>

(Debug) Output for test-case 15:

```
testing against input file ./InterviewPrepKit/Sorting/MergesortCountingInversions/input15.txt...
arr: [1, 3, 5, 7]
depth 0:lb=0, mid=0, ub=1 --> left: [1], right: [3]
depth 0:        (left) ary[0]=1 > (right) ary[1]=3 ? False --> NOT inverted
depth 0:lb=2, mid=2, ub=3 --> left: [5], right: [7]
depth 0:        (left) ary[2]=5 > (right) ary[3]=7 ? False --> NOT inverted
depth 0:lb=0, mid=1, ub=3 --> left: [1, 3], right: [5, 7]
depth 0:        (left) ary[0]=1 > (right) ary[2]=5 ? False --> NOT inverted
depth 0:        (left) ary[0]=1 > (right) ary[3]=7 ? False --> NOT inverted
depth 0:        (left) ary[1]=3 > (right) ary[2]=5 ? False --> NOT inverted
depth 0:        (left) ary[1]=3 > (right) ary[3]=7 ? False --> NOT inverted
depth 0:        (right) sort [5, 7]
depth 0:                (inspect) ary[2]=5 > (compare) ary[3]=7 ? False --> NOT inverted
arr (after mergesort): [1, 3, 5, 7]
mergesort swapped 0 (number of inversions)

arr: [3, 2, 1]
depth 0:lb=0, mid=0, ub=1 --> left: [3], right: [2]
depth 0:        (left) ary[0]=3 > (right) ary[1]=2 ? True --> INVERTED, incremented inv_count to 1
depth 0:                swapped (left) ary[0]=3 <--> (right) ary[1]=2
depth 0:                        left: [2], right: [3]
depth 0:lb=0, mid=1, ub=2 --> left: [2, 3], right: [1]
depth 0:        (left) ary[0]=2 > (right) ary[2]=1 ? True --> INVERTED, incremented inv_count to 1
depth 0:                swapped (left) ary[0]=2 <--> (right) ary[2]=1
depth 0:                        left: [1, 3], right: [2]
depth 0:        (left) ary[1]=3 > (right) ary[2]=2 ? True --> INVERTED, incremented inv_count to 2
depth 0:                swapped (left) ary[1]=3 <--> (right) ary[2]=2
depth 0:                        left: [1, 2], right: [3]
arr (after mergesort): [1, 2, 3]
mergesort swapped 3 (number of inversions)

expect: 0
result: 0

expect: 3
result: 3
```


## Second Try:
It turns out my in-place solution DOES sort the array correctly.  But the implementation is not entirely mergesort, according to tradition theory.  In particular, after the block that swaps inverted elements from the left and right partitions completes, the block that sorts the right partition is inefficient.  It turns out that the implementation for that block is standard bubble sort... VERY INEFFICIENT.  As a sidenote, in the future, I will update that part of the implementation to use a more effcient sorting algorithm.

The moral of the story here is that I had to use standard (new array) mergesort (instead of the above in-place approach).  This resulted in ALL test-cases passing.

(see below)

```
def merge(arr_left, arr_right):
    n_inversions = 0

    n_left = len(arr_left)
    i_left = 0

    n_right = len(arr_right)
    i_right = 0

    arr_merged = []
    
    while i_left < n_left and i_right < n_right:
        if arr_left[i_left] <= arr_right[i_right]:
            arr_merged.append(arr_left[i_left])
            i_left += 1

        else:
            arr_merged.append(arr_right[i_right])
            i_right += 1
            n_inversions += n_left - i_left

    arr_merged += arr_left[i_left:n_left]
    arr_merged += arr_right[i_right:n_right]

    return n_inversions, arr_merged

def mergesort(arr):
    n = len(arr)

    if n > 1:
        mid = n // 2

        n_inversions_left, arr_left = mergesort(arr[:mid])
        n_inversions_right, arr_right = mergesort(arr[mid:])
        n_inversions_merged, arr_merged = merge(arr_left, arr_right)

        n_inversions = n_inversions_left + n_inversions_right + n_inversions_merged

        return n_inversions, arr_merged

    else:
        return 0, arr

def countInversions(arr, debug=False):
    if debug:
        print(f"arr: {arr}")
    n_inversions = mergesort.mergesort(arr)[0]
    if debug:
        print(f"arr (after mergesort): {arr}")
        print(f"mergesort swapped {n_inversions} (number of inversions)\n")

    return n_inversions
```

## POST-MORTEM:

See "Second Try" commentary.