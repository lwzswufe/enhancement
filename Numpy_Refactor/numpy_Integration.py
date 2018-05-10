# author='lwz'
# coding:utf-8

# author='lwz'
# coding:utf-8
import numpy as np
'''
拦截索引
'''


class Arr():
    def __init__(self, nrow=5, ncol=5):
        self.data = np.zeros([nrow, ncol])

    def set_columns(self, columns):
        assert len(columns) == self.data.shape[1]
        self.columns = columns
        self.columns_dict = dict(zip(columns, range(len(columns))))
        print(self.columns_dict)

    def __setitem__(self, item, value):        # 拦截分片
        item = self.translate_slice(item)
        self.data[item] = value

    def __getitem__(self, item):        # 拦截分片
        item = self.translate_slice(item)
        return self.data[item]

    def shift(self, t, column=None, fill_nan=True):   # 前移 后移

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

        return zero_arr

    def translate_slice(self, item):                        # 翻译字符指针
        if isinstance(item, tuple) and len(item) == 2:
            if isinstance(item[1], str):    # 取单列
                item = (item[0], self.columns_dict[item[1]])
            elif isinstance(item[1], list):
                if isinstance(item[1][0], str): # 取多列
                    idxs = [self.columns_dict[key] for key in item[1]]
                    item = (item[0], idxs)

        elif isinstance(item, str):   # 取单列
            item = (slice(None, None, None), self.columns_dict[item])

        elif isinstance(item, list):  # 取多列
            if isinstance(item[0], str):
                idxs = [self.columns_dict[key] for key in item]
                item = (slice(None, None, None), idxs)

        return item


def shift(arr, t, fill_nan=True):
    if t == 0:
        return arr

    zero_arr = np.zeros(len(arr))
    fill_data = np.nan

    if t > 0:
        if not fill_nan:
            fill_data = arr[0]

        zero_arr[t:] = arr[:-t]
        zero_arr[:t] = fill_data
    else:
        if not fill_nan:
            fill_data = arr[-1]
            
        zero_arr[:t] = arr[-t:]
        zero_arr[t:] = fill_data

    return zero_arr


if __name__ == "__main__":
    a = Arr()
    a.set_columns(["zero", "one", "two", "three", "four"])
    print(a.data)
    a['three'] = np.ones(5)
    print(a.data)
    a[1, ['one', 'four']] = 3
    print(a.data)