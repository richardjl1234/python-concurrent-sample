import multiprocessing as mp
import time
import concurrent.futures as futures

def timefunc(func):
    def inner(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f'Elapsed time is {end - start}')
    return inner

def read_dummy(num):
    for _ in range(num):
        with open('temp.txt', 'r') as f:
            res = f.read()
    return res
def read_dummy1(num):
    for _ in range(num):
        with open('temp1.txt', 'r') as f:
            res = f.read()
    return res


@timefunc
def main(q):
    for i in range(10000):
        for j in range(10000):
            x = i * j
    print(x)
    q.put({'a': x})
    with futures.ThreadPoolExecutor() as exe:
        f1 = exe.submit(read_dummy, 100000)
        f2 = exe.submit(read_dummy, 100000)
    q.put({'a_thread1': f1.result()})
    q.put({'a_thread2': f2.result()})


@timefunc
def main2(p):
    for i in range(10000):
        for j in range(10001):
            x = i * j
    print(x)
    q.put({'b': x})
    with futures.ThreadPoolExecutor() as exe:
        f1 = exe.submit(read_dummy, 100000)
        f2 = exe.submit(read_dummy, 100000)
    q.put({'b_thread1': f1.result()})
    q.put({'b_thread12': f2.result()})

#if __name__ == '__main__':
@timefunc
def overall_normal(q):
    main(q)
    main2(q)

@timefunc
def overall(q):
    p1 = mp.Process(target = main, args = (q,))
    p2 = mp.Process(target = main2, args = (q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    items = [q.get() for _ in range(q.qsize())]
    for item in items:
        print(item)

q = mp.Queue()
overall(q)


overall_normal(q)

