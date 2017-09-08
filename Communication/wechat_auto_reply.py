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
from Communication import Recommend


class trade_list(trade_signal.trade_list):
    pass


def file_path():
    PC = 'D:\\Share\\Trade\\'
    return PC


def get_nickname(msg_str):
	tmp = ''

	for s in msg_str.split(','):
		if 'RemarkName' in s:
			nickname = s.split("'")[3]
			print(nickname)
			return nickname
		elif 'filehelper' in s:
			tmp = 'filehelper'
	else:
		if tmp == 'filehelper':
			return 'filehelper'
		else:
			print("we can not get nickname")
			return ''


class auto_reply(object):
    def __init__(self, config_file='D:\\Python_Config\\WeChat_reply.json'):
        config = json.load(open(config_file, 'r', encoding="utf-8"))
        self.position_file_name = config['position_file_name']
        self.stock_signal_file_name = config['stock_signal_file_name']
        self.stock_signal_keyname = config['stock_signal_keyname']
        self.buy_signal_file_name = config['buy_signal_file_name']
        self.sell_signal_file_name = config['sell_signal_file_name']
        self.recommend_fn = config['recommend_fn']
        self.manager = config['manager']
        self.recommender = config['recommender']

        self.rcmd = Recommend.recommender()
        self.stock_signal_update_time = list()
#        self.stock_position = list()
#        self.stock_buy_table = list()
#        self.stock_sell_table = list()
#        for fn in self.stock_signal_file_name:
#            self.stock_signal_update_time.append(0)
#            df = pd.read_csv(fn, dtype={'code': str})
#            df = df.set_index('code', drop=True)
#            self.stock_position.append(df)
#            self.stock_sell_table.append(pd.DataFrame())
#            self.stock_buy_table.append(pd.DataFrame())

    def reply_signal(self, msg=dict, wechat_class=None):
        try:
            context = msg['Text']
            self.from_user = get_nickname(msg.__str__())
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
            self.from_user = get_nickname(msg.__str__())
            texts = self.reply(context[1:], wechat_class)
            if len(texts) > 0:
                return texts

    def reply(self, context=str, wechat_class=None):
        print('{}: {}'.format(self.from_user, context))
        if context == 'help' or context == '帮助':
            texts = self.reply_help()
        elif context[1:].isdigit():
            texts = qurry_position(context)
        elif context == 'sendfile':
            wechat_class.send_wechat_file(mandatory_order=True)
            texts = ''
        elif context[1:] == 'buy' or context[1:] == 'sell':
            texts = send_file(context)
        elif 'rcmd' in context or '荐股' in context or '推荐' in context:
            texts = self.get_recommend(context)
        elif context == '套利' or context == 'fast_query':
            texts = wechat_class.future_query.fast_query()
        elif context[:4] == 'wind':
            if context == 'wind':
                texts = wechat_class.future_query.get_wind_status()
            elif context == 'wind start':
                texts = wechat_class.future_query.re_start()
            elif context == 'wind close':
                texts = wechat_class.future_query.temp_close()
        elif context[0] == 'f' and len(context) > 1:
            texts = wechat_class.future_query.query_by_text(context[1:])
        else:
            texts = ''
        return texts

    def reply_help(self):
        texts = '请输入信息与我开始互动(若在群聊中清以#开头)\n查询股票持仓：\n ' \
                '超短线 sxxxxxx \n小时线 hxxxxxx \n日线 dxxxxxx\n' \
                '查询今日股票信号：\n' \
                '超短线买入 sbuy\n超短线卖出 ssell\n' \
                '小时线买入 hbuy\n小时线卖出 hsell\n' \
                '日线买入   dbuy\n日线卖出   dsell\n'

        if self.from_user in self.manager:
            texts += '荐股持仓 推荐持仓 或 荐股持仓\n今日荐股 今日推荐 或 今日荐股\n'

        if self.from_user in self.recommender:
            texts = '请输入信息与我开始互动:\n'\
	                '荐股持仓 推荐持仓 或 荐股持仓\n' \
                    '今日荐股 今日推荐 或 今日荐股\n' \
                    '推荐买入 推荐买入 600000 浦发银行 17.20\n' \
                    '推荐卖出 推荐卖出 600000 浦发银行 17.20\n' \
                    '撤销推荐 撤销推荐 600000\n'

        return texts

    def get_recommend(self, texts):
        if self.from_user not in self.recommender and self.from_user not in self.manager:
            return ''
        elif self.from_user in self.recommender:
            recommender = self.from_user
        else:
            recommender = None

        if texts == '推荐持仓' or texts == '荐股持仓':
            df = self.rcmd.get_position_data(recommender=recommender)
        elif texts == '今日推荐' or texts == '今日荐股':
            df = self.rcmd.get_today_data(recommender=recommender)
        elif '推荐买入' in texts:
            _, code, name, price, *arr = split_str(texts)
            df = self.rcmd.append(code=code, name=name, price=price, buyorsell='买入', recommender=recommender, arrs=arr)
        elif '推荐卖出' in texts:
            _, code, name, price, *arr = split_str(texts)
            df = self.rcmd.append(code=code, name=name, price=price, buyorsell='卖出', recommender=recommender, arrs=arr)
        elif '撤销推荐' in texts:
            _, code, *arr = split_str(texts)
            df = self.rcmd.remove(code=code, recommender=recommender)
        elif '更新' in texts:
            winorloss, code, _, price, *arr = split_str(texts)
            self.rcmd.update(code, winorloss, price)
        else:
            df = '输入指令错误'

        if isinstance(df, pd.DataFrame):
            df.columns = ['荐股人', '买卖', '代码', '名称', '日期',  '时间', '价格', '止盈', '止损']

            if len(df) == 0:
                return '无荐股记录'
            elif len(df) < 5:
                return df.__str__()
            else:
                fn = 'D:\\Cache\\tmp.txt'
                df.to_csv(fn, index=False)
                return '@fil@' + fn
        else:
            return df



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


