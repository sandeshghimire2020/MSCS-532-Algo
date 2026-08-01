"""
Directed Graph for Flight Route Optimization.
Airports are vertices, flight routes are weighted edges.
Supports BFS (fewest stops) and Dijkstra's (shortest path by weight).
"""

import heapq
from collections import deque, defaultdict


class FlightGraph:
    """Graph representing the flight network. Supports BFS and Dijkstra."""

    def __init__(self):
        self.adj = defaultdict(list)  # airport -> [(dest, weight, info), ...]
        self.airports = set()

    def add_airport(self, code):
        self.airports.add(code)

    def add_route(self, origin, dest, weight, info=None):
        """Add a directed flight route with a weight (price, duration, etc)."""
        self.airports.add(origin)
        self.airports.add(dest)
        self.adj[origin].append((dest, weight, info))

    def get_neighbors(self, airport):
        return self.adj.get(airport, [])

    def bfs_shortest_path(self, start, end, max_stops=None):
        """
        Find the route with fewest stops using BFS.
        Returns (path, num_connections) or (None, -1) if no path.
        """
        if start not in self.airports or end not in self.airports:
            return None, -1

        queue = deque()
        queue.append((start, [start], 0))
        visited = set()
        visited.add(start)

        while queue:
            current, path, stops = queue.popleft()

            if current == end:
                return path, stops - 1  # subtract 1 bc stops counts edges, connections = edges-1

            if max_stops is not None and stops > max_stops:
                continue

            for nb, w, info in self.adj[current]:
                if nb not in visited:
                    visited.add(nb)
                    queue.append((nb, path + [nb], stops + 1))

        return None, -1

    def dijkstra(self, start, end):
        """
        Find cheapest path from start to end.
        Returns (path, total_cost) or (None, inf) if unreachable.
        """
        if start not in self.airports or end not in self.airports:
            return None, float('inf')

        dist = {}
        prev = {}
        for ap in self.airports:
            dist[ap] = float('inf')
            prev[ap] = None
        dist[start] = 0

        pq = [(0, start)]

        while pq:
            cost, curr = heapq.heappop(pq)

            if curr == end:
                # build the path by backtracking
                path = []
                node = end
                while node is not None:
                    path.append(node)
                    node = prev[node]
                path.reverse()
                return path, cost

            if cost > dist[curr]:
                continue  # we already found a better way

            for nb, w, info in self.adj[curr]:
                new_cost = cost + w
                if new_cost < dist[nb]:
                    dist[nb] = new_cost
                    prev[nb] = curr
                    heapq.heappush(pq, (new_cost, nb))

        return None, float('inf')

    def __repr__(self):
        num_routes = sum(len(v) for v in self.adj.values())
        return f"FlightGraph({len(self.airports)} airports, {num_routes} routes)"
