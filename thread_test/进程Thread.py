"""example 1"""
def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i

import time
numbers = [2139079, 1214759, 1516637, 1852285]
start = time.time()

for number in numbers:
    list(factorize(number))

end = time.time()
delta = end - start
print(f'took {delta:.3f} second')


"""example 2"""
from threading import Thread
class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))

start = time.time()
threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'took {delta:.3f} second')


"""example 3"""
import select
import socket
def slow_systemcall():
    select.select([socket.socket()], [], [], 0.1)

start = time.time()
for _ in range(5):
    slow_systemcall()

end = time.time()
delta = end - start
print(f'took {delta:.3f} second')


"""example 4"""
start = time.time()
threads = []
for _ in range(5):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)


def compute_helicopter_location(index):
    pass

for i in range(5):
    compute_helicopter_location(i)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'took {delta:.3f} second')

