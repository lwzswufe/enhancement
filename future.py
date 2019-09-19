# author='lwz'
# coding:utf-8

import time
import datetime
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
import pandas as pd


def MatlabTime_to_str(matlabTime=736698):
    '''
    MATLAB时间转化为字符串
    :param matlabTime:
    :return:
    '''
    if not matlabTime > 0:
        return ''
    pythonTime = ((matlabTime - 719529) * 24 - 8) * 3600
    try:
        timestr = time.strftime('%Y-%m-%d', time.strptime(time.ctime(pythonTime)))
    except:
        print(pythonTime)
    return timestr


def load_data(dirname, filename):
    '''
    读取数据
    :param dirname:  数据文件夹路径
    :param filename: 文件名
    :return:
    '''
    fn = "{}\\{}".format(dirname, filename)
    df = pd.read_csv(fn)
    time_series = df["trade_date"].apply(MatlabTime_to_str)
    df["trade_date"] = pd.to_datetime(time_series)
    return df.loc[:, ["trade_date", "CLOSE", "VOLUME"]]


def load_trade_record(dirname, filename):
    fn = "{}\\{}".format(dirname, filename)
    df = pd.read_csv(fn)
    df["Trade_date_open"] = pd.to_datetime(df["Trade_date_open"])
    df["Trade_date_cover"] = pd.to_datetime(df["Trade_date_cover"])
    df["Cover_price"] = df["Cover_price"]
    return df


def get_record(df, month, start_date, end_date):
    trade_record = []
    df = df[(df["Month"] == month) &
            (df["Trade_date_open"] >= start_date) &
            (df["Trade_date_cover"] <= end_date)]
    if len(df) == 0:
        return trade_record
    for i in df.index:
        direction = df.loc[i, "Direction"]
        trade_record.append((df.loc[i, "Trade_date_open"], df.loc[i, "Open_price"], direction))
        trade_record.append((df.loc[i, "Trade_date_cover"], df.loc[i, "Cover_price"], -direction))
    return trade_record


def get_datetime(year, month, day, month_bias):
    '''
    根据期货持有月份 month_bias 计算交易开始日期 结束日期
    :param year: 年份 int yyyy
    :param month: 期货合约月份 int mm
    :param day: 日期 int dd
    :param month_bias: 自期货合约开始的第X个月
    :return:
    '''
    year_ = year + (month + month_bias - 1) // 12
    month_ = (month + month_bias - 1) % 12 + 1
    date = datetime.datetime(year=year_, month=month_, day=day)
    return date


class TradeRecord(object):
    def __init__(self, year, month, direction, open_date, open_price):
        self.year = year
        self.month = month
        self.direction = direction
        self.open_date = open_date
        self.open_price = open_price
        self.cover_date = None
        self.cover_price = 0.0
        self.income = 0.0
        self.is_cover = False

    def cover(self, cover_date, cover_price):
        self.cover_date = cover_date
        self.cover_price = cover_price
        self.is_cover = True
        self.income = (self.cover_price - self.open_price) * self.direction - 3

    def __str__(self):
        s = "{:d},{:d},{:d},{},{},{:.2f},{:.2f}".format(
            self.month, self.year, self.direction,
            self.open_date, self.cover_date, self.open_price, self.cover_price)
        return s


def get_param_list():
    '''
    生成参数列表
    :return:
    '''
    sigma_step = 0.2

    watch_sigma_list = []
    watch_sigma = 1.0
    while watch_sigma <= 2.0:
        watch_sigma_list.append(watch_sigma)
        watch_sigma += sigma_step
    # watch_sigma_list = [1.50]

    open_sigma_list = []
    open_sigma = 0.2
    while open_sigma <= 1.0:
        open_sigma_list.append(open_sigma)
        open_sigma += sigma_step
    # open_sigma_list = [0.10]

    cover_sigma_list = []
    cover_sigma = -1.0
    while cover_sigma <= 1.4:
        cover_sigma_list.append(cover_sigma)
        cover_sigma += sigma_step
   # cover_sigma_list = [0.30]

    stop_sigma_list = []
    stop_sigma = 0.4
    while stop_sigma <= 1.4:
        stop_sigma_list.append(stop_sigma)
        stop_sigma += sigma_step

    param_list = []
    for watch_sigma in watch_sigma_list:
        for open_sigma in open_sigma_list:
            for cover_sigma in cover_sigma_list:
                for stop_sigma in stop_sigma_list:
                    param_list.append((watch_sigma, open_sigma, cover_sigma, stop_sigma))
    return param_list


