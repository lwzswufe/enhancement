# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import pandas as pd
import pickle
import sys
import shutil
import os
sys.path.append(r'D:\Code\Code\PythonCode')
import stockdownloads.trade_signal as trade_signal
import itchat


class trade_list(trade_signal.trade_list):
    pass


def file_address():
    PC = 'D:\\Share\\Trade\\'
    return PC


def reply_signal(msg=dict, wechat_class=None):
    try:
        context = msg['Text']
        texts = reply(context, wechat_class)
        if len(texts) > 0:
            return texts
    except TypeError:
        print(msg)


def reply_group(msg=dict, wechat_class=None):
    try:
        context = msg['Text']
        # fromUserName = msg['FromUserName']
    except TypeError:
        print(msg)
    if context[0] == '#':
        texts = reply(context[1:], wechat_class)
        if len(texts) > 0:
            return texts


def reply(context=str, wechat_class=None):
    if context == 'help' or context == '帮助':
        texts = '请输入信息与我开始互动(若在群聊中清以#开头)\n查询股票持仓：\n' +\
                '超短线 sxxxxxx \n小时线 hxxxxxx \n日线 dxxxxxx\n' +\
                '查询今日股票信号：\n' +\
                '超短线买入 sbuy\n超短线卖出 ssell\n' +\
                '小时线买入 hbuy\n小时线卖出 hsell\n' +\
                '日线买入   dbuy\n日线卖出   dsell\n'
    elif context[1:].isdigit():
        texts = qurry_position(context)
    elif context == 'sendfile':
        wechat_class.send_wechat_file(mandatory_order=True)
        texts = ''
    elif context[1:] == 'buy' or context[1:] == 'sell':
        texts = send_file(context)
    elif context == '套利' or context == 'fast_query':
        texts = wechat_class.future_query.fast_query()
    else:
        texts = wechat_class.future_query.query_by_text(context)
    return texts


def qurry_position(code=str, position_file='\\\\SWFUTURES-PC\\Share\\Trade\\macd_v2_position.csv',
                   pick_fname='D:\\Share\\Trade\\macd_v2.pic'):
    if code[0] == 'd':
        position_file = 'D:\\Share\\Trade\\macd_240_position.csv'
        pick_fname = 'D:\\Share\\Trade\\macd_240.pic'
    elif code[0] == 'h':
        position_file = 'D:\\Share\\Trade\\macd_60_position.csv'
        pick_fname = 'D:\\Share\\Trade\\macd_60.pic'
    elif code[0] == 's':
        position_file = 'D:\\Share\\Trade\\macd_v2_position.csv'
        pick_fname = 'D:\\Share\\Trade\\macd_v2.pic'
    else:
        context = '股票代码错误， \n超短线#sxxxxxx \n小时线#hxxxxxx \n日线#dxxxxxx'
        return context

    code = code[1:]
    f = open(pick_fname, 'rb')
    try:
        table_pic = pickle.load(f, encoding='gbk')
    except AttributeError:
        print(pick_fname)
        return ''
    else:
        buy_table = table_pic[0]
        sell_table = table_pic[1]
    f.close()

    if code in buy_table.code:
        k = buy_table.code.index(code)
        context = code + ' 今日 ' + buy_table.time[k] + ' 买入  价格 ' + str(round(float(buy_table.price[k]), 2))
        return context
    elif code in sell_table.code:
        k = sell_table.code.index(code)
        context = code + ' 今日 ' + sell_table.time[k] + ' 卖出  价格 ' + str(round(float(sell_table.price[k]), 2))
        return context

    df = pd.read_csv(position_file, dtype={'code': str})
    position_list = df.code
    df = df.set_index('code', drop=True)
    if code in set(position_list):
        context = code + ' 有持仓 买入时间 ' + str(df.buyday[code]) + ' 买入价格 ' +\
                  str(round(float(df.buyprice[code]), 2))
        if 'stopprice' in df.columns:
            context += ' 止损价 ' + str(round(float(df.stopprice[code]), 2))
    else:
        context = code + ' 无持仓'
    return context


def send_file(command=str, address='D:\\Share\\Trade\\'):
    if len(command) == 4:
        buyorsell = 'buylist'
        new_filename = 'buy'
    else:
        buyorsell = 'selllist'
        new_filename = 'sell'
    if command[0] == 'd':
        file_name = address + buyorsell + '_macd_240.txt'
    elif command[0] == 'h':
        file_name = address + buyorsell + '_macd_60.txt'
    elif command[0] == 's':
        file_name = address + buyorsell + '_macd_v2.txt'
    if not os.path.exists(file_name):        # 判断文件是否存在
        message = '今日暂无信号'
        return message
    elif os.path.getsize(file_name) == 0:
        message = '今日暂无信号'
        return message
    else:
        new_filepath = '@fil@' + create_file(new_filename, file_name)
        return new_filepath


def create_file(filename='buy.txt', old_filepath='D:\\Share\\Trade\\macd_240_position.csv'):
    site = old_filepath.rfind('\\')
    file_path = old_filepath[:site+1]
    new_filepath = file_path + filename + '.txt'
    shutil.copyfile(old_filepath, new_filepath)
    return new_filepath


if __name__ == '__main__':
    text = reply_signal(msg={'Type': 'Text', 'Text': 'h600010'})
    print(text)
    text = reply_signal(msg={'Type': 'Text', 'Text': 'd600128'})
    print(text)
    text = reply_signal(msg={'Type': 'Text', 'Text': 's600037'})
    print(text)
    text = reply_signal(msg={'Type': 'Text', 'Text': 'ssell'})
    print(text)
    text = reply_signal(msg={'Type': 'Text', 'Text': 'help'})
    print(text)

