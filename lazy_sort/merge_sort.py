import heapq


def merge_sort(unsorted):
    # Don't sort already-sorted list
    if len(unsorted) <= 1:
        yield from unsorted
        return

    midpoint = len(unsorted) // 2

    yield from heapq.merge(
        merge_sort(unsorted[:midpoint]),
        merge_sort(unsorted[midpoint:])
    )
