# author='lwz'
# coding:utf-8
import multiprocessing
from multiprocessing import Pool
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


main:
普通多进程

main_2:
按任务创建queue  不同进程的相同任务使用一个queue
有时候会出发bug
put发送数据建立连接 get会接受并关闭连接
连续put put get get会导致第二个get出现管道已关闭的异常

main_3
按任务, 进程创建queue  每个进程的每个任务都有一个单独的queue
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
    new_prime_get_queue = manager.Queue()
    primes = list([3, 5, 7, 11, 13, 17, 19])
    st = 21
    jobs = []
    pool = Pool(processes=n)

    for i in range(n):
        job = multiprocessing.Process(target=worker_2,
            args=(i, num_get_queue, prime_get_queue, new_prime_get_queue))
        jobs.append(job)
        job.start()

    ed = st * st
    while ed < 500000:
        step = n * 2
        for i in range(n):
            nums = range(st + i * 2, ed, step)
            num_get_queue.put(nums)
            byte_primes = pickle.dumps(primes)
            prime_get_queue.put(byte_primes)
            print("main__ send data to process {}".format(i))

        print("main__ wait for answer ...")

        print("main__ awake ...")
        for i in range(n):
            results = pickle.loads(new_prime_get_queue.get())
            print("main__ we get {} primes".format(len(results)))
            if results is None:
                pass
            else:
                primes += results
        print("main__ get answer ....")
        print("main__ now there is {} primes".format(len(primes)))
        st = ed
        ed = st * st
        print("main__ st: {} ed: {}".format(st, ed))

    for _ in jobs:
        num_get_queue.put(b'stop')
        time.sleep(0.05)

    print("main__ send stop msg over")


def worker_2(i, num_get_queue, prime_get_queue, new_prime_get_queue):
    print("process{} start....".format(i))
    while True:
        print("process{} wait for data....".format(i))
        nums = num_get_queue.get()
        if not isinstance(nums, range):
            # 如果接收到的对象不是range类型 就终止进程
            print("process{} end....".format(i))
            break
        else:
            print(nums)

        byte_primes = prime_get_queue.get()
        primes = pickle.loads(byte_primes)

        print("process{} get {} primes {} number data....".format(i, len(primes), len(nums)))
        p_list = []
        for num in nums:
            for p in primes:
                if num % p == 0:
                    break
            else:
                p_list.append(num)

        print("process{} push data....".format(i))
        new_prime_get_queue.put(pickle.dumps(p_list))
        print("process{} push data over....".format(i))
        time.sleep(0.1 + i / 1000)


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


def main_3(n=3):
    start_time = time.time()
    manager = multiprocessing.Manager()
    primes = list([3, 5, 7, 11, 13, 17, 19])
    st = 21
    jobs = []
    pool = Pool(processes=n)
    queues = []

    for i in range(n):
        queues.append([])
        for j in range(3):
            queue = manager.Queue()
            queues[i].append(queue)

        job = multiprocessing.Process(target=worker_3,
            args=(i, queues[i]))
        jobs.append(job)
        job.start()

    ed = st * st
    while ed < 500000:
        step = n * 2
        for i in range(n):
            nums = range(st + i * 2, ed, step)
            queues[i][0].put(nums)
            byte_primes = pickle.dumps(primes)
            queues[i][1].put(byte_primes)
            print("main__ send data to process {}".format(i))

        print("main__ wait for answer ...")
        print("main__ awake ...")
        for i in range(n):
            results = pickle.loads(queues[i][2].get())
            time_str = time.strftime("%H:%M:%S", time.localtime())
            print("main__ we get {} primes from process_{} at {}".format(len(results), i, time_str))
            if results is None:
                pass
            else:
                primes += results

        print("main__ get answer ....")
        print("main__ now there is {} primes".format(len(primes)))
        st = ed
        ed = st * 8
        print("main__ st: {} ed: {}".format(st, ed))

    for i in range(n):
        queues[i][0].put(b'stop')

    print("main__ send stop msg over")


def worker_3(i, queues):
    print("process{} start....".format(i))
    while True:
        print("process{} wait for data....".format(i))
        nums = queues[0].get()
        if not isinstance(nums, range):
            # 如果接收到的对象不是range类型 就终止进程
            if nums == b'stop':
                print("process{} end....".format(i))
                break
            else:
                print(pickle.loads(nums))
        else:
            print(nums)

        byte_primes = queues[1].get()
        primes = pickle.loads(byte_primes)

        print("process{} get {} primes {} number data....".format(i, len(primes), len(nums)))
        p_list = []
        for num in nums:
            for p in primes:
                if num % p == 0:
                    break
            else:
                p_list.append(num)

        time_str = time.strftime("%H:%M:%S", time.localtime())
        print("process{} push data at {}....".format(i, time_str))
        queues[2].put(pickle.dumps(p_list))
        time_str = time.strftime("%H:%M:%S", time.localtime())
        print("process{} push data over at {}....".format(i, time_str))


if __name__ == '__main__':
     main_3(4)
