import threading as th
import multiprocessing as mp
import time

def timefunc(func):
    def inner(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f'Elapsed time is {end - start}')
    return inner


@timefunc
def main(q):
    for i in range(10000):
        for j in range(10000):
            x = i * j
    print(x)
    q.put(x)


@timefunc
def main2(p):
    for i in range(10000):
        for j in range(10000):
            x = i + j
    print(x)
    q.put(x)

@timefunc
def overall(q):
    p1 = th.Thread(target = main, args = (q,))
    p2 = th.Thread(target = main2, args = (q,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    res1 = q.get()
    res2 = q.get()
    print(res1, res2)


q = mp.Queue()
overall(q)
