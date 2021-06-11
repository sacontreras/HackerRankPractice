[link](https://www.hackerrank.com/challenges/minimum-swaps-2/problem?h_l=interview&playlist_slugs%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D=arrays&isFullScreen=true)


## First Try:

In theory, this puzzle is fairly straightforward.  My initial attempt is logically correct.  However, it does not account for the complexity involved in using the List.index() method in Python.  Thus, it failed due to timeout in some of the larger test cases. (see below)

```python
def minimumSwaps(arr):
    n_swaps = 0
    
    for i0 in range(len(arr)):
        e = arr[i0]
        e0 = i0+1
        if e != e0:    # then we need to swap with what it should be
            # locate index of e0 in arr
            i = arr.index(e0)   # but this takes a looong time, so use O(1) 

            # swap in array and update the dict
            arr[i0] = e0
            arr[i] = e
            
            n_swaps += 1

    return n_swaps
```


# Second Try:

So, an O(1) lookup is required.  Thus, a dictionary is used to do the lookups instead.  Simple.  (see below)

```python
def minimumSwaps(arr):
    d_arr = {v:i for i,v in enumerate(arr)} # for O(1) lookup

    n_swaps = 0
    
    for i0 in range(len(arr)):
        e = arr[i0]
        e0 = i0+1
        if e != e0:    # then we need to swap with what it should be
            # locate index of e0 in arr
            # i = arr.index(e0)   # but this takes a looong time, so use O(1) lookup of dict
            i = d_arr[e0]

            # swap in array and update the dict
            arr[i0] = e0
            d_arr[e0] = i0
            arr[i] = e
            d_arr[e] = i

            n_swaps += 1

    return n_swaps
```


## POST-MORTEM:

I DID actually think about the potential performance hit that List.index() can occur.  Moral of the story: AGAIN... TRUST YOUR INSTINCTS!