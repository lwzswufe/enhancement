# author='lwz'
# coding:utf-8
import numpy as np


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
        if isinstance(item, tuple) and len(item) == 2:
            if isinstance(item[1], str):
                item = (item[0], self.columns_dict[item[1]])
            elif isinstance(item[1], list):
                if isinstance(item[1][0], str):
                    idxs = [self.columns_dict[key] for key in item[1]]
                    item = (item[0], idxs)

        elif isinstance(item, str):
            item = (slice(None, None, None), self.columns_dict[item])

        elif isinstance(item, list):
            if isinstance(item[0], str):
                idxs = [self.columns_dict[key] for key in item]
                item = (slice(None, None, None), idxs)

        self.data[item] = value

if __name__ == "__main__":
    a = Arr()
    a.set_columns(["zero", "one", "two", "three", "four"])
    print(a.data)
    a['three'] = np.ones(5)
    print(a.data)
    a[1, ['one', 'four']] = 3
    print(a.data)

