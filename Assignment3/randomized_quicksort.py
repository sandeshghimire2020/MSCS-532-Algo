import random
import time
import sys

sys.setrecursionlimit(50000)


def randomized_quicksort(arr):
    """Sort array using randomized quicksort (pivot chosen uniformly at random)."""
    if len(arr) <= 1:
        return arr
    pivot = arr[random.randint(0, len(arr) - 1)]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return randomized_quicksort(left) + middle + randomized_quicksort(right)


def deterministic_quicksort(arr):
    """Sort array using deterministic quicksort (first element as pivot)."""
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return deterministic_quicksort(left) + middle + deterministic_quicksort(right)


def measure_time(sort_func, arr, trials=3):
    """Measure average execution time over multiple trials."""
    total = 0.0
    for _ in range(trials):
        copy = arr[:]
        start = time.perf_counter()
        sort_func(copy)
        end = time.perf_counter()
        total += (end - start)
    return total / trials


def generate_inputs(n):
    """Generate four types of input arrays of size n."""
    random_arr = [random.randint(0, n * 10) for _ in range(n)]
    sorted_arr = list(range(n))
    reverse_arr = list(range(n, 0, -1))
    repeated_arr = [random.choice([1, 2, 3, 4, 5]) for _ in range(n)]
    return {
        "Random": random_arr,
        "Sorted": sorted_arr,
        "Reverse-sorted": reverse_arr,
        "Repeated elements": repeated_arr,
    }


def run_comparison():
    """Run the empirical comparison and print results."""
    sizes = [100, 500, 1000, 5000, 10000]
    print(f"{'Size':<8} {'Distribution':<20} {'Randomized QS (s)':<22} {'Deterministic QS (s)':<22}")
    print("-" * 75)

    results = []

    for n in sizes:
        inputs = generate_inputs(n)
        for dist_name, arr in inputs.items():
            rand_time = measure_time(randomized_quicksort, arr)
            det_time = measure_time(deterministic_quicksort, arr)
            print(f"{n:<8} {dist_name:<20} {rand_time:<22.6f} {det_time:<22.6f}")
            results.append((n, dist_name, rand_time, det_time))

    return results


if __name__ == "__main__":
    print("=" * 75)
    print("Empirical Comparison: Randomized vs Deterministic Quicksort")
    print("=" * 75)
    results = run_comparison()
    print("\nDone. See report for detailed analysis.")
