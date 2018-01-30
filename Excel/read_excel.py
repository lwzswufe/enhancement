# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import time
import pandas as pd


st_time = time.time()
fn1 = r'C:\Users\lwzswufe\Documents\B.xlsx'
fn2 = r'C:\Users\lwzswufe\Documents\B.txt'

B = pd.read_excel(fn1)
b = pd.read_csv(fn2)

b = set(b['PhoneNumber'])
B = set(B['PhoneNumber'])

A = B - b

with open('D:\\useful.csv', 'w') as f:
    for a in A:
        f.write(str(a) + '\n')

print('used {:.4f}s'.format(time.time() - st_time))
