# author='lwz'
# coding:utf-8
'''
单进程 依次读取 依次写入
strategy_1 used 21.6271s
read: 3.4298s  calculate: 15.4644s  write: 2.7260s
单进程 依次读取 集中写入
strategy_2 used 21.9728s
read: 3.4938s  calculate: 15.7605s  write: 2.6934s
单进程 依次读取 集中写入一个文件
strategy_3 used 19.3427s
read: 3.1310s  calculate: 14.2042s  write: 1.9824s
多进程 独立依次读取 独立依次写入
total: 8.3542s  read: 1.1992s  calculate: 6.3188s  write: 0.8362s
total: 8.4786s  read: 1.2815s  calculate: 6.3870s  write: 0.8091s
total: 8.5056s  read: 1.2704s  calculate: 6.4512s  write: 0.7820s
total: 8.5969s  read: 1.2524s  calculate: 6.5464s  write: 0.7971s
strategy_4 used 14.4318s
read: 0.0000s  calculate: 0.0000s  write: 0.0000s
多进程 单独一个进程负责读写 其余进程处理数据
total: 11.2409s    calculate: 6.0561s
total: 11.2530s    calculate: 5.7653s
total: 11.1347s    calculate: 5.3592s
strategy_5 used 13.2012s
read: 0.0000s  calculate: 0.0000s  write: 0.0000s
total: 11.1788s    calculate: 4.8168s
多进程 单独一个进程负责读写 通过单独的queue通讯 其余进程处理数据
strategy_6 used 9.5777s
read: 0.0000s  calculate: 0.0000s  write: 0.0000s
total: 8.1722s    calculate: 5.9753s
total: 8.1712s    calculate: 5.9351s
total: 8.1070s    calculate: 5.9131s
total: 8.1682s    calculate: 5.9542s
'''
import pickle as pkl
import pandas as pd
import os
import time
import shutil
import datetime as dt
from multiprocessing import Pool, Manager, Queue, Process
import warnings
import pickle


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


def get_stockname(fn='E:\\data\\tick_sh\\20170103\\600277_20170103.txt'):
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
    csv_path = "E:\\20170103\\"
    pkl_path = "E:\\pkl_data\\"
    def_list = [strategy_1, strategy_2, strategy_3, strategy_4, strategy_5, strategy_6]
    # def_list = [strategy_6]
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
    print("单进程 依次读取 依次写入")
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
    print("单进程 依次读取 集中写入")
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
    print("单进程 依次读取 集中写入一个文件")
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
    print("多进程 独立依次读取 独立依次写入")
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


def task_5(queue, csv_path, pkl_path, process_i):
    cal_time = 0
    st_time = time.time()
    while True:
        # print("process{} wait for data....".format(process_i))
        data = queue.get()
        if data == b'stop':
            # print("process{} end....".format(process_i))
            break
        else:
            df_ = pickle.loads(data)

        if "trade_vol" not in df_.columns:
            queue.put(pickle.dumps(pd.DataFrame()))
            continue

        t0 = time.time()
        df = csv_to_pickle(df_)
        t1 = time.time()
        cal_time += t1 - t0

        queue.put(pickle.dumps(df))
        # print("process{} send data over".format(process_i))

    total_time = time.time() - st_time
    print("total: {:.4f}s    calculate: {:.4f}s ".
          format(total_time,  cal_time))


def strategy_5(csv_path, pkl_path, num=30):
    print("多进程 单独一个进程负责读写 其余进程处理数据")
    process_n = 4
    files = os.listdir(csv_path)
    files = [file for file in files if file[-4:] == '.txt']
    df_list = []
    code_list = []
    jobs = list()
    cal_time = 0
    read_time = 0
    write_time = 0
    queues = [Queue() for _ in range(process_n)]

    for i in range(process_n):
        job = Process(target=task_5, args=(queues[i], csv_path, pkl_path, i))
        jobs.append(job)
        job.start()

    flag = 0
    N = min(len(files), num)

    while flag < N:
        for i in range(0, min(flag+process_n, N) - flag):
            file = files[flag + i]
            code = get_stockname(file)
            code_list.append(code)
            if code:
                df = pd.read_csv(csv_path + file)

                queues[i].put(pickle.dumps(df))
            else:
                queues[i].put(pickle.dumps(pd.DataFrame()))

        for i in range(0, min(flag+process_n, N) - flag):
            code = code_list[flag + i]
            df_ = pickle.loads(queues[i].get())
            if len(df_) == 0:
                pass
                # print(code)
            else:
                df_.to_pickle(pkl_path + code + ".pkl")

        flag += process_n

    for i in range(process_n):
        queues[i].put(b'stop')

    return read_time, cal_time, write_time


def task_6(queue_put, queue_get, csv_path, pkl_path, process_i):
    cal_time = 0
    st_time = time.time()
    while True:
        # print("process{} wait for data....".format(process_i))
        data = queue_put.get()
        if data == b'stop':
            # print("process{} end....".format(process_i))
            break
        else:
            df_ = pickle.loads(data)

        if "trade_vol" not in df_.columns:
            queue_get.put(pickle.dumps(pd.DataFrame()))
            continue

        t0 = time.time()
        df = csv_to_pickle(df_)
        t1 = time.time()
        cal_time += t1 - t0

        queue_get.put(pickle.dumps(df))
        # print("process{} send data over".format(process_i))

    total_time = time.time() - st_time
    print("total: {:.4f}s    calculate: {:.4f}s ".
          format(total_time,  cal_time))


def strategy_6(csv_path, pkl_path, num=30):
    print("多进程 单独一个进程负责读写 通过公用的queue通讯 其余进程处理数据")
    process_n = 4
    files = os.listdir(csv_path)
    files = [file for file in files if file[-4:] == '.txt']
    df_list = []
    code_list = []
    jobs = list()
    cal_time = 0
    read_time = 0
    write_time = 0
    queue_put = Queue(process_n)
    queue_get = Queue()
    put_flag = 0
    get_flag = 0

    for i in range(process_n):
        job = Process(target=task_6, args=(queue_put, queue_get, csv_path, pkl_path, i))
        jobs.append(job)
        job.start()

    flag = 0
    N = min(len(files), num)

    while flag < N or put_flag > get_flag:
        if flag < N:
            file = files[flag]
            flag += 1
            code = get_stockname(file)
            code_list.append(code)
            if code:
                df = pd.read_csv(csv_path + file)
                queue_put.put(pickle.dumps(df))
                put_flag += 1

        if flag < N and put_flag - get_flag < process_n:
            pass
        else:
            df_ = pickle.loads(queue_get.get())
            get_flag += 1
            if len(df_) == 0:
                pass
            else:
                df_.to_pickle(pkl_path + code + ".pkl")

    for i in range(process_n):
        queue_put.put(b'stop')

    return read_time, cal_time, write_time


if __name__ == "__main__":
    main()

