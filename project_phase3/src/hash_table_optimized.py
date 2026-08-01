# hash_table_optimized.py - Optimized hash table with open addressing (linear probing)
# Better cache performance than chaining for dense tables


class OptimizedFlightHashTable:
    """Hash table using open addressing with linear probing.
    Better cache locality than chaining since everything lives in one array."""

    EMPTY = object()
    DELETED = object()

    def __init__(self, capacity=128):
        self.capacity = capacity
        self.size = 0
        self.keys = [self.EMPTY] * capacity
        self.values = [None] * capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def _probe(self, key):
        """Find the slot for this key (or next empty slot)."""
        idx = self._hash(key)
        first_deleted = None
        for _ in range(self.capacity):
            if self.keys[idx] is self.EMPTY:
                return first_deleted if first_deleted is not None else idx
            if self.keys[idx] is self.DELETED:
                if first_deleted is None:
                    first_deleted = idx
            elif self.keys[idx] == key:
                return idx
            idx = (idx + 1) % self.capacity
        # table is full (shouldnt happen if we resize properly)
        return first_deleted if first_deleted is not None else -1

    def _resize(self):
        old_keys = self.keys
        old_values = self.values
        self.capacity *= 2
        self.keys = [self.EMPTY] * self.capacity
        self.values = [None] * self.capacity
        self.size = 0
        for i in range(len(old_keys)):
            if old_keys[i] is not self.EMPTY and old_keys[i] is not self.DELETED:
                self.put(old_keys[i], old_values[i])

    def put(self, key, value):
        """Insert or update. Resizes at 70% load."""
        if self.size / self.capacity > 0.7:
            self._resize()
        idx = self._probe(key)
        if self.keys[idx] is self.EMPTY or self.keys[idx] is self.DELETED:
            self.size += 1
        self.keys[idx] = key
        self.values[idx] = value

    def get(self, key):
        """Lookup by key."""
        idx = self._hash(key)
        for _ in range(self.capacity):
            if self.keys[idx] is self.EMPTY:
                return None
            if self.keys[idx] == key:
                return self.values[idx]
            idx = (idx + 1) % self.capacity
        return None

    def delete(self, key):
        """Lazy deletion with tombstone."""
        idx = self._hash(key)
        for _ in range(self.capacity):
            if self.keys[idx] is self.EMPTY:
                return False
            if self.keys[idx] == key:
                self.keys[idx] = self.DELETED
                self.values[idx] = None
                self.size -= 1
                return True
            idx = (idx + 1) % self.capacity
        return False

    def __len__(self):
        return self.size
