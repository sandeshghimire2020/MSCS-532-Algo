# Assignment 3: Understanding Algorithm Efficiency and Scalability

## Author
Sandesh Ghimire

## Overview
This repository contains Python implementations and an analytical report for two fundamental algorithms:

1. **Randomized Quicksort** — with empirical comparison against Deterministic Quicksort
2. **Hash Table with Chaining** — with dynamic resizing and a universal hash function


## How to Run

### Prerequisites
- Python 3.8 or higher
- No external libraries required (uses only Python standard library)

### Running Quicksort Comparison
```bash
cd assignment3
python randomized_quicksort.py
```
This will run both Randomized and Deterministic Quicksort on arrays of varying sizes (100 to 10,000) across four distributions (random, sorted, reverse-sorted, repeated elements) and print a comparison table.

### Running Hash Table Demo
```bash
cd a3
python hash_table_chaining.py
```
This will demonstrate insert, search, delete, and update operations on the hash table with sample data.

## Summary of Findings

### Quicksort
- **Randomized Quicksort** consistently achieves O(n log n) performance across all input distributions because the random pivot selection avoids worst-case partitioning.
- **Deterministic Quicksort** (first-element pivot) degrades to O(n²) on sorted and reverse-sorted inputs, as the pivot always lands at an extreme position.
- On random and repeated-element inputs, both algorithms perform comparably.

### Hash Table with Chaining
- Under simple uniform hashing, expected time for insert, search, and delete is O(1 + α), where α is the load factor.
- Dynamic resizing keeps the load factor bounded, ensuring amortized O(1) operations.
- The universal hash function family minimizes collision probability regardless of input distribution.

