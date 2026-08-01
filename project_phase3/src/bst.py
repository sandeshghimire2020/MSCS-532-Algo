# bst.py - Binary Search Tree for price/time range queries on flights


class BSTNode:
    def __init__(self, key, data=None):
        self.key = key
        self.data = [data] if data else []  # list so we can store multiple flights at same price
        self.left = None
        self.right = None


class FlightBST:
    """BST for range-based lookups like 'flights between $200 and $350'."""

    def __init__(self):
        self.root = None
        self._size = 0

    def insert(self, key, data=None):
        """Insert a record. If key already exists, just append to that node's list."""
        if self.root is None:
            self.root = BSTNode(key, data)
            self._size += 1
        else:
            self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if key == node.key:
            # same price - just add to the list
            if data:
                node.data.append(data)
        elif key < node.key:
            if node.left is None:
                node.left = BSTNode(key, data)
                self._size += 1
            else:
                self._insert(node.left, key, data)
        else:
            if node.right is None:
                node.right = BSTNode(key, data)
                self._size += 1
            else:
                self._insert(node.right, key, data)

    def search(self, key):
        """Find exact key, returns list of data or None."""
        node = self._find(self.root, key)
        return node.data if node else None

    def _find(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node
        elif key < node.key:
            return self._find(node.left, key)
        else:
            return self._find(node.right, key)

    def range_query(self, low, high):
        """Get all entries where low <= key <= high."""
        results = []
        self._range(self.root, low, high, results)
        return results

    def _range(self, node, low, high, results):
        if node is None:
            return
        # only go left if there could be results there
        if node.key > low:
            self._range(node.left, low, high, results)
        # include this node if its in range
        if low <= node.key <= high:
            for d in node.data:
                results.append((node.key, d))
        # only go right if there could be results there
        if node.key < high:
            self._range(node.right, low, high, results)

    def inorder(self):
        """Return everything sorted by key."""
        results = []
        self._inorder(self.root, results)
        return results

    def _inorder(self, node, results):
        if node is None:
            return
        self._inorder(node.left, results)
        for d in node.data:
            results.append((node.key, d))
        self._inorder(node.right, results)

    def __len__(self):
        return self._size
