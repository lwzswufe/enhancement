# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import pandas as pd
import numpy as np
import tushare as ts

s = pd.Series([1, 7, -3, 5], index=['a', 'b', 'c', 'd'])
print('a' in s)

sdata = {'a':10, 'b':0}
s2 = pd.Series(sdata)

print('pandas 自动对齐索引:\n', s + s2)

data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}
df = pd.DataFrame(data)
print('由字典生成DataFrame:\n', df)
print('DataFrame转置:\n', df.T)

obj3 = pd.Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])
print('重新索引并向前填充缺失值:\n', obj3.reindex(range(6), method='ffill'))
# 向后填充bfill

data = pd.DataFrame(np.arange(16).reshape((4, 4)),
                 index=['Ohio', 'Colorado', 'Utah', 'New York'],
                 columns=['one', 'two', 'three', 'four'])

print('通过布尔数组选取行\n', data[data['three'] > 5])
print('通过切片选取行\n', data[:2])
print('通过布尔型DataFrame\n', data[data<5])

print('通过DataFrame.ix\n',data.ix['Colorado', ['two', 'three']])
print('通过DataFrame.ix\n',data.ix[['Colorado', 'Utah'], [3, 0, 1]])

frame = pd.DataFrame(np.arange(12.).reshape((4, 3)), columns=list('bde'),
                  index=['Utah', 'Ohio', 'Texas', 'Oregon'])
series = frame.ix[0]
f = lambda x: x.max() - x.min()
print('函数映射到每列:\n', frame.apply(f))
print('函数映射到每行:\n', frame.apply(f, axis=1))
format = lambda x: '%.2f' % x
print('函数映射到每个元素:\n',frame.applymap(format))

# df = ts.get_today_all()
# print(df.index.is_unique)

obj = pd.Series(['c', 'a', 'd', 'a', 'a', 'b', 'b', 'c', 'c'])
print('频率统计:\n',obj.value_counts())

data = pd.Series(np.random.randn(10),
              index=[['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'd', 'd'],
                     [1, 2, 3, 1, 2, 3, 1, 2, 2, 3]])
print('层次化索引:\n',obj.value_counts())