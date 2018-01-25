# author='lwz'
# coding:utf-8
import multiprocessing
import time
import pickle
'''
Python中进程间共享数据，处理基本的queue，pipe和value+array外，还提供了更高层次的封装。
使用multiprocessing.Manager可以简单地使用这些高级接口。
Manager()返回的manager对象控制了一个server进程，此进程包含的python对象
可以被其他的进程通过proxies来访问。从而达到多进程间数据通信且安全。

Manager支持的类型有list,dict,Namespace,Lock,RLock,Semaphore,BoundedSemaphore,Condition,Event,Queue,Value和Array。

Queue:
put() 方法再将数据放入队列后会写一个单字节到某个套接字中去。
而 get() 方法在从队列中移除一个元素时会从另外一个套接字中读取到这个单字节数据。

'''


def worker(n, i, prime, st):
    while st < 10000:
        # prime_s = prime
        for p in prime:
            if st % p == 0:
                break
        else:
            prime.append(st)
            # prime = prime_s

        st += n * 2


def main(n=3):
    start_time = time.time()
    mgr = multiprocessing.Manager()
    p = mgr.list([3, 5, 7, 11, 13, 17, 19])
    st = 21
    jobs = [multiprocessing.Process(target=worker, args=(n, i, p, st + i * 2))
            for i in range(n)
            ]
    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    print('process {} find {} primes used {:4f}s'.format(n, len(p), time.time() - start_time))


def main_2(n=3):
    start_time = time.time()
    manager = multiprocessing.Manager()
    num_get_queue = manager.Queue()
    prime_get_queue = manager.Queue()
    primes = list([3, 5, 7, 11, 13, 17, 19])
    st = 21
    jobs = [multiprocessing.Process(target=worker_2, args=(i, num_get_queue, prime_get_queue))
            for i in range(n)
            ]
    for j in jobs:
        j.start()

    ed = st * st
    while ed < 40000:
        step = n * 2
        for i in range(n):
            nums = range(st + i * 2, ed, step)
            num_get_queue.put(nums)
            byte_primes = pickle.dumps(primes)
            prime_get_queue.put(byte_primes)

        for i in range(n):
            results = pickle.loads(prime_get_queue.get())
            if results is None:
                pass
            else:
                primes += results

        st = ed
        ed = st * st

    for _ in jobs:
        num_get_queue.put(primes, pickle.dumps([]))


def worker_2(i, num_get_queue, prime_get_queue):
    print("process{} start....".format(i))
    while True:
        print("process{} wait for data....".format(i))
        nums = num_get_queue.get()
        byte_primes = prime_get_queue.get()
        primes = pickle.loads(byte_primes)
        if len(nums) is 0:
            print("process{} end....".format(i))
            break

        print("process{} get {} primes {} number data....".format(i, len(primes), len(nums)))
        p_list = []
        for num in nums:
            for p in primes:
                if num % p == 0:
                    break
            else:
                p_list.append(num)

        print("process{} push data....".format(i))
        prime_get_queue.put(pickle.dumps(p_list))
        print("process{} push data over....".format(i))


if __name__ == '__main__':
     main_2(1)
