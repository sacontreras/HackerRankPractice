def sort(ary, lb, mid, ub):
    # pivot on left partition first
    i_inspect = lb
    i_right_partition = mid + 1 # note that i_right_partition will advance

    inv_count = 0
    
    while i_inspect < mid+1:
        if ary[i_inspect] > ary[i_right_partition]:	# then item in left partition is greater than item in right partition
            # there has been an inversion
            inv_count += mid-i_inspect + 1

            # so swap the value we are inspecting in the left partition with value we are comparing it to in the right partition
            val_left_partition = ary[i_inspect]
            ary[i_inspect] = ary[i_right_partition]
            ary[i_right_partition] = val_left_partition	
        
        if i_right_partition < ub:
            i_right_partition += 1 # advance the right-comparison index to the next element
        else:   # then we have compared the pivot ("inspection") element in the left partition to every element in the right partition
            i_inspect += 1  # so we can now advance to the next pivot ("inspection") element in the left partition
            i_right_partition = mid + 1 # now we need to reset the right-position "pointer" back to the beginning (of the right partition)
        

    # now reconcile (sort) right partition
    i_inspect = mid + 1 # obviously we start inspection at first elt in right partition
    i_right_partition = mid + 2 # and we begin with the second element in the right partition (since it is pointless to compared the inspection element to itself)
    while i_inspect < ub:
        if ary[i_inspect] > ary[i_right_partition]:
            # so swap the value we are inspecting in the right partition with value we are comparing it to (also in the right partition)
            val_right_partition = ary[i_inspect]
            ary[i_inspect] = ary[i_right_partition]
            ary[i_right_partition] = val_right_partition	
            
        if i_right_partition < ub:
            i_right_partition += 1
        else:
            i_inspect += 1
            i_right_partition = i_inspect+1

    return inv_count
			
		
# merge_sort uses the concept known as Divide and Conquer
def merge_sort(ary, lb, rb):
    # this is a recursive function, so we need a base case
    if lb == rb:	# then we have sub-divided ary until the point that the current sub-array contains only a single element
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
    mid = (lb + rb) // 2	# note that since this is integer division, we will implicitly round down
    
    # now recursively partition ary into left and right sub-arrays
    # left partition will consist of elements from ary ranging from indexes lb to mid
    inv_count += merge_sort(ary, lb, mid)
    # right partition will consist of elements from ary ranging from indexes mid+1 to rb
    inv_count += merge_sort(ary, mid+1, rb)
    
    # now we need to sort/merge the left and right partitions
    inv_count += sort(ary, lb, mid, rb)

    return inv_count


def mergesort(ary):
    return merge_sort(ary, 0, len(ary)-1)
