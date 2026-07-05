"""Insertion sort is carried out in monotonically decreasing order. 
This follows the structure of the algorithm outlined in Introduction to Algorithms, 
but modifies the comparison so that larger values are moved toward the front.
"""

from __future__ import annotations

from typing import List


def insertion_sort_descending(values: List[int]) -> List[int]:
    """Sort a list of integers in-place in decreasing order and return it."""

    for i in range(1, len(values)):
        key = values[i]
        j = i - 1

        while j >= 0 and values[j] < key:
            values[j + 1] = values[j]
            j -= 1

        values[j + 1] = key

    return values


def main() -> None:
    sample = [31, 41, 59, 26, 41, 58]
    sorted_values = insertion_sort_descending(sample)
    print(sorted_values)


if __name__ == "__main__":
    main()
