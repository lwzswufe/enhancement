# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import multiprocessing as mp
import os,time


def control(n):
    pool = mp.Pool()
    start_time = time.time()
    for i in range(n):
        pool.apply_async(task, args=(i, ))
    print('pool start')
    pool.close()
    pool.join()
    print('{} process total used {:.4f}s'.format(n, time.time()-start_time))

def task(i):
    start_time = time.time()
    primes = list()
    x = 1
    while x < 100000:
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
    control(4)
