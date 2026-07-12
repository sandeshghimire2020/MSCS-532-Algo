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


def quick_sort_inplace(arr, low=0, high=None):
    """
    In-place version that matches textbook pseudocode.
    More space-efficient but slightly more complex.
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Partition and get pivot index
        pivot_index = partition(arr, low, high)
        
        # Recursively sort left and right partitions
        quick_sort_inplace(arr, low, pivot_index - 1)
        quick_sort_inplace(arr, pivot_index + 1, high)
    
    return arr


def partition(arr, low, high):
    """
    Partitions array around pivot (last element).
    Elements <= pivot go left, elements > pivot go right.
    """
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Place pivot in correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1