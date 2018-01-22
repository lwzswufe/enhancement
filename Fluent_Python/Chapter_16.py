# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import inspect
from functools import wraps
from collections import namedtuple


Result = namedtuple('Result', 'count average')
'''
协程状态：
'GEN_CREATED': Waiting to start execution.
                等待开始执行
'GEN_RUNNING': Currently being executed by the interpreter.[
                解释器正在执行
'GEN_SUSPENDED' Currently suspended at a yield expression.
                在yield表达式处暂停
'GEN_CLOSED' Execution has completed.
                执行结束
'''


def simple_coroutine():  # 1
    print('-> coroutine started')
    x = yield  # yield 后面没有表达式 默认返回None
    print('-> coroutine received:', x)
    print("-> Stop")


def simple_coro2(a):
    print('-> Started: a =', a)
    b = yield a  # 产出a的值 暂停 并等待为b赋值
    print('-> Received: b =', b)
    print("value a = {}, b = {}".format(a, b))
    c = yield a + b
    print('-> Received: c =', c)
    print("-> Stop")


def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count


def coroutine3(func):
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer


@coroutine3
def coro_averager():
    print("start 预激协程的装饰器")
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count


def averager2():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)


def gen_1():
    for c in "AB":
        yield c
    for i in range(1, 3):
        yield i


def gen_2():
    print("在def gen() 中 \nyield from x 会将控制权转移给x 并将返回的值传递给调用方")
    print("与此同时gen()会阻塞并等待x终止")
    yield from 'AB'
    yield from range(1, 3)


# 子生成器
def averager3():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)


# the delegating generator
# 委派生成器
def grouper(results, key):
    while True:
        results[key] = yield from averager3()


# the client code, a.k.a. the caller
# 客户端代码 调用方
def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)
        # 预激 group 协程
        for value in values:
            group.send(value)

        group.send(None)  # important!
        # 输入None以终止迭代器 yield from 会自动捕获StopIteration
    # print(results) # uncomment to debug
    report(results)
    # output report


# 输出报告
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
        result.count, group, result.average, unit))

data = {
    'girls;kg':
    [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
    [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
    [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
    [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
    }


if __name__ == "__main__":
    my_coro = simple_coroutine()
    print("返回的是一个生成器，程序并没有开始运行: \n", my_coro)
    print('协程状态：', inspect.getgeneratorstate(my_coro))
    print("调用next方法后 程序开始运行")
    next(my_coro)
    print('协程状态：', inspect.getgeneratorstate(my_coro))

    try:
        my_coro.send(42)
    except StopIteration:
        print('协程状态：', inspect.getgeneratorstate(my_coro))

    print("\n\n########################\n\n")

    my_coro2 = simple_coro2(14)
    print('协程状态：', inspect.getgeneratorstate(my_coro2))
    next(my_coro2)
    print('协程状态：', inspect.getgeneratorstate(my_coro2))
    my_coro2.send(28)
    print('协程状态：', inspect.getgeneratorstate(my_coro2))
    # next(my_coro2.send(99))
    try:
        my_coro2.send(99)
        print('_协程状态：', inspect.getgeneratorstate(my_coro2))
        next(my_coro2)
        print('_协程状态：', inspect.getgeneratorstate(my_coro2))
    except StopIteration as err:
        print('a协程状态：', inspect.getgeneratorstate(my_coro2))

    print("\n\n########################\n\n")

    coro_avg = averager()
    print('协程状态：', inspect.getgeneratorstate(coro_avg))
    next(coro_avg)
    print('协程状态：', inspect.getgeneratorstate(coro_avg))
    print("平均值:", coro_avg.send(5))
    print("平均值:", coro_avg.send(20))
    print("平均值:", coro_avg.send(15))
    coro_avg.close()
    print('协程状态：', inspect.getgeneratorstate(coro_avg))

    print("\n\n########################\n\n")
    coro_avg = coro_averager()
    print('协程状态：', inspect.getgeneratorstate(coro_avg))
    print("平均值:", coro_avg.send(5))
    print("平均值:", coro_avg.send(20))
    print("平均值:", coro_avg.send(15))
    coro_avg.close()
    print('协程状态：', inspect.getgeneratorstate(coro_avg))

    print("\n\n########################\n\n")

    coro_avg = averager2()
    print('协程状态：', inspect.getgeneratorstate(coro_avg))
    next(coro_avg)
    print('协程状态：', inspect.getgeneratorstate(coro_avg))
    print("平均值:", coro_avg.send(5))
    print("平均值:", coro_avg.send(20))
    print("平均值:", coro_avg.send(15))
    try:
        print("输入None终止程序:", coro_avg.send(None))
    except StopIteration as err:
        print(err.value)
    print("输入None终止程序 并关闭协程")
    # coro_avg.close()
    print('协程状态：', inspect.getgeneratorstate(coro_avg))

    print("\n\n########################\n\n")
    print('yield     :', list(gen_1()))
    print('yield from:', list(gen_2()))

    print("\n\n########################\n\n")
    main(data)

