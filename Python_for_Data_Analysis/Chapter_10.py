# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta

df = pd.read_csv('ticks.txt')
df.time = pd.to_datetime(df.time)

df.time[1] + timedelta(0, 3)
print('使用pd.todatetime()转换为时间戳:\n',df.time[1])
print('加上一个特定时间戳timedelta(0, 3):\n',df.time[1] + timedelta(0, 3))
print('时间戳相减:\n',df.time[1] - df.time[0])

stamp = datetime(2017, 1, 3)
print('时间戳转字符串:\n',str(stamp))
print('时间戳转特定格式字符串:\n',stamp.strftime('%Y-%m-%d'))
print('时间戳转特定格式字符串:\n',stamp.strftime('%y-%m-%d'))
print('时间戳转特定格式字符串:\n',stamp.strftime('%F'))
print('%F 是 %Y-%m-%d即 yyyy-mm-dd的简写形式')

value = '2011-01-03'
print('特定格式字符串转时间戳:\n',datetime.strptime(value, '%Y-%m-%d'))

longer_ts = pd.Series(np.random.randn(1000),
                   index=pd.date_range('1/1/2000', periods=1000))
print('按年选取数据切片:\n', longer_ts["2001"])
print('按月选取数据切片:\n', longer_ts["2001-05"])
print('按日选取数据切片:\n', longer_ts[datetime(2001, 1, 7):])
print('按日选取数据切片:\n', longer_ts[longer_ts.index > datetime(2001, 1, 7)])

print('使用truncate')
print('按日选取数据切片:\n', longer_ts.truncate(after='2002/01/09'))
print('按日选取数据切片:\n', longer_ts.truncate(before='2002/01/09'))
print('按日选取数据切片:\n', longer_ts.truncate(after='2002/01/13', before='2002/01/09'))

print('生成日期范围:\n',  pd.date_range('2012/1/4', '2012/1/6', normalize=True))
print('生成日期范围:\n',  pd.date_range('2012/1/4', '2012/4/6', freq='BM'))
print('生成日期范围:\n',  pd.date_range('2012/3/4', '2012/4/6', freq='W-FRI'))

ts = pd.Series(np.random.randn(4),index=pd.date_range('1/1/2000', periods=4, freq='M'))
print('时间位移:', ts.shift(2))
print('时间位移:', ts.shift(-2))
print('时间位移:', ts.shift(1, freq='3D'))

s = pd.Series(df.trade_vol.values, index=df.time)
s2 = pd.Series(df.trade_pr.values, index=df.time)
ticks = pd.DataFrame({'open':df.trade_pr.values, 'high': df.s1pr.values, 'low':df.b1pr.values, 'close':df.trade_pr.values}, index=df.time)
ms = s.resample('5min', how=sum)
print('降采样:', ms[:5])
mt = s2.resample('1min', how='ohlc', fill_method="ffill")
print('open high low close降采样:', mt[:10])

s15t = mt.resample('15s', fill_method='ffill')
print('升采样:', s15t[:10])

mean_s = pd.rolling_mean(s, 5, min_periods=1)
print('求移动均值:', mean_s[:10])
ema_s = pd.ewma(s, 60)
print('求指数移动均值:', mean_s[:10])