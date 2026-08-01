# hash_table.py - Hash table for indexing flights by composite keys
# uses chaining for collisions


class FlightHashTable:
    """Hash table for fast flight lookups by route+date or flight number."""

    def __init__(self, capacity=64):
        self.capacity = capacity
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

    def _hash(self, key):
        return hash(key) % self.capacity

    def _resize(self):
        # double the table and rehash everything
        old = self.table
        self.capacity = self.capacity * 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0
        for chain in old:
            for k, v in chain:
                self.put(k, v)

    def put(self, key, value):
        """Insert or update a key-value pair."""
        idx = self._hash(key)
        # check if key already exists in the chain
        for i, (k, v) in enumerate(self.table[idx]):
            if k == key:
                self.table[idx][i] = (key, value)
                return
        self.table[idx].append((key, value))
        self.size += 1
        # resize if we're getting too full
        if self.size / self.capacity > 0.75:
            self._resize()

    def get(self, key):
        """Look up a value by key. Returns None if not found."""
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        return None

    def delete(self, key):
        """Remove a key. Returns True if it was there, False otherwise."""
        idx = self._hash(key)
        chain = self.table[idx]
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain.pop(i)
                self.size -= 1
                return True
        return False

    def contains(self, key):
        return self.get(key) is not None

    def keys(self):
        all_keys = []
        for chain in self.table:
            for k, v in chain:
                all_keys.append(k)
        return all_keys

    def __len__(self):
        return self.size

    def __repr__(self):
        items = []
        for chain in self.table:
            for k, v in chain:
                items.append(f"{k}: {v}")
        # just show first few so it doesnt flood the console
        preview = ", ".join(items[:5])
        if len(items) > 5:
            preview += ", ..."
        return f"FlightHashTable({{{preview}}})"
