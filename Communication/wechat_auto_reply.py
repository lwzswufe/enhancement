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
import json


class trade_list(trade_signal.trade_list):
    pass


def file_path():
    PC = 'D:\\Share\\Trade\\'
    return PC


class auto_reply(object):
    def __init__(self, config_file='D:\\Python_Config\\WeChat_reply.json'):
        config = json.load(open(config_file, 'r', encoding="utf-8"))
        self.position_file_name = config['position_file_name']
        self.stock_signal_file_name = config['stock_signal_file_name']
        self.stock_signal_keyname = config['stock_signal_keyname']
        self.buy_signal_file_name = config['buy_signal_file_name']
        self.sell_signal_file_name = config['sell_signal_file_name']
        self.stock_signal_update_time = list()
        self.stock_position = list()
        self.stock_buy_table = list()
        self.stock_sell_table = list()
        for fn in self.stock_signal_file_name:
            self.stock_signal_update_time.append(0)
            df = pd.read_csv(fn, dtype={'code': str})
            df = df.set_index('code', drop=True)
            self.stock_position.append(df)
            self.stock_sell_table.append(pd.DataFrame())
            self.stock_buy_table.append(pd.DataFrame())

    def reply_signal(self, msg=dict, wechat_class=None):
        try:
            context = msg['Text']
            texts = self.reply(context, wechat_class)
            if len(texts) > 0:
                return texts
        except TypeError:
            print(msg)

    def reply_group(self, msg=dict, wechat_class=None):
        try:
            context = msg['Text']
        # fromUserName = msg['FromUserName']
        except TypeError:
            print(msg)
        if context[0] == '#':
            texts = self.reply(context[1:], wechat_class)
            if len(texts) > 0:
                return texts

    def reply(self, context=str, wechat_class=None):
        context = context.lower()
        if context == 'help':
            texts = '请输入信息与我开始互动(若在群聊中清以#开头)\n查询股票持仓：\n' +\
                    '超短线 sxxxxxx \n小时线 hxxxxxx \n日线 dxxxxxx\n' +\
                    '查询今日股票信号：\n' +\
                    '超短线买入 sbuy\n超短线卖出 ssell\n' +\
                    '小时线买入 hbuy\n小时线卖出 hsell\n' +\
                    '日线买入   dbuy\n日线卖出   dsell\n'
        elif context[1:].isdigit():
            texts = self.qurry_position(context)
        elif context == 'sendfile':
            wechat_class.send_wechat_file(mandatory_order=True)
            texts = ''
        elif context[1:] == 'buy' or context[1:] == 'sell':
            texts = self.send_file(context)
        else:
            texts = ''
        return texts

    def qurry_position(self, code=str, position_file='\\\\SWFUTURES-PC\\Share\\Trade\\macd_v2_position.csv',
                       pick_fname='D:\\Share\\Trade\\macd_v2.pic'):
        if code[0] in self.stock_signal_keyname:
            flag = self.stock_signal_keyname.index(code[0])
            pick_fname = file_path() + self.sell_signal_file_name[flag]
            code = code[1:]
        else:
            context = '股票代码错误， \n超短线#sxxxxxx \n小时线#hxxxxxx \n日线#dxxxxxx'
            return context

        update_time = os.stat(fn).st_mtime
        if update_time > self.stock_signal_update_time[flag]:
            f = open(pick_fname, 'rb')
            table_pic = pickle.load(f, encoding='gbk')
            buy_table = table_pic[0]
            sell_table = table_pic[1]
            self.stock_buy_table[flag] = buy_table
            self.stock_sell_table[flag] = sell_table
            f.close()

        if code in self.stock_buy_table[flag].code:
            k = self.stock_buy_table[flag].code.index(code)
            context = code + ' 今日 ' + self.stock_buy_table[flag].time[k] +\
                      ' 买入  价格 ' + str(round(float(self.stock_buy_table[flag].price[k]), 2))
            return context
        elif code in self.stock_sell_table[flag].code:
            k = self.stock_sell_table[flag].code.index(code)
            context = code + ' 今日 ' + self.stock_sell_table[flag].time[k] +\
                      ' 卖出  价格 ' + str(round(float(self.stock_sell_table[flag].price[k]), 2))
            return context

        if code in set(self.stock_position[flag].code):
            context = code + ' 有持仓 买入时间 ' + str(self.stock_position[flag].buyday[code]) +\
                  ' 买入价格 ' + str(round(float(self.stock_position[flag].buyprice[code]), 2))
            if 'stopprice' in self.stock_position[flag].columns:
                context += ' 止损价 ' + str(round(float(self.stock_position[flag].stopprice[code]), 2))
        else:
            context = code + ' 无持仓'
        return context

    def send_file(self, command=str, address='D:\\Share\\Trade\\'):
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
    ar = auto_reply()
    text = ar.reply_signal(msg={'Type': 'Text', 'Text': 'h600010'})
    print(text)
    text = ar.reply_signal(msg={'Type': 'Text', 'Text': 'd600128'})
    print(text)
    text = ar.reply_signal(msg={'Type': 'Text', 'Text': 's600037'})
    print(text)
    text = ar.reply_signal(msg={'Type': 'Text', 'Text': 'ssell'})
    print(text)
    text = ar.reply_signal(msg={'Type': 'Text', 'Text': 'help'})
    print(text)

