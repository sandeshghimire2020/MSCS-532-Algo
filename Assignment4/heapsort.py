import random
import time
import sys

sys.setrecursionlimit(50000)


# --------------- Heapsort ---------------

def heapsort(arr):
    """Sort array in-place using Heapsort (max-heap based)."""
    n = len(arr)

    # Build max-heap (start from last non-leaf node)
    for i in range(n // 2 - 1, -1, -1):
        _max_heapify(arr, n, i)

    # Extract elements one by one from the heap
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _max_heapify(arr, i, 0)

    return arr


def _max_heapify(arr, heap_size, i):
    """Maintain the max-heap property for the subtree rooted at index i."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < heap_size and arr[left] > arr[largest]:
        largest = left
    if right < heap_size and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _max_heapify(arr, heap_size, largest)


# --------------- Quicksort (randomized) ---------------

def quicksort(arr):
    """Randomized Quicksort for comparison purposes."""
    if len(arr) <= 1:
        return arr
    pivot = arr[random.randint(0, len(arr) - 1)]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


# --------------- Merge Sort ---------------

def merge_sort(arr):
    """Standard Merge Sort implementation."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    """Merge two sorted arrays."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# --------------- Benchmarking ---------------

def measure_time(sort_func, arr, in_place=False, trials=3):
    """Measure average execution time over multiple trials."""
    total = 0.0
    for _ in range(trials):
        copy = arr[:]
        start = time.perf_counter()
        if in_place:
            sort_func(copy)
        else:
            sort_func(copy)
        end = time.perf_counter()
        total += (end - start)
    return total / trials


def generate_inputs(n):
    """Generate four types of input arrays of size n."""
    return {
        "Random": [random.randint(0, n * 10) for _ in range(n)],
        "Sorted": list(range(n)),
        "Reverse-sorted": list(range(n, 0, -1)),
        "Repeated elements": [random.choice([1, 2, 3, 4, 5]) for _ in range(n)],
    }


def run_comparison():
    """Run the empirical comparison and print results."""
    sizes = [100, 500, 1000, 5000, 10000]
    header = f"{'Size':<8} {'Distribution':<20} {'Heapsort (s)':<18} {'Quicksort (s)':<18} {'Merge Sort (s)':<18}"
    print(header)
    print("-" * len(header))

    results = []
    for n in sizes:
        inputs = generate_inputs(n)
        for dist_name, arr in inputs.items():
            hs_time = measure_time(heapsort, arr, in_place=True)
            qs_time = measure_time(quicksort, arr)
            ms_time = measure_time(merge_sort, arr)
            print(f"{n:<8} {dist_name:<20} {hs_time:<18.6f} {qs_time:<18.6f} {ms_time:<18.6f}")
            results.append((n, dist_name, hs_time, qs_time, ms_time))

    return results


if __name__ == "__main__":
    print("=" * 82)
    print("Empirical Comparison: Heapsort vs Quicksort vs Merge Sort")
    print("=" * 82)
    results = run_comparison()
    print("\nDone. See report for detailed analysis.")
