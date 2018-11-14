from queue import Queue
from Worker import Worker


class ThreadPool:
    """ Pool of threads consuming tasks from a queue """
    def __init__(self, n_threads, t=[]):
        self.tasks = Queue(n_threads)
        self.workers = []
        self.done = False
        for task in t:
            self.tasks.put(task)
        print("init ThreadPool with %d threads".format(n_threads))

    def init_workers(self, n_threads):
        for i in range(n_threads):
            worker = Worker(self.tasks, i)
            self.workers.append(worker)
        print("init_workers %d workers".format(n_threads))

    def add_task(self, func, *args, **kw_args):
        self.tasks.put( (func, args, kw_args) )
        print("add task to the queue")

    def close_all_threads(self):
        for worker in self.workers:
            worker.signal_exit()
        self.workers = []
        print("Close all threads")

    def wait_completion(self):
        self.tasks.join()
        print("Wait for completion of all the tasks in the queue")

