"""
Flight Search Engine - Proof of Concept Demo
Ties together all four data structures: Trie, Hash Table, BST, and Graph.
"""

from src.trie import AirportTrie
from src.hash_table import FlightHashTable
from src.bst import FlightBST
from src.graph import FlightGraph


def setup_data():
    """Load up sample airports and flights for the demo."""

    # -- Trie for autocomplete --
    trie = AirportTrie()
    airports = [
        ("JFK", {"name": "John F. Kennedy International", "city": "New York", "country": "US"}),
        ("LAX", {"name": "Los Angeles International", "city": "Los Angeles", "country": "US"}),
        ("ORD", {"name": "O'Hare International", "city": "Chicago", "country": "US"}),
        ("DEN", {"name": "Denver International", "city": "Denver", "country": "US"}),
        ("MIA", {"name": "Miami International", "city": "Miami", "country": "US"}),
        ("SFO", {"name": "San Francisco International", "city": "San Francisco", "country": "US"}),
        ("ATL", {"name": "Hartsfield-Jackson Atlanta", "city": "Atlanta", "country": "US"}),
        ("SEA", {"name": "Seattle-Tacoma International", "city": "Seattle", "country": "US"}),
        ("DFW", {"name": "Dallas/Fort Worth International", "city": "Dallas", "country": "US"}),
        ("BOS", {"name": "Logan International", "city": "Boston", "country": "US"}),
    ]
    for code, info in airports:
        trie.insert(code, info)
        trie.insert(info["city"].lower(), info)

    # -- Hash table for flight lookups --
    flight_table = FlightHashTable()
    flights = [
        {"flight": "AA100", "origin": "JFK", "dest": "LAX", "date": "2024-12-15", "price": 320, "depart": "08:00", "duration": 330},
        {"flight": "UA200", "origin": "JFK", "dest": "LAX", "date": "2024-12-15", "price": 375, "depart": "11:30", "duration": 345},
        {"flight": "DL300", "origin": "JFK", "dest": "LAX", "date": "2024-12-15", "price": 290, "depart": "14:00", "duration": 320},
        {"flight": "AA150", "origin": "JFK", "dest": "ORD", "date": "2024-12-15", "price": 180, "depart": "07:00", "duration": 150},
        {"flight": "UA250", "origin": "ORD", "dest": "LAX", "date": "2024-12-15", "price": 220, "depart": "12:00", "duration": 240},
        {"flight": "DL350", "origin": "JFK", "dest": "MIA", "date": "2024-12-15", "price": 210, "depart": "09:00", "duration": 180},
        {"flight": "AA400", "origin": "MIA", "dest": "LAX", "date": "2024-12-15", "price": 280, "depart": "15:00", "duration": 300},
        {"flight": "UA500", "origin": "DEN", "dest": "MIA", "date": "2024-12-15", "price": 250, "depart": "06:00", "duration": 240},
        {"flight": "SW600", "origin": "DEN", "dest": "LAX", "date": "2024-12-15", "price": 150, "depart": "10:00", "duration": 180},
        {"flight": "AA700", "origin": "LAX", "dest": "SFO", "date": "2024-12-15", "price": 95, "depart": "16:00", "duration": 75},
        {"flight": "DL800", "origin": "ATL", "dest": "JFK", "date": "2024-12-15", "price": 175, "depart": "06:30", "duration": 140},
        {"flight": "UA900", "origin": "SEA", "dest": "DEN", "date": "2024-12-15", "price": 200, "depart": "08:00", "duration": 180},
    ]
    for f in flights:
        route_key = f["origin"] + "_" + f["dest"] + "_" + f["date"]
        existing = flight_table.get(route_key)
        if existing:
            existing.append(f)
        else:
            flight_table.put(route_key, [f])
        # also index by flight number for direct lookups
        flight_table.put(f["flight"], f)

    # -- BST for price filtering --
    price_tree = FlightBST()
    for f in flights:
        price_tree.insert(f["price"], f)

    # -- Graph for route finding --
    graph = FlightGraph()
    for code, info in airports:
        graph.add_airport(code)
    for f in flights:
        graph.add_route(f["origin"], f["dest"], f["price"], f)

    return trie, flight_table, price_tree, graph


def demo():
    trie, flight_table, price_tree, graph = setup_data()

    print("=" * 65)
    print("  Flight Search Engine - Proof of Concept Demo")
    print("=" * 65)

    # 1. Autocomplete
    print("\n--- 1. Airport Autocomplete (Trie) ---")
    for prefix in ["j", "d", "new", "san"]:
        matches = trie.starts_with(prefix)
        names = [m["data"]["name"] for m in matches if m["data"]]
        print(f"  '{prefix}' -> {names}")

    print(f"  Exact 'JFK': {trie.search('jfk')}")
    print(f"  Exact 'XYZ': {trie.search('xyz')}")

    # 2. Hash table lookups
    print("\n--- 2. Flight Lookup (Hash Table) ---")
    key = "JFK_LAX_2024-12-15"
    results = flight_table.get(key)
    print(f"  Flights for {key}: {len(results)} found")
    for f in results:
        print(f"    {f['flight']}: ${f['price']}, departs {f['depart']}")

    print(f"  AA100: {flight_table.get('AA100')}")
    print(f"  XY999: {flight_table.get('XY999')}")

    # 3. Range queries
    print("\n--- 3. Price Range Query (BST) ---")
    cheap = price_tree.range_query(0, 200)
    print(f"  Under $200: {len(cheap)} flights")
    for price, f in sorted(cheap):
        print(f"    ${price}: {f['flight']} ({f['origin']}->{f['dest']})")

    mid = price_tree.range_query(250, 350)
    print(f"  $250-$350: {len(mid)} flights")
    for price, f in sorted(mid):
        print(f"    ${price}: {f['flight']} ({f['origin']}->{f['dest']})")

    # 4. Route finding
    print("\n--- 4. Route Optimization (Graph) ---")
    path, stops = graph.bfs_shortest_path("DEN", "MIA")
    print(f"  Fewest stops DEN->MIA: {' -> '.join(path)} ({stops} connections)")

    path, stops = graph.bfs_shortest_path("SEA", "LAX")
    print(f"  Fewest stops SEA->LAX: {' -> '.join(path)} ({stops} connections)")

    path, cost = graph.dijkstra("JFK", "LAX")
    print(f"  Cheapest JFK->LAX: {' -> '.join(path)}, ${cost}")

    path, cost = graph.dijkstra("SEA", "SFO")
    print(f"  Cheapest SEA->SFO: {' -> '.join(path)}, ${cost}")

    # 5. Integrated search
    print("\n--- 5. Integrated: 'JFK to LAX under $400' ---")
    origin = trie.search("jfk")
    dest = trie.search("lax")
    print(f"  From: {origin['name']}")
    print(f"  To: {dest['name']}")

    direct = flight_table.get("JFK_LAX_2024-12-15")
    print(f"  Direct flights: {len(direct)}")

    affordable = price_tree.range_query(0, 400)
    matched = [f for _, f in affordable if f["origin"] == "JFK" and f["dest"] == "LAX"]
    print(f"  Under $400: {len(matched)}")
    for f in sorted(matched, key=lambda x: x["price"]):
        print(f"    {f['flight']}: ${f['price']}, departs {f['depart']}")

    path, cost = graph.dijkstra("JFK", "LAX")
    print(f"  Cheapest route (incl connections): {' -> '.join(path)}, ${cost}")

    print("\n" + "=" * 65)
    print("  Done.")


if __name__ == "__main__":
    demo()
