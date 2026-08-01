# selection.py - Order Statistics: Deterministic (Median of Medians) and Randomized Quickselect

import random
import time


# --- Randomized Quickselect ---

def randomized_select(arr, k):
    """Find the k-th smallest element using randomized pivot selection.
    k is 1-indexed (k=1 means smallest)."""
    if len(arr) == 1:
        return arr[0]

    pivot = arr[random.randint(0, len(arr) - 1)]
    lows = [x for x in arr if x < pivot]
    highs = [x for x in arr if x > pivot]
    pivots = [x for x in arr if x == pivot]

    if k <= len(lows):
        return randomized_select(lows, k)
    elif k <= len(lows) + len(pivots):
        return pivot
    else:
        return randomized_select(highs, k - len(lows) - len(pivots))


# --- Deterministic Selection (Median of Medians) ---

def deterministic_select(arr, k):
    """Find the k-th smallest element using median of medians.
    Guarantees O(n) worst case. k is 1-indexed."""
    if len(arr) <= 5:
        return sorted(arr)[k - 1]

    # split into groups of 5, find median of each
    chunks = [arr[i:i+5] for i in range(0, len(arr), 5)]
    medians = [sorted(chunk)[len(chunk) // 2] for chunk in chunks]

    # recursively find the median of medians
    pivot = deterministic_select(medians, len(medians) // 2 + 1)

    # partition around the pivot
    lows = [x for x in arr if x < pivot]
    highs = [x for x in arr if x > pivot]
    pivots = [x for x in arr if x == pivot]

    if k <= len(lows):
        return deterministic_select(lows, k)
    elif k <= len(lows) + len(pivots):
        return pivot
    else:
        return deterministic_select(highs, k - len(lows) - len(pivots))


# --- Benchmarking ---

def time_it(func, arr, k, trials=5):
    total = 0
    for _ in range(trials):
        copy = arr[:]
        start = time.perf_counter()
        func(copy, k)
        total += time.perf_counter() - start
    return total / trials


def run_comparison():
    sizes = [100, 1000, 5000, 10000, 50000]
    print(f"{'n':<10} {'Distribution':<16} {'Randomized (s)':<18} {'Deterministic (s)':<18}")
    print("-" * 64)

    for n in sizes:
        inputs = {
            "Random": [random.randint(0, n*10) for _ in range(n)],
            "Sorted": list(range(n)),
            "Reverse": list(range(n, 0, -1)),
        }
        for name, arr in inputs.items():
            k = n // 2  # find median
            t_rand = time_it(randomized_select, arr, k)
            t_det = time_it(deterministic_select, arr, k)
            print(f"{n:<10} {name:<16} {t_rand:<18.6f} {t_det:<18.6f}")


if __name__ == "__main__":
    # quick sanity check
    test = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    print("Test array:", test)
    print(f"  1st smallest (randomized): {randomized_select(test[:], 1)}")
    print(f"  6th smallest (randomized): {randomized_select(test[:], 6)}")
    print(f"  1st smallest (deterministic): {deterministic_select(test[:], 1)}")
    print(f"  6th smallest (deterministic): {deterministic_select(test[:], 6)}")
    print()

    print("=" * 64)
    print("  Empirical Comparison: Randomized vs Deterministic Selection")
    print("=" * 64)
    run_comparison()
    print("\nDone.")
