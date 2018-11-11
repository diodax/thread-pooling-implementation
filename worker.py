from threading import Thread


class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, queue):
        super(Worker, self).__init__()
        self.queue = queue
        self.daemon = True
        self.start()

    def run(self):
        while True:
            f, args, kwargs = self.queue.get()
            try:
                print("The result from the worker task is: " + str(f(*args, **kwargs)))
            except Exception as e:
                # An exception happened in this thread
                print(e)
                self.queue.task_done()

