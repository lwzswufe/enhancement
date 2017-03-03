# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import numpy as np
from lstm_gru import LstmParam, LstmNetwork
import matplotlib.pyplot as plt
# from lstm import lstm


class ToyLossLayer(object):
    """
    Computes square loss with first element of hidden layer array.
    """
    @classmethod
    def loss(self, pred, label):
        return (pred[0] - label) ** 2  # 误差函数  **=^
    # 一般来说，要使用某个类的方法，需要先实例化一个对象再调用方法。
    # 而使用@staticmethod或@classmethod，就可以不需要实例化，直接类名.方法名()来调用。

    @classmethod
    def loss2(self, pred, label):
        s = pred * np.log(label + 0.01) + (1 - pred) * np.log(1 - label + 0.01)  # 误差函数  **=^
        return s[0, 0]

    @classmethod
    def bottom_diff(self, pred, label):
        diff = np.zeros_like(pred)
        diff[0] = pred[0] - label
        return diff
    # 损失函数的导函数


def example_0():
    # learns to repeat simple sequence from random inputs
    np.random.seed(0)
    # 一般计算机的随机数都是伪随机数，以一个真随机数（种子）作为初始条件，然后用一定的算法不停迭代产生随机数

    # parameters for input data dimension and lstm cell count
    mem_cell_ct = 7  # hidden 输出的维度
    x_dim = 50  # 输入变量维度
    lstm_param = LstmParam(mem_cell_ct, x_dim)  # 神经网络初始化 返回初始化的net对象
    lstm_net = LstmNetwork(lstm_param)
    y_list = [0.5, 0.4, 0.7, 0.9, 0.1]
    input_val_arr = [np.random.random([x_dim, 1]) for _ in y_list]
    loss = list()
    loss_diff = 1
    cur_iter = 0
    lr0 = 0.8
    lr = 0.42
    lr_list = list()
    attenuation = 0.99

    while cur_iter < 400 and loss_diff > -9999:  # 迭代次数
        for ind in range(len(y_list)):
            lstm_net.x_list_add(input_val_arr[ind])
            # print("y_pred[%d] : %f" % (ind, lstm_net.lstm_node_list[ind].state.y[0]))

        loss.append(lstm_net.y_list_is(y_list, ToyLossLayer))  # 计算误差并且计算梯度
        if cur_iter > 1:
            loss_diff = loss[cur_iter - 1] - loss[cur_iter]
        cur_iter += 1
        # lr = lr0 / (1 + np.exp(cur_iter*0.0085))
        lr *= attenuation
        lr_list.append(lr)
        lstm_param.apply_diff(lr=lr)  # 梯度下降法 修正net
        lstm_net.x_list_clear()
        # print(lstm_net.lstm_node_list[2].param.wg[0] - lstm_param.wg[0])
    print("lr:", lr)
    print("loss_diff: ", loss_diff)
    print("loss: ", loss[cur_iter - 1])
    for ind in range(len(y_list)):
        print("y_pred[%d] : %f" % (ind, lstm_net.lstm_node_list[ind].state.y[0]))
    legend = ['loss', 'lr']
    i = 0
    plt.plot(loss)
    plt.plot(lr_list)
    for y in lstm_net.y_list:
        plt.plot(y, '.')
        i += 1
        legend.append('y_' + str(i))
    plt.legend(legend)
    plt.show()

if __name__ == "__main__":
    example_0()

