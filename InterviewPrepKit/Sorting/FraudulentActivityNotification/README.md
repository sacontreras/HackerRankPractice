[link](https://www.hackerrank.com/challenges/fraudulent-activity-notifications/problem?h_l=interview&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D=sorting&h_r=next-challenge&h_v=zen)


## First Try:

This puzzle involves a clear understanding of the correct indexing scheme.  The correct median calculation is based first on understanding the correct indexing scheme and then sorting the window of prior expenditures.  Of course this also necessitates using the correct formula for calculating the median based on the size of the window --> if odd (using mod 2), then the median is just the value at d/2 (integer division, rounds down), otherwise it is the average of values at indices d/2 (integer division, rounds down) - 1 and d/2 (integer division, rounds down).  All free test-cases passed with the following implementation.  However, test-cases t through 5 failed due to timeout.  However, unlocking test-cases 01 and 02 passed successfully locally... they just took a long time.  Timeout failures are likely due to complexity of the sorting involved at each step.

(see below)

```
def activityNotifications(expenditure, d):
    debug = True

    n_notify = 0

    n = len(expenditure)

    if debug:
        print(f"expenditure: {expenditure}, d: {d}")

    for i_end in range(d,n):
        i_start = i_end-d
        prev_expenditures = expenditure[i_start:i_end]
        prev_exp_sorted = sorted(prev_expenditures)

        med = None
        i_med_offset = d // 2
        print(f"\texpenditure indices: [{i_start},{i_end-1}] --> i_med_offset: {i_start+i_med_offset}")
        if d % 2 == 1:
            med = prev_exp_sorted[i_med_offset]
        else:
            med = (prev_exp_sorted[i_med_offset-1]+prev_exp_sorted[i_med_offset]) / 2
        exp_thresh = 2*med

        exp_today = expenditure[i_end]

        thresh_reached = exp_today >= exp_thresh

        if debug:
            print(f"\ton day {i_end+1}, prior {d} expenditures: {prev_expenditures} (sorted: {prev_exp_sorted})")
            print(f"\t\t--> median: {med} --> expenditure threshold: {exp_thresh}")
            print(f"\t\t\texpenditure today (day {i_end+1}) is {exp_today} --> notify (exp >= thresh)? {exp_today} >= {exp_thresh}? {thresh_reached}")
    
        n_notify += 1 if thresh_reached else 0
    
    return n_notify
```

<p><br>

(Debug) Output for test-case 00:
```
testing against input file ./InterviewPrepKit/Sorting/FraudulentActivityNotification/input00.txt...
expenditure: [2, 3, 4, 2, 3, 6, 8, 4, 5], d: 5
        expenditure indices: [0,4] --> i_med_offset: 2
        on day 6, prior 5 expenditures: [2, 3, 4, 2, 3] (sorted: [2, 2, 3, 3, 4])
                --> median: 3 --> expenditure threshold: 6
                        expenditure today (day 6) is 6 --> notify (exp >= thresh)? 6 >= 6? True
        expenditure indices: [1,5] --> i_med_offset: 3
        on day 7, prior 5 expenditures: [3, 4, 2, 3, 6] (sorted: [2, 3, 3, 4, 6])
                --> median: 3 --> expenditure threshold: 6
                        expenditure today (day 7) is 8 --> notify (exp >= thresh)? 8 >= 6? True
        expenditure indices: [2,6] --> i_med_offset: 4
        on day 8, prior 5 expenditures: [4, 2, 3, 6, 8] (sorted: [2, 3, 4, 6, 8])
                --> median: 4 --> expenditure threshold: 8
                        expenditure today (day 8) is 4 --> notify (exp >= thresh)? 4 >= 8? False
        expenditure indices: [3,7] --> i_med_offset: 5
        on day 9, prior 5 expenditures: [2, 3, 6, 8, 4] (sorted: [2, 3, 4, 6, 8])
                --> median: 4 --> expenditure threshold: 8
                        expenditure today (day 9) is 5 --> notify (exp >= thresh)? 5 >= 8? False
result: 2
expect: 2
```

<p><br>

(Debug) Output for test-case 06:
```
testing against input file ./InterviewPrepKit/Sorting/FraudulentActivityNotification/input06.txt...
expenditure: [1, 2, 3, 4, 4], d: 4
        expenditure indices: [0,3] --> i_med_offset: 2
        on day 5, prior 4 expenditures: [1, 2, 3, 4] (sorted: [1, 2, 3, 4])
                --> median: 2.5 --> expenditure threshold: 5.0
                        expenditure today (day 5) is 4 --> notify (exp >= thresh)? 4 >= 5.0? False
result: 0
expect: 0
```

<p><br>

(Debug) Output for test-case 07:
```
testing against input file ./InterviewPrepKit/Sorting/FraudulentActivityNotification/input07.txt...
expenditure: [10, 20, 30, 40, 50], d: 3
        expenditure indices: [0,2] --> i_med_offset: 1
        on day 4, prior 3 expenditures: [10, 20, 30] (sorted: [10, 20, 30])
                --> median: 20 --> expenditure threshold: 40
                        expenditure today (day 4) is 40 --> notify (exp >= thresh)? 40 >= 40? True
        expenditure indices: [1,3] --> i_med_offset: 2
        on day 5, prior 3 expenditures: [20, 30, 40] (sorted: [20, 30, 40])
                --> median: 30 --> expenditure threshold: 60
                        expenditure today (day 5) is 50 --> notify (exp >= thresh)? 50 >= 60? False
result: 1
expect: 1
```

## Second Try:

Pre-sorting `prev_exp_sorted = sorted(expenditure[0:d])` prior to iterating expenditures yields a nearly sorted list for all subsequent iterations.  We simply shift the window to the right by one for the new expenditure.  That is, we remove the expenditure from the window corresponding to index `i - d`.  Since we are simply removing the first element in the window, the remaining window is still sorted.  So, locating the index of where the new i'th expenditure should go in the window happens in O(log n) time (binary search).  However, shifting elements after that position will occur in O(n) time.

This solved the timeout failures.  ALL test-cases passed!

(see below)

```
from bisect import bisect_left, insort_left
def activityNotifications(expenditure, d):
    debug = False

    n_notify = 0

    n = len(expenditure)
    
    if debug:
        print(f"expenditure: {expenditure}, d: {d}")

    # new for v. 2: 
    #   pre-sorting this the first time yields a nearly sorted list for all subsequent iterations
    #   and then we can find the index of the one new expenditure to be replaced
    #   via bisect_left() and then replace it with insort_left with O(n) complexity
    prev_exp_sorted = sorted(expenditure[0:d])

    for i_end in range(d,n):
        i_start = i_end-d

        if debug:
            prev_expenditures = expenditure[i_start:i_end]  # # new for v. 2: only need this when debugging
        # prev_exp_sorted = sorted(prev_expenditures) # bottleneck in v. 1
        
        med = None
        i_med_offset = d // 2
        if debug:
            print(f"\texpenditure indices: [{i_start},{i_end-1}] --> i_med_offset: {i_start+i_med_offset}")
        if d % 2 == 1:
            med = prev_exp_sorted[i_med_offset]
        else:
            med = (prev_exp_sorted[i_med_offset-1]+prev_exp_sorted[i_med_offset]) / 2

        exp_thresh = 2*med

        exp_today = expenditure[i_end]

        thresh_reached = exp_today >= exp_thresh

        if debug:
            print(f"\ton day {i_end+1}, prior {d} expenditures: {prev_expenditures} (sorted: {prev_exp_sorted})")
            print(f"\t\t--> median: {med} --> expenditure threshold: {exp_thresh}")
            print(f"\t\t\texpenditure today (day {i_end+1}) is {exp_today} --> notify (exp >= thresh)? {exp_today} >= {exp_thresh}? {thresh_reached}")
    
        n_notify += 1 if thresh_reached else 0

        # new for v. 2
        remove_at = bisect_left(prev_exp_sorted, expenditure[i_end-d])
        prev_exp_sorted.pop(remove_at)
        insort_left(prev_exp_sorted, expenditure[i_end])
    
    return n_notify
```

## POST-MORTEM:

I expected the first try to timeout on test-cases with large input since (completely re) sorting with each iteration would amount to complexity >= O(n^2 log n) for the implementation overall.  The trick in this case was to find an efficient way to sort at each iteration.  Dealing with the previously sorted window (save for the new element) was key here.