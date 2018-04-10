# author='lwz'
# coding:utf-8
import pandas as pd
import h5py
import numpy as np
import os
import time
'''
columns = dates,times,trade_pr,trade_vol,d_vol,trade_amt,
b1pr,b1vol,b2pr,b2vol,b3pr,b3vol,b4pr,b4vol,b5pr,b5vol,
s1pr,s1vol,s2pr,s2vol,s3pr,s3vol,s4pr,s4vol,s5pr,s5vol,bs

float32 times trade_pr  **pr
int32  **vol trade_amt bs

dt = np.dtype([("temp", np.float), ("pressure", np.float), ("wind",np.float)])
int4  -2147483648到2147483647


pandas.read_hdf(path_or_buf, key=None, **kwargs)
read from the store, close it if we opened it

Retrieve pandas object stored in file, optionally based on where criteria

Parameters:
path_or_buf : path (string), or buffer to read from
key : group identifier in the store. Can be omitted a HDF file contains
a single pandas object.
'''

csv_fn = '000007_20170103.txt'
hdf_fn = '20170103.hdf5'
code = csv_fn[:6]
if code[0] is '6':
    code = 'SH' + code
else:
    code = 'SZ' + code


def csv2hdf5_1(csv_fn, hdf_fn, code):

    df = pd.read_csv(csv_fn)

    dtype_list = list()
    for key in df.columns[1:]:
        if 'pr' in key:
            dtype_list.append((key, np.float))
        elif key == "times":
            dtype_list.append((key, np.dtype("S8")))
        else:
            dtype_list.append((key, np.int))

    dt = np.dtype(dtype_list)
    print(dt)
    n_col = len(dt) - 1
    n_row = len(df)

    time_st = time.time()
    f = h5py.File(hdf_fn, 'w')
    dset = f.create_dataset(name=code, shape=(n_row, ), dtype=dt)
    for col_name in df.columns[1:]:
        dset[col_name, :] = np.array(df[col_name])

    f.close()
    print("size:{}, write_used{:.4f}s".format(os.path.getsize(hdf_fn), time.time()-time_st))


def csv2hdf5_2(csv_fn, hdf_fn, code):

    df = pd.read_csv(csv_fn)

    dtype_list = list()
    for key in df.columns[1:]:
        if 'pr' in key:
            df[key] = df[key] * 100
            df[key] = df[key].apply(np.round)
            dtype_list.append((key, np.int))
        elif key == "times":
            dtype_list.append((key, np.dtype("S8")))
        else:
            dtype_list.append((key, np.int))

    dt = np.dtype(dtype_list)
    print(dt)
    n_row = len(df)

    time_st = time.time()
    f = h5py.File(hdf_fn, 'w')
    dset = f.create_dataset(name=code, shape=(n_row, ), dtype=dt)
    for col_name in df.columns[1:]:
        dset[col_name, :] = np.array(df[col_name])

    f.close()
    print("size:{}, write_used{:.4f}s".format(os.path.getsize(hdf_fn), time.time() - time_st))


def csv2hdf5_3(csv_fn, hdf_fn, code):

    df = pd.read_csv(csv_fn)

    datetime = int(time.mktime(time.strptime(df['dates'][0], "%Y-%m-%d")))
    columns = []
    for key in df.columns[1:]:
        if 'pr' in key:
            df[key] = df[key].apply(lambda x: np.int(np.round(x * 100)))
            columns.append(key)
        elif key == "times":
            df[key] = df[key].apply(lambda x: str2time(x) + datetime)
            columns.append(key)
        elif key == 'dates':
            pass
        else:
            columns.append(key)

    data = np.array(df.ix[:, columns].values, dtype=np.int64)
    n_row, n_col = data.shape

    time_st = time.time()
    f = h5py.File(hdf_fn, 'w')
    f.create_dataset(name=code, shape=(n_row, n_col), dtype=np.int64, data=data)
    f.close()
    print("size:{}, write_used{:.4f}s".format(os.path.getsize(hdf_fn), time.time() - time_st))


def str2time(x='09:02:01'):
    return int(x[:2]) * 3600 + int(x[3:5]) * 60 + int(x[6:])


def read_hdf(fn, code):
    time_st = time.time()
    f = h5py.File(fn, 'r')
    data = np.array(f[code])
    f.close()
    print("read_used{:.4f}s".format(time.time() - time_st))


if __name__ == "__main__":
    # df = pd.read_hdf(hdf_fn, key=code)
    csv2hdf5_1(csv_fn, hdf_fn, code)
    read_hdf(hdf_fn, code)
    csv2hdf5_2(csv_fn, hdf_fn, code)
    read_hdf(hdf_fn, code)
    csv2hdf5_3(csv_fn, hdf_fn, code)
    read_hdf(hdf_fn, code)






