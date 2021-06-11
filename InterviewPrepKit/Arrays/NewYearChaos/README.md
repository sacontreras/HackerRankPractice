[link](https://www.hackerrank.com/challenges/new-year-chaos/problem?h_l=interview&h_r%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=next-challenge&h_r%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=next-challenge&h_v%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=zen&h_v%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=zen&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=arrays)


## First Try:

Initially, I correctly solved this with quadratic complexity, O(n^2) but this resulted in timeout error on Hackerrank.  (see below)

```python
def minimumBribes(q):
    n_total_bribes = 0
    
    for i, p in enumerate(q):
        pos_moved = p - (i+1)
        
        if pos_moved > 2:
            print("Too chaotic")
            return
        
        n_bribes_to_p = 0
        for j in range(max(pos_moved, 0), i):
            if q[j] > p:
                n_bribes_to_p += 1
                
        if n_bribes_to_p > 0:
            n_total_bribes += n_bribes_to_p
    
    print(f"{n_total_bribes}")
```


# Second Try:

Then I did some research into a solution based on counting inversions - not quite what we need - but close.  This solution is based on the Merge Sort algorithm.  But was still ultimately incorrect.  Tested locally and did not even submit it.  Run time is O(n log n).  Run time might be okay but the problem is not to count inversions.  Still, could have taken more time to make it correct.


# Third Try:

Then, I did more research and found a linear, O(n) complexity solution from https://www.tutorialspoint.com/program-to-count-number-of-swaps-required-to-change-one-list-to-another-in-python.  (see below)

```python
def minimumBribes(q):
    # credit where credit is due:
    #   referenced article https://www.tutorialspoint.com/program-to-count-number-of-swaps-required-to-change-one-list-to-another-in-python

    # e.g.
    #   q   = [2,1,5,3,4]   (if and only if)
    #   q0  = [1,2,3,4,5]
    #
    #   iterating through q, we have:
    #       p = 2   <-->    q0.index(p) == 1    (moved forward 1 spot from q0)
    #           (increment n_bribes by spots moved from q0 for p==2)                                n_bribed += q0.index(p) --> n_bribed = 1
    #           (now pop this index, q0.index(p)==1, from q0 since we are done handling p == 2)     q0.pop(q0.index(p))     --> q0 = [1,3,4,5]
    #       p = 1   <-->    q0.index(p) == 0    (did not move forward from q0)
    #           (increment n_bribes by spots moved from q0 for p==1)                                n_bribed += q0.index(p) --> n_bribed = 1
    #           (now pop this index, q0.index(p)==0, from q0 since we are done handling p == 1)     q0.pop(q0.index(p))     --> q0 = [3,4,5]
    #       p = 5   <-->    q0.index(p) == 2    (moved forward 2 spots from q0)
    #           (increment n_bribes by spots moved from q0 for p==5)                                n_bribed += q0.index(p) --> n_bribed = 3
    #           (now pop this index, q0.index(p)==2, from q0 since we are done handling p == 5)     q0.pop(q0.index(p))     --> q0 = [3,4]
    #       p = 3   <-->    q0.index(p) == 0    (did not move forward from q0)
    #           (increment n_bribes by spots moved from q0 for p==3)                                n_bribed += q0.index(p) --> n_bribed = 3
    #           (now pop this index, q0.index(p)==0, from q0 since we are done handling p == 3)     q0.pop(q0.index(p))     --> q0 = [4]
    #       p = 4   <-->    q0.index(p) == 0    (did not move forward from q0)
    #           (increment n_bribes by spots moved from q0 for p==4)                                n_bribed += q0.index(p) --> n_bribed = 3
    #           (now pop this index, q0.index(p)==0, from q0 since we are done handling p == 4)     q0.pop(q0.index(p))     --> q0 = []

    # get q0 (prior to bribes), so that we can compare it to q (after bribes have occurred)
    q0 = [p0 for p0 in range(1,len(q)+1)]

    n_bribes = 0

    for p in q:        
        i0 = pos_forward_from_q0 = q0.index(p)

        if pos_forward_from_q0 > 2:
            print("Too chaotic")
            return

        # now pop value at this index, q0.index(p), from q0 since we are done handling this p
        q0.pop(i0)

        n_bribes += pos_forward_from_q0

    print(n_bribes)
```

## POST-MORTEM:

My very first attempts were based on my third try.  Moral of the story: TRUST YOUR INSTINCTS!