class SPSCRingBuffer:
    def __init__(self, capacity: int):
        # Capacity must be a power of 2 for fast bitwise modulo, 
        # but standard modulo works cleanly for general capacities too.
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.head = 0  # Modified only by the consumer
        self.tail = 0  # Modified only by the producer

    def push(self, item) -> bool:
        """
        Producer-only method. Returns True if successful, 
        False if the buffer is full.
        """
        current_tail = self.tail
        next_tail = (current_tail + 1) % self.capacity

        # Check if buffer is full (next tail equals head)
        if next_tail == self.head:
            return False

        self.buffer[current_tail] = item
        self.tail = next_tail  # Atomic update visible to consumer
        return True

    def pop(self):
        """
        Consumer-only method. Returns the next item, 
        or None if the buffer is empty.
        """
        current_head = self.head

        # Check if buffer is empty (head equals tail)
        if current_head == self.tail:
            return None

        item = self.buffer[current_head]
        self.buffer[current_head] = None  # Help garbage collection
        self.head = (current_head + 1) % self.capacity  # Atomic update visible to producer
        return item

    def is_empty(self) -> bool:
        return self.head == self.tail

    def is_full(self) -> bool:
        return (self.tail + 1) % self.capacity == self.head
