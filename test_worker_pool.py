import threading
import time
import unittest
from worker_pool import WorkerPool

class TestWorkerPool(unittest.TestCase):
    def test_worker_pool_execution(self):
        results = []
        lock = threading.Lock()

        def sample_task(val):
            time.sleep(0.005)
            with lock:
                results.append(val * 2)

        # Initialize pool with 4 workers
        pool = WorkerPool(num_workers=4)
        
        # Submit 20 tasks
        task_count = 20
        for i in range(task_count):
            pool.submit(sample_task, i)

        # Gracefully shut down and wait for completion
        pool.shutdown(wait=True)

        # Verify all tasks completed and results are correct
        self.assertEqual(len(results), task_count)
        self.assertEqual(sorted(results), [i * 2 for i in range(task_count)])
        print(f"\nSuccessfully executed {task_count} concurrent tasks across worker pool!")

if __name__ == "__main__":
    unittest.main()