def extract_data(df_1, df_2, month, window):
    '''
    提取数据并计算 均值 标准差
    :param df_1:
    :param df_2:
    :param month:
    :param window: 计算均值标准差的滑动窗口大小
    :return:
    '''
    ser_month = df_1["trade_date"].apply(lambda x: x.month)
    next_month = (month + 1 - 1) % 12 + 1   # (m - 1) % 12 + 1 月份取整 m in [1, 12]
    # df_1 = df_1[(ser_month != month) & (ser_month != next_month)]
    # df_2 = df_2[(ser_month != month) & (ser_month != next_month)]
    ser_diff = df_1["CLOSE"] - df_2["CLOSE"]
    df_new = pd.DataFrame({"date": df_1["trade_date"],
                           "diff": ser_diff,
                           "contract_1": df_1["CLOSE"],
                           "contract_2": df_2["CLOSE"]})
    df_new["std"] = df_new["diff"].rolling(window).std()
    df_new["mean"] = df_new["diff"].rolling(window).mean()
    return df_new


def record_stat(trade_record_list):
    tradenum = 0
    income = 0.0
    for trade_record in trade_record_list:
        tradenum += 1
        income += trade_record.income
    return income, tradenum


def mock_trading(params, window):
    data_dir = "C:\\data\\futures_day_data"
    watch_sigma, open_sigma, cover_sigma, stop_sigma = params
    total_record_list = []
    for month in [1, 5, 10]:
        df_1 = load_data(data_dir, "HC{:02d}M.SHF.csv".format(month))
        df_2 = load_data(data_dir, "RB{:02d}M.SHF.csv".format(month))
        df_new = extract_data(df_1, df_2, month, window)
        for year in range(2015, 2020):
            start_date = get_datetime(year, month, 1, 1)
            end_date = get_datetime(year, month, 28, 11)
            df_ = df_new[(df_new["date"] >= start_date) & (df_new["date"] <= end_date)]
            sigmas = (watch_sigma, open_sigma, cover_sigma, stop_sigma)
            trade_record_list = mock_trading_single_contract(df_, year, month, sigmas)
            total_record_list += trade_record_list
    record_file = "{}\\each_trade_simple.csv".format(data_dir)
    with open(record_file, "w") as f:
        f.write("Month,Year,Direction,Trade_date_open,Trade_date_cover,Open_price,Cover_price\n")
        for trade_record in total_record_list:
            f.write(trade_record.__str__())
            f.write("\n")
    print("{} write over".format(record_file))


def searsh_best_param(window):
    data_dir = "C:\\data\\futures_day_data"
    param_list = get_param_list()
    param_num = len(param_list)
    total_income = np.zeros(param_num)
    total_tradenum = np.zeros(param_num)
    for month in [1, 5, 10]:
        df_1 = load_data(data_dir, "HC{:02d}M.SHF.csv".format(month))
        df_2 = load_data(data_dir, "RB{:02d}M.SHF.csv".format(month))
        df_new = extract_data(df_1, df_2, month, window)

        for year in range(2015, 2020):
            start_date = get_datetime(year, month, 1, 1)
            end_date = get_datetime(year, month, 28, 11)
            df_thisyear = df_new[(df_new["date"] >= start_date) & (df_new["date"] <= end_date)]

            for param_id, (watch_sigma, open_sigma, cover_sigma, stop_sigma) in enumerate(param_list):
                sigmas = (watch_sigma, open_sigma, cover_sigma, stop_sigma)
                trade_record_list = mock_trading_single_contract(df_thisyear, year, month, sigmas)
                income, trade_num = record_stat(trade_record_list)
                del trade_record_list
                total_income[param_id] += income
                total_tradenum[param_id] += trade_num
                if (param_id + 1) % 100 == 0:
                    print("month:{:02d} year:{} {}/{}".format(month, year, param_id, param_num))
    best_id = np.argmax(total_income)
    print("best watch_sigma:{:.2f}, open_sigma:{:.2f}, cover_sigma:{:.2f} stop_sigma:{:.2f}".format(*(param_list[best_id])))
    print("best income:{:.2f} trade_num:{}".format(total_income[best_id], total_tradenum[best_id]))
    return param_list, total_income, total_tradenum


