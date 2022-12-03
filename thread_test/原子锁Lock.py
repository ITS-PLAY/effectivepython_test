"""example 1"""
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset

def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        counter.increment(1)

from threading import Thread
how_many = 10**5
counter = Counter()

threads = []
for i in range(5):
    thread = Thread(target=worker, args=(i, how_many, counter))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f'counter should be {expected}, got {found}')


"""example 2"""
from threading import Lock

class LockingCounter:
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset

counter = LockingCounter()
threads = []
for i in range(5):
    thread = Thread(target=worker, args=(i, how_many, counter))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f'counter should be {expected}, got {found}')