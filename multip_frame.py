import multiprocessing as mp
import time
import concurrent.futures as futures
NUM = 5000
pool = mp.Pool()
print(pool._processes)

def timefunc(func):
    def inner(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(f'Elapsed time is {end - start}')
        return res
    return inner

## the original functions are defined here
def main1(num):
    for i in range(num):
        for j in range(num):
            x = i * j
            y = i + j
    #print(x, y )
    return x, y

def main2(num):
    for i in range(num+1):
        for j in range(num+1):
            x = i * j
            y = i + j
    #print(x, y)
    return x, y

#main1 = timefunc(main1)
#main2 = timefunc(main2)
funcs =[]
funcs.append({'F': main1, 'ARG': (NUM, )})
funcs.append({'F': main2, 'ARG': (NUM, )})
@timefunc
def overall_normal():
    print('** Non multiprocessing **')
    results = []
    for func in funcs:
        res = func['F'](*func['ARG'])
        results.append({func['F'].__name__: res})
    for item in results:
        print(item)
overall_normal()

# handle the multi processing here
q = mp.Queue()
def mp_wrapper(func):
    def inner(q, *args, **kwargs):
        res = func(*args, **kwargs)
        q.put({func.__name__:res})
    return inner
mp_q_wrapper = lambda func: mp_wrapper(q, func)

main1 = mp_wrapper(main1)
main2 = mp_wrapper(main2)
funcs =[]
funcs.append({'F': main1, 'ARG': (NUM, )})
funcs.append({'F': main2, 'ARG': (NUM, )})

@timefunc
def overall(q):
    print('** Multiprocessing **')
    ps = []
    for func in funcs:
        p = mp.Process(target = func['F'], args = (q, *func['ARG'] ))
        ps.append(p)
    for p in ps:
        p.start()
    for p in ps:
        p.join()
    items = [q.get() for _ in range(q.qsize())]
    for item in items:
        print(item)


overall(q)


