# author='lwz'
# coding:utf-8
import numpy as np
import time
'''
拦截索引
'''


class Arr():
    def __init__(self, nrow=50000, ncol=5):
        self.data = np.zeros([nrow, ncol])

    def set_columns(self, columns):
        assert len(columns) == self.data.shape[1]
        self.columns = columns
        self.columns_dict = dict(zip(columns, range(len(columns))))
        print(self.columns_dict)

    def append_col(self, n):
        time_st = time.time()
        self.data = np.hstack((self.data, np.zeros([self.data.shape[0], n])))
        print("used {:.4f}s".format(time.time() - time_st))

if __name__ == "__main__":
    a = Arr()
    a.append_col(3)
