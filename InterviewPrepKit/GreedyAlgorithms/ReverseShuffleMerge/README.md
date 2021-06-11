[link](https://www.hackerrank.com/challenges/reverse-shuffle-merge/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=greedy-algorithms)


## First Try:

It required a fair amount of time for me to understand the exact nature of this puzzle.  FULL DISCLOSURE: I did A LOT of reading from the discussion forum for this puzzle.  I did take suggestions from this discussion.  The discussion primarily helped me understand the nature of the problem.  The algorithm below passed all of the free test-cases.

(see below)

```python
def reverseShuffleMerge(s, debug=False):
    if debug:
        s_reversed = s[::-1]
        i_mid = len(s)//2
        s_l = s[:i_mid]
        s_r = s[i_mid:]
        print(f"s: '{s}'\n\ts_reversed: {s_reversed}\n\tsplit is s_l:'{s_l}', s_r:'{s_r}'\n")

    d_s_c_freq = {}
    for c in s:
        d_s_c_freq[c] = d_s_c_freq.get(c,0) + 1
    d_A_c_freq_required = {c:n_c//2 for c, n_c in d_s_c_freq.items()}
    if debug:
        print(f"char freqs required of final version of string A: {d_A_c_freq_required}")
    d_A_shuff_c_freq_required = d_A_c_freq_required.copy()
    
    A_arr = []
		
    s_rev = s[::-1]
    if debug:
        print(f"processing s in reverse: {s_rev}...")
    for c in s_rev:
        n_c_A_req = d_A_c_freq_required[c]

        if n_c_A_req > 0:
            if debug:
                print(f"\tstring A still requires {n_c_A_req} '{c}' chars")

            while True:
                l_A = len(A_arr)

                if l_A > 0:
                    c_last_of_A = A_arr[-1]
                    n_c_A_shuff_req = d_A_shuff_c_freq_required[c_last_of_A]

                    violates_lexicographical_req = c_last_of_A > c
                    shuff_A_needs_chars = n_c_A_shuff_req > 0
                    if debug:
                        if violates_lexicographical_req:
                            print(f"\t\tlexicographical violation: last char of string A: '{c_last_of_A}' > '{c}", end=" ")
                            if shuff_A_needs_chars:
                                print(f"and shuffle(A) needs {n_c_A_shuff_req} chars")
                            else:
                                print(f"but shuffle(A) does not need anymore chars")

                    if violates_lexicographical_req and shuff_A_needs_chars:
                        A_arr.pop()
                        if debug:
                            print(f"\t\t\tremoving last char of string A: '{c_last_of_A}' --> A is now: '{''.join(A_arr)}'")
                        d_A_c_freq_required[c_last_of_A] += 1
                        if debug:
                            print(f"\t\t\tincrementing count of '{c_last_of_A}' required in A to {d_A_c_freq_required[c_last_of_A]}")
                        d_A_shuff_c_freq_required[c_last_of_A] -= 1
                        if debug:
                            print(f"\t\t\tdecrementing count of '{c_last_of_A}' required in shuffle(A) to {d_A_shuff_c_freq_required[c_last_of_A]}")

                    else:
                        break

                else:
                    break
            
            A_arr.append(c)
            if debug:
                print(f"\t\tafter appending '{c}', string A is: '{''.join(A_arr)}'")
            d_A_c_freq_required[c] -= 1

        else:
            d_A_shuff_c_freq_required[c] -= 1

    return ''.join(A_arr)
```

<p><br>

(Debug) Output for test-case 00:

```
s: 'eggegg'
        s_reversed: ggegge
        split is s_l:'egg', s_r:'egg'

char freqs required of final version of string A: {'e': 1, 'g': 2}
processing s in reverse: ggegge...
        string A still requires 2 'g' chars
                after appending 'g', string A is: 'g'
        string A still requires 1 'g' chars
                after appending 'g', string A is: 'gg'
        string A still requires 1 'e' chars
                lexicographical violation: last char of string A: 'g' > 'e and shuffle(A) needs 2 chars
                        removing last char of string A: 'g' --> A is now: 'g'
                        incrementing count of 'g' required in A to 1
                        decrementing count of 'g' required in shuffle(A) to 1
                lexicographical violation: last char of string A: 'g' > 'e and shuffle(A) needs 1 chars
                        removing last char of string A: 'g' --> A is now: ''
                        incrementing count of 'g' required in A to 2
                        decrementing count of 'g' required in shuffle(A) to 0
                after appending 'e', string A is: 'e'
        string A still requires 2 'g' chars
                after appending 'g', string A is: 'eg'
        string A still requires 1 'g' chars
                after appending 'g', string A is: 'egg'
result: egg
expect: egg
```

<p><br>

(Debug) Output for test-case 15:

```
s: 'abcdefgabcdefg'
        s_reversed: gfedcbagfedcba
        split is s_l:'abcdefg', s_r:'abcdefg'

char freqs required of final version of string A: {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1}
processing s in reverse: gfedcbagfedcba...
        string A still requires 1 'g' chars
                after appending 'g', string A is: 'g'
        string A still requires 1 'f' chars
                lexicographical violation: last char of string A: 'g' > 'f and shuffle(A) needs 1 chars
                        removing last char of string A: 'g' --> A is now: ''
                        incrementing count of 'g' required in A to 1
                        decrementing count of 'g' required in shuffle(A) to 0
                after appending 'f', string A is: 'f'
        string A still requires 1 'e' chars
                lexicographical violation: last char of string A: 'f' > 'e and shuffle(A) needs 1 chars
                        removing last char of string A: 'f' --> A is now: ''
                        incrementing count of 'f' required in A to 1
                        decrementing count of 'f' required in shuffle(A) to 0
                after appending 'e', string A is: 'e'
        string A still requires 1 'd' chars
                lexicographical violation: last char of string A: 'e' > 'd and shuffle(A) needs 1 chars
                        removing last char of string A: 'e' --> A is now: ''
                        incrementing count of 'e' required in A to 1
                        decrementing count of 'e' required in shuffle(A) to 0
                after appending 'd', string A is: 'd'
        string A still requires 1 'c' chars
                lexicographical violation: last char of string A: 'd' > 'c and shuffle(A) needs 1 chars
                        removing last char of string A: 'd' --> A is now: ''
                        incrementing count of 'd' required in A to 1
                        decrementing count of 'd' required in shuffle(A) to 0
                after appending 'c', string A is: 'c'
        string A still requires 1 'b' chars
                lexicographical violation: last char of string A: 'c' > 'b and shuffle(A) needs 1 chars
                        removing last char of string A: 'c' --> A is now: ''
                        incrementing count of 'c' required in A to 1
                        decrementing count of 'c' required in shuffle(A) to 0
                after appending 'b', string A is: 'b'
        string A still requires 1 'a' chars
                lexicographical violation: last char of string A: 'b' > 'a and shuffle(A) needs 1 chars
                        removing last char of string A: 'b' --> A is now: ''
                        incrementing count of 'b' required in A to 1
                        decrementing count of 'b' required in shuffle(A) to 0
                after appending 'a', string A is: 'a'
        string A still requires 1 'g' chars
                after appending 'g', string A is: 'ag'
        string A still requires 1 'f' chars
                lexicographical violation: last char of string A: 'g' > 'f but shuffle(A) does not need anymore chars
                after appending 'f', string A is: 'agf'
        string A still requires 1 'e' chars
                lexicographical violation: last char of string A: 'f' > 'e but shuffle(A) does not need anymore chars
                after appending 'e', string A is: 'agfe'
        string A still requires 1 'd' chars
                lexicographical violation: last char of string A: 'e' > 'd but shuffle(A) does not need anymore chars
                after appending 'd', string A is: 'agfed'
        string A still requires 1 'c' chars
                lexicographical violation: last char of string A: 'd' > 'c but shuffle(A) does not need anymore chars
                after appending 'c', string A is: 'agfedc'
        string A still requires 1 'b' chars
                lexicographical violation: last char of string A: 'c' > 'b but shuffle(A) does not need anymore chars
                after appending 'b', string A is: 'agfedcb'
result: agfedcb
expect: agfedcb
```

<p><br>

(Debug) Output for test-case 16:

```
s: 'aeiouuoiea'
        s_reversed: aeiouuoiea
        split is s_l:'aeiou', s_r:'uoiea'

char freqs required of final version of string A: {'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1}
processing s in reverse: aeiouuoiea...
        string A still requires 1 'a' chars
                after appending 'a', string A is: 'a'
        string A still requires 1 'e' chars
                after appending 'e', string A is: 'ae'
        string A still requires 1 'i' chars
                after appending 'i', string A is: 'aei'
        string A still requires 1 'o' chars
                after appending 'o', string A is: 'aeio'
        string A still requires 1 'u' chars
                after appending 'u', string A is: 'aeiou'
result: aeiou
expect: aeiou
```

Upon submission, all remaining locked test-cases passed.

## POST-MORTEM:

This was a tough puzzle primarily because the problem statement itself requires a lot of thought and study upfront in order to even get started.  If one does not properly understand the puzzle how can one solve the problem?  I didn't actually fully understand the problem on my own, initially.  It required consulting with others working on the same problem in order to do so.
