import queue
import threading

class WorkerPool:
    def __init__(self, num_workers: int):
        self.num_workers = num_workers
        self.task_queue = queue.Queue()
        self.workers = []
        self._stop_event = threading.Event()
        
        # Initialize and start worker threads
        for i in range(num_workers):
            t = threading.Thread(target=self._worker_loop, daemon=True)
            self.workers.append(t)
            t.start()

    def _worker_loop(self):
        """Internal loop executed by each worker thread."""
        # Keep running while not stopped OR while items remain in the queue
        while not self._stop_event.is_set() or not self.task_queue.empty():
            try:
                task, args, kwargs = self.task_queue.get(timeout=0.05)
            except queue.Empty:
                continue
            
            try:
                task(*args, **kwargs)
            except Exception as e:
                print(f"Worker encountered an error: {e}")
            finally:
                self.task_queue.task_done()

    def submit(self, func, *args, **kwargs):
        """Submit a callable task with arguments to the pool."""
        if self._stop_event.is_set():
            raise RuntimeError("Cannot submit tasks to a shut-down WorkerPool.")
        self.task_queue.put((func, args, kwargs))

    def shutdown(self, wait: bool = True):
        """Signal workers to stop and wait for all queued tasks to finish."""
        self._stop_event.set()
        if wait:
            self.task_queue.join()
            for t in self.workers:
                t.join()
