from queue import Queue
from worker import Worker


class ThreadPool(object):
    """ Pool of threads consuming tasks from a queue """
    def __init__(self, num_threads):
        self.queue = Queue(num_threads)
        # Create Worker Thread
        for _ in range(num_threads):
            Worker(self.queue)

    def add_task(self, f, *args, **kwargs):
        """ Add a task to the queue """
        self.queue.put((f, args, kwargs))
        print("Task " + f.__name__ + " has been added to the queue")

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(func, args)

    def wait_complete(self):
        """ Wait for completion of all the tasks in the queue """
        self.queue.join()
