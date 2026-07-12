import time
import random
import matplotlib.pyplot as plt
import numpy as np

# ============== MERGESORT IMPLEMENTATION ==============
def merge_sort(arr):
    """
    Sorts array using merge sort divide-and-conquer approach.
    Time: O(n log n) guaranteed
    Space: O(n) for temporary arrays during merging
    """
    if len(arr) <= 1:
        return arr
    
    # DIVIDE: split into two halves
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    # CONQUER: recursively sort both halves
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)
    
    # COMBINE: merge the sorted halves
    return merge(left_sorted, right_sorted)


def merge(left, right):
    """
    Merges two sorted arrays into one sorted array.
    Takes O(n) time where n = len(left) + len(right)
    """
    result = []
    i = j = 0
    
    # Compare elements from left and right, add smaller
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining elements (one array will be empty)
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


# ============== QUICKSORT IMPLEMENTATION ==============
def quick_sort(arr):
    """
    Sorts array using quicksort divide-and-conquer approach.
    Average: O(n log n)
    Worst: O(n²) - rare with good pivot selection
    Space: O(log n) for recursion stack (not counting output)
    """
    if len(arr) <= 1:
        return arr
    
    # DIVIDE: partition around a pivot
    pivot = arr[len(arr) // 2]  # Better than first/last
    
    # Split into three groups
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]  # Handle duplicates
    right = [x for x in arr if x > pivot]
    
    # CONQUER: recursively sort partitions, then combine
    return quick_sort(left) + middle + quick_sort(right)


# ============== TEST FRAMEWORK ==============
def generate_test_data(n, data_type='random'):
    """Generate different test datasets"""
    if data_type == 'random':
        return [random.randint(0, n*10) for _ in range(n)]
    elif data_type == 'sorted':
        return list(range(n))
    elif data_type == 'reverse':
        return list(range(n, 0, -1))
    elif data_type == 'nearly_sorted':
        arr = list(range(n))
        # Swap 5% of elements
        for _ in range(n // 20):
            i, j = random.sample(range(n), 2)
            arr[i], arr[j] = arr[j], arr[i]
        return arr


def measure_time(sort_function, arr, num_trials=3):
    """Measure average execution time over multiple trials"""
    times = []
    for _ in range(num_trials):
        arr_copy = arr.copy()
        start = time.perf_counter()
        sort_function(arr_copy)
        end = time.perf_counter()
        times.append(end - start)
    return np.mean(times)


def run_comprehensive_test():
    """Run full comparison across all scenarios"""
    
    sizes = [100, 500, 1000, 5000, 10000]
    data_types = ['random', 'sorted', 'reverse']
    
    results = {
        'merge_sort': {dt: [] for dt in data_types},
        'quick_sort': {dt: [] for dt in data_types}
    }
    
    for size in sizes:
        print(f"\nTesting size: {size}")
        
        for data_type in data_types:
            test_data = generate_test_data(size, data_type)
            
            # Test MergeSort
            merge_time = measure_time(merge_sort, test_data)
            results['merge_sort'][data_type].append(merge_time)
            print(f"  MergeSort ({data_type:10}): {merge_time*1000:.3f} ms")
            
            # Test QuickSort
            quick_time = measure_time(quick_sort, test_data)
            results['quick_sort'][data_type].append(quick_time)
            print(f"  QuickSort ({data_type:10}): {quick_time*1000:.3f} ms")
    
    return sizes, results


# ============== RUN TESTS ==============
if __name__ == "__main__":
    sizes, results = run_comprehensive_test()

    # Create comparison plots
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    for idx, data_type in enumerate(['random', 'sorted', 'reverse']):
        ax = axes[idx]
        
        merge_times = results['merge_sort'][data_type]
        quick_times = results['quick_sort'][data_type]
        
        ax.plot(sizes, merge_times, 'o-', label='MergeSort', linewidth=2, markersize=8)
        ax.plot(sizes, quick_times, 's-', label='QuickSort', linewidth=2, markersize=8)
        
        ax.set_xlabel('Array Size', fontsize=11)
        ax.set_ylabel('Time (seconds)', fontsize=11)
        ax.set_title(f'{data_type.capitalize()} Data', fontsize=12, weight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

    plt.suptitle('MergeSort vs QuickSort Performance Comparison', 
                 fontsize=14, weight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('algorithm_comparison.png', dpi=300, bbox_inches='tight')
    print("\n✓ Graph saved as 'algorithm_comparison.png'")
    plt.show()