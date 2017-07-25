# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import pandas as pd
import numpy as np

df = pd.DataFrame({'key1' : ['a', 'a', 'b', 'b', 'a'],
                'key2' : ['one', 'two', 'one', 'two', 'one'],
                'data1' : np.random.randn(5),
                'data2' : np.random.randn(5)})

grouped = df['data1'].groupby(df['key1'])
print('按key1 GroupBy:\n', grouped.mean())
grouped = df['data1'].groupby([df['key1'], df['key2']])
print('按key1, key2 GroupBy:\n', grouped.mean())
print('按key1, key2 GroupBy:\n', grouped.size())

print('按key1 分组迭代')
for name, group in df.groupby('key1'):
    print(name)
    print(group)

print('按key1 key2 分组迭代')
for (k1, k2), group in df.groupby(['key1', 'key2']):
    print((k1, k2))
    print(group)

    grouped = df.groupby(df.dtypes, axis=1)
    print(dict(list(grouped)))

people = pd.DataFrame(np.random.randn(5, 5),
                       columns=['a', 'b', 'c', 'd', 'e'],
                       index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
people.ix[2:3, ['b', 'c']] = np.nan  # Add a few NA values

mapping = {'a': 'red', 'b': 'red', 'c': 'blue',
           'd': 'blue', 'e': 'red', 'f': 'orange'}

by_column = people.groupby(mapping, axis=1)
print('按字典GroupBy：', by_column.sum())

print('通过函数GroupBy：', people.groupby(len).sum())

df = pd.DataFrame({'key1' : ['a', 'a', 'b', 'b', 'a'],
                'key2' : ['one', 'two', 'one', 'two', 'one'],
                'data1' : np.random.randn(5),
                'data2' : np.random.randn(5)})
grouped = df.groupby([df['key1'], df['key2']])

grouped_pct = grouped.agg(['mean', 'std'])
print('面向列的多函数应用：', grouped_pct)
grouped_pct = grouped.agg([('foo', 'mean'), ('bar', np.std)])
# (应用方法， 列名)
print('面向列的多函数应用，自定义新列名：', grouped_pct)
grouped_pct = grouped.agg({'data1' : ['min', 'max', 'mean', 'std'], 'data2' : 'sum'})
# 应用列：应用方法
print('面向列的多函数应用， 不同列使用不同方法：', grouped_pct)

states = ['Ohio', 'New York', 'Vermont', 'Florida',
          'Oregon', 'Nevada', 'California', 'Idaho']
group_key = ['East'] * 4 + ['West'] * 4
data = pd.Series(np.random.randn(8), index=states)
data[['Vermont', 'Nevada', 'Idaho']] = np.nan
fill_mean = lambda g: g.fillna(g.mean())
group_key = ['East'] * 4 + ['West'] * 4
filled_data = data.groupby(group_key).apply(fill_mean)

print('groupby.apply 填充缺失值:\n', filled_data)

