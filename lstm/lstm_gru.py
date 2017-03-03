# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import numpy as np


class LstmParam(object):  # 网络初始化
    def __init__(self, mem_cell_ct, x_dim):
        self.mem_cell_ct = mem_cell_ct  # 细胞记忆维度
        self.x_dim = x_dim  # 外部输入维度
        concat_len = x_dim + mem_cell_ct
        y_len = 1
        # weight matrices
        self.wg = rand_arr(-0.1, 0.1, mem_cell_ct, concat_len)  # 随机矩阵
        self.wi = rand_arr(-0.1, 0.1, mem_cell_ct, concat_len)
        self.wf = rand_arr(-0.1, 0.1, mem_cell_ct, concat_len)
        self.wo = rand_arr(-0.1, 0.1, mem_cell_ct, concat_len)
        self.wh = rand_arr(-0.1, 0.1, mem_cell_ct, mem_cell_ct)
        self.wy = rand_arr(-0.1, 0.1, y_len, mem_cell_ct)
        # bias terms
        self.bg = rand_arr(-0.1, 0.1, mem_cell_ct, 1)
        self.bi = rand_arr(-0.1, 0.1, mem_cell_ct, 1)
        self.bf = rand_arr(-0.1, 0.1, mem_cell_ct, 1)
        self.bo = rand_arr(-0.1, 0.1, mem_cell_ct, 1)
        self.bh = rand_arr(-0.1, 0.1, mem_cell_ct, 1)
        self.by = rand_arr(-0.1, 0.1, y_len, 1)
        # diffs (derivative of loss function w.r.t. all parameters)
        self.wg_diff = np.zeros_like(self.wg)
        self.wi_diff = np.zeros_like(self.wi)
        self.wf_diff = np.zeros_like(self.wf)
        self.wo_diff = np.zeros_like(self.wo)
        self.wh_diff = np.zeros_like(self.wh)
        self.wy_diff = np.zeros_like(self.wy)

        self.bg_diff = np.zeros_like(self.bg)
        self.bi_diff = np.zeros_like(self.bi)
        self.bf_diff = np.zeros_like(self.bf)
        self.bo_diff = np.zeros_like(self.bo)
        self.bh_diff = np.zeros_like(self.bh)
        self.by_diff = np.zeros_like(self.by)

    def apply_diff(self, lr=1):  # 梯度下降法修正误差
        self.wg -= lr * self.wg_diff
        self.wi -= lr * self.wi_diff
        self.wf -= lr * self.wf_diff
        self.wo -= lr * self.wo_diff
        self.wh -= lr * self.wh_diff
        self.wy -= lr * self.wy_diff

        self.bg -= lr * self.bg_diff
        self.bi -= lr * self.bi_diff
        self.bf -= lr * self.bf_diff
        self.bo -= lr * self.bo_diff
        self.bh -= lr * self.bh_diff
        self.by -= lr * self.by_diff
        # reset diffs to zero
        self.wg_diff = np.zeros_like(self.wg)
        self.wi_diff = np.zeros_like(self.wi)
        self.wf_diff = np.zeros_like(self.wf)
        self.wo_diff = np.zeros_like(self.wo)
        self.wh_diff = np.zeros_like(self.wh)
        self.wy_diff = np.zeros_like(self.wy)

        self.bg_diff = np.zeros_like(self.bg)
        self.bi_diff = np.zeros_like(self.bi)
        self.bf_diff = np.zeros_like(self.bf)
        self.bo_diff = np.zeros_like(self.bo)
        self.bh_diff = np.zeros_like(self.bh)
        self.by_diff = np.zeros_like(self.by)


class LstmState(object):
    def __init__(self, mem_cell_ct, x_dim):  # 节点状态
        self.g = np.zeros([mem_cell_ct, 1])
        self.i = np.zeros([mem_cell_ct, 1])
        self.f = np.zeros([mem_cell_ct, 1])
        self.o = np.zeros([mem_cell_ct, 1])
        self.s = np.zeros([mem_cell_ct, 1])
        self.h = np.zeros([mem_cell_ct, 1])
        self.hh = np.zeros([mem_cell_ct, 1])
        self.y = np.zeros(1)  # y_len
        self.bottom_diff_h = np.zeros_like(self.h)
        self.bottom_diff_s = np.zeros_like(self.s)
        self.bottom_diff_x = np.zeros(x_dim)


