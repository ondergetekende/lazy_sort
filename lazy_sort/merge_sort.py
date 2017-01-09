import heapq


# def merge_sort(unsorted):
#     # Don't sort already-sorted list
#     if len(unsorted) <= 1:
#         yield from unsorted
#         return

#     midpoint = len(unsorted) // 2

#     yield from heapq.merge(
#         merge_sort(unsorted[:midpoint]),
#         merge_sort(unsorted[midpoint:])
#     )

def merge_sort(unsorted, start=None, end=None):
    if start is None:
        start = 0
        end = len(unsorted)

    midpoint = (start + end) // 2

    if end - start == 1:
        yield unsorted[start]
    elif end - start > 1:
        yield from heapq.merge(
            merge_sort(unsorted, start, midpoint),
            merge_sort(unsorted, midpoint, end))
