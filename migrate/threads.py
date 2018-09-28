"""Thread handling."""
import logging

from queue import Queue
from threading import Thread


class Worker(Thread):
    """Thread executing tasks from a given tasks queue."""

    def __init__(self, tasks):
        """Setup the worker on the queue."""
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        """Do the work."""
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception:
                logging.exception("message")
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()


class ThreadPool:
    """Pool of threads consuming tasks from a queue."""

    def __init__(self, num_threads):
        """Setup the queue."""
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue."""
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """Add a list of tasks to the queue."""
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue."""
        self.tasks.join()
