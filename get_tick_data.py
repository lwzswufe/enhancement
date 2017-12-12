# author='lwz'
# coding:utf-8
import os
import pandas as pd
import matplotlib as plt
import numpy as np


trade_record_path = 'D:\\Cache\\yc.csv'
data_path = '\\\\SEVER-SYWGQHCD\\data2\\'
date_st = 20150625
date_ed = 20150707
code = 'SH600711'

df_record = pd.read_csv(trade_record_path, encoding='gbk', dtype={'code': str, 'date': str})
df_record.amt = df_record.vol * df_record.price
datetimes = list()
for i in range(len(df_record)):
    datetimes.append(df_record.date[i] + 'T' + str(df_record.time[i] / 100))

df_record['datetime'] = pd.to_datetime(datetimes)

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
df_.ix[0, 'position'] = 86.94 * 10000
asset_init = 0.0
df_['debt'] = np.zeros(len(df_))
df_.ix[0, 'debt'] = 685 * 10000
df_['fee'] = np.zeros(len(df_))

flag = 0
iter = 0

while flag < len(df_record) and iter < len(df_):
    if df_record.datetime[flag] > df_.datetimes[iter]:
        iter += 1
    else:
        df_.ix[iter, 'position'] -= df_record.vol[flag]
        df_.ix[iter, 'debt'] -= df_record.amt[flag]
        df_.ix[iter, 'fee'] += df_record.amt[flag] * 0.0013
        print(df_.datetimes[iter], 'price:', df_.trade_pr[iter])
        print(df_record.date[flag], df_record.time[flag], 'price:', df_record.price[flag])
        flag += 1
        iter += 1

df_['fee'] = df_['fee'].cumsum()
df_['position'] = df_['position'].cumsum()
df_['asset'] = df_['position'] * df_['trade_pr'] - df_['fee'] + asset_init
df_['debt'] = df_['debt'].cumsum() + df_['fee']
df_['percent'] = df_['asset'] / df_['debt']
df_.to_csv('D:\\Cache\\stock.csv', index=False)
df2 = df_[(df_.dates != df_.dates.shift(-1)) | (df_.dates != df_.dates.shift(1))]
print(df2)
df2.to_csv('D:\\Cache\\stock2.csv', index=False)
