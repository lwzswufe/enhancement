# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
# 斐波拉契数列


def fib(n=10):
    a, b = 1, 1
    for i in range(n):
        yield a  # 依次返回a的值
        a, b = b, a+b


if __name__ == "__main__":
    print(list(fib(50)))