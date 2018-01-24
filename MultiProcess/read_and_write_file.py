# author='lwz'
# coding:utf-8
import pickle as pkl
import pandas as pd
import os
import time
import shutil
import datetime as dt
from multiprocessing import Pool
import warnings


warnings.filterwarnings("ignore")


def csv_to_pickle(df):
    df = df[(df.trade_vol > 0) | (df.index == 0)]
    df['d_amt'] = df['trade_amt'].cumsum()
    df = df.ix[:, ['dates', 'times', 'd_vol', 'd_amt', 'trade_pr']]

    datestr = df.ix[df.index[0], 'dates'] + ' '
    df['datetimes'] = pd.to_datetime(df.times.apply(lambda x: datestr + x))
    df.set_index('datetimes', inplace=True, drop=False)
    df.drop_duplicates(subset='datetimes', keep='last', inplace=True)
    df = df.resample('3S', limit=None).ffill()
    df.datetimes = df.index
    df.times = df.datetimes.apply(lambda x: int(str(x.time()).replace(':', '')))
    df.dates = pd.to_datetime(df.dates)
    df = df[df.times >= 93000]
    df = df[(df.times < 113004) | (df.times >= 130000)]
    df.index = range(len(df))

    return df


def get_stockname(fn='D:\\data\\tick_sh\\20170103\\600277_20170103.txt'):
    if fn[0] is '6':
        exchange = 'SH'
    elif fn[0] is '0' or fn[0] is '3':
        exchange = 'SZ'
    else:
        print(fn)
        return False

    code = fn[-19:-13]
    if code.isdigit():
        if exchange == 'SH' and code[0] == '6':
            return exchange + code
        elif exchange == 'SZ' and (code[:2] == '30' or code[0] == '0'):
            return exchange + code

    return False


def main():
    csv_path = "D:\\20170103\\"
    pkl_path = "D:\\pkl_data\\"
    def_list = [strategy_1, strategy_2, strategy_3, strategy_4]
    num = 300
    for func in def_list:
        pkl_path_ = pkl_path + func.__name__ + "\\"
        if os.path.exists(pkl_path_):
            shutil.rmtree(pkl_path_)
            # os.removedirs(pkl_path_)

        os.mkdir(pkl_path_)

        start_time = time.time()
        read_time, cal_time, write_time = func(csv_path, pkl_path_, num)
        print("{} used {:.4f}s".format(func.__name__, time.time() - start_time))
        print("read: {:.4f}s  calculate: {:.4f}s  write: {:.4f}s".format(read_time, cal_time, write_time))


def strategy_1(csv_path, pkl_path, num=30):
    files = os.listdir(csv_path)
    files = [file for file in files if file[-4:] == '.txt']
    cal_time = 0
    read_time = 0
    write_time = 0
    for file in files[:num]:
        code = get_stockname(file)
        if code:
            t0 = time.time()
            df_ = pd.read_csv(csv_path + file)
            t1 = time.time()
            df = csv_to_pickle(df_)
            t2 = time.time()
            df.to_pickle(pkl_path + get_stockname(file) + ".pkl")
            t3 = time.time()

            read_time += t1 - t0
            cal_time += t2 - t1
            write_time += t3 - t2

    return read_time, cal_time, write_time


def strategy_2(csv_path, pkl_path, num=30):
    files = os.listdir(csv_path)
    files = [file for file in files if file[-4:] == '.txt']
    df_list = []
    code_list = []
    cal_time = 0
    read_time = 0
    write_time = 0

    for file in files[:num]:
        code = get_stockname(file)
        if code:
            t0 = time.time()
            df = pd.read_csv(csv_path + file)
            t1 = time.time()
            df_list.append(csv_to_pickle(df))
            t2 = time.time()
            code_list.append(code)
            read_time += t1 - t0
            cal_time += t2 - t1

    st_time = time.time()
    for i, df in enumerate(df_list):
        df.to_pickle(pkl_path + code_list[i] + ".pkl")
    write_time = time.time() - st_time

    return read_time, cal_time, write_time


def strategy_3(csv_path, pkl_path, num=30):
    files = os.listdir(csv_path)
    files = [file for file in files if file[-4:] == '.txt']
    df_list = []
    code_list = []
    cal_time = 0
    read_time = 0
    write_time = 0

    for file in files[:num]:
        code = get_stockname(file)
        if code:
            t0 = time.time()
            df = pd.read_csv(csv_path + file)
            t1 = time.time()
            df_list.append(csv_to_pickle(df))
            t2 = time.time()
            code_list.append(code)
            read_time += t1 - t0
            cal_time += t2 - t1

    st_time = time.time()
    with open(pkl_path + "data_dict.pkl", 'wb') as f:
        pkl.dump(dict(zip(code_list, df_list)), f)
    write_time = time.time() - st_time

    return read_time, cal_time, write_time


def task_4(files, csv_path, pkl_path):
    cal_time = 0
    read_time = 0
    write_time = 0
    st_time = time.time()
    for file in files:
        code = get_stockname(file)
        if code:
            t0 = time.time()
            df_ = pd.read_csv(csv_path + file)
            t1 = time.time()
            df = csv_to_pickle(df_)
            t2 = time.time()
            df.to_pickle(pkl_path + code + ".pkl")
            t3 = time.time()
            read_time += t1 - t0
            cal_time += t2 - t1
            write_time += t3 - t2

    total_time = time.time() - st_time
    print("total: {:.4f}s  read: {:.4f}s  calculate: {:.4f}s  write: {:.4f}s".
          format(total_time, read_time, cal_time, write_time))


def strategy_4(csv_path, pkl_path, num=30):
    files = os.listdir(csv_path)
    files = [file for file in files if file[-4:] == '.txt']
    df_list = []
    code_list = []
    cal_time = 0
    read_time = 0
    write_time = 0
    pool = Pool(4)

    for i in range(4):
        pool.apply_async(task_4, args=(files[i:num:4], csv_path, pkl_path))

    pool.close()
    pool.join()

    return read_time, cal_time, write_time


def task_5(files, csv_path, pkl_path):
    cal_time = 0
    read_time = 0
    write_time = 0
    st_time = time.time()
    for file in files:
        code = get_stockname(file)
        if code:
            t0 = time.time()
            df_ = pd.read_csv(csv_path + file)
            t1 = time.time()
            df = csv_to_pickle(df_)
            t2 = time.time()
            df.to_pickle(pkl_path + code + ".pkl")
            t3 = time.time()
            read_time += t1 - t0
            cal_time += t2 - t1
            write_time += t3 - t2

    total_time = time.time() - st_time
    print("total: {:.4f}s  read: {:.4f}s  calculate: {:.4f}s  write: {:.4f}s".
          format(total_time, read_time, cal_time, write_time))


def strategy_5(csv_path, pkl_path, num=30):
    files = os.listdir(csv_path)
    files = [file for file in files if file[-4:] == '.txt']
    df_list = []
    code_list = []
    cal_time = 0
    read_time = 0
    write_time = 0
    pool = Pool()

    for i in range(4):
        pool.apply_async(task_4, args=(files[i:num:4], csv_path, pkl_path))

    pool.close()
    pool.join()

    return read_time, cal_time, write_time


if __name__ == "__main__":
    main()

