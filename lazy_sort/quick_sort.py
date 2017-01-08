
def partition(unsorted):
    sublist_length = len(unsorted)

    pivot = unsorted[0]

    if sublist_length == 1:
        return (), unsorted[0], ()

    lhs = []
    rhs = []

    for idx in range(1, sublist_length):
        finger = unsorted[idx]
        if finger < pivot:
            lhs.append(finger)
        else:
            rhs.append(finger)

    return lhs, pivot, rhs


def quicksort(unsorted):
    if len(unsorted) < 2:
        yield from unsorted
    else:
        lhs, pivot, rhs = partition(unsorted)
        yield from quicksort(lhs)
        del lhs  # release memory used by lhs
        yield pivot
        yield from quicksort(rhs)


def quicksort_hybrid(unsorted):
    if len(unsorted) < 16:
        unsorted.sort()
        yield from unsorted
    else:
        lhs, pivot, rhs = partition(unsorted)
        yield from quicksort(lhs)
        del lhs  # release memory used by lhs
        yield pivot
        yield from quicksort(rhs)


def quicksort_flat(unsorted):
    # unsorted stack contains a list of 2-tuples: an unsorted list and a
    # sorted list. The sorted list is actually the pivot from the partition fn.
    # Because of this stack, quicksort doesn't need to be recursive
    unsorted_stack = [unsorted]

    while unsorted_stack:
        unsorted = unsorted_stack.pop()
        lhs, pivot, rhs = partition(unsorted)
        if len(lhs) <= 1:
            yield from lhs
            yield pivot

            if len(rhs) <= 1:
                yield from rhs
            else:
                unsorted_stack.append(rhs)

        else:
            lhs.append(pivot)
            if rhs:
                unsorted_stack.append(rhs)
            unsorted_stack.append(lhs)
