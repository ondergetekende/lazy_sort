import typing
import itertools

import heapq


def lazysort(l: list) -> typing.Iterator:
    # Stage 1
    stack = []
    current_list = iter(l)
    sentinel = object()
    first = next(current_list, sentinel)
    while first is not sentinel:
        sortedish, surplus = dropsort(itertools.chain((first,), current_list))
        stack.append(sortedish)
        current_list = surplus
        first = next(current_list, sentinel)

    # Stage 2
    if len(stack) < 2:  # the case where the list `l` is already sorted
        return iter(l)

    cur = heapq.merge(stack.pop(), stack.pop())
    while stack:
        cur = heapq.merge(cur, stack.pop())

    return cur


def dropsort(s: typing.Iterable):
    def result_iterator(seq: typing.Iterator):
        last_element = next(seq)
        yield last_element

        while True:
            current_element = next(seq)
            if current_element >= last_element:
                last_element = current_element
                yield last_element

    def surplus_iterator(seq: typing.Iterator):
        last_element = next(seq)

        while True:
            current_element = next(seq)
            if current_element >= last_element:
                last_element = current_element
            else:
                yield current_element

    it1, it2 = itertools.tee(s, 2)
    return result_iterator(it1), surplus_iterator(it2)