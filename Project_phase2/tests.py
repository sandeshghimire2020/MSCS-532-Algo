# tests.py - basic tests for all the data structures

from src.trie import AirportTrie
from src.hash_table import FlightHashTable
from src.bst import FlightBST
from src.graph import FlightGraph


def test_trie():
    print("=== Trie Tests ===")
    t = AirportTrie()

    t.insert("JFK", {"name": "JFK Airport"})
    t.insert("JFK", {"name": "JFK Airport Updated"})
    assert t.search("jfk")["name"] == "JFK Airport Updated"
    assert t.search("xyz") is None
    print("  [PASS] insert and exact search")

    t.insert("LAX", {"name": "LAX Airport"})
    t.insert("LAS", {"name": "Las Vegas"})
    t.insert("LGA", {"name": "LaGuardia"})
    results = t.starts_with("la")
    keys = [r["key"] for r in results]
    assert "las" in keys and "lax" in keys
    print("  [PASS] prefix search")

    assert t.starts_with("zzz") == []
    print("  [PASS] no match returns empty")


def test_hash_table():
    print("\n=== Hash Table Tests ===")
    ht = FlightHashTable(capacity=4)

    ht.put("JFK_LAX", [{"flight": "AA100"}])
    assert ht.get("JFK_LAX") == [{"flight": "AA100"}]
    assert ht.get("nope") is None
    print("  [PASS] put and get")

    ht.put("JFK_LAX", [{"flight": "AA100"}, {"flight": "UA200"}])
    assert len(ht.get("JFK_LAX")) == 2
    print("  [PASS] update existing key")

    assert ht.delete("JFK_LAX") == True
    assert ht.get("JFK_LAX") is None
    assert ht.delete("JFK_LAX") == False
    print("  [PASS] delete")

    # test resizing
    for i in range(20):
        ht.put(f"key_{i}", f"val_{i}")
    assert len(ht) == 20
    assert ht.get("key_0") == "val_0"
    print(f"  [PASS] resize worked (capacity={ht.capacity})")


def test_bst():
    print("\n=== BST Tests ===")
    bst = FlightBST()

    bst.insert(300, {"flight": "AA100"})
    bst.insert(150, {"flight": "SW600"})
    bst.insert(400, {"flight": "DL900"})
    bst.insert(300, {"flight": "UA200"})  # dup key

    assert len(bst.search(300)) == 2
    assert bst.search(999) is None
    print("  [PASS] insert and search")

    bst.insert(200, {"flight": "B1"})
    bst.insert(250, {"flight": "B2"})
    bst.insert(350, {"flight": "B3"})

    assert len(bst.range_query(0, 250)) == 3
    assert len(bst.range_query(200, 350)) == 5
    assert len(bst.range_query(500, 600)) == 0
    print("  [PASS] range queries")

    inorder = bst.inorder()
    keys = [k for k, d in inorder]
    assert keys == sorted(keys)
    print("  [PASS] inorder is sorted")


def test_graph():
    print("\n=== Graph Tests ===")
    g = FlightGraph()
    g.add_route("JFK", "ORD", 180)
    g.add_route("ORD", "LAX", 220)
    g.add_route("JFK", "LAX", 320)
    g.add_route("JFK", "MIA", 210)
    g.add_route("MIA", "LAX", 280)

    # bfs
    path, stops = g.bfs_shortest_path("JFK", "LAX")
    assert path == ["JFK", "LAX"]
    print(f"  [PASS] BFS JFK->LAX: direct, {stops} stops")

    path, stops = g.bfs_shortest_path("LAX", "JFK")
    assert path is None
    print("  [PASS] BFS no path")

    # dijkstra
    path, cost = g.dijkstra("JFK", "LAX")
    assert cost == 320
    print(f"  [PASS] Dijkstra JFK->LAX: ${cost}")

    # make sure it picks cheaper multi-hop
    g2 = FlightGraph()
    g2.add_route("A", "B", 100)
    g2.add_route("B", "C", 100)
    g2.add_route("A", "C", 500)
    path, cost = g2.dijkstra("A", "C")
    assert path == ["A", "B", "C"] and cost == 200
    print(f"  [PASS] Dijkstra picks cheaper connection: ${cost}")

    path, cost = g2.dijkstra("C", "A")
    assert path is None
    print("  [PASS] Dijkstra no path")


if __name__ == "__main__":
    test_trie()
    test_hash_table()
    test_bst()
    test_graph()
    print("\nAll tests passed.")
