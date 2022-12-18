"""example 1"""
def download(item):
    pass

def resize(item):
    pass

def upload(item):
    pass

from collections import deque
from threading import Lock

class MyQueue:
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            self.items.popleft()


from threading import Thread
import time
class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    # 重写了Thread的run
    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                time.sleep(0.01)
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1

download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()
threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

i = 0
while i < 3:
    processed = len(done_queue.items)
    polled = sum(t.polled_count for t in threads)
    print(f'processed {processed} items after'
          f'polling {polled} times')
    time.sleep(1)
    i += 1


"""example 2"""
# from queue import Queue
# my_queue = Queue()
#
# def consumer():
#     print("consumer waiting")
#     my_queue.get()
#     print('consumer done')
#
# thread = Thread(target=consumer)
# thread.start()
#
# print('Producer putting')
# my_queue.put(object())
# print('Producer done')
# thread.join()


"""example 3"""
# my_queue = Queue(1)
#
# def consumer():
#     time.sleep(0.1)
#     my_queue.get()
#     print('Consumer got 1')
#     my_queue.get()
#     print('Consumer got 2')
#     print('Consumer done')
#
# thread = Thread(target=consumer)
# thread.start()
#
# my_queue.put(object())
# print('Producer put 1')
# my_queue.put(object())
# print('Producer put 2')
# print('Producer done')
# thread.join()


"""example 4"""
from queue import Queue
class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)


    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()

class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]


for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

download_queue.close()
download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), 'items finished')

for thread in threads:
    thread.join()
