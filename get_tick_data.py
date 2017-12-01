# author='lwz'
# coding:utf-8
import os
import pandas as pd
import matplotlib as plt
data_path = '\\\\SEVER-SYWGQHCD\\data2\\'
date_st = 20150408
date_ed = 20150707
code = 'SH600711'

data_path = data_path + 'tick_'+ code[:2].lower() + '\\'
dir_list = os.listdir(data_path)
dir_list = [d for d in dir_list if d.isdigit() and date_st <= int(d) <= date_ed]
df_list = []

for dir_ in dir_list:
    filename = data_path + dir_ + '\\' + code[2:] + '_' + dir_ + '.txt'
    df = pd.read_csv(filename)
    datestr = df.ix[df.index[0], 'dates'] + ' '
    df['datetimes'] = pd.to_datetime(df.times.apply(lambda x: datestr + x))
    df_list.append(df[['datetimes', 'trade_pr']])

df_ = pd.concat(df_list, ignore_index=True)
df_['stock_value'] = df_['trade_pr'] * 86.94 * 10000
df_['total_value'] = df_['stock_value'] + 214850
df_['debt'] = 685 * 10000
df_['percent'] = df_['total_value'] / df_['debt']
df_.to_csv('D:\\Cache\\stock.csv', index=False)
