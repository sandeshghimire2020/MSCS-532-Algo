import random


class HashTableChaining:
    """
    A hash table that uses chaining (linked lists) for collision resolution.
    Uses a universal hash function family to minimize collisions.
    Supports dynamic resizing to maintain a low load factor.
    """

    def __init__(self, initial_capacity=8, max_load_factor=0.75):
        self.capacity = initial_capacity
        self.size = 0
        self.max_load_factor = max_load_factor
        self.table = [[] for _ in range(self.capacity)]
        # parameters for universal hash function: h(k) = ((a*k + b) mod p) mod m
        self._prime = 100003  # a large prime
        self._a = random.randint(1, self._prime - 1)
        self._b = random.randint(0, self._prime - 1)

    def _hash(self, key):
        """Universal hash function from Carter and Wegman's family."""
        hash_val = hash(key)
        return ((self._a * hash_val + self._b) % self._prime) % self.capacity

    def _load_factor(self):
        return self.size / self.capacity

    def _resize(self, new_capacity):
        """Resize the hash table and rehash all existing entries."""
        old_table = self.table
        self.capacity = new_capacity
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0
        for chain in old_table:
            for key, value in chain:
                self.insert(key, value)

    def insert(self, key, value):
        """
        Insert a key-value pair. If the key already exists, update its value.
        Resizes the table if load factor exceeds the threshold.
        """
        index = self._hash(key)
        chain = self.table[index]
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)
                return
        chain.append((key, value))
        self.size += 1
        if self._load_factor() > self.max_load_factor:
            self._resize(self.capacity * 2)

    def search(self, key):
        """
        Search for a key and return its value.
        Returns None if the key is not found.
        """
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key):
        """
        Delete a key-value pair from the hash table.
        Returns True if deleted, False if key was not found.
        """
        index = self._hash(key)
        chain = self.table[index]
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain.pop(i)
                self.size -= 1
                # shrink if load factor drops too low
                if self.capacity > 8 and self._load_factor() < 0.2:
                    self._resize(max(8, self.capacity // 2))
                return True
        return False

    def __len__(self):
        return self.size

    def __contains__(self, key):
        return self.search(key) is not None

    def __repr__(self):
        items = []
        for chain in self.table:
            for k, v in chain:
                items.append(f"{k}: {v}")
        return "{" + ", ".join(items) + "}"


# --- Demo / Quick test ---

if __name__ == "__main__":
    ht = HashTableChaining()

    # Insert some data
    print("Inserting key-value pairs...")
    test_data = [("alice", 90), ("bob", 85), ("charlie", 92), ("diana", 88),
                 ("eve", 95), ("frank", 78), ("grace", 91), ("hank", 83)]
    for name, score in test_data:
        ht.insert(name, score)

    print(f"Hash table size: {len(ht)}, capacity: {ht.capacity}")
    print(f"Load factor: {ht._load_factor():.2f}")
    print(f"Table contents: {ht}")

    # Search
    print(f"\nSearch 'alice': {ht.search('alice')}")
    print(f"Search 'bob': {ht.search('bob')}")
    print(f"Search 'unknown': {ht.search('unknown')}")

    # Delete
    print(f"\nDelete 'bob': {ht.delete('bob')}")
    print(f"Search 'bob' after delete: {ht.search('bob')}")
    print(f"Hash table size after delete: {len(ht)}")

    # Update existing key
    ht.insert("alice", 99)
    print(f"\nUpdated 'alice' to 99. Search 'alice': {ht.search('alice')}")

    print("\nDone.")
