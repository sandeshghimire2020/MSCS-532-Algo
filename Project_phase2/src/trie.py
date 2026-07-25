# trie.py - Prefix tree for airport code autocomplete

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.data = None


class AirportTrie:
    """Trie for looking up airports by code or city name prefix."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, key, data=None):
        # walk down the trie, creating nodes as needed
        current = self.root
        for ch in key.lower():
            if ch not in current.children:
                current.children[ch] = TrieNode()
            current = current.children[ch]
        current.is_end = True
        current.data = data

    def search(self, key):
        """Exact match lookup. Returns data or None."""
        node = self._get_node(key.lower())
        if node and node.is_end:
            return node.data
        return None

    def starts_with(self, prefix):
        """Find all entries that start with the given prefix (autocomplete)."""
        node = self._get_node(prefix.lower())
        if node is None:
            return []
        results = []
        self._collect_all(node, prefix.lower(), results)
        return results

    def _get_node(self, key):
        # just walks down the path, returns None if it doesnt exist
        current = self.root
        for ch in key:
            if ch not in current.children:
                return None
            current = current.children[ch]
        return current

    def _collect_all(self, node, prefix_so_far, results):
        # grab everything below this node
        if node.is_end:
            results.append({"key": prefix_so_far, "data": node.data})
        for ch in sorted(node.children.keys()):
            self._collect_all(node.children[ch], prefix_so_far + ch, results)
