import time


class Task:

    def __init__(self, task_id, priority, description="", deadline=None):
        self.task_id = task_id
        self.priority = priority
        self.arrival_time = time.time()
        self.deadline = deadline
        self.description = description

    def __repr__(self):
        return f"Task({self.task_id}, priority={self.priority}, desc='{self.description}')"

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return self.task_id == other.task_id


class MaxHeapPriorityQueue:

    def __init__(self):
        self._heap = []
        self._index_map = {}  # task_id -> index, for O(1) lookup during key changes

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        """Swap two elements and update the index map."""
        self._index_map[self._heap[i].task_id] = j
        self._index_map[self._heap[j].task_id] = i
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _sift_up(self, i):
        """Move element at index i upward to restore the heap property."""
        while i > 0 and self._heap[i] > self._heap[self._parent(i)]:
            self._swap(i, self._parent(i))
            i = self._parent(i)

    def _sift_down(self, i):
        """Move element at index i downward to restore the heap property."""
        n = len(self._heap)
        while True:
            largest = i
            left = self._left(i)
            right = self._right(i)

            if left < n and self._heap[left] > self._heap[largest]:
                largest = left
            if right < n and self._heap[right] > self._heap[largest]:
                largest = right

            if largest == i:
                break
            self._swap(i, largest)
            i = largest

    def insert(self, task):

        self._heap.append(task)
        idx = len(self._heap) - 1
        self._index_map[task.task_id] = idx
        self._sift_up(idx)

    def extract_max(self):

        if self.is_empty():
            raise IndexError("extract_max called on an empty priority queue")

        max_task = self._heap[0]
        last_task = self._heap.pop()
        del self._index_map[max_task.task_id]

        if self._heap:
            self._heap[0] = last_task
            self._index_map[last_task.task_id] = 0
            self._sift_down(0)

        return max_task

    def increase_key(self, task_id, new_priority):

        if task_id not in self._index_map:
            raise KeyError(f"Task '{task_id}' not found in the priority queue")

        idx = self._index_map[task_id]
        if new_priority < self._heap[idx].priority:
            raise ValueError("New priority must be >= current priority. Use decrease_key instead.")

        self._heap[idx].priority = new_priority
        self._sift_up(idx)

    def decrease_key(self, task_id, new_priority):

        if task_id not in self._index_map:
            raise KeyError(f"Task '{task_id}' not found in the priority queue")

        idx = self._index_map[task_id]
        if new_priority > self._heap[idx].priority:
            raise ValueError("New priority must be <= current priority. Use increase_key instead.")

        self._heap[idx].priority = new_priority
        self._sift_down(idx)

    def is_empty(self):
        """
        Check whether the priority queue is empty.

        Time Complexity: O(1)
        """
        return len(self._heap) == 0

    def peek(self):
        """Return the highest-priority task without removing it."""
        if self.is_empty():
            raise IndexError("peek called on an empty priority queue")
        return self._heap[0]

    def __len__(self):
        return len(self._heap)

    def __repr__(self):
        return f"MaxHeapPriorityQueue({[str(t) for t in self._heap]})"


# --------------- Task Scheduler Simulation ---------------

def run_scheduler_simulation():

    pq = MaxHeapPriorityQueue()

    # Simulate task arrivals
    tasks = [
        Task("T1", 5, "Low-priority background job"),
        Task("T2", 20, "User login request"),
        Task("T3", 10, "Database backup"),
        Task("T4", 35, "Critical security patch"),
        Task("T5", 15, "Email notification"),
        Task("T6", 25, "Payment processing"),
        Task("T7", 8, "Log rotation"),
        Task("T8", 40, "System health check - URGENT"),
    ]

    print("--- Task Arrivals ---")
    for task in tasks:
        pq.insert(task)
        print(f"  Inserted: {task}")

    print(f"\nQueue size: {len(pq)}")
    print(f"Highest priority task: {pq.peek()}")

    # Simulate a priority boost
    print("\n--- Priority Change ---")
    print(f"  Boosting T1 priority from 5 to 50 (emergency escalation)")
    pq.increase_key("T1", 50)
    print(f"  New highest priority task: {pq.peek()}")

    # Process all tasks in priority order
    print("\n--- Processing Tasks (highest priority first) ---")
    order = 1
    while not pq.is_empty():
        task = pq.extract_max()
        print(f"  {order}. Processed: {task}")
        order += 1

    print("\nScheduler simulation complete.")


if __name__ == "__main__":
    print("=" * 60)
    print("Priority Queue (Max-Heap) — Task Scheduler Simulation")
    print("=" * 60)
    run_scheduler_simulation()
