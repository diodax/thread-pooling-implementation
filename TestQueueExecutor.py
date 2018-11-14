from Utils import profile
import concurrent.futures
import urllib.request
import time
import queue
import random

q = queue.PriorityQueue()

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://stackoverflow.com/',
        'http://web.whatsapp.com/',
        'http://giphy.com/',
        'http://docs.python.org/',
        'http://www.tutorialspoint.com/',
        'http://github.com/',
        'http://www.lucidchart.com/']


def feed_the_workers(spacing):
    """ Simulate outside actors sending in work to do, request each url twice """
    for url in URLS + URLS:
        time.sleep(spacing)
        q.put(url)
    return "DONE FEEDING"


def feed_the_workers_prioritized(spacing):
    """ Simulate outside actors sending in work to do, request each url twice """
    random_priorities = [random.randrange(1, 11) for i in range(11)]
    tuples = zip([10,10,10,10,10,10,10,10,10,1,10], URLS)

    for value in tuples:
        print("priority queue = ", value)
        time.sleep(spacing)
        q.put(value)

    return "DONE FEEDING"


def load_url(tuple, timeout):
    """ Retrieve a single page and report the URL and contents """
    pri = tuple[0]
    url = tuple[1]
    print("OPENING --> {} with priority {}.".format(url, pri))
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


@profile
def concurrent_function():
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

        # start a future for a thread which sends work in through the queue
        future_to_url = {executor.submit(feed_the_workers_prioritized, 0.25): 'FEEDER DONE'}

        while future_to_url:
            # check for status of the futures which are currently working
            done, not_done = concurrent.futures.wait(
                future_to_url, timeout=15,  # 0.25,
                return_when=concurrent.futures.FIRST_COMPLETED)

            # if there is incoming work, start a new future
            while not q.empty():
                # fetch a url from the queue
                q_value = q.get()
                url = q_value[1]
                # Start the load operation and mark the future with its URL
                future_to_url[executor.submit(load_url, q_value, 60)] = url
                print("STARTING REQUEST --> {} with priority {}.".format(q_value[1], q_value[0]))

            # process any completed futures
            for future in done:
                url = future_to_url[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                else:
                    if url == 'FEEDER DONE':
                        print(data)
                    else:
                        print('FINISHED LOAD --> %r, SIZE is %d bytes' % (url, len(data)))

                # remove the now completed future
                del future_to_url[future]


if __name__ == '__main__':
    concurrent_function()