[link](https://www.hackerrank.com/challenges/ctci-ransom-note/problem?h_l=interview&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D=dictionaries-hashmaps)


## First Try:

This is a very straightforward problem.  But I got the condition check wrong the first time.  (see below)

```python
def checkMagazine(magazine, note):
    debug = False

    if debug:
        print(f"magazine: {magazine}")
        print(f"note: {note}")

    d_magazine = {}
    for w in magazine:
        d_magazine[w] = d_magazine.get(w,0) + 1
    d_note = {}
    for w in note:
        d_note[w] = d_note.get(w,0) + 1

    if debug:
        print(f"d_magazine: {d_magazine}")
        print(f"d_note: {d_note}")

    for w_note, n_w_note in d_note.items():
        if w_note not in d_magazine.keys():
            print("No")
            return

        n_w_magazine = d_magazine[w_note]
        if n_w_note != n_w_magazine:    # WRONG!
            print("No")
            return

    # if we are here then the ransom note can be created from the magazine
    print("Yes")
```


# Second Try:

Fixed the condition check.  (see below)

ALL TEST CASES PASSED!

```python
def checkMagazine(magazine, note):
    debug = True

    if debug:
        print(f"magazine: {magazine}")
        print(f"note: {note}")

    d_magazine = {}
    for w in magazine:
        d_magazine[w] = d_magazine.get(w,0) + 1
    d_note = {}
    for w in note:
        d_note[w] = d_note.get(w,0) + 1

    if debug:
        print(f"d_magazine: {d_magazine}")
        print(f"d_note: {d_note}")

    for w_note, n_w_note in d_note.items():
        if w_note not in d_magazine.keys():
            print("No")
            return

        n_w_magazine = d_magazine[w_note]
        if n_w_note > n_w_magazine:
            print("No")
            return

    # if we are here then the ransom note can be created from the magazine
    print("Yes")
```


## POST-MORTEM:

Pay attention to conditions!