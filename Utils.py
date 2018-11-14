import time


def profile(func):
    def wrapper(*args, **kwargs):
        print(func.__name__)
        s = time.time()

        func(*args, **kwargs)

        e = time.time()
        print("cost: {0}".format(e-s))
    return wrapper
