# Assignment 6: Medians and Order Statistics & Elementary Data Structures

## Author
Sandesh Ghimire


## How to Run

```bash
cd a6
python selection.py        # runs sanity check + empirical comparison
python data_structures.py  # demos all data structure operations
```

Requirements: Python 3.8+, no external packages.

## Summary

### Part 1 - Selection Algorithms
- Randomized Quickselect: O(n) expected, simple, fast in practice
- Deterministic (Median of Medians): O(n) worst case, but slower constants due to overhead of finding median of medians

### Part 2 - Data Structures
- Dynamic Array: O(1) access, O(n) insert/delete at arbitrary positions
- Stack: O(1) push/pop (array-based)
- Queue: O(1) enqueue, O(n) dequeue (array-based, tradeoff vs linked list)
- Linked List: O(1) insert at front, O(n) search/delete
