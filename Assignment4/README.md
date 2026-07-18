# Assignment 4: Heap Data Structures — Implementation, Analysis, and Applications

## Author
Sandesh Ghimire

## Overview
This repository contains Python implementations and a detailed analytical report for:

1. **Heapsort** — with empirical comparison against Quicksort and Merge Sort
2. **Priority Queue** — max-heap based, with a task scheduler simulation


## How to Run

### Prerequisites
- Python 3.8 or higher
- No external libraries required

### Running Heapsort Comparison
```bash
cd Assignment4
python heapsort.py
```
Runs Heapsort, Randomized Quicksort, and Merge Sort on arrays of sizes 100–10,000 across four distributions (random, sorted, reverse-sorted, repeated) and prints a comparison table.

### Running Priority Queue Simulation
```bash
cd cd Assignment4
python priority_queue.py
```
Demonstrates a task scheduler that inserts tasks with varying priorities, performs a priority boost, and processes all tasks in priority order.

## Summary of Findings

### Heapsort
- Achieves O(n log n) in all cases (worst, average, best), making it very predictable.
- Sorts in-place with O(1) auxiliary space.
- Slightly slower than Quicksort on random inputs due to poor cache locality, but never degrades to O(n²).

### Priority Queue
- All core operations (insert, extract_max, increase/decrease_key) run in O(log n).
- Array-based heap representation gives O(1) parent/child access and strong cache performance.
- The task scheduler simulation shows how priority queues naturally model real-world scheduling.

