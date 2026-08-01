# stress_test.py - Shows where AVL beats plain BST: sorted/adversarial inputs

import time
import sys
sys.setrecursionlimit(200000)

from src.bst import FlightBST
from src.avl_tree import FlightAVL


def test_sorted_insertion():
    """Sorted input is the worst case for plain BST (becomes a linked list)."""
    print("--- Sorted Insertion: BST vs AVL ---")
    print("  (This is BST's worst case - it degenerates into a linked list)")
    print()

    sizes = [100, 500, 1000, 2000, 5000]
    print(f"  {'n':<8} {'BST insert':<14} {'AVL insert':<14} {'BST height':<12} {'AVL height':<12}")
    print("  " + "-" * 60)

    for n in sizes:
        # BST with sorted input
        bst = FlightBST()
        start = time.perf_counter()
        for i in range(n):
            bst.insert(i, {"id": i})
        bst_time = time.perf_counter() - start

        # AVL with sorted input
        avl = FlightAVL()
        start = time.perf_counter()
        for i in range(n):
            avl.insert(i, {"id": i})
        avl_time = time.perf_counter() - start

        # measure tree heights
        # bst height on sorted = n (basically a linked list)
        # avl height should be ~log2(n)
        bst_h = _get_height(bst.root)
        avl_h = avl.get_height()

        print(f"  {n:<8} {bst_time:<14.6f} {avl_time:<14.6f} {bst_h:<12} {avl_h:<12}")

    print()
    print("  BST degrades to O(n) height on sorted input.")
    print("  AVL stays at O(log n) height regardless of input order.")


def test_range_query_sorted():
    """Range query performance: BST vs AVL on sorted (worst-case) trees."""
    print("\n--- Range Query on Sorted Trees ---")
    sizes = [500, 1000, 2000, 5000]
    print(f"  {'n':<8} {'BST range (ms)':<16} {'AVL range (ms)':<16}")
    print("  " + "-" * 40)

    for n in sizes:
        bst = FlightBST()
        avl = FlightAVL()
        for i in range(n):
            bst.insert(i, {"id": i})
            avl.insert(i, {"id": i})

        # range query in the middle
        lo, hi = n // 4, 3 * n // 4

        start = time.perf_counter()
        for _ in range(50):
            bst.range_query(lo, hi)
        bst_time = (time.perf_counter() - start) / 50 * 1000

        start = time.perf_counter()
        for _ in range(50):
            avl.range_query(lo, hi)
        avl_time = (time.perf_counter() - start) / 50 * 1000

        print(f"  {n:<8} {bst_time:<16.4f} {avl_time:<16.4f}")


def _get_height(node):
    if node is None:
        return 0
    return 1 + max(_get_height(node.left), _get_height(node.right))


if __name__ == "__main__":
    print("=" * 60)
    print("  Stress Test: Adversarial Input (Sorted Data)")
    print("=" * 60)
    print()
    test_sorted_insertion()
    test_range_query_sorted()
    print("\nDone.")
