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