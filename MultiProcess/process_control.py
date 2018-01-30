# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import multiprocessing as mp
import os,time


def control(n):
    pool = mp.Pool()
    start_time_main = time.time()
    for i in range(n):
        pool.apply_async(task, args=(i, ))
    print('pool start')
    pool.close()
    pool.join()
    used_time = time.time()-start_time_main
    print('{} process total used {:.4f}s'.format(n, used_time))
    with open("log.txt", 'a') as f:
        f.write(str(round(used_time, 2)) + '\n')


def task(i):
    start_time = time.time()
    primes = list()
    x = 1
    while x < 10000:
        x += 1
        for z in primes:
            if x % z == 0:
                break
        else:
            primes.append(x)

    print('process {} find {} primes used {:4f}s'.format(i, len(primes), time.time()-start_time))
    # print(primes)


if __name__ == '__main__':
    task(0)
    with open("log.txt", 'w') as f:
        pass
    for i in range(1):
        control(1)
