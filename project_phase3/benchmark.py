# benchmark.py - Performance comparison: Phase 2 vs Phase 3 (optimized)
# Tests with progressively larger datasets to show scaling behavior

import time
import random
import sys

sys.setrecursionlimit(100000)

# import phase 2 originals
from src.trie import AirportTrie
from src.hash_table import FlightHashTable
from src.bst import FlightBST
from src.graph import FlightGraph

# import phase 3 optimized versions
from src.avl_tree import FlightAVL
from src.hash_table_optimized import OptimizedFlightHashTable


def generate_flights(n):
    """Generate n random flight records."""
    airports = ["JFK", "LAX", "ORD", "DEN", "MIA", "SFO", "ATL", "SEA", "DFW", "BOS",
                "PHX", "IAH", "MSP", "DTW", "FLL", "EWR", "CLT", "LAS", "MCO", "SLC"]
    airlines = ["AA", "UA", "DL", "SW", "B6", "NK", "AS", "F9"]

    flights = []
    for i in range(n):
        origin = random.choice(airports)
        dest = random.choice([a for a in airports if a != origin])
        price = random.randint(80, 900)
        flights.append({
            "flight": f"{random.choice(airlines)}{random.randint(100,9999)}",
            "origin": origin,
            "dest": dest,
            "date": "2024-12-15",
            "price": price,
            "depart": f"{random.randint(5,22):02d}:{random.choice(['00','15','30','45'])}",
            "duration": random.randint(60, 400),
        })
    return flights


def bench_bst_vs_avl(flights):
    """Compare plain BST vs AVL tree for range queries."""
    print("\n--- BST vs AVL Tree ---")
    sizes = [100, 1000, 5000, 10000, 50000]

    print(f"  {'n':<8} {'BST insert':<14} {'AVL insert':<14} {'BST range':<14} {'AVL range':<14}")
    print("  " + "-" * 56)

    for n in sizes:
        subset = flights[:n] if n <= len(flights) else flights

        # BST
        bst = FlightBST()
        start = time.perf_counter()
        for f in subset:
            bst.insert(f["price"], f)
        bst_insert = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(100):
            bst.range_query(200, 500)
        bst_range = (time.perf_counter() - start) / 100

        # AVL
        avl = FlightAVL()
        start = time.perf_counter()
        for f in subset:
            avl.insert(f["price"], f)
        avl_insert = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(100):
            avl.range_query(200, 500)
        avl_range = (time.perf_counter() - start) / 100

        print(f"  {n:<8} {bst_insert:<14.6f} {avl_insert:<14.6f} {bst_range:<14.6f} {avl_range:<14.6f}")


def bench_hash_tables(flights):
    """Compare original vs optimized hash table."""
    print("\n--- Hash Table: Original vs Optimized ---")
    sizes = [100, 1000, 5000, 10000, 50000]

    print(f"  {'n':<8} {'Orig insert':<14} {'Opt insert':<14} {'Orig lookup':<14} {'Opt lookup':<14}")
    print("  " + "-" * 56)

    for n in sizes:
        subset = flights[:n] if n <= len(flights) else flights

        # Original
        ht = FlightHashTable()
        start = time.perf_counter()
        for f in subset:
            key = f["origin"] + "_" + f["dest"] + "_" + f["date"]
            ht.put(key, f)
        orig_insert = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(1000):
            ht.get("JFK_LAX_2024-12-15")
        orig_lookup = (time.perf_counter() - start) / 1000

        # Optimized
        oht = OptimizedFlightHashTable()
        start = time.perf_counter()
        for f in subset:
            key = f["origin"] + "_" + f["dest"] + "_" + f["date"]
            oht.put(key, f)
        opt_insert = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(1000):
            oht.get("JFK_LAX_2024-12-15")
        opt_lookup = (time.perf_counter() - start) / 1000

        print(f"  {n:<8} {orig_insert:<14.6f} {opt_insert:<14.6f} {orig_lookup:<14.6f} {opt_lookup:<14.6f}")


def bench_trie(flights):
    """Benchmark trie with larger airport datasets."""
    print("\n--- Trie Autocomplete Scaling ---")
    trie = AirportTrie()
    # insert a bunch of city names
    cities = ["New York", "Los Angeles", "Chicago", "Denver", "Miami", "San Francisco",
              "Atlanta", "Seattle", "Dallas", "Boston", "Phoenix", "Houston",
              "Minneapolis", "Detroit", "Fort Lauderdale", "Newark", "Charlotte",
              "Las Vegas", "Orlando", "Salt Lake City", "San Diego", "San Antonio",
              "San Jose", "Sacramento", "Santa Fe", "Savannah", "Nashville",
              "New Orleans", "Norfolk", "Newport"]
    for city in cities:
        trie.insert(city.lower(), {"name": city + " Airport", "city": city})

    prefixes = ["s", "sa", "san", "new", "n", "de"]
    print(f"  {'Prefix':<10} {'Results':<10} {'Time (µs)':<12}")
    print("  " + "-" * 32)
    for p in prefixes:
        start = time.perf_counter()
        for _ in range(1000):
            results = trie.starts_with(p)
        elapsed = (time.perf_counter() - start) / 1000 * 1_000_000
        print(f"  {p:<10} {len(results):<10} {elapsed:<12.2f}")


def bench_graph(flights):
    """Benchmark graph route finding at different scales."""
    print("\n--- Graph: Route Finding at Scale ---")
    sizes = [100, 1000, 5000, 10000]

    print(f"  {'n routes':<10} {'BFS (ms)':<12} {'Dijkstra (ms)':<14}")
    print("  " + "-" * 36)

    for n in sizes:
        g = FlightGraph()
        for f in flights[:n]:
            g.add_route(f["origin"], f["dest"], f["price"], f)

        # BFS
        start = time.perf_counter()
        for _ in range(100):
            g.bfs_shortest_path("JFK", "SFO")
        bfs_time = (time.perf_counter() - start) / 100 * 1000

        # Dijkstra
        start = time.perf_counter()
        for _ in range(100):
            g.dijkstra("JFK", "SFO")
        dijk_time = (time.perf_counter() - start) / 100 * 1000

        print(f"  {n:<10} {bfs_time:<12.4f} {dijk_time:<14.4f}")


if __name__ == "__main__":
    print("=" * 60)
    print("  Phase 3: Performance Benchmarks - Before vs After")
    print("=" * 60)

    # generate a big dataset
    print("\nGenerating 50,000 random flights...")
    all_flights = generate_flights(50000)
    print("Done.\n")

    bench_bst_vs_avl(all_flights)
    bench_hash_tables(all_flights)
    bench_trie(all_flights)
    bench_graph(all_flights)

    print("\n" + "=" * 60)
    print("  Benchmarks complete.")
    print("=" * 60)
