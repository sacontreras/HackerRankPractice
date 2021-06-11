[link](https://www.hackerrank.com/challenges/two-strings/problem?h_l=interview&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D=dictionaries-hashmaps&h_r=next-challenge&h_v=zen)


## First Try:

This problem is straightforward.  The logic appears to be correct.  But the solution is sub-optimal (very, VERY slow) and results in timeout.  (see below)

```python
def twoStrings(s1, s2):
    debug = False

    if debug:
        print(f"s1: {s1}")
    l_s1 = len(s1)
    s1_subs = []
    for i_start in range(l_s1):
        for i_end in range(i_start, l_s1):
            sub_s1 = s1[i_start:i_end+1]
            if debug:
                print(f"\tsubstring: {sub_s1}")
            s1_subs.append(sub_s1)

    if debug:
        print(f"s2: {s2}")
    l_s2 = len(s2)
    s2_subs = []
    for i_start in range(l_s2):
        for i_end in range(i_start, l_s2):
            sub_s2 = s2[i_start:i_end+1]
            if debug:
                print(f"\tsubstring: {sub_s2}")
            s2_subs.append(sub_s2)

    for sub_s1 in s1_subs:
        if sub_s1 in s2_subs:
            if debug:
                print(f"'{s1}' has substring '{sub_s1}' in '{s2}'")
            return "YES"

    if debug:
        print(f"'{s1}' and '{s2}' do not have any substrings in common")
    return "NO"
```


# Second Try:

Used dicts for O(1) lookup.  Better than the above but still failing due to timeout on some (but fewer) test cases. (see below)

```python
def twoStrings(s1, s2):
    debug = False

    if debug:
        print(f"s1: {s1}")

    l_s1 = len(s1)
    d_s1_subs = {}
    for i_start in range(l_s1):
        for i_end in range(i_start, l_s1):
            sub_s1 = s1[i_start:i_end+1]
            if debug:
                print(f"\tsubstring: {sub_s1}")
            d_s1_subs[sub_s1] = d_s1_subs.get(sub_s1,0) + 1

    if debug:
        print(f"s2: {s2}")
    l_s2 = len(s2)
    d_s2_subs = {}
    for i_start in range(l_s2):
        for i_end in range(i_start, l_s2):
            sub_s2 = s2[i_start:i_end+1]
            if debug:
                print(f"\tsubstring: {sub_s2}")
            try:
                n_sub_s2_in_s1 = d_s1_subs[sub_s2]
                if n_sub_s2_in_s1 > 0:
                    return "YES"
            except:
                pass    
            d_s2_subs[sub_s2] = d_s1_subs.get(sub_s2,0) + 1

    if debug:
        print(f"'{s1}' and '{s2}' do not have any substrings in common")
    return "NO"
```

# Third Try:

Dicts for O(1) lookup is definitely the correct approach.  But on closer observation, we see that to have any substring in common, both strings must have at least one char in common... so that's all we check.  There is no need to find ALL substrings.  This takes WAY too long!  (see below)

ALL TEST CASES PASSED!

```python
def twoStrings(s1, s2):
    d_s1_subs = {}
    d_s2_subs = {}

    # to have any substring in common, both strings must have at least one char in common
    for c in s1:
        d_s1_subs[c] = d_s1_subs.get(c,0) + 1
    for c in s2:
        try:
            n_sub_s2_in_s1 = d_s1_subs[c]
            if n_sub_s2_in_s1 > 0:
                return "YES"
        except:
            pass 
        d_s2_subs[c] = d_s1_subs.get(c,0) + 1

    return "NO"
```


## POST-MORTEM:

Solve the problem and nothing more!