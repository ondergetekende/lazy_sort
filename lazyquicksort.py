import sys
import time
import random
import matplotlib.pyplot as plt

from lazy_sort.merge_sort import merge_sort
from lazy_sort.boramalper import lazysort
from lazy_sort.quick_sort import quicksort, quicksort_flat, quicksort_hybrid
from lazy_sort.insertion_sort import insertion_sort


def take(iterable, n):
    """Return the first few items of an iterator"""
    iterator = iter(iterable)
    while n > 0:
        # Just let the StopIteration bubble
        yield next(iterator)
        n -= 1


def benchmark_one(sort_fn, size, fraction, ints, verify=False):
    unsorted_ints = ints[:size]
    item_count = min(size, fraction)
    t0 = time.time()
    sorted_ints = iter(sort_fn(unsorted_ints))
    result = [next(sorted_ints) for _ in range(item_count)]
    duration = time.time() - t0

    if verify and result != sorted(unsorted_ints)[:item_count]:
        print()
        print(repr(sorted(unsorted_ints)[:item_count]))
        print(repr(result))
        assert False
    return duration


def do_benchmark():
    functions = [
        quicksort_flat,
        quicksort_hybrid,
        quicksort,
        lazysort,
        sorted,
        insertion_sort,
        merge_sort,
    ]

    r = random.Random(0)
    batch_unsorted_ints = [
        [r.randint(0, 1024) for _ in range(1 << 21)],
        [r.randint(0, 1024) for _ in range(1 << 21)],
        [r.randint(0, 1024) for _ in range(1 << 21)],
    ]

    sizes = [1 << i for i in range(5, 17)]
    sizes += [s * 3 for s in sizes if s > 100]
    sizes += [s * 5 for s in sizes if s > 100]
    sizes.sort()
    # sizes = range(1000, 50000, 1000)
    print("%20s" % "", end="")
    for size in sizes:
        print("%6i   " % size, end="")
    print()

    plt.xlabel("Number of Integers")
    plt.ylabel("Total ms spent")
    plt.axis([0, max(sizes), 0, 400])
    # plt.semilogx()
    # plt.semilogy()

    for sort_fn in functions:
        print("%20s" % sort_fn.__name__, end="")
        results = []
        for size in sizes:
            durations = [
                benchmark_one(sort_fn, size, 10, i) * 1000
                for i in batch_unsorted_ints
            ]
            durations.sort()
            duration = durations[1]
            results.append(duration)
            print("%6.1fms " % duration, end="")
            sys.stdout.flush()
            if duration > 2000:
                break
        plt.plot(sizes[:len(results)], results,
                 label=sort_fn.__name__)
        print()

    plt.legend()
    plt.show()


def do_detail_analysis_for(fn, test_sets):
    times = []
    for test_set in test_sets:
        t0 = time.time()
        times.append([time.time() - t0 for _ in fn(test_set)])
    return [sum(x) for x in zip(*times)]


def do_detail_analysis():
    r = random.Random(0)
    count = 1 << 16
    test_sets = [
        [r.randint(1, 10000) for _ in range(count)]
        for i in range(4)
        ]

    # Compute how much time is spent in iteration
    iter_times = do_detail_analysis_for(lambda x: x, test_sets)

    functions = [
        # quicksort_flat,
        # quicksort_hybrid,
        quicksort,
        # lazysort,
        sorted,
        # insertion_sort,
        # merge_sort,
    ]

    plt.xlabel("Percentage iterated")
    plt.ylabel("Cumulative time spent (s)")

    for fn in functions:
        times = [a - b for (a, b) in
                 zip(do_detail_analysis_for(fn, test_sets), iter_times)]

        plt.plot([100 * i / count for i in range(count)],
                 times,
                 label=fn.__name__)

    plt.legend()
    plt.show()


if __name__ == '__main__':
    # do_benchmark()
    do_detail_analysis()
