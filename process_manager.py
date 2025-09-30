# process_manager.py

import multiprocessing
import time
import logging
from typing import Callable, List

# ============================
# Logger Configuration
# ============================

def setup_logger() -> logging.Logger:
    """
    Sets up a logger to capture process manager logs.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Console handler for logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# ============================
# Worker Function
# ============================

def worker_function(worker_id: int, task_queue: multiprocessing.Queue, result_queue: multiprocessing.Queue) -> None:
    """
    Worker function that processes tasks from the task queue and puts results into the result queue.

    Args:
        worker_id (int): The ID of the worker.
        task_queue (multiprocessing.Queue): The queue from which tasks are fetched.
        result_queue (multiprocessing.Queue): The queue where results are put.
    """
    logger = setup_logger()
    logger.info(f"Worker-{worker_id} started.")

    while True:
        try:
            task = task_queue.get(timeout=3)  # Wait for a task
            if task is None:  # None is the signal to stop
                logger.info(f"Worker-{worker_id} received stop signal.")
                break
            logger.info(f"Worker-{worker_id} processing task: {task}")
            result = task()  # Execute the task
            result_queue.put(result)  # Put the result in the result queue
        except Exception as e:
            logger.error(f"Worker-{worker_id} encountered an error: {e}")
            break

    logger.info(f"Worker-{worker_id} stopped.")

# ============================
# Process Manager Class
# ============================

class ProcessManager:
    def __init__(self, num_workers: int, worker_function: Callable, tasks: List[Callable]):
        """
        Initializes the ProcessManager with the specified number of workers and tasks.

        Args:
            num_workers (int): The number of worker processes to spawn.
            worker_function (Callable): The function that each worker will execute.
            tasks (List[Callable]): The list of tasks to be processed by the workers.
        """
        self.num_workers = num_workers
        self.worker_function = worker_function
        self.tasks = tasks
        self.task_queue = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()
        self.workers = []

        # Add tasks to the task queue
        for task in tasks:
            self.task_queue.put(task)

        # Add stop signals to the task queue
        for _ in range(num_workers):
            self.task_queue.put(None)

    def start_workers(self) -> None:
        """
        Starts the worker processes.
        """
        logger = setup_logger()
        logger.info("Starting worker processes.")

        for i in range(self.num_workers):
            worker = multiprocessing.Process(target=self.worker_function, args=(i, self.task_queue, self.result_queue))
            self.workers.append(worker)
            worker.start()

    def collect_results(self) -> List:
        """
        Collects results from the result queue.

        Returns:
            List: A list of results from the workers.
        """
        logger = setup_logger()
        logger.info("Collecting results from workers.")

        results = []
        for _ in self.tasks:
            result = self.result_queue.get()
            results.append(result)
        return results

    def stop_workers(self) -> None:
        """
        Stops the worker processes.
        """
        logger = setup_logger()
        logger.info("Stopping worker processes.")

        for worker in self.workers:
            worker.join()

# ============================
# Example Usage
# ============================

if __name__ == "__main__":
    # Define some example tasks
    def task1():
        time.sleep(1)
        return "Task 1 completed"

    def task2():
        time.sleep(2)
        return "Task 2 completed"

    tasks = [task1, task2]

    # Create a ProcessManager instance
    manager = ProcessManager(num_workers=2, worker_function=worker_function, tasks=tasks)

    # Start the worker processes
    manager.start_workers()

    # Collect the results from the workers
    results = manager.collect_results()
    for result in results:
        print(result)

    # Stop the worker processes
    manager.stop_workers()