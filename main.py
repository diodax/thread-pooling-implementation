# producer and consumer architecture
from threadpool import ThreadPool


# Function to be executed in a thread
def fib(n):
    if n <= 2:
        return 1
    return fib(n-1)+fib(n-2)


if __name__ == '__main__':
    # Instantiate a thread pool with 5 worker threads
    pool = ThreadPool(5)
    for _ in range(3):
        pool.add_task(fib, 35)
    pool.wait_complete()