class LstmNode(object):
    def __init__(self, lstm_param, lstm_state):
        # store reference to parameters and to activations
        self.state = lstm_state
        self.param = lstm_param  # net对象
        # non-recurrent input to node
        self.x = None
        # non-recurrent input concatenated with recurrent input
        self.xc = None
        self.sc = None
        self.h_prev = None
        self.s_prev = None

    def bottom_data_is(self, x, s_prev=None, h_prev=None):  # 前向计算
        # if this is the first lstm node in the network
        if s_prev is None:
            s_prev = np.zeros_like(self.state.s)
        if h_prev is None:
            h_prev = np.zeros_like(self.state.h)
        # save data for use in backprop
        self.s_prev = s_prev
        self.h_prev = h_prev

        # concatenate x(t) and h(t-1)
        xc = np.vstack((x,  h_prev))
        self.state.g = np.tanh(np.dot(self.param.wg, xc) + self.param.bg)
        self.state.i = sigmoid(np.dot(self.param.wi, xc) + self.param.bi)  # input gate
        self.state.f = sigmoid(np.dot(self.param.wf, xc) + self.param.bf)  # forget gate
        self.state.o = sigmoid(np.dot(self.param.wo, xc) + self.param.bo)  # output gate
        self.state.s = self.state.g * self.state.i + s_prev * self.state.f
        # s_t = new_message * input_gate + s_t-1 * forget_gate
        self.state.hh = np.tanh(np.dot(self.param.wh, self.state.s) + self.param.bh)
        self.state.h = self.state.hh * self.state.o
        self.state.y = sigmoid(np.dot(self.param.wy, self.state.h) + self.param.by)
        # cell output for gru model
        # self.state.h = self.state.s * self.state.o  # output
        self.x = x
        self.xc = xc
        self.sc = self.state.s

    def top_diff_is(self, top_diff_h, top_diff_s, loss_y):  # 后向计算
        # notice that top_diff_s is carried along the constant error carousel
        # 注意 top_diff_表示是前N个神经元通过state传递下来的常数误差
        # self.state.o * top_diff_h 表示这个神经元通过链式求导传递进来的误差
        dh = self.param.wy.T * loss_y + top_diff_h
        dhh = dh * self.state.o
        ds = np.dot(self.param.wh.T, (1 - self.state.hh ** 2) * dhh) + top_diff_s
        do = dh * self.state.hh
        di = ds * self.state.g
        dg = ds * self.state.i
        df = ds * self.s_prev

        # diffs w.r.t. vector inside sigma / tanh function
        # diff(1/(1 + exp(-x))) = y(1 - y)
        di_input = (1. - self.state.i) * self.state.i * di
        df_input = (1. - self.state.f) * self.state.f * df
        do_input = (1. - self.state.o) * self.state.o * do
        # diff(tanh) = 1 - tanh^2 = 1 - y^2
        dg_input = (1. - self.state.g ** 2) * dg
        dh_input = (1. - self.state.hh ** 2) * dhh
        dy_input = loss_y

        # diffs w.r.t. inputs
        self.param.wi_diff += np.outer(di_input, self.xc)
        self.param.wf_diff += np.outer(df_input, self.xc)
        self.param.wo_diff += np.outer(do_input, self.xc)
        self.param.wg_diff += np.outer(dg_input, self.xc)
        self.param.wh_diff += np.outer(dh_input, self.sc)
        self.param.wy_diff += np.outer(dy_input, self.state.h)

        self.param.bi_diff += di_input
        self.param.bf_diff += df_input
        self.param.bo_diff += do_input
        self.param.bg_diff += dg_input
        self.param.bh_diff += dh_input
        self.param.by_diff += dy_input

        # compute bottom diff
        dxc = np.zeros_like(self.xc)
        dxc += np.dot(self.param.wi.T, di_input)
        dxc += np.dot(self.param.wf.T, df_input)
        dxc += np.dot(self.param.wo.T, do_input)
        dxc += np.dot(self.param.wg.T, dg_input)

        # save bottom diffs
        self.state.bottom_diff_s = ds * self.state.f
        self.state.bottom_diff_x = dxc[:self.param.x_dim]
        self.state.bottom_diff_h = dxc[self.param.x_dim:]


