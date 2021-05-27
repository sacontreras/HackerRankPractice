[link](https://www.hackerrank.com/challenges/ctci-comparator-sorting/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=sorting)


## First Try:
This puzzle is fairly straightforward.  It only requires understanding of how comparators work.  That is, given objects a and b, return -1 if a < b, 1 if a > b, and 0 if a == b based on comparison rules.  Comparison rules are provided in problem description.  All free test-cases passed.  (see below)

```
from functools import cmp_to_key
class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score
        
    def __repr__(self):
        pass
        
    def comparator(a, b):
        if a.score > b.score:
            return -1

        elif a.score < b.score:
            return 1

        else: # scores are equal, compare based on name
            if a.name < b.name:
                return -1
            elif a.name > b.name:
                return 1
            else:
                return 0
```

ALL test-cases based on the above implementation passed upon submission.

## POST-MORTEM:

To reiterate, this puzzle is straightforward.  It only requires proper understanding of how comparators work.