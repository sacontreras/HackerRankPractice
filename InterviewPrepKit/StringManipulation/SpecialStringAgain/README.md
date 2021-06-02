[link](https://www.hackerrank.com/challenges/special-palindrome-again/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=strings)


## First Try:

This puzzle is fairly tricky.  The first part of the algorithm tests if the original string is the span of a single unique character.  If so, we can immediately short-circuit to the total number of substrings, which is simply the value $\frac{n(n+1)}{2}$.

If not, then we iterate over all indices, treating each index as the midpoint of a substring.  The idea is to construct substrings using this midpoint with a given radius, 
$
r_{max} = 
\begin{cases}
    i_{mid} &, i_{mid} < \frac{n}{2} \\
    (n-1) - i_{mid} &, i_{mid} > \frac{n}{2} \\
    \frac{n}{2} &, i_{mid} = \frac{n}{2}
\end{cases}
$.

This approach passed all free test-cases but as we can see right off the bat, with a large test-case (string), the complexity is going to definitely be sub-optimal.

First, not considering operations internal to the loops, we have at a minimum $O(n^2)$ complexity since we first iterate over every index $i$, and then over every radius $r: 0 \le r \le \frac{i}{2}$.

I didn't even bother officially submitting this implementation for grading.  Instead, I unlocked and downloaded test-case 02 beforehand.  Running this implementation against test-case 02 confirmed that this initial implementation is DEFINITELY insufficient, as it took a very, very long time to complete.

(see below)

```
def substrCount(n, s, debug=False):
    if debug:
        print(f"n: {n}, s: {s}")

    n_special_strings = 0

    set_chars = set(list(s))
    if len(set_chars) == 1:
        n_special_strings = n*(n+1)//2
        if debug:
            print(f"short circuit to n(n+1)/2 since there is only one unique char")

    else:
        if debug:
            n_subs = 0
            print("ALL substrings:", end=" ")
            for i_start in range(n):
                for l in range(n-i_start,0,-1):
                    subs = s[i_start:i_start+l]
                    print(subs, end=" ")
                    n_subs += 1
            print(f"\n\t{n_subs} total")

            n_subs = 0
            print("odd-length substrings:", end=" ")
            for i_start in range(n):
                for l in range(n-i_start,0,-1):
                    subs = s[i_start:i_start+l]
                    if len(subs)%2 == 1:
                        print(subs, end=" ")
                        n_subs += 1
            print(f"\n\t{n_subs} total\n")

        mid = n // 2

        if debug:
            n_subs = 0

        for i_mid in range(n):
            max_r = mid
            if i_mid < mid:
                max_r = i_mid
            elif i_mid > mid:
                max_r = (n-1) - i_mid

            for r in range(0,max_r+1):
                i_start = i_mid-r
                i_end = i_mid+r
                subs = s[i_mid] if r == 0 else s[i_start:i_end+1]
                if debug:
                    print(f"odd-length substring '{subs}' at indices {list(range(i_start,i_end+1))}")

                if len(subs) > 1:
                    l_sub = s[i_start:i_mid]
                    l_sub_first_dup = l_sub[0]*len(l_sub)
                    is_special = l_sub_first_dup==l_sub
                    r_sub = s[i_mid+1:i_end+1]
                    r_sub_first_dup = r_sub[0]*len(r_sub)
                    is_special = is_special and r_sub_first_dup==l_sub_first_dup
                    if debug:
                        print(f"\thas: mid({i_mid})='{s[i_mid]}', radius={r} --> left-half='{l_sub}' ({list(range(i_start,i_mid))}), right-half='{r_sub}' ({list(range(i_mid+1,i_end+1))}) --> {'SPECIAL' if is_special else 'NOT special'}")
                    n_special_strings += 1 if is_special else 0
                else:
                    if debug:
                        print(f"\tSPECIAL since length is 1")
                    n_special_strings += 1
                
                if debug:
                    n_subs += 1

        if debug:
            print(f"{n_subs} odd-length substrings total")
        
    return n_special_strings
```

<p><br>

(Debug) Output for test-case 00:

```
n: 5, s: asasd
ALL substrings: asasd asas asa as a sasd sas sa s asd as a sd s d 
        15 total
odd-length substrings: asasd asa a sas s asd a s d 
        9 total

odd-length substring 'a' at indices [0]
        SPECIAL since length is 1
odd-length substring 's' at indices [1]
        SPECIAL since length is 1
odd-length substring 'asa' at indices [0, 1, 2]
        has: mid(1)='s', radius=1 --> left-half='a' ([0]), right-half='a' ([2]) --> SPECIAL
odd-length substring 'a' at indices [2]
        SPECIAL since length is 1
odd-length substring 'sas' at indices [1, 2, 3]
        has: mid(2)='a', radius=1 --> left-half='s' ([1]), right-half='s' ([3]) --> SPECIAL
odd-length substring 'asasd' at indices [0, 1, 2, 3, 4]
        has: mid(2)='a', radius=2 --> left-half='as' ([0, 1]), right-half='sd' ([3, 4]) --> NOT special
odd-length substring 's' at indices [3]
        SPECIAL since length is 1
odd-length substring 'asd' at indices [2, 3, 4]
        has: mid(3)='s', radius=1 --> left-half='a' ([2]), right-half='d' ([4]) --> NOT special
odd-length substring 'd' at indices [4]
        SPECIAL since length is 1
9 odd-length substrings total
result: 7
expect: 7
```

<p><br>

(Debug) Output for test-case 01:

```
n: 7, s: abcbaba
ALL substrings: abcbaba abcbab abcba abcb abc ab a bcbaba bcbab bcba bcb bc b cbaba cbab cba cb c baba bab ba b aba ab a ba b a 
        28 total
odd-length substrings: abcbaba abcba abc a bcbab bcb b cbaba cba c bab b aba a b a 
        16 total

odd-length substring 'a' at indices [0]
        SPECIAL since length is 1
odd-length substring 'b' at indices [1]
        SPECIAL since length is 1
odd-length substring 'abc' at indices [0, 1, 2]
        has: mid(1)='b', radius=1 --> left-half='a' ([0]), right-half='c' ([2]) --> NOT special
odd-length substring 'c' at indices [2]
        SPECIAL since length is 1
odd-length substring 'bcb' at indices [1, 2, 3]
        has: mid(2)='c', radius=1 --> left-half='b' ([1]), right-half='b' ([3]) --> SPECIAL
odd-length substring 'abcba' at indices [0, 1, 2, 3, 4]
        has: mid(2)='c', radius=2 --> left-half='ab' ([0, 1]), right-half='ba' ([3, 4]) --> NOT special
odd-length substring 'b' at indices [3]
        SPECIAL since length is 1
odd-length substring 'cba' at indices [2, 3, 4]
        has: mid(3)='b', radius=1 --> left-half='c' ([2]), right-half='a' ([4]) --> NOT special
odd-length substring 'bcbab' at indices [1, 2, 3, 4, 5]
        has: mid(3)='b', radius=2 --> left-half='bc' ([1, 2]), right-half='ab' ([4, 5]) --> NOT special
odd-length substring 'abcbaba' at indices [0, 1, 2, 3, 4, 5, 6]
        has: mid(3)='b', radius=3 --> left-half='abc' ([0, 1, 2]), right-half='aba' ([4, 5, 6]) --> NOT special
odd-length substring 'a' at indices [4]
        SPECIAL since length is 1
odd-length substring 'bab' at indices [3, 4, 5]
        has: mid(4)='a', radius=1 --> left-half='b' ([3]), right-half='b' ([5]) --> SPECIAL
odd-length substring 'cbaba' at indices [2, 3, 4, 5, 6]
        has: mid(4)='a', radius=2 --> left-half='cb' ([2, 3]), right-half='ba' ([5, 6]) --> NOT special
odd-length substring 'b' at indices [5]
        SPECIAL since length is 1
odd-length substring 'aba' at indices [4, 5, 6]
        has: mid(5)='b', radius=1 --> left-half='a' ([4]), right-half='a' ([6]) --> SPECIAL
odd-length substring 'a' at indices [6]
        SPECIAL since length is 1
16 odd-length substrings total
result: 10
expect: 10
```

<p><br>

(Debug) Output for test-case 16:

```
n: 4, s: aaaa
short circuit to n(n+1)/2 since there is only one unique char
result: 10
expect: 10
```

## Second Try

For this iteration, I focused on finding a linear implementation using the above logical concept.  All free test-cases passed with this approach, as did the unlocked test-case 02.

(see below)

```
def vectorize_char_counts(n, s):
    char_count_tuples = []
    i = 0

    while (i < n):
        c = s[i]
        n_c = 1

        while (i+1 < n and s[i+1]==c):   # adjacent chars, left-to-right, are the same
            i += 1
            n_c += 1

        char_count_tuples.append((c,n_c))
        i += 1

    return char_count_tuples

def vectorize_case2_special_substrings(n, s):
    case2_special_substrings = []

    for i_mid in range(1, n):
        char_radius = 1

        while True:
            i_start = i_mid - char_radius
            i_end = i_mid + char_radius

            if 0 <= i_start < i_end < n:
                is_mid_char_different = s[i_mid] != s[i_mid-1]  # unique middle char differentiates from case 1 (same-character substrings)
                is_same_surrounding_char = s[i_start] == s[i_end]
                is_contiguous_same_char_left = s[i_mid-1] == s[i_start]

                if is_mid_char_different and is_same_surrounding_char and is_contiguous_same_char_left:
                    case2_special_substrings.append(s[i_start:i_end+1])
                    char_radius += 1

                else:
                    break

            else:
                break

    return case2_special_substrings

def substrCount(n, s, debug=False):
    if debug:
        print(f"n: {n}, s: {s}\n")

    n_special_strings = 0

    # case 1: all same-character substrings: given any string of length n, it will have n(n+1)/2 substrings
    #   and we count all of them since the base string is based on a single char
    n_case1_subs = 0
    char_count_tuples = vectorize_char_counts(n, s)
    if debug:
        i = 0
        print(f"counting same-character (case-1) substrings...")
    for c, n_c in char_count_tuples:
        n_substrings = n_c*(n_c+1)//2
        if debug:
            print(f"\tsubstring '{c*n_c}' ({[_i for _i in range(i,i+n_c)]}) has {n_substrings} sub-substrings")
            i += n_c
        n_case1_subs += n_substrings
    if debug:
        print(f"\t\t{n_case1_subs} total same-character special substrings")

    # case 2
    n_case2_subs = 0
    case2_special_substrings = vectorize_case2_special_substrings(n, s)
    if debug:
        print(f"\ncounting case-2 substrings...")
        for c2subs in case2_special_substrings:
            print(f"\t{c2subs}")
    n_case2_subs = len(case2_special_substrings)
    if debug:
        print(f"\t\t{n_case2_subs} total case-2 special substrings\n")

    n_special_strings = n_case1_subs + n_case2_subs

    return n_special_strings
```

<p><br>

(Debug) Output for test-case 00:

```
n: 5, s: asasd

counting same-character (case-1) substrings...
        substring 'a' ([0]) has 1 sub-substrings
        substring 's' ([1]) has 1 sub-substrings
        substring 'a' ([2]) has 1 sub-substrings
        substring 's' ([3]) has 1 sub-substrings
        substring 'd' ([4]) has 1 sub-substrings
                5 total same-character special substrings

counting case-2 substrings...
        asa
        sas
                2 total case-2 special substrings

result: 7
expect: 7
```

<p><br>

(Debug) Output for test-case 01:

```
n: 7, s: abcbaba

counting same-character (case-1) substrings...
        substring 'a' ([0]) has 1 sub-substrings
        substring 'b' ([1]) has 1 sub-substrings
        substring 'c' ([2]) has 1 sub-substrings
        substring 'b' ([3]) has 1 sub-substrings
        substring 'a' ([4]) has 1 sub-substrings
        substring 'b' ([5]) has 1 sub-substrings
        substring 'a' ([6]) has 1 sub-substrings
                7 total same-character special substrings

counting case-2 substrings...
        bcb
        bab
        aba
                3 total case-2 special substrings

result: 10
expect: 10
```

<p><br>

(Debug) Output for test-case 16:

```
n: 4, s: aaaa

counting same-character (case-1) substrings...
        substring 'aaaa' ([0, 1, 2, 3]) has 10 sub-substrings
                10 total same-character special substrings

counting case-2 substrings...
                0 total case-2 special substrings

result: 10
expect: 10
```

Upon submission, ALL test-cases passed!

## POST-MORTEM:

There are two things to note here with regard to be able to successfully solve this puzzle.  As usual, $O(n^2)$ complexity is almost always going to be sub-optimal and, therefore, fail a good chunk of the test-cases due to timeout.

Secondly, the catch to arriving at the second version of the implementation - based on observations gleaned from the first implementation - was to adhere closely to the two conditions (cases) defining "special strings".  Providing implementations for each case, with linear complexity in mind, proved to be the correct approach in the end.