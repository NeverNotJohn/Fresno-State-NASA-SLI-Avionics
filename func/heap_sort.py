class MaxHeap:
    def __init__(self, key="altitude"):
        self.heap = []
        self.key = key

    def parent(self, index):
        return (index - 1) // 2

    def left_child(self, index):
        return 2 * index + 1

    def right_child(self, index):
        return 2 * index + 2

    def insert(self, data):
        """Insert a value into the heap."""
        self.heap.append(data)
        self._heapify_up(len(self.heap) - 1)

    def extract_max(self):
        """Remove and return the largest element from the heap."""
        if len(self.heap) == 0:
            raise IndexError("Heap is empty")
        if len(self.heap) == 1:
            return self.heap.pop()

        # Swap root with the last element
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, index):
        """Ensure the heap property is maintained while inserting."""
        while index > 0 and self.heap[index][self.key] > self.heap[self.parent(index)][self.key]:
            # Swap the current element with its parent
            self.heap[index], self.heap[self.parent(index)] = (
                self.heap[self.parent(index)],
                self.heap[index],
            )
            index = self.parent(index)

    def _heapify_down(self, index):
        """Ensure the heap property is maintained after extracting the root."""
        largest = index
        left = self.left_child(index)
        right = self.right_child(index)

        # Find the largest among the current node and its children
        if left < len(self.heap) and self.heap[left][self.key] > self.heap[largest][self.key]:
            largest = left
        if right < len(self.heap) and self.heap[right][self.key] > self.heap[largest][self.key]:
            largest = right

        # If the largest is not the current node, swap and continue heapifying
        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._heapify_down(largest)

    def get_max(self):
        """Return the largest element without removing it."""
        if not self.heap:
            raise IndexError("Heap is empty")
        return self.heap[0]

    def __str__(self):
        """String representation of the heap."""
        return str(self.heap)
    
    def heapsort(self, n):
        # Heapsort n times to get the n largest elements
        """Perform heapsort on the given iterable."""
        heap = MaxHeap()
        for value in self.heap:
            heap.insert(value)
        
        sorted_list = []
        while len(sorted_list) < n:
            sorted_list.append(heap.extract_max())
        
        return sorted_list  # Reverse to get descending order

def create_data(time, temperature, pressure, altitude):
    return {"time": time, "temperature": temperature, "pressure": pressure, "altitude": altitude}

# Example Usage
heap = MaxHeap("altitude")
heap.insert(create_data(0, 10, 12, 3))
heap.insert(create_data(0, 10, 12, 10))
heap.insert(create_data(0, 10, 12, 12))
heap.insert(create_data(0, 10, 12, 1))
heap.insert(create_data(0, 10, 12, -1))
heap.insert(create_data(0, 10, 12, 5))
heap.insert(create_data(0, 10, 12, 8))
heap.insert(create_data(0, 10, 12, 11))
heap.insert(create_data(0, 10, 12, 10))

print("Heap:", heap)  # Heap: [100, 22, 20, 13, 5, 12, 10, 3, 5]
print("Top three indexes:",heap.heapsort(3))