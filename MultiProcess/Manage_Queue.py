# author='lwz'
# coding:utf-8
import multiprocessing
import time
'''
Python中进程间共享数据，处理基本的queue，pipe和value+array外，还提供了更高层次的封装。
使用multiprocessing.Manager可以简单地使用这些高级接口。
Manager()返回的manager对象控制了一个server进程，此进程包含的python对象
可以被其他的进程通过proxies来访问。从而达到多进程间数据通信且安全。

Manager支持的类型有list,dict,Namespace,Lock,RLock,Semaphore,BoundedSemaphore,Condition,Event,Queue,Value和Array。

'''


def worker(n, i, prime, st):
    while st < 10000:
        for p in prime:
            if st % p == 0:
                break
        else:
            prime.append(st)

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

if __name__ == '__main__':
     main()
