# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
# 绘制科赫曲线
from numpy import *
import matplotlib.pyplot as plt

'''
绘制科赫曲线 分形
'''


def fractal(x, y, length):
    x_st = x[:-1]
    x_ed = x[1:]
    y_st = y[:-1]
    y_ed = y[1:]

    x1 = x_st * 2/3 + x_ed * 1/3
    x2 = x_st * 1/2 + x_ed * 1/2 - (y_ed - y_st) / 2 / sqrt(3)
    x3 = x_st * 1/3 + x_ed * 2/3

    y1 = y_st * 2/3 + y_ed * 1/3
    y2 = y_st * 1/2 + y_ed * 1/2 + (x_ed - x_st) / 2 / sqrt(3)
    y3 = y_st * 1/3 + y_ed * 2/3

    length *= 1/3
    x = concatenate([x_st, x1, x2, x3], axis=1)
    x = concatenate([x.flatten(), x_ed[-1]])
    x = x.reshape([x.size, 1])
    y = concatenate([y_st, y1, y2, y3], axis=1)
    y = concatenate([y.flatten(), y_ed[-1]])
    y = y.reshape([y.size, 1])
    return x, y, length


def main(x=array([0, 1]), y=array([0, 0]), length=1):
    x = x.reshape([x.size, 1])
    y = y.reshape([y.size, 1])
    for i in range(6):
        plt.subplot(2, 3, i+1)
        plt.plot(x, y)
        x, y, length = fractal(x, y, length)
    plt.show()


def Hexagon(length=1):
    x = array([-1/2, 1/2]) * length
    y = array([1/sqrt(3)/2, 1/sqrt(3)/2]) * length
    x = x.reshape([x.size, 1])
    y = y.reshape([y.size, 1])
    for i in range(6):
        plt.subplot(2, 3, i+1)
        plt.plot(x, y)
        theta = 2 * pi / 3
        plt.plot(x * cos(theta) - y * sin(theta), x * sin(theta) + y * cos(theta))
        theta = 4 * pi / 3
        plt.plot(x * cos(theta) - y * sin(theta), x * sin(theta) + y * cos(theta))
        x, y, length = fractal(x, y, length)
    plt.show()


if __name__ == '__main__':
    main()
    Hexagon()
