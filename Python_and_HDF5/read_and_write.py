# author='lwz'
# coding:utf-8
import numpy as np
import h5py
import time
import pandas as pd
import random
import pickle
import numpy
'''
hdf, pickle, csv与pandas.DataFrame() 读写速度测试
'''

dir_ = 'E:\\Cache\\'
fn = dir_ + '20140102.hdf'


f = h5py.File(fn)
code_list = []


for name in f:
    code_list.append(name)
f.close()

if False:
    time_1 = time.time()
    t1 = 0
    t2 = 0
    df_dict = dict()
    for code in code_list:
        df = pd.read_hdf(fn, key=code)
        time_2 = time.time()
        t1 += time_2 - time_1
        df.to_csv('{}tick\\{}.csv'.format(dir_, code), index=False)
        time_1 = time.time()
        t2 += time_1 - time_2
        df_dict[code] = df

    with open(dir_ + '20140102.pkl', 'wb') as f:
        pickle.dump(df_dict, f)

    del df_dict
    print('read hdf used{:.4f}s  write csv used{:.4f}'.format(t1, t2))

read_n = 20
if True:
    st_time = time.time()
    for code in code_list:
        df = pd.read_hdf(fn, key=code)
        for i in range(read_n):
            a = random.randint(0, len(df)-1)
            c = df.ix[a, 'trade_pr']
    t1 = time.time() - st_time

    st_time = time.time()
    for code in code_list:
        fn = '{}tick\\{}.csv'.format(dir_, code)
        df = pd.read_csv(fn)
        for i in range(read_n):
            a = random.randint(0, len(df)-1)
            c = df.ix[a, 'trade_pr']
    t2 = time.time() - st_time

    st_time = time.time()
    for code in code_list:
        fn = '{}tick\\{}.csv'.format(dir_, code)
        with open(fn, 'r') as f:
            lines = f.readlines()
        for i in range(read_n):
            a = random.randint(1, len(lines) - 1)
            c = lines[a]
    t3 = time.time() - st_time

    st_time = time.time()
    fn = dir_ + '20140102.pkl'
    with open(fn, 'rb') as f:
        df_dict = pickle.load(f)

    for code in code_list:
        df = df_dict[code]
        for i in range(read_n):
            a = random.randint(0, len(df)-1)
            c = df.ix[a, 'trade_pr']
    del df_dict
    t4 = time.time() - st_time

    st_time = time.time()
    fn = dir_ + '20140102.hdf'
    f = h5py.File(fn)
    for code in code_list:
        for i in range(read_n):
            array_ = np.array(f[code][:, 'trade_pr'])
            a = random.randint(0, len(array_)-1)
            c = array_[a]
    f.close()
    t5 = time.time() - st_time

    print('read pd_hdf used{:.4f}s\nread pd_csv   used{:.4f}s\n'
          'read line   used{:.4f}s\nread pkl_df   used{:.4f}s\n'
          'read hdf_h5py used{:.4f}s\n'.
          format(t1, t2, t3, t4, t5))