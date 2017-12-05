# author='lwz'
# coding:utf-8
from numpy import sin, cos, power
import numpy as np


class car(object):
    '''
    x : x坐标
    y : y坐标
    v : 速度
    a : 车头角度 x轴方向为0
    d_s: 车头转向速度
    v_s: 汽车加速度
    '''
    def __init__(self, x, y, v, a, d_s=3.14159 / 12, v_s=0.1):
        self.x = x
        self.y = y
        self.v = v
        self.a = a
        self.direction_step = d_s
        self.velocity_step = v_s

    def acceleration(self):
        self.v += 0.1

    def decelerate(self):
        self.v = max(0, self.v - 0.1)

    def left_turn(self):
        self.a += self.direction_step

    def right_turn(self):
        self.a -= self.direction_step

    def go(self):
        self.x += self.v * cos(self.a)
        self.y -= self.v * sin(self.a)

    def decision(self, action_id):
        if action_id == 0:
            self.acceleration()
        elif action_id == 1:
            self.decelerate()
        elif action_id == 2:
            self.left_turn()
        elif action_id == 3:
            self.right_turn()
        else:
            print("get error action_id: ", action_id)


def fuzzy_membership(x1, y1, x2, y2, direction_class, distance_class):
    '''
    模糊隶属度
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :param direction_class： 方向聚类中心
    :return:
    '''
    r = np.log(power(x2 - x1, 2) + power(y2 - y1, 2) + 1)
    r = power(distance_class - r, 2)
    r -= min(r)
    r /= np.sum(r)
    # shape[1, m]

    d = direction_class * np.array([[x2 - x1], [y2 - y1]])
    d[d < 0] = 0
    d = np.power(d, 2)
    d /= np.sum(d)
    # shape  [n, 1]

    u = d * r
    # shape [n, m]
    return u.flatten()
