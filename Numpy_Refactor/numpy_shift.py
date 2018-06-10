# author='lwz'
# coding:utf-8
import numpy as np
import time
'''
拦截索引
'''


class Arr():
    def __init__(self, nrow=5000, ncol=5):
        self.data = np.zeros([nrow, ncol])
        for i in range(nrow):
            self.data[i, :] += i

    def set_columns(self, columns):
        assert len(columns) == self.data.shape[1]
        self.columns = columns
        self.columns_dict = dict(zip(columns, range(len(columns))))
        print(self.columns_dict)

    def shift(self, t, column=None, fill_nan=True):   # 前移 后移
        time_st = time.time()

        if column is None:
            zero_arr = np.zeros(self.data.shape)
            col_slice = slice(None, None, None)
            col_slice_new = slice(None, None, None)
        else:
            zero_arr = np.zeros([self.data.shape[0]])
            col_slice = self.columns_dict[column]
            col_slice_new = 0

        if fill_nan:
            fill_data = np.nan
        elif t > 0:
            fill_data = self.data[0, col_slice]
        else:
            fill_data = self.data[-1, col_slice]

        if t > 0:
            if isinstance(col_slice_new, int):
                zero_arr[t:] = self.data[:-t, col_slice]
                zero_arr[:t] = fill_data
            else:
                zero_arr[t:] = self.data[:-t, col_slice]
                zero_arr[:t] = fill_data

        elif t < 0:
            if isinstance(col_slice_new, int):
                zero_arr[:t] = self.data[-t:, col_slice]
                zero_arr[t:] = fill_data
            else:
                zero_arr[:t, :] = self.data[-t:, col_slice]
                zero_arr[t:, :] = fill_data
        else:
            zero_arr = self.data[:, col_slice]

        print("used {:.12f}s".format(time.time() - time_st))
        return zero_arr.shape


if __name__ == "__main__":
    a = Arr()
    a.set_columns(["zero", "one", "two", "three", "four"])
    # print(a.data)
    print(a.shift(2))
    print(a.shift(-1))
    print(a.shift(2, 'zero'))
    print(a.shift(-2, 'four'))
    print(a.shift(2, fill_nan=False))
    print(a.shift(-1, fill_nan=False))
    print(a.shift(2, 'zero', fill_nan=False))
    print(a.shift(-2, 'four', fill_nan=False))