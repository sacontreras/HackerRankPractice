[link](https://www.hackerrank.com/challenges/sherlock-and-anagrams/problem?h_l=interview&h_r=next-challenge&h_v=zen&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=dictionaries-hashmaps&h_r=next-challenge&h_v=zen)


## First Try:

The logic goes like this. Base it on all substrings. First find them.  Then for each substring, sort it.  This forms the anagram "basis".  The dictionary is keyed by the anagram basis.  The "values" associated with an anagram basis will be the lists of indices of chars in the original string.  Thus, we can later reconstruct all anagrams associated with this basis.  The final answer will be the count of all unique anagram bases.

But, after submitting, we seem some test cases failing, in particular Test Case 01.  Expected 10, returned 3.

My debug output:
```
string: kkkk
{'k': [[0], [1], [2], [3]], 'kk': [[0, 1], [1, 2], [2, 3]], 'kkk': [[0, 1, 2], [1, 2, 3]], 'kkkk': [[0, 1, 2, 3]]}
anagrams: k k k k 
anagrams: kk kk kk 
anagrams: kkk kkk 
result: 3
expect: 10
```

(implementation below)

```
def sherlockAndAnagrams(s):
    debug = True

    if debug:
        print(f"string: {s}")

    l_s = len(s)
    d_s_sub_anagrams = {}
    for i_start in range(l_s):
        for i_end in range(i_start, l_s):
            sub_s = s[i_start:i_end+1]
            sub_s_arr_sorted = sorted(list(sub_s))
            sub_s_sorted = "".join(sub_s_arr_sorted)
            lst = d_s_sub_anagrams.get(sub_s_sorted,[])
            lst.append(list(range(i_start,i_end+1)))
            d_s_sub_anagrams[sub_s_sorted] = lst

    if debug:
        print(d_s_sub_anagrams)

    n_anagram_basis = 0
    lst_s = None
    if debug:
        lst_s = list(s)
    for _, lst_lst_indices in d_s_sub_anagrams.items():
        if len(lst_lst_indices) > 1:
            if debug:
                print("anagrams:", end=" ")
                for lst_indices in lst_lst_indices:
                    print("".join([lst_s[i] for i in lst_indices]), end=" ")
                print()
            n_anagram_basis += 1
        
    return n_anagram_basis
```


# Second Try:

It turns out that I was counting incorrectly. The following changes resulted in all test cases passing.  (see below)

```
def sherlockAndAnagrams(s):
    debug = False

    n_anagram_basis = 0

    l_s = len(s)

    if debug:
        print(f"string '{s}'")

    d_s_sub_anagrams_basis = {}
    for i_start in range(l_s):
        for i_end in range(i_start, l_s):
            sub_s = s[i_start:i_end+1]
            sub_s_arr_sorted = sorted(list(sub_s))
            sub_s_sorted = "".join(sub_s_arr_sorted)
            indices = list(range(i_start,i_end+1))
            if sub_s_sorted in d_s_sub_anagrams_basis:
                n_anagram_basis += len(d_s_sub_anagrams_basis[sub_s_sorted])
                lst = d_s_sub_anagrams_basis[sub_s_sorted]
                lst.append(indices)
                d_s_sub_anagrams_basis[sub_s_sorted] = lst
            else:
                d_s_sub_anagrams_basis[sub_s_sorted] = [indices]

    if debug:
        print(d_s_sub_anagrams_basis)
        
    return n_anagram_basis
```


## POST-MORTEM:

Pay close attention to examples and make sure they pass!