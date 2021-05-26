[link](https://www.hackerrank.com/challenges/ctci-array-left-rotation/problem?h_l=interview&playlist_slugs%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D=arrays)


## First Try:

I had to reconstruct my prior (successful) effort.  So, unfortunately, I do not have the narrative of my progress.  But here is the final successful implementation. (see below)

```
def rotLeft(a, d):
    a_left_rotated = []
    l = len(a)
    for i in range(l):
        a_left_rotated.append(a[(i+d) % l]) 
    
    return a_left_rotated
```


## POST-MORTEM:

(None.)