# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import pandas as pd
import numpy as np

df1 = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                 'data1': range(7)})
df2 = pd.DataFrame({'key': ['a', 'b', 'd'],
                 'data2': range(3)})

print('df1:\n', df1)
print('df2:\n', df2)
print('合并df:\n', pd.merge(df1, df2))
print('按key合并df:\n', pd.merge(df1, df2, on='key'))

df1 = pd.DataFrame({'key1': ['foo', 'foo', 'bar'],
                  'key2': ['one', 'two', 'one'],
                  'lval': [1, 2, 3]})
df2 = pd.DataFrame({'key1': ['foo', 'foo', 'bar', 'bar'],
                   'key2': ['one', 'one', 'one', 'two'],
                   'rval': [4, 5, 6, 7]})

print('df1:\n', df1)
print('df2:\n', df2)
print('合并df:\n', pd.merge(df1, df2))
print('根据多个键进行合并df:\n', pd.merge(df1, df2, on=['key1', 'key2'], how='outer'))

s1 = pd.Series([0, 1], index=['a', 'b'])
s2 = pd.Series([2, 3, 4], index=['c', 'd', 'e'])
s3 = pd.Series([5, 6], index=['f', 'g'])
s4 = pd.concat([s1 * 5, s3])
print('连接序列:\n', pd.concat([s1, s2, s3]))
print('使用指定的索引连接序列:\n', pd.concat([s1, s4], axis=1, join_axes=[['a', 'c', 'b', 'e']]))

df1 = pd.DataFrame(np.random.randn(3, 4), columns=['a', 'b', 'c', 'd'])
df2 = pd.DataFrame(np.random.randn(2, 3), columns=['b', 'd', 'a'])
print('舍弃不必要的索引连接序列:\n', pd.concat([df1, df2], ignore_index=True))

s1 = pd.Series([np.nan, 2.5, np.nan, 3.5, 4.5, np.nan],
           index=['f', 'e', 'd', 'c', 'b', 'a'])
s2 = pd.Series(np.arange(len(s1), dtype=np.float64),
           index=['f', 'e', 'd', 'c', 'b', 'a'])
s2[-1] = np.nan
print('合并重叠数据并选择重复数据来源:\n', np.where(pd.isnull(s1), s2, s1))

data = pd.DataFrame({'food': ['bacon', 'pulled pork', 'bacon', 'Pastrami',
                           'corned beef', 'Bacon', 'pastrami', 'honey ham',
                           'nova lox'],
                  'ounces': [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})
meat_to_animal = {
  'bacon': 'pig',
  'pulled pork': 'pig',
  'pastrami': 'cow',
  'corned beef': 'cow',
  'honey ham': 'pig',
  'nova lox': 'salmon'
}
data['animal'] = data['food'].map(str.lower).map(meat_to_animal)
print('应用map方法:\n', data)

ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
bins = [18, 25, 35, 60, 100]
cats = pd.cut(ages, bins)
print('离散化:\n', cats)
group_names = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior']
cats = pd.cut(ages, bins, labels=group_names)
print('离散化  自定义面元名称:\n', cats)


data = np.random.randn(1000) # Normally distributed
cats = pd.qcut(data, 4) # Cut into quartiles
print('按分位数离散化:\n', cats)