# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import pandas as pd
import os, time

'''
测试 IO速度
'''

dir = 'E:\\data\\tick_pickle\\'

time_st = time.time()
list_pic = os.listdir(dir)
with open('log.txt', 'w') as f:
    for pic_ in list_pic[:100]:
        df = pd.read_pickle(dir + pic_)
        time_used = time.time() - time_st
        time_st = time.time()
        print('file{} used{:.4f}s'.format(pic_, time_used))
        f.write(str(round(time_used, 2))+ '\n')
        del df