def split_str(strs=''):
	word_list = list()
	strs = strs.strip()
	x = ord(strs[0])
	word_tmp = ''
	for c in strs[:-1]:
		if (ord(c) - 256) * (x - 256) < 0:
			word_list.append(word_tmp)
			word_tmp = ''
			x = ord(c)
		word_tmp += c
	word_list.append(word_tmp)

	return word_list

if __name__ == '__main__':
	print(split_str('推荐买入600000浦发银行17.20止损18.00止盈17.00'))
	ar = auto_reply()
	text = ar.reply_signal(msg={'Type': 'Text', 'Text': 'h600010', 'NickName': 'sdada'})
	print(text)
	text = ar.reply_signal(msg={'Type': 'Text', 'Text': 'd600128', 'NickName': '申购易罗小雨'})
	print(text)
	text = ar.reply_signal(msg={'Type': 'Text', 'Text': 's600037', 'NickName': '申购易罗小雨'})
	print(text)
	text = ar.reply_signal(msg={'Type': 'Text', 'Text': 'ssell', 'NickName': '申购易罗小雨'})
	print(text)
	text = ar.reply_signal(msg={'Type': 'Text', 'Text': 'help', 'NickName': '申购易罗小雨'})
	print(text)
	text = ar.reply_signal(msg={'Type': 'Text', 'Text': 'help', 'NickName': '申购易罗小雨'})
	print(text)
	text = ar.reply_signal(msg={'Type': 'Text', 'Text': 'help', 'NickName': '申购易苟峻'})
	print(text)
	text = ar.reply_signal(msg={'Type': 'Text', 'Text': '推荐买入 云南成 600239 17.2', 'NickName': '申购易罗小雨'})
	print(text)
	text = ar.reply_signal(msg={'Type': 'Text', 'Text': '推荐买入 云成 600239 17.2', 'NickName': '申购易蒲龙波'})
	print(text)
	text = ar.reply_signal(msg={'Type': 'Text', 'Text': '推荐卖出 云成 600239 17.2', 'NickName': '申购易蒲龙波'})
	print(text)
	text = ar.reply_signal(msg={'Type': 'Text', 'Text': '今日荐股', 'NickName': '申购易蒲龙波'})
	print(text)
	text = ar.reply_signal(msg={'Type': 'Text', 'Text': '今日荐股', 'NickName': '申购易苟峻'})
	print(text)
	text = ar.reply_signal(msg={'Type': 'Text', 'Text': '撤销推荐 600239', 'NickName': '申购易蒲龙波'})
	print(text)

