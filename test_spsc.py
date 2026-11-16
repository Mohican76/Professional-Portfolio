import threading
import unittest
from spsc_ring_buffer import SPSCRingBuffer

class TestSPSCRingBuffer(unittest.TestCase):
    def test_single_producer_single_consumer_concurrency(self):
        buffer_capacity = 1024
        item_count = 50000
        
        q = SPSCRingBuffer(buffer_capacity)
        produced_items = list(range(item_count))
        consumed_items = []

        def producer():
            i = 0
            while i < item_count:
                if q.push(produced_items[i]):
                    i += 1
                # If buffer is full, yield briefly to avoid busy-wait spinning

        def consumer():
            while len(consumed_items) < item_count:
                item = q.pop()
                if item is not None:
                    consumed_items.append(item)

        # Spin up threads
        t_prod = threading.Thread(target=producer)
        t_cons = threading.Thread(target=consumer)

        t_prod.start()
        t_cons.start()

        t_prod.join()
        t_cons.join()

        # Verify absolute data integrity and ordering
        self.assertEqual(consumed_items, produced_items)
        print(f"\nSuccessfully passed {item_count} items through SPSC Lock-Free Buffer concurrently!")

if __name__ == "__main__":
    unittest.main()
