# data_structures.py - Elementary data structures: Array, Stack, Queue, Linked List


# --- Dynamic Array ---

class DynamicArray:
    """Basic dynamic array with insert, delete, access."""

    def __init__(self):
        self._data = []
        self._size = 0

    def access(self, index):
        """Get element at index. O(1)."""
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        return self._data[index]

    def insert(self, index, value):
        """Insert value at index, shifting elements right. O(n)."""
        if index < 0 or index > self._size:
            raise IndexError("index out of range")
        self._data.insert(index, value)
        self._size += 1

    def append(self, value):
        """Add to end. Amortized O(1)."""
        self._data.append(value)
        self._size += 1

    def delete(self, index):
        """Remove element at index, shifting elements left. O(n)."""
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        val = self._data.pop(index)
        self._size -= 1
        return val

    def size(self):
        return self._size

    def __repr__(self):
        return f"DynamicArray({self._data})"


# --- Matrix (2D Array) ---

class Matrix:
    """Simple matrix with basic operations."""

    def __init__(self, rows, cols, fill=0):
        self.rows = rows
        self.cols = cols
        self.data = [[fill] * cols for _ in range(rows)]

    def get(self, r, c):
        return self.data[r][c]

    def set(self, r, c, value):
        self.data[r][c] = value

    def __repr__(self):
        lines = [str(row) for row in self.data]
        return "\n".join(lines)


# --- Stack (array-based) ---

class Stack:
    """LIFO stack using a list."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Push onto top. O(1)."""
        self._items.append(item)

    def pop(self):
        """Remove and return top. O(1)."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Look at top without removing."""
        if self.is_empty():
            raise IndexError("peek on empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack(top={self._items[-1] if self._items else 'empty'})"


# --- Queue (array-based) ---

class Queue:
    """FIFO queue using a list. Not the most efficient but simple."""

    def __init__(self):
        self._items = []

    def enqueue(self, item):
        """Add to back. O(1)."""
        self._items.append(item)

    def dequeue(self):
        """Remove from front. O(n) because of shifting - thats the tradeoff."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)

    def front(self):
        if self.is_empty():
            raise IndexError("front on empty queue")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __repr__(self):
        return f"Queue(front={self._items[0] if self._items else 'empty'})"


# --- Singly Linked List ---

class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Singly linked list with insert, delete, traversal."""

    def __init__(self):
        self.head = None
        self._size = 0

    def insert_front(self, data):
        """Insert at head. O(1)."""
        node = ListNode(data)
        node.next = self.head
        self.head = node
        self._size += 1

    def insert_back(self, data):
        """Insert at tail. O(n) since we dont keep a tail pointer."""
        node = ListNode(data)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
        self._size += 1

    def delete(self, data):
        """Delete first occurrence of data. O(n)."""
        if self.head is None:
            return False
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def search(self, data):
        """Find if data exists. O(n)."""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def traverse(self):
        """Return all elements as a list."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def size(self):
        return self._size

    def __repr__(self):
        items = self.traverse()
        return " -> ".join(str(x) for x in items) + " -> None"


# --- Demo ---

if __name__ == "__main__":
    print("=== Dynamic Array ===")
    arr = DynamicArray()
    for i in [10, 20, 30, 40, 50]:
        arr.append(i)
    print(f"  Array: {arr}")
    arr.insert(2, 25)
    print(f"  After insert 25 at idx 2: {arr}")
    arr.delete(0)
    print(f"  After delete idx 0: {arr}")
    print(f"  Access idx 1: {arr.access(1)}")

    print("\n=== Matrix ===")
    m = Matrix(3, 3)
    m.set(0, 0, 1)
    m.set(1, 1, 5)
    m.set(2, 2, 9)
    print(m)

    print("\n=== Stack ===")
    s = Stack()
    for x in ["a", "b", "c", "d"]:
        s.push(x)
    print(f"  Stack: {s}")
    print(f"  Pop: {s.pop()}")
    print(f"  Pop: {s.pop()}")
    print(f"  Peek: {s.peek()}")

    print("\n=== Queue ===")
    q = Queue()
    for x in [1, 2, 3, 4]:
        q.enqueue(x)
    print(f"  Queue: {q}")
    print(f"  Dequeue: {q.dequeue()}")
    print(f"  Dequeue: {q.dequeue()}")
    print(f"  Front: {q.front()}")

    print("\n=== Linked List ===")
    ll = LinkedList()
    for x in [10, 20, 30, 40]:
        ll.insert_back(x)
    print(f"  List: {ll}")
    ll.insert_front(5)
    print(f"  After insert_front(5): {ll}")
    ll.delete(30)
    print(f"  After delete(30): {ll}")
    print(f"  Search 20: {ll.search(20)}")
    print(f"  Search 99: {ll.search(99)}")

    print("\nDone.")
