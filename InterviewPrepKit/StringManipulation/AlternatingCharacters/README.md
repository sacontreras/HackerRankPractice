[link](https://www.hackerrank.com/challenges/alternating-characters/problem?h_l=interview&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D=strings&h_r=next-challenge&h_v=zen)


## First Try:

This puzzle is fairly straightforward.  Dictionaries (Hash Tables) are your friend here.  The logic goes like this.  Create two dictionaries.  The first one is an enhanced character frequency table.  In it, we of course key by character and it will store the list of indices incident in the string.  The second dictionary, also keyed by character, will store the list of adjacent indices for a given character, up to the last one.  So, we enumerate the string, which will provide the index and character tuple.  For each index, character tuple in the string, get the list of associated incidence indices.  If it doesn't yet exist, create an empty list to store them.  If that list does exist and its length is greater than 0, get the last index (last element) from it.  If the last index is equal to the current index, minus 1, that we are iterating, then we know we have encountered adjacent indices.  Add the last index to the dictionarie which tracks the list of (adjacent) indices to be removed.  Finally, the total sum of characters to be removed will simply be the cumulative lengths of the lists in the second dictionary.  All of the free test-cases passed.  ALL test-cases passed upon submission.

(see below)

```python
def alternatingCharacters(s, debug=False):
    if debug:
        print(f"s: {s}")

    n_del_req = 0

    d_s_char_incidence = {}
    d_s_char_remove = {}
    for i,c in enumerate(s):
        lst_incidence = d_s_char_incidence.get(c,[])

        if len(lst_incidence) > 0:
            last_index = lst_incidence[-1]
            if last_index == i-1:
                lst_remove_at = d_s_char_remove.get(c,[])
                lst_remove_at.append(last_index)
                d_s_char_remove[c] = lst_remove_at

        lst_incidence.append(i)
        d_s_char_incidence[c] = lst_incidence

    if debug:
        print(f"d_s_char_incidence: {d_s_char_incidence}")
        print(f"d_s_char_remove: {d_s_char_remove}\n")

    for c, lst_remove_at in d_s_char_remove.items():
        n_del_req += len(lst_remove_at)

    return n_del_req
```

<p><br>

(Debug) Output for test-case 00:

```
s: AAAA
d_s_char_incidence: {'A': [0, 1, 2, 3]}
d_s_char_remove: {'A': [0, 1, 2]}

s: BBBBB
d_s_char_incidence: {'B': [0, 1, 2, 3, 4]}
d_s_char_remove: {'B': [0, 1, 2, 3]}

s: ABABABAB
d_s_char_incidence: {'A': [0, 2, 4, 6], 'B': [1, 3, 5, 7]}
d_s_char_remove: {}

s: BABABA
d_s_char_incidence: {'B': [0, 2, 4], 'A': [1, 3, 5]}
d_s_char_remove: {}

s: AAABBB
d_s_char_incidence: {'A': [0, 1, 2], 'B': [3, 4, 5]}
d_s_char_remove: {'A': [0, 1], 'B': [3, 4]}

expect: 3
result: 3

expect: 4
result: 4

expect: 0
result: 0

expect: 0
result: 0

expect: 4
result: 4
```

<p><br>

(Debug) Output for test-case 13:

```
s: AAABBBAABB
d_s_char_incidence: {'A': [0, 1, 2, 6, 7], 'B': [3, 4, 5, 8, 9]}
d_s_char_remove: {'A': [0, 1, 6], 'B': [3, 4, 8]}

s: AABBAABB
d_s_char_incidence: {'A': [0, 1, 4, 5], 'B': [2, 3, 6, 7]}
d_s_char_remove: {'A': [0, 4], 'B': [2, 6]}

s: ABABABAA
d_s_char_incidence: {'A': [0, 2, 4, 6, 7], 'B': [1, 3, 5]}
d_s_char_remove: {'A': [6]}

expect: 6
result: 6

expect: 4
result: 4

expect: 1
result: 1
```

<p><br>

(Debug) Output for test-case 15:

```
s: ABBABBAA
d_s_char_incidence: {'A': [0, 3, 6, 7], 'B': [1, 2, 4, 5]}
d_s_char_remove: {'B': [1, 4], 'A': [6]}

expect: 3
result: 3
```

## POST-MORTEM:

Once again, dictionaries (Hash Tables) are key.