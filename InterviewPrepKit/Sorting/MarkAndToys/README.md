[link](https://www.hackerrank.com/challenges/mark-and-toys/problem?h_l=interview&isFullScreen=false&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D%5B%5D%5B%5D%5B%5D%5B%5D=sorting&h_r=next-challenge&h_v=zen)


## First Try:
This puzzle is straightforward.  Simply sort the array of prices.  Compute the cumulative sum of each price.  Continue advancing through the array of sorted prices doing this until the cumulative sum is >= k.  When this occurs we exit the loop.  With each iteration, each time this condition is not true, i.e. cumulative sum < k, we increment max_toys by 1.  All free test-cases pased based on this implementation. (see below)

```
def maximumToys(prices, k):
    debug = True

    if debug:
        print(f"prices: {prices}, k: {k}")

    max_toys = 0

    prices.sort()

    sum_prices = 0
    for p in prices:
        sum_prices += p
        if sum_prices >= k:
            break
        max_toys += 1

    return max_toys
```

ALL test-cases passed upon submission.

## POST-MORTEM:

It is important to note the subtlety of exactly what this puzzle is asking for.  Maximizing the number of toys means accumulating the greatest cumulative sum with the most items (toys).  This implies investigating the non-decreasing sequence of toy prices.  This obviously requires sorting.
