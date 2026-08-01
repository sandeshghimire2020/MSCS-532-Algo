# avl_tree.py - Self-balancing AVL tree for guaranteed O(log n) range queries
# This is the optimized replacement for the plain BST from Phase 2


class AVLNode:
    def __init__(self, key, data=None):
        self.key = key
        self.data = [data] if data else []
        self.left = None
        self.right = None
        self.height = 1


class FlightAVL:
    """AVL tree - same interface as FlightBST but stays balanced."""

    def __init__(self):
        self.root = None
        self._size = 0

    def _height(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, y):
        x = y.left
        t2 = x.right
        x.right = y
        y.left = t2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        t2 = y.left
        y.left = x
        x.right = t2
        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, node):
        self._update_height(node)
        bf = self._balance_factor(node)

        # left heavy
        if bf > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # right heavy
        if bf < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, key, data=None):
        self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if node is None:
            self._size += 1
            return AVLNode(key, data)

        if key == node.key:
            if data:
                node.data.append(data)
            return node
        elif key < node.key:
            node.left = self._insert(node.left, key, data)
        else:
            node.right = self._insert(node.right, key, data)

        return self._rebalance(node)

    def search(self, key):
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
        """Same as BST range query, but tree is balanced so worst case is O(log n + k)."""
        results = []
        self._range(self.root, low, high, results)
        return results

    def _range(self, node, low, high, results):
        if node is None:
            return
        if node.key > low:
            self._range(node.left, low, high, results)
        if low <= node.key <= high:
            for d in node.data:
                results.append((node.key, d))
        if node.key < high:
            self._range(node.right, low, high, results)

    def get_height(self):
        """Return the actual height of the tree (for verification)."""
        return self._height(self.root)

    def __len__(self):
        return self._size
