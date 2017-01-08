Lazy sorting in python
======================

A common need when working with data, is to find the top 10 in a larger list. An easy solution is to use the built-in sort function to sort the entire list, and then just take the first 10 items. While this works, it feels wasteful. Other than knowing what _is_ the tail, you're not interested in the tail of the list at all.

January 2017, Bora M. Alper [posted](https://www.reddit.com/r/Python/comments/5mpmj8) his [take](https://github.com/boramalper/lazysort) on this problem: `lazysort`. Using python generators, he sorted the list using dropsort as needed, returning just the part of the list that was requested. While Bora's idea is quite neat, sadly his benchmark showed that it couldn't actually compete with using python's built-in sort function. This is not very surprising, cpython's `sorted` function uses the state-of-the-art TimSort algorithm, and it is implemented in optimized C.

But his approach gave me inspiration. While I feel dropsort is sort of a gimmick, Bora might actually be on to something here. During my time as a game developer, I built an early-out version of quicksort, which returned as soon as the head of the list was sorted. We should be able to build a something similar using python generators.

A generator-based quicksort could look like this:

```python
def partition(unsorted):
    sublist_length = len(unsorted)
    if sublist_length <= 1:
        return unsorted, ()

    pivot = unsorted[0]
    lhs = []
    rhs = []

    for idx in range(1, sublist_length):
        finger = unsorted[idx]
        if finger < pivot:
            lhs.append(finger)
        else:
            rhs.append(finger)

    lhs.append(pivot)
    return lhs, pivot, rhs


def quicksort(unsorted):
    if len(unsorted) < 2:
        yield from unsorted
    else:
        lhs, rhs = partition(unsorted)
        yield from quicksort(lhs)
        del lhs  # release memory used by lhs
        yield pivot
        yield from quicksort(rhs)
```

For the uninitiated: quicksort works by splitting lists in two parts: one list with all items smaller than some pivot value, one with all items larger than that pivot value, and then repeating that procedure on both lists. Splitting the lists is the task of the partition function. 

When comparing my implementation to lazy sort and the built-in `sorted` function, you can clearly see that while Bora's `lazysort` can't compete, his idea is sound. (This benchmark was based on retrieving the top 10 from a list of integers).

<a href="images/sort_results1.png" title="Finding top 10 in a list of integers" width="200" height="150"><img src="images/sort_results1.png" alt="Triangle"></a>

If we remove `lazysort` from the chart, we can clearly see that my generator-based quicksort can indeed a bit faster than the built-in `sorted` function, if we only need the first 10 items.

<a href="images/sort_results2.png" title="Finding top 10 in a list of integers" width="200" height="150"><img src="images/sort_results2.png"></a>

Further Analysis
================

Now that we know we can beat `sorted`, let's see why this is. A lazy sorting algorithm only has benefit when it can decide not to do some work. In quicksort's case, not having to sort the right partition severaltimes in a row is a huge benefit. But where's the cut-off when sorting items?

<a href="images/sort_results3.png" title="Finding top 10 in a list of integers" width="200" height="150"><img src="images/sort_results3.png"></a>

That's disapointing. If you just need the first few percent, lazy `quicksort` can help you out, but beyond that, you're probably better off sorting the entire list.

Possible performance improvements
=================================

IMHO, first course of action would be to port this code to C; that's where performant low-level code lives; and that's were our benchmark `sorted` is implemented. This code can benefit significantly from pointer arithmatic, which is not an option in Python.

The algorithm itself can also be improved. Quicksort is known to be highly performant on large lists, but have poor performance on short lists. Quicksort could internally fall back to (e.g.) mergesort or bubblesort for short lists. This could make sorting the inner lists a bit faster. Also, one needn't use Python's call stack for recursion, a lighter structure may yield better performance, too.

Possible feature improvements
=============================

Currently support for `sorted`'s `key` and `reverse` parameters is lacking, but those are trivial to add.

Lazy Quicksort could fake an list-like interface. The current implementation only sorts the head, but the priciple applies to any part of the sorted list. This coult speed up computation of median values, and percentiles.
