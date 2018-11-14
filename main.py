import concurrent.futures
import urllib.request
import time
import heapq

priority_queue = []

URLS = [(2, 'http://www.foxnews.com/'),
        (5, 'http://www.cnn.com/'),
        (7, 'http://europe.wsj.com/'),
        (1, 'http://www.bbc.co.uk/'),
        (1, 'http://www.npr.org/'),
        (9, 'http://www.facebook.com/'),
        (8, 'http://www.google.com/'),
        (4, 'http://www.twitter.com/'),
        (2, 'http://www.youtube.com/'),
        (5, 'http://www.se.rit.edu/'),
        (3, 'http://www.reddit.com/')]


def task_generator(spacing):
    """ Generates urls in real time to send to the queue """
    while True:
        for priority, url in URLS:
            time.sleep(spacing)
            heapq.heappush(priority_queue, (priority, url))
            print("Added URL task with priority " + str(priority) + " to the queue")


def load_url(url, priority, timeout):
    """ Retrieve a single page and report the URL and contents """
    print("Opening " + url + " with priority " + str(priority) + "...")
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

    # start a thread for the task_generator method, which sends work in through the queue
    future_to_url = {executor.submit(task_generator, 1.0): 'FEEDER DONE'}

    while future_to_url:
        # check for status of the tasks which are currently working
        done, not_done = concurrent.futures.wait(
            future_to_url, timeout=5.0,
            return_when=concurrent.futures.FIRST_COMPLETED)
        print("Finished threads: " + str(len(done)) +
              ", unfinished threads: " + str(len(not_done)) +
              ", queue size: " + str(len(priority_queue)))

        # if there is incoming work, start a new task(future)
        while priority_queue:

            # fetch a url with its priority from the queue
            priority, url = heapq.heappop(priority_queue)

            # Start the load operation and mark the task with its URL
            future_to_url[executor.submit(load_url, url, priority, 60)] = url

        # process any completed tasks
        for future in done:
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                print('%r page is %d bytes' % (url, len(data)))

            # allow the thread from the now completed task to be used again
            del future_to_url[future]
