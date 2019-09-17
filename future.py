# author='lwz'
# coding:utf-8

import time
import datetime
import numpy as np
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
    df["Cover_price"] = -df["Cover_price"]
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


def plot(df_1, df_2, df_record, year, month, sub_plot_id):
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
    df_1 = df_1[(df_1["trade_date"] >= start_date) & (df_1["trade_date"] <= end_date)]
    df_2 = df_2[(df_2["trade_date"] >= start_date) & (df_2["trade_date"] <= end_date)]
    diff = df_1["CLOSE"] - df_2["CLOSE"]
    trade_record = get_record(df_record, month, start_date, end_date)
    plt.subplot(*sub_plot_id)
    plt.plot(df_1["trade_date"], diff)
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


def main():
    data_dir = "C:\\data\\futures_day_data"
    record_file = "each_trade_simple.csv"
    df_record = load_trade_record(data_dir, record_file)
    for month in [1, 5, 10]:
        df_1 = load_data(data_dir, "HC{:02d}M.SHF.csv".format(month))
        df_2 = load_data(data_dir, "RB{:02d}M.SHF.csv".format(month))
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.4)
        sub_figure_id = 0
        for year in range(2014, 2020):
            sub_figure_id += 1
            plot(df_1, df_2, df_record, year, month, (2, 3, sub_figure_id))
        plt.show()


if __name__ == "__main__":
    main()
