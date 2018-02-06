# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import multiprocessing
from multiprocessing import Pool
import time
import pickle


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

        time.sleep(1)
        print("process{} push data....".format(i))
        new_prime_get_queue.put(pickle.dumps(p_list))
        print("process{} push data over....".format(i))
        time.sleep(0.1 + i / 1000)


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
        ed = ed + 1000
        print("main__ st: {} ed: {}".format(st, ed))

    for _ in jobs:
        num_get_queue.put(b'stop')
        time.sleep(0.05)

    print("main__ send stop msg over")


if __name__ == "__main__":
    main_2(4)