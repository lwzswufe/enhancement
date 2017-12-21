# author='lwz'
# coding:utf-8
# 疯狂的司机——模糊Q学习
import numpy as np
from numpy import inf, sin, cos, pi
from ReinforcementLearning.Car import car, fuzzy_membership
from ReinforcementLearning.fuzzy_logic import *


direction_n = 6
distance_n = 3
speed_action_n = 2
direction_action_n = 2
action_n = speed_action_n * direction_action_n
state_n = direction_n * distance_n

direction_class = np.array([[cos(x/direction_n * 2 * pi), sin(x/direction_n * 2 * pi)]
                   for x in range(direction_n)])
# 方向类中心
c = np.array([2, 4, 8])
distance_class = np.log(c + 1.0)
# 距离类中心

R_1 = (np.ones([direction_n, 1]) * c).flatten()
R_1 = R_1 - np.min(R_1)
R_2 = (np.ones([direction_n, 1]) * c).flatten()


V_1 = np.ones([state_n, action_n])
V_2 = np.ones([state_n, action_n])
V_1_ = np.ones([state_n, action_n]) * inf
V_2_ = np.ones([state_n, action_n]) * inf

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
gamma = 0.90            # learning parameter
alpha = 0.05             # 误差学习速率
lam = 0.5               # lambda 轨迹衰减速率
iter = 0
count = 0
state_car_1 = fuzzy_membership(car_1.x, car_1.y, car_2.x, car_2.y,
                                   direction_class, distance_class)

state_car_2 = fuzzy_membership(car_2.x, car_2.y, car_1.x, car_1.y,
                                   direction_class, distance_class)
while iter < 500000:
    iter += 1

    return_1 = np.dot(state_car_1, V_1)
    return_2 = np.dot(state_car_2, V_2)

    if np.random.rand() < 0.05:
        action_1 = np.random.randint(0, action_n)
    else:
        action_1 = np.argmax(return_1)

    if np.random.rand() < 0.05:
        action_2 = np.random.randint(0, action_n)
    else:
        action_2 = np.argmax(return_2)

    car_1.decision(action_1)
    car_2.decision(action_2)

    next_state_car_1 = fuzzy_membership(car_1.x, car_1.y, car_2.x, car_2.y,
                                   direction_class, distance_class)

    next_state_car_2 = fuzzy_membership(car_2.x, car_2.y, car_1.x, car_1.y,
                                   direction_class, distance_class)

    rho = state_car_1 @ R_1 + gamma * next_state_car_1 @ np.max(V_1, axis=1) - state_car_1 @ V_1[:, action_1]
    # p123 公式5.33
    V_1[:, action_1] += alpha * rho * state_car_1
    # p123 公式5.34

    rho = state_car_2 @ R_2 + gamma * next_state_car_2 @ np.max(V_2, axis=1) - state_car_2 @ V_2[:, action_2]
    # p123 公式5.33
    V_2[:, action_2] += alpha * rho * state_car_2
    # p123 公式5.34


    if np.sum(abs(V_1-V_1_)) + np.sum(abs(V_2-V_2_)) < 0.000001 and np.sum(V_1) > 0:
        if count > 50000:
            print(iter, count)
            break          # for
        else:
             count += 1  # set counter if deviation of q is small

        print(np.round(V_1, 2))
        car_1 = car(x=3, y=3, v=2, a=pi / 8, d_s=pi / 12, v_s=0.1)
        # 逃跑者 转向块 加速慢
        car_2 = car(x=0, y=0, v=0, a=pi / 8, d_s=pi / 36, v_s=0.2)
        # 追击者 转向慢 加速快
        state_car_1 = fuzzy_membership(car_1.x, car_1.y, car_2.x, car_2.y,
                                       direction_class, distance_class)

        state_car_2 = fuzzy_membership(car_2.x, car_2.y, car_1.x, car_1.y,
                                       direction_class, distance_class)
    else:
        V_1_ = V_1
        V_2_ = V_2
        count = 0
        state_car_1 = next_state_car_1
        state_car_2 = next_state_car_2


print('迭代次数：{}'.format({iter}))
print(np.round(V_1, 2))
print(np.round(V_2, 2))

