# author='lwz'
# coding:utf-8
import pandas as pd
import h5py
import numpy as np
import os
import time
import pickle


'''
write hdf 速度测试 
使用矩阵的话读写速度接近pickle
'''

csv_dir = 'E:\\20170103\\'
hdf_fn = 'E:\\Cache\\20140103.hdf5'
pkl_fn = 'E:\\Cache\\20140103.pickle'


def main():
    if os.path.exists(hdf_fn):
        os.remove(hdf_fn)

    time_st = time.time()
    csv_list = os.listdir(csv_dir)
    data_dict = dict()
    for csv_fn in csv_list[:100]:
        code = csv_fn[:8]
        code = 'SH' + code if code[0] == '6' else 'SZ' + code
        df = pd.read_csv(csv_dir + csv_fn)
        data_dict[code] = df2arr(df)
    read_time = time.time() - time_st

    time_st = time.time()
    f = h5py.File(hdf_fn, 'w')
    for code in data_dict.keys():
        f[code] = data_dict[code]
    f.close()
    write_time = time.time() - time_st

    time_st = time.time()
    f = h5py.File(hdf_fn, 'r')
    for code in data_dict.keys():
        data = np.array(f[code])
    f.close()
    read_hdf_time = time.time() - time_st

    time_st = time.time()
    with open(pkl_fn, 'wb') as f:
        pickle.dump(data_dict, f)
    write_pkl_time = time.time() - time_st

    time_st = time.time()
    with open(pkl_fn, 'rb') as f:
        data_dict = pickle.load(f)
    read_pkl_time = time.time() - time_st

    print("readused{:.4f}s\n write used {:.4f}s\n read_hdf_time used{:.4f}s\n readpkl used{:.4f}s\n writepkl used {:.4f}s\n"
          .format(read_time, write_time, read_hdf_time, read_pkl_time, write_pkl_time))


def df2arr(df):
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
    return data


def str2time(x='09:02:01'):
    return int(x[:2]) * 3600 + int(x[3:5]) * 60 + int(x[6:])


if __name__ == '__main__':
    main()