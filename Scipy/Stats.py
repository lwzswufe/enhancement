# author='lwz'
# coding:utf-8

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt


def gamma(param):
    '''
    gamma 分布
    :param param:
    :return:
    '''
    x = np.array(range(101))
    y = stats.gamma.cdf(x, param[0], param[1])
    plt.plot(y)
    plt.show()
    y = stats.gamma.pdf(x, param[0], param[1])
    plt.plot(y)
    plt.show()


def expon(param):
    '''
    gamma 分布
    :param param:
    :return:
    '''
    x = np.array(range(101))
    y = stats.expon.cdf(x, param[0])
    plt.plot(y)
    plt.show()
    y = stats.expon.pdf(x, param[0])
    plt.plot(y)
    plt.show()


if __name__ == "__main__":
    expon([5])