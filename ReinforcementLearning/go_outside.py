# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
# http://mnemstudio.org/path-finding-q-learning-tutorial.htm
# http://blog.csdn.net/maggie_zhangxin/article/details/73481417
# 强化学习案例1 让机器人学会出门
import numpy as np
from numpy import inf

# 奖励表  行代表行动前的位置  列代表行动（即到达哪一个房间）
# 不能可能到达的区域设置为-inf
R = [[-inf, -inf, -inf, -inf,   0, -inf],
     [-inf, -inf, -inf,   0, -inf, 100],
     [-inf, -inf, -inf,   0, -inf, -inf],
     [-inf,   0,   0, -inf,   0, -inf],
     [0, -inf, -inf,   0, -inf, 100],
     [-inf,   0, -inf, -inf,   0, 100]]
R = np.array(R)

# 矩阵Q的行代表智能体当前的状态，列代表到达下一个状态的可能的动作。
# 因为智能体在最初对环境一无所知，因此矩阵Q被初始化为0。在这个例子中，为了阐述方便，
# 我们假设状态的数量是已知的（设为6）。如果我们不知道有多少状态时，矩阵Q在最初被设为只有一个元素。
# 如果新的状态一旦被发现，对矩阵Q增加新的行和新的列非常简单。
# Q-学习的转换规则非常简单，为下面的式子：
# Q(state, action)=R(state, action) + Gamma * Max(Q[next state, all actions])

gamma = 0.90            # learning parameter
q = np.zeros(R.shape)      # initialize Q as zero,q的行数和列数等于矩阵R的。
q1 = np.ones(R.shape) * inf  # initialize previous Q as big number
count = 0              # counter
position = np.array(range(R.shape[0]))
state_n = R.shape[0]

'''
利用矩阵Q的算法如下：
1、设置当前状态=初始状态；
2、从当前状态开始，寻找具有最高Q值的动作；
3、设置当前状态=下一个状态；
4、重复步骤2和3，直到当前状态=目标状态。
'''
for iter in range(50000):
    # random initial state
    state = np.random.randint(0, state_n)           # 取1到6的随机数的第一个数
    # select any action from this state
    x = position[R[state, :] >= 0]       # find possible action of this state.返回矩阵R第state行所有列中不小于零的数据的下标
    if len(x) == 0:
        continue

    x1 = x[np.random.randint(0, len(x))]               # select an action

    qMax = np.max(R, axis=1)   # get max of all actions 即每行最大值
    q[state, x1] = R[state, x1] + gamma * qMax[x1]  # get max of all actions
    # break if convergence: small deviation on q for 1000 consecutive
    if np.sum(abs(q1-q)) < 0.0001 and np.sum(q > 0):
        if count > 1000:
            print(iter)
            break          # for
        else:
             count += 1  # set counter if deviation of q is small
    else:
        q1 = q
        count = 0  # reset counter when deviation of q from previous q is large

    # normalize q
    g = np.max(q)
    if g > 0:
       q = 100 * q / g


print(np.round(q, 2))



