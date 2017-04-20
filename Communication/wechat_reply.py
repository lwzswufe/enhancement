# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import pandas as pd
import pickle


class trade_list(object):
    def __init__(self, fname='test'):
        self.code = list()
        self.time = list()
        self.price = list()
        self.name = list()
        self.context = list()
        self.textname = fname

    def append(self, code, name, time_str, price, repet=False, buyorsell='买入'):
        if repet or code not in self.code:
            self.code.append(code)
            self.name.append(name)
            self.time.append(time_str)
            self.price.append(price)
            context = buyorsell + ' ' + code + ' ' + name + ' 价格 ' +\
                      str(price) + '\n'
            self.context.append(context)

    def write(self):
        PC = file_address()
        fname = PC + self.textname
        if len(self.context) > 0:
            f = open(fname, 'w')
            line = '时间 ' + self.time[-1] + '\n'
            f.write(line)
            for line in self.context:
                f.write(line)
                print(line)
            f.close()

    def get_data(self):
        write_df = pd.DataFrame({'code': self.code, 'name': self.name,
                                 'time': self.time, 'price': self.price})
        return write_df

    def update(self, code, name=False, time=False, price=False):
        if code not in self.code:
            return
        i = self.code.index(code)
        if time:
            self.time[i] = time
        if price:
            self.price[i] = price
        if name:
            self.name[i] = name


def file_address():
    PC = 'D:\\Share\\Trade\\'
    return PC


def reply_signal(msg=dict, wechat_class=None):
    try:
        context = msg['Text']
    except TypeError:
        print(msg)
    if context[0] != '#':
        return ''
    else:
        context = context[1:]

    if context == 'help':
        text = '请输入#开头的信息与我开始互动\n查询股票持仓：\n' +\
               '\n超短线#sxxxxxx \n小时线#hxxxxxx \n日线#dxxxxxx'
        return text
    elif context[1:].isdigit():
        return qurry_position(context)
    elif context == 'sendfile':
        wechat_class.send_wechat_file(mandatory_order=True)
    return ''


def reply_group(msg=dict, wechat_class=None):
    return reply_signal(msg, wechat_class)


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


if __name__ == '__main__':
    text = reply_signal(msg={'Type': 'Text', 'Text': '#h600010'})
    print(text)
    text = reply_signal(msg={'Type': 'Text', 'Text': '#d600128'})
    print(text)
    text = reply_signal(msg={'Type': 'Text', 'Text': '#s600037'})
    print(text)
