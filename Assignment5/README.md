# Assignment 5: Quicksort Algorithm — Implementation, Analysis, and Randomization

## Author
Sandesh Ghimire

## Overview
This repo contains Python implementations of both Deterministic and Randomized Quicksort, along with an empirical performance comparison and a detailed report.

## How to Run

### Requirements
- Python 3.8+
- No external packages needed

### Running the benchmark
```bash
cd a5
python quicksort.py
```

This prints a table comparing Deterministic Quicksort (last-element pivot) vs Randomized Quicksort (random pivot) on arrays of size 100–10,000 across four input types.

**Note:** On sorted/reverse-sorted arrays with n > 5000, the deterministic version is skipped because it would take too long (O(n²) behavior). You might also hit Python's recursion limit — the script sets it to 50,000.

## Key Findings

1. **Random/unstructured inputs**: Both versions perform about the same (~O(n log n)).
2. **Sorted/reverse-sorted inputs**: Deterministic version degrades to O(n²); randomized version stays at O(n log n).
3. **Randomization cost**: Negligible — one `random.randint()` call per recursion level.
4. **Practical takeaway**: Always use randomized pivot selection (or shuffle input beforehand) unless you can guarantee your input won't be nearly sorted.

