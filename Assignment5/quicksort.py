import random
import time
import sys

sys.setrecursionlimit(50000)


def quicksort_deterministic(arr, low=0, high=None):
    """Standard quicksort using last element as pivot."""
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_idx = partition(arr, low, high)
        quicksort_deterministic(arr, low, pivot_idx - 1)
        quicksort_deterministic(arr, pivot_idx + 1, high)


def partition(arr, low, high):
    """Lomuto partition scheme - pivot is arr[high]."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ---- Randomized Quicksort ----

def quicksort_randomized(arr, low=0, high=None):
    """Quicksort with randomly chosen pivot."""
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_idx = randomized_partition(arr, low, high)
        quicksort_randomized(arr, low, pivot_idx - 1)
        quicksort_randomized(arr, pivot_idx + 1, high)


def randomized_partition(arr, low, high):
    """Pick a random element, swap it to the end, then do normal partition."""
    rand_idx = random.randint(low, high)
    arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
    return partition(arr, low, high)


# ---- Benchmarking ----

def time_sort(sort_func, arr, trials=3):
    """Average time over a few trials."""
    total = 0.0
    for _ in range(trials):
        copy = arr[:]
        start = time.perf_counter()
        sort_func(copy)
        elapsed = time.perf_counter() - start
        total += elapsed
    return total / trials


def generate_inputs(n):
    """Create different input distributions."""
    return {
        "Random": [random.randint(0, n * 10) for _ in range(n)],
        "Sorted": list(range(n)),
        "Reverse-sorted": list(range(n, 0, -1)),
        "Few unique": [random.choice(range(10)) for _ in range(n)],
    }


def run_benchmarks():
    """Run and print the comparison table."""
    sizes = [100, 500, 1000, 5000, 10000]

    print(f"{'n':<8} {'Distribution':<18} {'Deterministic (s)':<20} {'Randomized (s)':<20}")
    print("-" * 68)

    for n in sizes:
        inputs = generate_inputs(n)
        for name, arr in inputs.items():
            # for sorted/reverse on large n, deterministic will be slow (O(n^2))
            # skip if it would take too long
            if n > 5000 and name in ("Sorted", "Reverse-sorted"):
                det_time = "skipped (O(n^2))"
                rand_time = time_sort(quicksort_randomized, arr)
                print(f"{n:<8} {name:<18} {det_time:<20} {rand_time:<20.6f}")
            else:
                det_time = time_sort(quicksort_deterministic, arr)
                rand_time = time_sort(quicksort_randomized, arr)
                print(f"{n:<8} {name:<18} {det_time:<20.6f} {rand_time:<20.6f}")


if __name__ == "__main__":
    print("=" * 68)
    print("  Quicksort: Deterministic vs Randomized — Empirical Comparison")
    print("=" * 68)
    print()
    run_benchmarks()
    print()
    print("Done.")
