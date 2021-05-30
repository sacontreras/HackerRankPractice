[link](https://www.hackerrank.com/challenges/sherlock-and-valid-string/problem?h_l=interview&h_r=next-challenge&h_v=zen&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=strings&h_r=next-challenge&h_v=zen)


## First Try:

We use two dictionaries (Hash Tables).  The first one is the usual character frequency dictionary encountered in similar puzzles.  The second one inverts that.  That is, we key the second one by character frequency and it stores the set of characters mapped from that count.

From there, we operate on the (inverted) freq-to-char-set map.  

We know:
- if there is exactly 1 key in the freq-to-char-set map, then every character in the original string occurs the same number of times --> return "YES"
- if there are 3 or more keys in the freq-to-char-set map, then we cannot remove one occurrence of a single character to make case valid --> return "NO
- if there are exactly 2 keys, then:
  - get the associated set with minimum cardinality
    - return "YES" if exactly one character is in this set, otherwise return "NO"

This algorithm passed all of the free test-cases.  Upon submission, it passed all of the test-cases except for 3 and 5.

(see below)

```
def isValid(s, debug=False):
    if debug:
        print(f"s: {s}")

    d_c_freq = {}
    for c in s:
        d_c_freq[c] = d_c_freq.get(c,0) + 1
    d_freq_c = {}
    for c,n_c in d_c_freq.items():
        set_c = d_freq_c.get(n_c,set())
        set_c.add(c)
        d_freq_c[n_c] = set_c

    if debug:
        print(f"d_c_freq: {d_c_freq} (len={len(d_c_freq)})")
        print(f"d_freq_c: {d_freq_c} (len={len(d_freq_c)})")

    distinct_counts = len(d_freq_c)
    if distinct_counts <= 1:
        return "YES"

    elif distinct_counts > 2:
        return "NO"
    
    else:   # distinct_counts == 2
        # get set with minimum cardinality
        set_min = None
        for n_c, set_c in d_freq_c.items():
            if set_min is None:
                set_min = set_c
            else:
                if len(set_c) < len(set_min):
                    set_min = set_c

        return "YES" if len(set_min) == 1 else "NO"
```

<p><br>

(Debug) Output for test-case 00:

```
s: aabbcd
d_c_freq: {'a': 2, 'b': 2, 'c': 1, 'd': 1} (len=4)
d_freq_c: {2: {'a', 'b'}, 1: {'d', 'c'}} (len=2)
result: NO
expect: NO
```

<p><br>

(Debug) Output for test-case 01:

```
s: aabbccddeefghi
d_c_freq: {'a': 2, 'b': 2, 'c': 2, 'd': 2, 'e': 2, 'f': 1, 'g': 1, 'h': 1, 'i': 1} (len=9)
d_freq_c: {2: {'d', 'a', 'b', 'c', 'e'}, 1: {'i', 'g', 'h', 'f'}} (len=2)
result: NO
expect: NO
```

<p><br>

(Debug) Output for test-case 18:

```
s: abcdefghhgfedecba
d_c_freq: {'a': 2, 'b': 2, 'c': 2, 'd': 2, 'e': 3, 'f': 2, 'g': 2, 'h': 2} (len=8)
d_freq_c: {2: {'f', 'g', 'd', 'h', 'b', 'c', 'a'}, 3: {'e'}} (len=2)
result: YES
expect: YES
```

## Second Try

The difference in this version is how we handle the edge-cases.  Specifically, we first need to identify the max vs. min set.  If the min set has more than one character, then this results in an invalid scenario --> return "NO".  Otherwise, we need to do some basic arithmetic on the frequency of the min set.  After reducing the frequency by 1, if this would result in 0, then return "YES" (valid).  If this would result in the same frequency as the max set, return "YES".  Otherwise, return "NO".

(see below)

```
def isValid(s, debug=False):
    if debug:
        print(f"s: {s}")

    d_c_freq = {}
    for c in s:
        d_c_freq[c] = d_c_freq.get(c,0) + 1
    d_freq_c = {}
    for c,n_c in d_c_freq.items():
        set_c = d_freq_c.get(n_c,set())
        set_c.add(c)
        d_freq_c[n_c] = set_c

    if debug:
        print(f"d_c_freq: {d_c_freq} (len={len(d_c_freq)})")
        print(f"d_freq_c: {d_freq_c} (len={len(d_freq_c)})")

    distinct_counts = len(d_freq_c)
    if distinct_counts <= 1:
        return "YES"

    elif distinct_counts > 2:
        return "NO"
    
    else:   # distinct_counts == 2
        # get set with minimum cardinality (and its key)
        set_min = None
        set_min_key = None
        all_keys = set(d_freq_c.keys())
        for n_c, set_c in d_freq_c.items():
            if set_min is None:
                set_min = set_c
                set_min_key = n_c
            else:
                if len(set_c) < len(set_min):
                    set_min = set_c
                    set_min_key = n_c

        if len(set_min) == 1:
            all_keys.remove(set_min_key)
            set_max_key = list(all_keys)[0]
            if debug:
                print(f"set_max_key = all_keys - set_min_key: {set_max_key}")
            n_set_min_key_post_redux = set_min_key-1
            if n_set_min_key_post_redux<=0 or n_set_min_key_post_redux==set_max_key:
                return "YES"
            else:
                return "NO"
        else:
            return "NO"
```

## POST-MORTEM:

