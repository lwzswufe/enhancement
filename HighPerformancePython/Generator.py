# author='lwz''
# coding:utf-8
from functools import reduce
from math import log


f = lambda x: True if x > 20 else False
a = [2, 32, 41, 1, 4, 7, 81]
g = filter(f, a)
print("filter函数会对指定序列执行过滤操作。")
print(list(g))

f = lambda x, y: (x, y)
x = [0, 1, 2, 3, 4, 5, 6 ]
y = ['Sun', 'M', 'T', 'W', 'T', 'F', 'S']
g = map(f, y, x)
print("map()将函数调用映射到每个序列的对应元素上并返回一个含有所有返回值的列表")
print(list(g))

f = lambda past, new: past * 0.9 + new * 1.0
x = [1, 3, 5, 7, 9]
g = reduce(f, x, 1)
print("意思就是对sequence连续使用function, 如果不给出initial, 则第一次调用传递sequence的两个元素,"
      " 以后把前一次调用的结果和sequence的下一个元素传递给function. 如果给出initial, 则第一次传递"
      "initial和sequence的第一个元素给function.")
print(g)

