# author='lwz'
# coding:utf-8
# 疯狂的司机——模糊Q学习
import numpy as np
from numpy import inf, sin, cos, pi
from ReinforcementLearning.Car import car, fuzzy_membership

direction_n = 6
distance_n = 3
speed_action_n = 2
direction_action_n = 2
action_n = speed_action_n * direction_action_n
state_n = direction_n * distance_n

direction_class = np.array([[cos(x/direction_n * pi), sin(x/direction_n * pi)]
                   for x in range(direction_n)])
# 方向类中心
distance_class = np.log(np.array([2, 4, 8]) + 1.0)
# 距离类中心


V_1 = np.zeros(state_n, action_n)
V_2 = np.zeros(state_n, action_n)
V_1_ = np.ones(state_n, action_n) * inf
V_2_ = np.ones(state_n, action_n) * inf

car_1 = car(x=3, y=3, v=2, a=pi/8, d_s=pi/12, v_s=0.1)
# 逃跑者 转向块 加速慢
car_2 = car(x=0, y=0, v=0, a=pi/8, d_s=pi/36, v_s=0.2)
# 追击者 转向慢 加速快
'''
利用矩阵Q的算法如下：
1、设置当前状态=初始状态；
2、从当前状态开始，寻找具有最高Q值的动作；
3、设置当前状态=下一个状态；
4、重复步骤2和3，直到当前状态=目标状态。
'''
iter = 0

while iter < 500000:
    iter += 1
    state_car_1 = fuzzy_membership(car_1.x, car_1.y, car_2.x, car_2.y,
                                   direction_class, distance_class)

    state_car_2 = fuzzy_membership(car_2.x, car_2.y, car_1.x, car_1.y,
                                   direction_class, distance_class)
    
    if np.random.rand() < 0.05:
        action = np.random.randint(0, action_n)


    next_state = Link[state, action]
    next_action = np.argmax(q[next_state, :])
    delta = gamma * q[next_state, next_action] - q[state, action] + R[state, action]
    q[state, action] += alpha * delta

    if np.sum(abs(q1-q)) < 0.000001 and np.sum(q) > 0:
        if count > 50000:
            print(iter, count)
            break          # for
        else:
             count += 1  # set counter if deviation of q is small

        print(np.round(q, 2))
    else:
        q1 = q
        count = 0


print('迭代次数：{}'.format({iter}))
print(np.round(T, 2))
print(np.round(q1, 2))

