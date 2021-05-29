
# ******************** IN-PLACE: begin ********************
def merge_inplace(ary, lb, mid, ub, debug_depth=-1):
    # pivot on left partition first
    i_inspect = lb
    i_right_partition = mid + 1 # note that i_right_partition will advance

    debug_header = None
    if debug_depth > -1:
        debug_header = f"depth {debug_depth}:"  #+"\t"*debug_depth
        print(f"{debug_header}lb={lb}, mid={mid}, ub={ub} --> left: {ary[lb:mid+1]}, right: {ary[mid+1:ub+1]}")

    inv_count = 0
    
    while i_inspect < mid+1:
        val_inspect = ary[i_inspect]
        val_compare = ary[i_right_partition]

        if debug_depth > -1:
            print(f"{debug_header}\t(left) ary[{i_inspect}]={val_inspect} > (right) ary[{i_right_partition}]={val_compare} ?", end=" ")
        if val_inspect > val_compare:	# then item in left partition is greater than item in right partition
            # there has been an inversion
            inv_count += 1 # mid-i_inspect # 1
            if debug_depth > -1:
                print(f"True --> INVERTED, incremented inv_count to {inv_count}")

            # so swap the value we are inspecting in the left partition with value we are comparing it to in the right partition
            ary[i_inspect] = val_compare
            ary[i_right_partition] = val_inspect
            if debug_depth > -1:
                print(f"{debug_header}\t\tswapped (left) ary[{i_inspect}]={val_inspect} <--> (right) ary[{i_right_partition}]={val_compare}")
                print(f"{debug_header}\t\t\tleft: {ary[lb:mid+1]}, right: {ary[mid+1:ub+1]}")

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
        val_inspect = ary[i_inspect]
        val_compare = ary[i_compare]

        if debug_depth > -1:
            print(f"{debug_header}\t\t(inspect) ary[{i_inspect}]={val_inspect} > (compare) ary[{i_compare}]={val_compare} ?", end=" ")
        if val_inspect > val_compare:
            inv_count += 1
            if debug_depth > -1:
                print(f"True --> INVERTED, incremented inv_count to {inv_count}")

            # so swap the value we are inspecting in the right partition with value we are comparing it to (also in the right partition)
            ary[i_inspect] = val_compare
            ary[i_compare] = val_inspect
            if debug_depth > -1:
                print(f"{debug_header}\t\t\tswapped ary[{i_inspect}]={val_inspect} <--> ary[{i_compare}]={val_compare}")
                print(f"{debug_header}\t\t\t\tright: {ary[mid+1:ub+1]}")

        else:
            if debug_depth > -1:
                print(f"False --> NOT inverted")	
            
        if i_compare < ub:
            i_compare += 1
        else:
            i_inspect += 1
            i_compare = i_inspect+1

    return inv_count

def mergesort_inplace(ary, lb, ub, debug_depth=-1):
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
    inv_count += mergesort_inplace(ary, lb, mid, debug_depth+1 if debug_depth>-1 else -1)
    # right partition will consist of elements from ary ranging from indexes mid+1 to ub
    inv_count += mergesort_inplace(ary, mid+1, ub, debug_depth+1 if debug_depth>-1 else -1)
    
    # now we need to sort/merge the left and right partitions
    inv_count += merge_inplace(ary, lb, mid, ub, debug_depth)

    return inv_count


def mergesort_inplace(ary, debug=False):
    return mergesort_inplace(ary, 0, len(ary)-1, debug_depth=0 if debug else -1)
# ******************** IN-PLACE: end ********************




# ******************** NEW ARRAY: begin ********************
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
# ******************** NEW ARRAY: end ********************