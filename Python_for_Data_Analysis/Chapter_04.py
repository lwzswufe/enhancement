# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import numpy as np

arr = np.arange(32).reshape((8, 4))
print(arr)
print(arr[[1, 5, 2], [0, 2, 1]])         # 选取元素
print(arr[[1, 5, 2]][:, [0, 2, 1]])      # 分两步选取 一步选取行 一步选取列
ixgrid = np.ix_([1, 5, 2], [0, 2, 1])    # 生成索引器
print(arr[ixgrid])                       # 一次性选取行 + 列

xarr = np.array([1, 2, 3])
yarr = np.array([0.1, 0.2, 0.3])
cond = np.array([True, False, True])

result = [(x if c else y) for x, y, c in zip(xarr, yarr, cond)]
print(result)

result = np.where(cond, xarr, yarr)
print(result)

print('any is True:', cond.any())
print('all is True:', cond.all())

arr = np.random.randn(8)
print(arr)
np.sort(arr)
print(arr)                            # arr is not changed
arr.sort()                            # arr is changed
print(arr)

s = 'shdadjhauwhdkadkajd'
cs = np.array([x for x in s])
print(cs)
print('np.unique, 去重并排序:', np.unique(cs))


arr = np.random.randn(4, 4)
np.save('some_array', arr)
arr_read = np.load('some_array.npy')
print('写入,读取npy文件：\n', arr_read)

arr = np.loadtxt('array_ex', delimiter=',', dtype=float)
print('读取文档数据：\n', arr)