def mock_trading_single_contract(df, year, month, sigmas):
    watch_sigma, open_sigma, cover_sigma, stop_sigma = sigmas
    position = 0
    trade_record = []
    if len(df) == 0:
        return trade_record

    stop_line = 0
    open_times = 0
    last_open_price = 0
    highest = watch_sigma
    lowest = -watch_sigma
    record = None

    for i in df.index:
        diff = df.loc[i, "diff"]
        mean = df.loc[i, "mean"]
        sigma = df.loc[i, "std"]
        if position != 0:       # 有持仓
            if position > 0:    # 多仓
                if diff > mean - cover_sigma * sigma or diff < stop_line:
                    position = 0
                    record.cover(df.loc[i, "date"], diff)
                    trade_record.append(record)
                    last_open_price = record.open_price
            else:               # 空仓
                if diff < mean + cover_sigma * sigma or diff > stop_line:
                    position = 0
                    record.cover(df.loc[i, "date"], diff)
                    trade_record.append(record)
                    last_open_price = record.open_price
        else:                   # 无持仓
            if mean - watch_sigma * sigma <= diff <= mean + watch_sigma * sigma:
                highest = mean + watch_sigma * sigma
                lowest = mean + watch_sigma * sigma
                open_times = 0
                last_open_price = mean
            else:               # 观察线上方 准备开仓
                if diff < mean:
                    open_line = lowest + open_sigma * sigma
                    if diff > open_line and diff < last_open_price - open_times * 20:
                        position = 1
                        record = TradeRecord(year, month, 1, df.loc[i, "date"], diff)
                        stop_line = diff - stop_sigma * sigma
                        open_times += 1
                    lowest = min(lowest, diff)
                else:
                    open_line = highest - open_sigma * sigma
                    if diff < open_line and diff > last_open_price + open_times * 20:
                        position = -1
                        record = TradeRecord(year, month, -1, df.loc[i, "date"], diff)
                        stop_line = diff + stop_sigma * sigma
                        open_times += 1
                    highest = max(highest, diff)
    # 交割月前平仓
    i = df.index[-1]
    if position != 0:
        record.cover(df.loc[i, "date"], df.loc[i, "diff"])
    return trade_record


def plot(df_new, df_record, year, month, sub_plot_id, sigmas):
    '''
    :param df_1: DaaFrame 数据1
    :param df_2: DaaFrame 数据2
    :param year: 年份 int yyyy
    :param month: 期货合约月份 int mm
    :param sub_plot_id: 子图编号(int, int, int)
    :return:
    '''
    start_date = get_datetime(year, month, 1, 1)
    end_date = get_datetime(year, month, 28, 11)
    df_thisyear = df_new[(df_new["date"] >= start_date) & (df_new["date"] <= end_date)]
    trade_record = get_record(df_record, month, start_date, end_date)
    plt.subplot(*sub_plot_id)
    plt.plot(df_thisyear["date"], df_thisyear["diff"])
    for sigma in sigmas:
        ser = df_thisyear["mean"] + sigma * df_thisyear["std"]
        plt.plot(df_thisyear["date"], ser)
    plt.grid()
    plt.xlim([start_date, end_date])
    plt.title("{}".format(year))
    ax = plt.gca()
    # 绘制交易记录
    for trade_date, price, direction in trade_record:
        delta_y = direction * 50
        delta_x = 0
        if direction > 0:
            color = 'r'
        else:
            color = 'g'
        ax.arrow(trade_date, price+delta_y, delta_x, -delta_y,
                 length_includes_head=True,  # 增加的长度包含箭头部分
                 head_width=2, head_length=10, fc=color, ec=color)
    # 设置X轴
    monthdays = MonthLocator()
    ax.xaxis.set_major_locator(monthdays)

    mondayFormatter = DateFormatter('%m-%d')  # 如：2-29-2015
    ax.xaxis.set_major_formatter(mondayFormatter)

    for label in ax.get_xticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment('right')


def main(sigma, window):
    data_dir = "C:\\data\\futures_day_data"
    record_file = "each_trade_simple.csv"
    df_record = load_trade_record(data_dir, record_file)
    sigmas = [-sigma, sigma]
    for month in [1, 5, 10]:
        df_1 = load_data(data_dir, "HC{:02d}M.SHF.csv".format(month))
        df_2 = load_data(data_dir, "RB{:02d}M.SHF.csv".format(month))
        df_new = extract_data(df_1, df_2, month, window)
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.4)
        sub_figure_id = 0
        for year in range(2014, 2020):
            sub_figure_id += 1
            plot(df_new, df_record, year, month, (2, 3, sub_figure_id), sigmas)
        plt.show()


if __name__ == "__main__":
    window = 40
    # searsh_best_param(window)
    mock_trading((1.60, 0.80, 0.60, 1.40), window)
    main(1.60, window)
    #

