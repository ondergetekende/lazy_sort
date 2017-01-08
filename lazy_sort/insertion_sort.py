def insertion_sort(unsorted):
    unsorted = list(unsorted)
    insertion_sort_inplace(unsorted)
    return unsorted


def insertion_sort_inplace(unsorted):
    if len(unsorted) <= 1:
        return

    for idx in range(1, len(unsorted)):
        # The array before idx is sorted. Now insert unsorted[idx] into it
        inserted = unsorted[idx]
        insert_to = idx

        while insert_to > 0 and inserted < unsorted[insert_to - 1]:
            unsorted[insert_to] = unsorted[insert_to - 1]
            insert_to -= 1
        unsorted[insert_to] = inserted
