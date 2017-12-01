# author='lwz'
# coding:utf-8
import os
import pandas as pd
import matplotlib as plt
import numpy as np


trade_record_path = 'D:\\Cache\\yc.csv'
data_path = '\\\\SEVER-SYWGQHCD\\data2\\'
date_st = 20150624
date_ed = 20150707
code = 'SH600711'

df_record = pd.read_csv(trade_record_path, encoding='utf-8', dtype={'code': str})
df_record.time /= 100
df_record.amt = df_record.vol * df_record.price

data_path = data_path + 'tick_' + code[:2].lower() + '\\'
dir_list = os.listdir(data_path)
dir_list = [d for d in dir_list if d.isdigit() and date_st <= int(d) <= date_ed]
df_list = []

for dir_ in dir_list:
    filename = data_path + dir_ + '\\' + code[2:] + '_' + dir_ + '.txt'
    df = pd.read_csv(filename)
    datestr = df.ix[df.index[0], 'dates'] + ' '
    df['datetimes'] = pd.to_datetime(df.times.apply(lambda x: datestr + x))
    df_list.append(df[['datetimes', 'trade_pr', 'dates', 'times']])

del df

df_ = pd.concat(df_list, ignore_index=True)
df_['position'] = np.zeros(len(df_))
df_['position'][0] = 86.94 * 10000 + 7000
asset_init = 21.48 * 10000
df_['debt'] = 685 * 10000

flag = 0
iter = 0

while flag < len(df_record):
    while df_record.date[flag] < df_.dates[iter] or df_record.time[flag] < df_.times[iter]:
        iter += 1

    df_.ix['position', iter] -= df_record.vol[flag]
    df_.ix['debt', iter] -= df_record.amt[flag]
    flag += 1
    print(df_.datetimes[iter], 'price:', df_.trade_pr[iter])
    print(df_record.date[flag], df_record.time[flag], 'price:', df_record.price[flag])


df_['asset'] = df_['position'] * df_['trade_pr'] + asset_init
df_['debt'] = df_['debt'].cumsum()
df_['percent'] = df_['asset'] / df_['debt']
df_.to_csv('D:\\Cache\\stock.csv', index=False)
