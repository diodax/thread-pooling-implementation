from queue import Queue, Empty
from threading import Thread, Event


class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """

    def __init__(self, tasks, t_num):
        Thread.__init__(self)
        self.daemon = True
        self.thread_num = t_num
        self.done = Event()
        self.tasks = tasks
        self.start()

    def run(self):
        print("Called Worker.run")
        while not self.done.is_set():
            try:
                func, args, kw_args = self.tasks.get(block=True)
                try:
                    func(*args, **kw_args)
                except Exception as e:
                    print("Exception in Worker.run: ", e)
            except Empty:
                pass
        return

    def signal_exit(self):
        """" Send a signal to exit the thread. """
        self.done.set()