class LstmNetwork(object):
    def __init__(self, lstm_param):
        self.lstm_param = lstm_param
        self.lstm_node_list = []  # 节点(Node)
        # input sequence
        self.x_list = []
        self.y_list = list()

    def y_list_is(self, y_list, loss_layer):
        """
        Updates diffs by setting target sequence
        with corresponding loss layer.
        Will *NOT* update parameters.  To update parameters,
        call self.lstm_param.apply_diff()
        计算误差并且计算梯度
        """
        assert len(y_list) == len(self.x_list)
        # assert语句用来声明某个条件是真的 当assert语句失败的时候，会引发一AssertionError
        idx = len(self.x_list) - 1
        # first node only gets diffs from label ...
        loss = loss_layer.loss(self.lstm_node_list[idx].state.y, y_list[idx])
        if len(self.y_list) == 0:
            for y in y_list:
                self.y_list.append(list())
        self.y_list[0].append(self.lstm_node_list[idx].state.y[0, 0])
        # 损失函数
        loss_y = loss_layer.bottom_diff(self.lstm_node_list[idx].state.y, y_list[idx])
        # here s is not affecting loss due to h(t+1), hence we set equal to zero
        diff_h = np.zeros([self.lstm_param.mem_cell_ct, 1])
        diff_s = np.zeros([self.lstm_param.mem_cell_ct, 1])
        self.lstm_node_list[idx].top_diff_is(diff_h, diff_s, loss_y)  # 修正net
        idx -= 1

        # ... following nodes also get diffs from next nodes, hence we add diffs to diff_h
        # we also propagate error along constant error carousel using diff_s
        # 按时间从后向前迭代
        while idx >= 0:
            loss += loss_layer.loss(self.lstm_node_list[idx].state.y, y_list[idx])
            loss_y = loss_layer.bottom_diff(self.lstm_node_list[idx].state.y, y_list[idx])
            diff_h += self.lstm_node_list[idx + 1].state.bottom_diff_h
            diff_s = self.lstm_node_list[idx + 1].state.bottom_diff_s
            self.lstm_node_list[idx].top_diff_is(diff_h, diff_s, loss_y)  # 修正net
            self.y_list[len(self.x_list) - idx - 1].append(self.lstm_node_list[idx].state.y[0, 0])
            idx -= 1

        return loss

    def x_list_clear(self):
        self.x_list = []

    def x_list_add(self, x):
        self.x_list.append(x)
        if len(self.x_list) > len(self.lstm_node_list):
            # need to add new lstm node, create new state mem
            lstm_state = LstmState(self.lstm_param.mem_cell_ct, self.lstm_param.x_dim)
            # 初始化状态参数
            self.lstm_node_list.append(LstmNode(self.lstm_param, lstm_state))

        # get index of most recent x input
        idx = len(self.x_list) - 1
        if idx == 0:
            # no recurrent inputs yet
            self.lstm_node_list[idx].bottom_data_is(x)  # 预测/计算输出
        else:
            s_prev = self.lstm_node_list[idx - 1].state.s
            h_prev = self.lstm_node_list[idx - 1].state.h
            self.lstm_node_list[idx].bottom_data_is(x, s_prev, h_prev)


def sigmoid(x):  # 激活函数
    return 1. / (1 + np.exp(-x))


# createst uniform random array w/ values in [a,b) and shape args
# 创建均匀分布[a, b]
# 当函数的参数不确定时，可以使用*args和**kwargs。*args没有key值，**kwargs有key值
def rand_arr(a, b, *args):
    np.random.seed(0)
    return np.random.rand(*args) * (b - a) + a


if __name__ == "__main__":
    pass
