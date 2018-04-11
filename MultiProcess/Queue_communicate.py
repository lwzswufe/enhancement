# author='lwz'
# coding:utf-8
import pickle
from multiprocessing import Pool, Manager, Queue, Process
import time
import random


def task(queue_put, queue_get, process_i):
    while True:
        print("process{} wait for data....".format(process_i))
        data = queue_put.get()

        if data == b'stop':
            print("process{} end....".format(process_i))
            break
        elif data == b'null':
            queue_get.put(pickle.dumps(''))
        else:
            letter = pickle.loads(data)
            print("process{} get data : {}....".format(process_i, letter))
            time.sleep(random.random() * 0.1)
            queue_get.put(pickle.dumps(letter.upper()))
            print("process{} put data : {}....".format(process_i, letter.upper()))


def main(process_n=4):
    '''
    qsize 并不是线程安全的
    Queue(process_n) 需要添加上限以保证主进程不会一次性将所有任务放到队列中
                    任务数到达上限后 主进程会阻塞
    :param process_n:
    :return:
    '''
    print("多进程 单独一个进程负责读写 通过公用的queue通讯 其余进程处理数据")
    jobs = []
    queue_put = Queue(process_n)
    queue_get = Queue()

    for i in range(process_n):
        job = Process(target=task, args=(queue_put, queue_get, i))
        jobs.append(job)
        job.start()
    flag = 0
    string = 'C++ is a middle-level programming language developed by Bjarne Stroustrup starting in 1979 at Bell Labs'
    N = len(string)
    Strings = ''

    while flag < N + process_n:
        # print('flag: {} queue size: {}'.format(flag, queue_get.qsize()))
        if flag >= process_n:
            # time.sleep(0.4)
            letter_upper = pickle.loads(queue_get.get())
            Strings += letter_upper
            print('flag: {} main get: {}'.format(flag, letter_upper))

        if flag < N:
            letter = string[flag]
            if ord(letter) < 96 or ord(letter) > 122:
                queue_put.put(b'null')
            else:
                queue_put.put(pickle.dumps(letter))
            print('flag: {} main put: {} queue size: {}'.format(flag, letter, queue_put.qsize()))

        flag += 1

    print('queue_put qsize: ', queue_put.qsize())
    for i in range(process_n):
        queue_put.put(b'stop')
    print('queue_put qsize: ', queue_put.qsize())
    print(Strings)


if __name__ == '__main__':
    main()
