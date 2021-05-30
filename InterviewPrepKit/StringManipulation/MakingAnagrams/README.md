[link](https://www.hackerrank.com/challenges/ctci-making-anagrams/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=strings)


## First Try:

This puzzle is very straightforward.  It requires character frequencies.  Thus, dictionaries (Hash Tables) should be used.  After their creation, count the number of characters from each in the complement of their intersection - i.e. the sets of disjoint characters.  Then, after that, count the differences between remaining characters in common.  Simple.

(see below)

```
def makeAnagram(a, b, debug=False):
    if debug:
        print(f"a: {a}, b: {b}")
    
    n_del_req = 0

    d_a_freq = {}
    for c in a:
        d_a_freq[c] = d_a_freq.get(c,0) + 1
    d_b_freq = {}
    for c in b:
        d_b_freq[c] = d_b_freq.get(c,0) + 1
    if debug:
        print(f"d_a_freq: {d_a_freq}")
        print(f"d_b_freq: {d_b_freq}")

    chars_in_common = set(d_a_freq.keys()) & set(d_b_freq.keys())
    if debug:
        print(f"chars_in_common: {chars_in_common}")

    for c in (set(d_a_freq.keys()) - chars_in_common):
        n_c = d_a_freq[c]
        if debug:
            print(f"{n_c} instances of '{c}' must be deleted from a")
        n_del_req += n_c
    for c in (set(d_b_freq.keys()) - chars_in_common):
        n_c = d_b_freq[c]
        if debug:
            print(f"{n_c} instances of '{c}' must be deleted from b")
        n_del_req += n_c
    for c in chars_in_common:
        n_c_a = d_a_freq[c]
        n_c_b = d_b_freq[c]
        n_c_diff = max(n_c_a,n_c_b) - min(n_c_a,n_c_b)
        if debug and n_c_diff > 0:
            print(f"{n_c} disjoint instances of '{c}' must be deleted")
        n_del_req += n_c_diff
    
    return n_del_req
```

<p><br>

(Debug) Output for test-case 00:

```
a: cde, b: abc
d_a_freq: {'c': 1, 'd': 1, 'e': 1}
d_b_freq: {'a': 1, 'b': 1, 'c': 1}
chars_in_common: {'c'}
1 instances of 'd' must be deleted from a
1 instances of 'e' must be deleted from a
1 instances of 'a' must be deleted from b
1 instances of 'b' must be deleted from b
result: 4
expect: 4
```

<p><br>

(Debug) Output for test-case 01:

```
a: fcrxzwscanmligyxyvym, b: jxwtrhvujlmrpdoqbisbwhmgpmeoke
d_a_freq: {'f': 1, 'c': 2, 'r': 1, 'x': 2, 'z': 1, 'w': 1, 's': 1, 'a': 1, 'n': 1, 'm': 2, 'l': 1, 'i': 1, 'g': 1, 'y': 3, 'v': 1}
d_b_freq: {'j': 2, 'x': 1, 'w': 2, 't': 1, 'r': 2, 'h': 2, 'v': 1, 'u': 1, 'l': 1, 'm': 3, 'p': 2, 'd': 1, 'o': 2, 'q': 1, 'b': 2, 'i': 1, 's': 1, 'g': 1, 'e': 2, 'k': 1}
chars_in_common: {'l', 's', 'v', 'x', 'm', 'i', 'r', 'g', 'w'}
3 instances of 'y' must be deleted from a
2 instances of 'c' must be deleted from a
1 instances of 'z' must be deleted from a
1 instances of 'n' must be deleted from a
1 instances of 'f' must be deleted from a
1 instances of 'a' must be deleted from a
1 instances of 'q' must be deleted from b
1 instances of 'd' must be deleted from b
1 instances of 'u' must be deleted from b
1 instances of 't' must be deleted from b
2 instances of 'j' must be deleted from b
2 instances of 'h' must be deleted from b
2 instances of 'b' must be deleted from b
2 instances of 'e' must be deleted from b
2 instances of 'o' must be deleted from b
1 instances of 'k' must be deleted from b
2 instances of 'p' must be deleted from b
2 disjoint instances of 'x' must be deleted
2 disjoint instances of 'm' must be deleted
2 disjoint instances of 'r' must be deleted
2 disjoint instances of 'w' must be deleted
result: 30
expect: 30
```

<p><br>

(Debug) Output for test-case 15:

```
a: showman, b: woman
d_a_freq: {'s': 1, 'h': 1, 'o': 1, 'w': 1, 'm': 1, 'a': 1, 'n': 1}
d_b_freq: {'w': 1, 'o': 1, 'm': 1, 'a': 1, 'n': 1}
chars_in_common: {'w', 'n', 'o', 'm', 'a'}
1 instances of 's' must be deleted from a
1 instances of 'h' must be deleted from a
result: 2
expect: 2
```

## POST-MORTEM:

Dictionaries (Hash Tables) are key.