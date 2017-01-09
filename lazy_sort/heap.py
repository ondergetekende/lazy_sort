import heapq


def heap_sort(unsorted):
    # Copy the data
    unsorted = unsorted[:]

    return heap_sort_destructive(unsorted)


def heap_sort_destructive(items):
    heapq.heapify(items)

    while items:
        yield heapq.heappop(items)


def heap_sort_batch(unsorted):
    while unsorted:
        yield from heapq.nsmallest(100, unsorted)
