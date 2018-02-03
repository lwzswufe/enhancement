# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
'''
共享变量
Value的初始化非常简单，直接类似Value(‘d‘, 0.0)即可，具体构造方法为：

multiprocessing.Value(typecode_or_type, *args[, lock])。

该方法返回从共享内存中分配的一个ctypes 对象,其中typecode_or_type定义了返回的类型。
它要么是一个ctypes类型，要么是一个代表ctypes类型的code。比如c_bool和‘b‘是同样的
，因为‘b‘是c_bool的code。

ctypes是Python的一个外部函数库，它提供了和C语言兼任的数据类型，可以调用DLLs或者
共享库的函数，能被用作在python中包裹这些库。

　*args是传递给ctypes的构造参数

Manager利用list()方法提供了表的共享方式。实际上你可以利用dict()来共享词典，
Lock()来共享threading.Lock
'''


import multiprocessing as mp


def worker(d, l, num, arr, key, value):
     d[key] = value
     l.append(value)
     num.value = 3.14
     arr[key] = key


def main():
    mgr = mp.Manager()
    d = mgr.dict()
    l = mgr.list()
    num = mp.Value('d', 0.0)  # 'ctype' value
    arr = mp.Array('i', range(10))  # 'ctype' value
    jobs = [mp.Process(target=worker, args=(d, l, num, arr, i, i*2)) for i in range(10)]
    for j in jobs:
         j.start()
    for j in jobs:
         j.join()

    print('Results:' )
    for key, value in enumerate(dict(d)):
         print("%s=%s" % (key, value))

    print("list:", l)
    print(num.value)
    print(arr)


if __name__ == "__main__":
    main()