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


def feed_the_workers(spacing):
    """ Simulate outside actors sending in work to do """
    while True:
        for priority, url in URLS:
            time.sleep(spacing)
            # print('Current state of the queue (before push): [%s]' % ', '.join(map(str, priority_queue)))
            heapq.heappush(priority_queue, (priority, url))


def load_url(url, priority, timeout):
    """ Retrieve a single page and report the URL and contents """
    print("Opening " + url + " with priority " + str(priority) + "...")
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:

    # start a future for a thread which sends work in through the queue
    future_to_url = {
        executor.submit(feed_the_workers, 1.0): 'FEEDER DONE'}

    while future_to_url:
        # check for status of the futures which are currently working
        done, not_done = concurrent.futures.wait(
            future_to_url, timeout=5.0,
            return_when=concurrent.futures.FIRST_COMPLETED)
        print("Finished threads: " + str(len(done)) +
              ", unfinished threads: " + str(len(not_done)) +
              ", queue size: " + str(len(priority_queue)))

        # if there is incoming work, start a new future
        while priority_queue:

            # fetch a url with its priority from the queue
            # print('Current state of the queue (before pop): [%s]' % ', '.join(map(str, priority_queue)))
            priority, url = heapq.heappop(priority_queue)

            # Start the load operation and mark the future with its URL
            future_to_url[executor.submit(load_url, url, priority, 60)] = url

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
                    print('%r page is %d bytes' % (url, len(data)))

            # remove the now completed future
            del future_to_url[future]
