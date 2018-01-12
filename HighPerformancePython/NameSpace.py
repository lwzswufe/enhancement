# author='scarlett'
# coding:utf-8
import math
from math import sin


z = 1


def test_1(x):
    sin(x)
    print('局部变量', locals())
    print('全局变量', globals().keys())


if __name__ == '__main__':
    x = 5
    test_1(x)
    print('路径:', __file__)
